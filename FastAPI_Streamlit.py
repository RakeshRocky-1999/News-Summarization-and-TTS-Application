import os
import json
import time
import requests
import streamlit as st
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models.sentiment import analyze_sentiment
from models.summarizer import summarize
from models.hindi_tts import process_and_generate_tts
from models.comparative_analysis import generate_comparative_analysis
from utils.scraper import extract_news
from threading import Thread
import uvicorn


# ============================
# ✅ FastAPI Backend
# ============================

# Initialize FastAPI
app = FastAPI()


class RequestData(BaseModel):
    company_name: str


@app.post("/process")
def process_request(data: RequestData):
    """Process news, sentiment, summarization, and TTS for a company."""
    company_name = data.company_name.strip()
    print(f"🔎 Processing request for: {company_name}")

    if not company_name:
        raise HTTPException(status_code=400, detail="Company name is required")

    # Extract news articles
    articles = extract_news(company_name)
    print(f"📰 Articles Extracted: {articles}")

    if not articles:
        raise HTTPException(status_code=404, detail="No articles found")

    article_data = []
    sentiments = []

    for article in articles:
        print(f"📄 Processing article: {article}")

        # Check if article is string or dictionary
        if isinstance(article, str):
            content = article
            title = article.split(":")[0]
            topics = ["General"]
        else:
            content = article.get("Summary", "No content available.")
            title = article.get("Title", "No title available.")
            topics = article.get("Topics", ["General"])

        # Summarize and analyze each article
        summary = summarize(content)
        sentiment = analyze_sentiment(summary)

        article_data.append(
            {
                "Title": title,
                "Summary": summary,
                "Sentiment": sentiment.lower(),
                "Topics": topics,
            }
        )
        sentiments.append(sentiment.lower())

    # Comparative Sentiment Analysis
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    comparative_output_file = os.path.join(os.getcwd(), "data", "comparative_analysis.json")
    generate_comparative_analysis(article_data, comparative_output_file)
    time.sleep(1)

    if os.path.exists(comparative_output_file):
        with open(comparative_output_file, "r", encoding="utf-8") as file:
            comparative_results = json.load(file)
    else:
        comparative_results = {"message": "No comparative results available."}

    # Generate Sentiment Summary
    positive_count = sentiments.count("positive")
    negative_count = sentiments.count("negative")
    neutral_count = sentiments.count("neutral")

    if positive_count > negative_count:
        final_sentiment_analysis = f"{company_name}’s latest news coverage is mostly positive."
    elif negative_count > positive_count:
        final_sentiment_analysis = f"{company_name}’s recent news coverage raises concerns about regulatory hurdles."
    else:
        final_sentiment_analysis = f"{company_name}’s latest news reflects a neutral sentiment."

    # Generate Hindi TTS
    tts_text = final_sentiment_analysis
    audio_path = process_and_generate_tts(tts_text)

    return {
        "Company": company_name,
        "Articles": article_data,
        "Comparative Sentiment Score": comparative_results,
        "Final Sentiment Analysis": final_sentiment_analysis,
        "Audio": audio_path,
    }


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"message": "API is running successfully!"}


# ============================
# 🎨 Streamlit Frontend
# ============================

# Corrected API URL for FastAPI
API_URL = "http://127.0.0.1:8000/process"


def run_streamlit():
    """Streamlit UI for News Analysis, Sentiment Comparison, and Hindi TTS Application."""
    st.title("📰 News Analysis, Sentiment Comparison, and Hindi TTS Application")
    st.write(
        "Enter a company name to extract news, analyze sentiment, summarize, "
        "compare sentiment, and convert the analysis to Hindi speech."
    )

    company_name = st.text_input("🏢 Enter Company Name:", "")

    if st.button("🚀 Generate Analysis"):
        if company_name.strip():
            try:
                response = requests.post(API_URL, json={"company_name": company_name.strip()})

                if response.status_code == 200:
                    result = response.json()

                    st.subheader(f"📚 News Analysis for: {company_name}")
                    articles = result.get("Articles", [])
                    for idx, article in enumerate(articles, start=1):
                        st.write(f"### 📝 Article {idx}")
                        st.write(f"**Title:** {article['Title']}")
                        st.write(f"**Summary:** {article['Summary']}")
                        st.write(f"**Sentiment:** {article['Sentiment']}")
                        st.write(f"**Topics:** {', '.join(article['Topics'])}")

                    comparative_results = result.get("Comparative Sentiment Score", {})
                    if comparative_results:
                        st.subheader("📈 Comparative Sentiment Analysis Results")

                        sentiment_dist = comparative_results.get("Sentiment Distribution", {})
                        st.write("**Sentiment Distribution:**")
                        st.json(sentiment_dist)

                        coverage_diff = comparative_results.get("Coverage Differences", [])
                        st.subheader("🔀 Coverage Differences")
                        if isinstance(coverage_diff, list):
                            for diff in coverage_diff:
                                if isinstance(diff, dict):
                                    st.markdown(
                                        f"""
                                        - **Comparison:** {diff.get('Comparison', 'No Comparison Available')}
                                        - **Impact:** {diff.get('Impact', 'No Impact Available')}
                                        """
                                    )

                    st.subheader("💡 Final Sentiment Analysis")
                    final_sentiment = result.get("Final Sentiment Analysis", "No analysis available.")
                    st.write(f"**Summary:** {final_sentiment}")

                    audio_path = result.get("Audio", "")
                    if audio_path and os.path.isfile(audio_path):
                        st.subheader("🔊 Hindi Text-to-Speech Output")
                        st.audio(audio_path, format="audio/wav")
                        with open(audio_path, "rb") as audio_file:
                            st.download_button(
                                "⬇️ Download Audio",
                                audio_file,
                                file_name="hindi_tts_output.wav",
                                mime="audio/wav",
                            )
                    else:
                        st.warning("⚠️ No audio generated or file missing.")

                else:
                    st.error(f"❌ Error processing the request. HTTP Status: {response.status_code}")
                    st.write(response.text)

            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Error connecting to the API: {e}")

        else:
            st.warning("⚠️ Please enter a valid company name.")


# ============================
# 🚀 Run FastAPI & Streamlit
# ============================


def run_fastapi():
    """Run FastAPI backend."""
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    # Run FastAPI in a separate thread
    thread = Thread(target=run_fastapi, daemon=True)
    thread.start()

    # Run Streamlit in the main thread
    run_streamlit()