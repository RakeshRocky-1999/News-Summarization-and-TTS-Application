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
# Create a virtual environment and activate it
python3 -m TTS_venv env
source env/bin/activate  # For Mac/Linux
# or
env\Scripts\activate  # For Windows

# Install dependencies
pip install -r requirements.txt

# Run FastAPI
uvicorn main:app --host 127.0.0.1 --port 8000 --reload

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


## 🎯 API Endpoints Table

| **Method** | **Endpoint**           | **Description**                                 |
|------------|------------------------|-------------------------------------------------|
| `POST`     | `/get-news/`            | Fetch news articles, analyze sentiment, and generate audio |
| `GET`      | `/docs`                 | Access FastAPI Swagger UI                      |
| `POST`     | `/generate-audio/`      | Generate Hindi TTS audio from summarized news  |
| `GET`      | `/health`               | Check API health status                        |

## 📚 Project Workflow
Here’s a detailed breakdown of how the project works and potential future improvements:

🔥 How the Project Works
User Input:

User provides a company name via the Streamlit frontend or directly through the FastAPI backend.

Example Input:
```
{
  "company": "tesla"
}
```
**1.Scraping and Data Collection:**
- `scraper.py` fetches the latest news articles related to the given company.
- Data is cleaned and prepared for further analysis.

**2.Text Summarization:**
- `summarizer.py` generates concise summaries for each article.

**3.Sentiment Analysis:**
- `sentiment.py` evaluates the sentiment (positive, negative, or neutral) of each article.
- Sentiments are categorized and stored for comparative analysis.

**4.Comparative Sentiment Analysis:**
- `comparative_analysis.py` compares sentiments across articles to identify discrepancies.
- Insights such as sentiment distribution and topic overlap are highlighted.

**5.Hindi Text-to-Speech (TTS):**
- `hindi_tts.py` converts the summarized news into Hindi audio.
- Audio is saved in output/hindi_tts_output.mp3 and is included in the API response.

**6.FastAPI Backend:**
- API endpoints allow for seamless communication between the backend and frontend.
- Swagger documentation available at /docs.

**7.Streamlit Frontend:**
- Users can enter a company name and get:
    - Article Summaries
    - Sentiment Analysis
    - Hindi Audio Summary

## Sample Input for FastAPI
```
{
  "company": "tesla"
}

```
## Sample Output
```
{
  "Company": "tesla",
  "Articles": [
    {
      "Title": "Is Tesla cooked?",
      "Summary": " Tesla stock plunged 15 percent on Monday...",
      "Sentiment": "negative",
      "Topics": ["General"]
    },
    ...
  ],
  "Comparative Sentiment Score": {
    "Sentiment Distribution": {
      "negative": 1,
      "positive": 1,
      "neutral": 3
    },
    "Coverage Differences": [...],
    "Topic Overlap": {
      "Common Topics": ["General"],
      "Unique Topics": ["None"]
    }
  },
  "Final Sentiment Analysis": "tesla’s latest news reflects a neutral sentiment.",
  "Audio": "/output/hindi_tts_output_8418fbb1afe0422a8e36134ae74a0b58.mp3"
}

```

## 🚀 Future Improvements
**1.Enhanced NLP Models:** 
- Improve summarization using transformer-based models like BART or T5.
- Fine-tune sentiment models for domain-specific results.

**2.Advanced Topic Modeling:** Incorporate topic modeling to cluster articles by topic before comparison.

**3.Improved Audio Generation:** Upgrade to more realistic Hindi TTS models (e.g., Tacotron2 or VITS).

**4.User Interface Enhancements:** Improve Streamlit UI with advanced visualization and better interactivity.

**5.Caching for Faster Results:** Implement Redis or similar caching for repeated API calls.

**6.Multilingual Support:** Extend TTS to support multiple languages beyond Hindi.

**7.Docker Optimization:** Reduce image size and optimize for faster deployment.

## 🎯 Potential Use Cases
- **Market Sentiment Analysis:** Get a quick sentiment snapshot for trending companies.
- **Media Bias Detection:** Compare multiple sources to identify media bias.
- **Content Summarization:** Summarize long articles with sentiment insights.
- **Audio Accessibility:** Provide audio summaries for visually impaired users.
