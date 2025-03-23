import json
from textblob import TextBlob
import os


def analyze_sentiment(text):
    """Analyze sentiment of a given text using TextBlob."""
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"


def analyze_articles(input_path, output_path):
    """Analyze sentiment of summarized articles and save results."""
    with open(input_path, "r", encoding="utf-8") as file:
        news_data = json.load(file)

    articles = news_data.get("Summarized_Articles", [])

    analyzed_articles = []
    
    for article in articles:
        summary = article.get("Summary", "")
        
        if summary:
            sentiment = analyze_sentiment(summary)
        else:
            sentiment = "No content available."

        analyzed_articles.append({
            "Title": article["Title"],
            "Summary": summary,
            "Sentiment": sentiment,
            "Link": article["Link"]
        })

    # Save analyzed articles to a JSON file
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump({"Analyzed_Articles": analyzed_articles}, file, ensure_ascii=False, indent=4)
    
    print(f"Sentiment analysis saved to {output_path}")


# Run sentiment analysis if called directly
if __name__ == "__main__":
    # Get the base directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Corrected data directory path
    data_dir = os.path.join(base_dir, "../data")
    os.makedirs(data_dir, exist_ok=True)

    # Updated input and output paths
    input_path = os.path.join(base_dir, "../data/summarized_news.json")
    output_path = os.path.join(base_dir, "../data/sentiment_news.json")

    analyze_articles(input_path, output_path)
