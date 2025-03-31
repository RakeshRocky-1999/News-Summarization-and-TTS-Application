# 📰 Text Summarization and Hindi TTS Application

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.44.0-red)
![Docker](https://img.shields.io/badge/Docker-Enabled-lightblue)
![License](https://img.shields.io/badge/License-MIT-yellow)


## 🌐 Live Deployment Links

| Platform      | URL                                                                 |
|---------------|---------------------------------------------------------------------|
| 🚀 **FastAPI** | [FastAPI Endpoint](https://rakeshrocky-1999-fast-api-tts.hf.space/docs) |
| 🎨 **Streamlit** | [Streamlit Interface](https://rakeshrocky-1999-text-sum-to-tts-hindi.hf.space/) |

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

```
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
```


---

## 🎯 Key Features

| Feature                  | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| ✅ Text Summarization     | Summarizes news articles using NLP models.                                |
| ✅ Comparative Analysis   | Analyzes sentiment of multiple articles and generates insights.            |
| ✅ Hindi Text-to-Speech   | Converts summarized text into Hindi audio using `gtts`.                   |
| ✅ RESTful API with FastAPI | Handles incoming requests and processes text.                             |
| ✅ Streamlit Frontend     | Provides an intuitive and interactive UI for users.                       |
| ✅ Docker Support         | Easily deployable using Docker with optimized performance.                  |

---


---

## 🛠️ Technologies Used

| Technology      | Purpose                        |
|-----------------|--------------------------------|
| Python 3.11      | Core programming language      |
| FastAPI          | Backend API for text processing |
| Streamlit        | Frontend for interactive UI    |
| Docker           | Containerization and deployment |
| Googletrans      | Translation of text            |
| gTTS             | Text-to-Speech conversion      |
| Hugging Face API | Model hosting and deployment   |
| BeautifulSoup4   | Web scraping                   |
| NLTK & TextBlob  | Natural Language Processing    |
| Pandas           | Data manipulation              |
| Matplotlib/Seaborn | Data visualization           |
| PyTorch          | Machine Learning backend       |

---

## ⚡ Installation and Usage

### 📥 1. Clone the Repository
```bash
git remote add origin https://github.com/RakeshRocky-1999/News-Summarization-and-TTS-Application.git
```

### 🐍 2. Install Dependencies
```bash
# Using pip
pip install -r requirements.txt
```
### 🚀 3. Run FastAPI Backend (Local Machine)
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```
✅ API is now running on:

- http://127.0.0.1:8000/docs - API Documentation
- http://127.0.0.1:8000 - API Homepage

### 🎨 4. Run Streamlit Frontend (Local Machine)
```bash
streamlit run app.py
```
✅ Streamlit app is available at 
- http://localhost:8501.
- http://127.0.0.1:8501 - Streamlit Frontend Interface

### 5. Run Combined FastAPI and Streamlit Application (Local Only)
```bash
python FastAPI_Streamlit.py
```
✅ Combined interface is accessible locally at:
- http://127.0.0.1:8000/docs - FastAPI
- http://127.0.0.1:8501 - Streamlit UI

### 🚢 Docker Deployment
1. Build Docker Image
```bash
docker build -t text-summ-api .
```
2. Run Docker Container
```bash
docker run -p 7860:7860 -p 8501:8501 text-summ-api
```
✅ Access the following services:
- http://127.0.0.1:7860/docs - FastAPI Docs (Docker)
- http://127.0.0.1:8501 - Streamlit UI (Docker)




