# import os
# import json
# import time
# import asyncio
# from fastapi import FastAPI, HTTPException
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel
# from models.sentiment import analyze_sentiment
# from models.summarizer import summarize
# from models.hindi_tts import process_and_generate_tts
# from models.comparative_analysis import generate_comparative_analysis
# from utils.scraper import extract_news

# # ============================
# # ✅ FastAPI Backend
# # ============================

# # Initialize FastAPI
# app = FastAPI()

# # ----------------------------
# # ✅ Define correct paths for Docker
# # ----------------------------
# # Get the base directory (inside Docker it’s /app)
# base_dir = os.path.dirname(os.path.abspath(__file__))

# # ✅ Corrected output directory path
# output_dir = os.path.join(base_dir, "output")

# # ✅ Create output directory if it doesn't exist
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)

# # ✅ Mount the output directory to serve audio files
# app.mount("/output", StaticFiles(directory=output_dir), name="output")


# class RequestData(BaseModel):
#     company_name: str


# @app.post("/process")
# def process_request(data: RequestData):
#     """Process news, sentiment, summarization, and TTS for a company."""
#     company_name = data.company_name.strip()
#     print(f"🔎 Processing request for: {company_name}")

#     if not company_name:
#         raise HTTPException(status_code=400, detail="Company name is required")

#     # Extract news articles
#     articles = extract_news(company_name)
#     print(f"📰 Articles Extracted: {articles}")

#     if not articles:
#         raise HTTPException(status_code=404, detail="No articles found")

#     article_data = []
#     sentiments = []

#     for article in articles:
#         print(f"📄 Processing article: {article}")

#         # Check if article is string or dictionary
#         if isinstance(article, str):
#             content = article
#             title = article.split(":")[0]
#             topics = ["General"]
#         else:
#             content = article.get("Summary", "No content available.")
#             title = article.get("Title", "No title available.")
#             topics = article.get("Topics", ["General"])

#         # Summarize and analyze each article
#         summary = summarize(content)
#         sentiment = analyze_sentiment(summary)

#         article_data.append(
#             {
#                 "Title": title,
#                 "Summary": summary,
#                 "Sentiment": sentiment.lower(),
#                 "Topics": topics,
#             }
#         )
#         sentiments.append(sentiment.lower())

#     # Comparative Sentiment Analysis
#     data_dir = os.path.join(base_dir, "data")
#     if not os.path.exists(data_dir):
#         os.makedirs(data_dir)

#     comparative_output_file = os.path.join(data_dir, "comparative_analysis.json")
#     generate_comparative_analysis(article_data, comparative_output_file)
#     time.sleep(1)

#     if os.path.exists(comparative_output_file):
#         with open(comparative_output_file, "r", encoding="utf-8") as file:
#             comparative_results = json.load(file)
#     else:
#         comparative_results = {"message": "No comparative results available."}

#     # Generate Sentiment Summary
#     positive_count = sentiments.count("positive")
#     negative_count = sentiments.count("negative")
#     neutral_count = sentiments.count("neutral")

#     if positive_count > negative_count:
#         final_sentiment_analysis = f"{company_name}’s latest news coverage is mostly positive."
#     elif negative_count > positive_count:
#         final_sentiment_analysis = f"{company_name}’s recent news coverage raises concerns about regulatory hurdles."
#     else:
#         final_sentiment_analysis = f"{company_name}’s latest news reflects a neutral sentiment."

  
#     # ----------------------------
#     # ✅ Generate Hindi TTS
#     # ----------------------------
#     tts_text = final_sentiment_analysis

#     # ✅ Correct audio file extension to .mp3
#     audio_filename = "hindi_tts_output.mp3"  # Fixed to mp3 format
#     audio_path_ = os.path.join(output_dir, audio_filename)

#     # ✅ Call process_and_generate_tts as an async function
#     audio_path = asyncio.run(process_and_generate_tts(tts_text, audio_path_))
#     # # ✅ Generate and save the TTS audio
#     # audio_path = process_and_generate_tts(tts_text, audio_path=audio_path_)
#     print(f"🎙️ TTS Generated at: {audio_path}")

#     # ✅ Check if audio_path is valid and exists
#     if audio_path and os.path.exists(audio_path):
#         print(f"🎧 Audio file exists: {audio_path}")
#         audio_url = f"/output/{audio_filename}"
#     else:
#         print(f"⚠️ Audio file NOT created or path incorrect: {audio_path}")
#         audio_url = None




#     return {
#         "Company": company_name,
#         "Articles": article_data,
#         "Comparative Sentiment Score": comparative_results,
#         "Final Sentiment Analysis": final_sentiment_analysis,
#         "Audio": audio_url,
#     }

# @app.get("/health")
# def read_root():
#     """Health check endpoint."""
#     return {"message": "API is running successfully!"}


#--------------------------------------------------------------------------------------------
#successfull running code for docker hugging face

import os
import json
import time
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from models.sentiment import analyze_sentiment
from models.summarizer import summarize
from models.hindi_tts import process_and_generate_tts
from models.comparative_analysis import generate_comparative_analysis
from utils.scraper import extract_news

# ============================
# ✅ FastAPI Backend
# ============================

# Initialize FastAPI
app = FastAPI()

# ----------------------------
# ✅ Define correct paths for Docker/Hugging Face
# ----------------------------
# ✅ Use /tmp directory to avoid permission issues in Hugging Face
output_dir = "/tmp/output"
data_dir = "/tmp/data"

# ✅ Create required directories if they don't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# ✅ Mount the output directory to serve audio files
app.mount("/output", StaticFiles(directory=output_dir), name="output")


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
        print(f"👍 Processing article: {article}")

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
    comparative_output_file = os.path.join(data_dir, "comparative_analysis.json")
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

    # ----------------------------
    # ✅ Generate Hindi TTS
    # ----------------------------
    tts_text = final_sentiment_analysis

    # ✅ Correct audio file extension to .mp3
    audio_filename = "hindi_tts_output.mp3"
    audio_path_ = os.path.join(output_dir, audio_filename)

    # ✅ Call process_and_generate_tts as an async function
    audio_path = asyncio.run(process_and_generate_tts(tts_text, audio_path_))

    print(f"🎧 TTS Generated at: {audio_path}")

    # ✅ Check if audio_path is valid and exists
    if audio_path and os.path.exists(audio_path):
        print(f"🎵 Audio file exists: {audio_path}")
        audio_url = f"/output/{audio_filename}"
    else:
        print(f"⚠️ Audio file NOT created or path incorrect: {audio_path}")
        audio_url = None

    return {
        "Company": company_name,
        "Articles": article_data,
        "Comparative Sentiment Score": comparative_results,
        "Final Sentiment Analysis": final_sentiment_analysis,
        "Audio": audio_url,
    }


@app.get("/health")
def read_root():
    """Health check endpoint."""
    return {"message": "API is running successfully!"}

