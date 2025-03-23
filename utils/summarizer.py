import json
import numpy as np
import tensorflow as tf
from transformers import BertTokenizer, TFBertModel
import os


class BertSummarizer:
    def __init__(self, model_name="bert-base-uncased"):
        # Load BERT tokenizer and model
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = TFBertModel.from_pretrained(model_name)

    def tokenize_text(self, sentences):
        """Tokenize and encode sentences."""
        inputs = self.tokenizer(
            sentences,
            return_tensors="tf",
            padding=True,
            truncation=True,
            max_length=512,
            add_special_tokens=True,
        )
        return inputs

    def get_sentence_embeddings(self, inputs):
        """Get sentence embeddings using BERT."""
        # Get BERT output
        outputs = self.model(inputs["input_ids"], attention_mask=inputs["attention_mask"])
        cls_embeddings = outputs.last_hidden_state[:, 0, :]  # [CLS] token embedding
        return cls_embeddings

    def rank_sentences(self, embeddings, sentences, num_sentences=3):
        """Rank sentences based on cosine similarity with mean embedding."""
        # Calculate mean embedding
        mean_embedding = tf.reduce_mean(embeddings, axis=0)

        # Calculate cosine similarity between sentence embeddings and mean
        similarities = tf.keras.losses.cosine_similarity(embeddings, mean_embedding, axis=-1).numpy()
        ranked_indices = np.argsort(similarities)

        # Select top-ranked sentences
        selected_indices = ranked_indices[:num_sentences]
        selected_indices = np.sort(selected_indices)
        summary = [sentences[i] for i in selected_indices]
        return " ".join(summary)

    def summarize(self, text, num_sentences=3):
        """Main summarization function."""
        # Split text into sentences
        sentences = text.split(". ")
        if len(sentences) <= num_sentences:
            return text

        # Tokenize and get embeddings
        inputs = self.tokenize_text(sentences)
        embeddings = self.get_sentence_embeddings(inputs)

        # Rank and select top sentences
        summary = self.rank_sentences(embeddings, sentences, num_sentences)
        return summary


# Load news data and summarize
def summarize_articles(input_path, output_path, num_sentences=3):
    """Load articles from JSON and summarize."""
    with open(input_path, "r", encoding="utf-8") as file:
        news_data = json.load(file)

    articles = news_data.get("Articles", [])

    # Create summarizer instance
    summarizer = BertSummarizer()
    summarized_articles = []
    
    for article in articles:
        if article["Summary"]:
            summary = summarizer.summarize(article["Summary"], num_sentences)
        else:
            summary = "No content available."
        
        summarized_articles.append({
            "Title": article["Title"],
            "Summary": summary,
            "Link": article["Link"]
        })

    # Save summarized articles to a JSON file
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump({"Summarized_Articles": summarized_articles}, file, ensure_ascii=False, indent=4)
    
    print(f"Summarized articles saved to {output_path}")


# Run summarization if called directly
if __name__ == "__main__":
    # Get the base directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Corrected data directory path
    data_dir = os.path.join(base_dir, "../data")
    os.makedirs(data_dir, exist_ok=True)

    # Updated input and output paths
    input_path = os.path.join(base_dir, "../data/news.json")
    output_path = os.path.join(base_dir, "../data/summarized_news.json")

    summarize_articles(input_path, output_path)



