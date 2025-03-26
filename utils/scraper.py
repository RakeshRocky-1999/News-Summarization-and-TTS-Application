import requests
from bs4 import BeautifulSoup

def extract_news(company_name):
    """Extract news articles for a given company name."""
    base_url = "https://newsapi.org/v2/everything"
    api_key = "3a7d16eaa9d7489fae472b23492c9a6b"  

    params = {
        "q": company_name,
        "apiKey": api_key,
        "language": "en",
        "sortBy": "relevancy"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if "articles" not in data or not data["articles"]:
            print("No articles found.")
            return []

        # Extract article titles and content
        articles = []
        for article in data["articles"][:5]:
            articles.append(f"{article['title']}: {article['description']}")

        return articles

    except Exception as e:
        print(f"Error fetching news: {e}")
        return []
