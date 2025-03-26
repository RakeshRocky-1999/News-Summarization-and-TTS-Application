from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models.sentiment import analyze_sentiment
from models.summarizer import summarize
from models.hindi_tts import process_and_generate_tts
from models.comparative_analysis import generate_comparative_analysis
from utils.scraper import extract_news
import os
import json
import time

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
            # If article is a string, set defaults
            content = article
            title = article.split(":")[0]  # Extract title from string
            topics = ["General"]
        else:
            # Handle dictionary with keys like 'Title' and 'Summary'
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
                "Sentiment": sentiment.lower(),  # Make sentiment lowercase for consistency
                "Topics": topics,
            }
        )
        sentiments.append(sentiment.lower())

    print(f"✅ Processed Articles: {article_data}")

    # Ensure the data directory exists
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Define the output file path for comparative analysis
    comparative_output_file = os.path.join(os.getcwd(), "data", "comparative_analysis.json")

    # Perform comparative sentiment analysis
    generate_comparative_analysis(article_data, comparative_output_file)
    time.sleep(1)  # Delay to ensure file is written before reading

    # Read comparative analysis results
    if os.path.exists(comparative_output_file):
        with open(comparative_output_file, "r", encoding="utf-8") as file:
            comparative_results = json.load(file)
        print(f"✅ Comparative Results Loaded: {comparative_results}")
    else:
        print("❌ Comparative results file not found!")
        comparative_results = {"message": "No comparative results available."}

    # Generate the final sentiment summary
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
    print(f"🎙️ TTS Generated at: {audio_path}")

    # Return the processed results
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



