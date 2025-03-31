# 📰 Text Summarization and Hindi TTS Application

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.44.0-red)
![Docker](https://img.shields.io/badge/Docker-Enabled-lightblue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Overview
This project leverages **Natural Language Processing (NLP)** and **Machine Learning (ML)** techniques to:
- Extract and **summarize news articles**.
- Perform **sentiment analysis** and **comparative analysis**.
- Convert the summarized text to **Hindi audio** using Text-to-Speech (TTS).

The project consists of:
- 🎯 **FastAPI Backend:** To handle API requests and process text.
- 🎨 **Streamlit Frontend:** For user interaction, summarizing text, and playing generated audio.
- 📦 **Docker Integration:** Containerized for easy deployment on **Hugging Face Spaces**.

---

## 📂 Project Structure

C:\My Projects\text_summ_to_TTS
├── requirements.txt         # List of dependencies
├── Dockerfile               # Docker configuration for containerization
├── api.py                   # Backend API using FastAPI
├── app.py                   # Streamlit frontend app
├── FastAPI_Streamlit.py     # Combined FastAPI and Streamlit for local use
├── models
│   ├── __init__.py           # Module initialization
│   ├── hindi_tts.py          # Text-to-Speech (TTS) in Hindi
│   ├── summarizer.py         # News summarization logic
│   ├── comparative_analysis.py  # Sentiment comparison across articles
│   └── sentiment.py          # Sentiment analysis for articles
├── utils
│   └── scraper.py            # Web scraping with BeautifulSoup
├── data
│   └── comparative_analysis.json  # Output of comparative_analysis.py
├── output
│   └── hindi_tts_output.mp3  # TTS audio is saved in this folder
├── Notebooks
│   └── Test_extraction.py    # Testing and experimenting with article extraction
└── .gitignore                # Ignore unnecessary files in Git


## 🎯 Key Features

✅ **`Text Summarization:`** Summarizes news articles using NLP models.
✅ Comparative Analysis: Analyzes the sentiment of multiple articles and generates insights.
✅ Hindi Text-to-Speech (TTS): Converts summarized text into Hindi audio using gtts.
✅ RESTful API with FastAPI: Handles incoming requests and manages backend processes.
✅ Streamlit Frontend: Provides an intuitive and interactive UI for users.
✅ Docker Support: Easily deployable using Docker with optimized performance.