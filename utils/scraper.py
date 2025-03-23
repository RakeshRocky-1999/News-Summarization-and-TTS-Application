import requests
import json
import os

# Define function to fetch news articles using NewsAPI
def extract_news(company, api_key, num_articles=10):
    url = f"https://newsapi.org/v2/everything?q={company}&apiKey={api_key}&pageSize={num_articles}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        articles = []
        for article in data["articles"]:
            articles.append({
                "Title": article["title"],
                "Summary": article["description"],
                "Link": article["url"]
            })
        
        # Correctly set path to data directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "../data")
        
        # Create data directory if it does not exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Save articles to a JSON file
        output_file_path = os.path.join(data_dir, "news.json")
        with open(output_file_path, "w", encoding="utf-8") as file:
            json.dump({"Articles": articles}, file, ensure_ascii=False, indent=4)
        
        print(f"News articles saved to {output_file_path}")
    else:
        print(f"Error fetching news: {response.status_code}")
        return []

# Example usage
if __name__ == "__main__":
    API_KEY = "3a7d16eaa9d7489fae472b23492c9a6b"  # Replace with your NewsAPI key
    company_name = "Tesla"  # Example company name
    extract_news(company_name, API_KEY)