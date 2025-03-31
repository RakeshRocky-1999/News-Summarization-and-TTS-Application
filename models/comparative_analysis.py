# import json
# from collections import Counter
# from difflib import SequenceMatcher


# def calculate_sentiment_distribution(article_data):
#     """Calculate sentiment distribution from articles."""
#     sentiment_counter = Counter(article["Sentiment"].lower() for article in article_data)
#     return dict(sentiment_counter)


# def compare_articles(summary1, summary2, article_index_1=0, article_index_2=1):
#     """Compare summaries to identify key differences."""
#     similarity_ratio = SequenceMatcher(None, summary1, summary2).ratio()
#     if similarity_ratio < 0.7:  # Considered different if similarity is below 70%
#         return (
#             f"Article {article_index_1 + 1}: {summary1[:50]}... "
#             f"vs. Article {article_index_2 + 1}: {summary2[:50]}..."
#         )
#     return None


# def compare_topics(topics_1, topics_2):
#     """Compare article topics to find common and unique topics."""
#     topics_1_set = set(topics_1)
#     topics_2_set = set(topics_2)

#     common_topics = list(topics_1_set.intersection(topics_2_set))
#     unique_article_1 = list(topics_1_set.difference(topics_2_set))
#     unique_article_2 = list(topics_2_set.difference(topics_1_set))

#     return {
#         "Common Topics": common_topics if len(common_topics) > 0 else None,
#         "Unique Topics in Article 1": unique_article_1 if len(unique_article_1) > 0 else None,
#         "Unique Topics in Article 2": unique_article_2 if len(unique_article_2) > 0 else None,
#     }


# def generate_comparative_analysis(article_data, output_file):
#     """Generate comparative sentiment analysis and topic overlap."""
#     coverage_differences = []
#     topic_overlap_info = {"Common Topics": set(), "Unique Topics": set()}

#     for i in range(len(article_data) - 1):
#         for j in range(i + 1, len(article_data)):
#             article_1 = article_data[i]
#             article_2 = article_data[j]

#             # Compare articles for summary differences
#             diff_summary = compare_articles(
#                 article_1["Summary"], article_2["Summary"], i, j
#             )
#             diff_topics = compare_topics(article_1["Topics"], article_2["Topics"])

#             if diff_summary:
#                 coverage_differences.append(
#                     {
#                         "Comparison": diff_summary,
#                         "Impact": (
#                             "Potential impact on public perception due to differences in focus."
#                         ),
#                     }
#                 )

#             # Update topic overlap correctly
#             if diff_topics["Common Topics"] is not None:
#                 topic_overlap_info["Common Topics"].update(diff_topics["Common Topics"])
#             if diff_topics["Unique Topics in Article 1"] is not None:
#                 topic_overlap_info["Unique Topics"].update(diff_topics["Unique Topics in Article 1"])
#             if diff_topics["Unique Topics in Article 2"] is not None:
#                 topic_overlap_info["Unique Topics"].update(diff_topics["Unique Topics in Article 2"])

#     # Final results
#     results = {
#         "Sentiment Distribution": calculate_sentiment_distribution(article_data),
#         "Coverage Differences": coverage_differences
#         or [{"Comparison": "No major differences found.", "Impact": "Neutral coverage."}],
#         "Topic Overlap": {
#             "Common Topics": list(topic_overlap_info["Common Topics"])
#             if topic_overlap_info["Common Topics"]
#             else ["None"],
#             "Unique Topics": list(topic_overlap_info["Unique Topics"])
#             if topic_overlap_info["Unique Topics"]
#             else ["None"],
#         },
#     }

#     # Save to output file
#     with open(output_file, "w", encoding="utf-8") as file:
#         json.dump(results, file, ensure_ascii=False, indent=4)


#above codes for local machine directory
#--------------------------------------------------------------------------------------------
#below codes for docker directory


import json
import os
from collections import Counter
from difflib import SequenceMatcher


def calculate_sentiment_distribution(article_data):
    """Calculate sentiment distribution from articles."""
    sentiment_counter = Counter(
        article.get("Sentiment", "").lower() for article in article_data if article.get("Sentiment")
    )
    return dict(sentiment_counter)


def compare_articles(summary1, summary2, article_index_1=0, article_index_2=1):
    """Compare summaries to identify key differences."""
    if not summary1 or not summary2:
        return f"Article {article_index_1 + 1} or {article_index_2 + 1} has no summary."
    
    similarity_ratio = SequenceMatcher(None, summary1, summary2).ratio()
    if similarity_ratio < 0.7:  # Considered different if similarity is below 70%
        return (
            f"Article {article_index_1 + 1}: {summary1[:50]}... "
            f"vs. Article {article_index_2 + 1}: {summary2[:50]}..."
        )
    return None


def compare_topics(topics_1, topics_2):
    """Compare article topics to find common and unique topics."""
    topics_1_set = set(topics_1) if topics_1 else set()
    topics_2_set = set(topics_2) if topics_2 else set()

    common_topics = list(topics_1_set.intersection(topics_2_set))
    unique_article_1 = list(topics_1_set.difference(topics_2_set))
    unique_article_2 = list(topics_2_set.difference(topics_1_set))

    return {
        "Common Topics": common_topics if common_topics else None,
        "Unique Topics in Article 1": unique_article_1 if unique_article_1 else None,
        "Unique Topics in Article 2": unique_article_2 if unique_article_2 else None,
    }


def generate_comparative_analysis(article_data, output_file):
    """Generate comparative sentiment analysis and topic overlap."""
    coverage_differences = []
    topic_overlap_info = {"Common Topics": set(), "Unique Topics": set()}

    for i in range(len(article_data) - 1):
        for j in range(i + 1, len(article_data)):
            article_1 = article_data[i]
            article_2 = article_data[j]

            # Compare articles for summary differences
            diff_summary = compare_articles(
                article_1.get("Summary", ""), article_2.get("Summary", ""), i, j
            )
            diff_topics = compare_topics(
                article_1.get("Topics", []), article_2.get("Topics", [])
            )

            if diff_summary:
                coverage_differences.append(
                    {
                        "Comparison": diff_summary,
                        "Impact": (
                            "Potential impact on public perception due to differences in focus."
                        ),
                    }
                )

            # Update topic overlap correctly
            if diff_topics["Common Topics"]:
                topic_overlap_info["Common Topics"].update(diff_topics["Common Topics"])
            if diff_topics["Unique Topics in Article 1"]:
                topic_overlap_info["Unique Topics"].update(diff_topics["Unique Topics in Article 1"])
            if diff_topics["Unique Topics in Article 2"]:
                topic_overlap_info["Unique Topics"].update(diff_topics["Unique Topics in Article 2"])

    # Final results
    results = {
        "Sentiment Distribution": calculate_sentiment_distribution(article_data),
        "Coverage Differences": coverage_differences
        or [{"Comparison": "No major differences found.", "Impact": "Neutral coverage."}],
        "Topic Overlap": {
            "Common Topics": list(topic_overlap_info["Common Topics"])
            if topic_overlap_info["Common Topics"]
            else ["None"],
            "Unique Topics": list(topic_overlap_info["Unique Topics"])
            if topic_overlap_info["Unique Topics"]
            else ["None"],
        },
    }

    # Ensure the directory exists before writing
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Save to output file with error handling
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(results, file, ensure_ascii=False, indent=4)
    except PermissionError:
        raise PermissionError(f"Unable to write to {output_file}. Check file permissions.")

