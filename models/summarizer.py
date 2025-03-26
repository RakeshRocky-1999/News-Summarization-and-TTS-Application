from transformers import pipeline

# Load summarizer pipeline
summarizer = pipeline("summarization")

def summarize(text, max_length=150, min_length=50):
    """Summarize the given text using Hugging Face summarization pipeline."""
    if not text.strip():
        return "No content to summarize."

    try:
        # Summarize the content
        summary_result = summarizer(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )
        return summary_result[0]["summary_text"]
    except Exception as e:
        print(f"Error in summarization: {e}")
        return "Error occurred during summarization."

