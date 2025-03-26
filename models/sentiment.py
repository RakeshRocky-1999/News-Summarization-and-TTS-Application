from textblob import TextBlob

def analyze_sentiment(text):
    """Analyze sentiment using TextBlob with confidence threshold."""
    if not text.strip():
        return "Neutral"

    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    # Confidence threshold to determine neutral sentiment
    if -0.05 < polarity < 0.05:
        return "Neutral"
    elif polarity > 0:
        return "Positive"
    else:
        return "Negative"

