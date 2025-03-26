import streamlit as st
import requests
import os

# Corrected API URL for FastAPI (using api.py endpoint)
API_URL = "http://127.0.0.1:8000/process"


def main():
    """Streamlit UI for News Analysis, Sentiment Comparison, and Hindi TTS Application."""
    st.title("📰 News Analysis, Sentiment Comparison, and Hindi TTS Application")
    st.write(
        "Enter a company name to extract news, analyze sentiment, summarize, "
        "compare sentiment, and convert the analysis to Hindi speech."
    )

    # Input field for the company name
    company_name = st.text_input("🏢 Enter Company Name:", "")

    # Submit button to trigger API call
    if st.button("🚀 Generate Analysis"):
        if company_name.strip():  # Validate non-empty input
            # Send POST request to FastAPI
            try:
                response = requests.post(API_URL, json={"company_name": company_name.strip()})

                if response.status_code == 200:
                    result = response.json()

                    # ✅ Display extracted articles and sentiment
                    st.subheader(f"📚 News Analysis for: {company_name}")
                    articles = result.get("Articles", [])
                    for idx, article in enumerate(articles, start=1):
                        st.write(f"### 📝 Article {idx}")
                        st.write(f"**Title:** {article['Title']}")
                        st.write(f"**Summary:** {article['Summary']}")
                        st.write(f"**Sentiment:** {article['Sentiment']}")
                        st.write(f"**Topics:** {', '.join(article['Topics'])}")

                    # 📊 Display Comparative Sentiment Analysis
                    comparative_results = result.get("Comparative Sentiment Score", {})
                    if comparative_results:
                        st.subheader("📈 Comparative Sentiment Analysis Results")

                        # 🎯 Sentiment Distribution
                        sentiment_dist = comparative_results.get("Sentiment Distribution", {})
                        st.write("**Sentiment Distribution:**")
                        st.json(sentiment_dist)

                        # 🔎 Coverage Differences
                        coverage_diff = comparative_results.get("Coverage Differences", [])

                        st.subheader("🔀 Coverage Differences")
                        if isinstance(coverage_diff, list):
                            for diff in coverage_diff:
                                if isinstance(diff, dict):
                                    st.markdown(
                                        f"""
                                        - **Comparison:** {diff.get('Comparison', 'No Comparison Available')}
                                        - **Impact:** {diff.get('Impact', 'No Impact Available')}
                                        """
                                    )
                        else:
                            st.write("⚠️ No valid coverage differences found.")

                        # 🧠 Topic Overlap
                        topic_overlap = comparative_results.get("Topic Overlap", {})
                        if topic_overlap:
                            st.subheader("🔗 Topic Overlap")

                            common_topics = topic_overlap.get("Common Topics", [])
                            unique_article_1 = topic_overlap.get("Unique Topics in Article 1", [])
                            unique_article_2 = topic_overlap.get("Unique Topics in Article 2", [])

                            st.markdown(
                                f"""
                                - **Common Topics:** {', '.join(common_topics) if common_topics else 'None'}
                                - **Unique Topics in Article 1:** {', '.join(unique_article_1) if unique_article_1 else 'None'}
                                - **Unique Topics in Article 2:** {', '.join(unique_article_2) if unique_article_2 else 'None'}
                                """
                            )
                        else:
                            st.write("⚠️ No valid topic overlap information available.")

                    # 📝 Display Final Sentiment Analysis
                    st.subheader("💡 Final Sentiment Analysis")
                    final_sentiment = result.get("Final Sentiment Analysis", "No analysis available.")
                    st.write(f"**Summary:** {final_sentiment}")

                    # 🎙️ Hindi Text-to-Speech (TTS) Section
                    audio_path = result.get("Audio", "")
                    if audio_path and os.path.isfile(audio_path):
                        st.subheader("🔊 Hindi Text-to-Speech Output")
                        st.audio(audio_path, format="audio/wav")
                        st.success("✅ Audio generated successfully!")

                        # Provide download option for generated audio
                        with open(audio_path, "rb") as audio_file:
                            st.download_button(
                                "⬇️ Download Audio",
                                audio_file,
                                file_name="hindi_tts_output.wav",
                                mime="audio/wav",
                            )
                    else:
                        st.warning("⚠️ No audio generated or file missing.")

                else:
                    st.error(f"❌ Error processing the request. HTTP Status: {response.status_code}")
                    st.write(response.text)

            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Error connecting to the API: {e}")

        else:
            st.warning("⚠️ Please enter a valid company name.")


if __name__ == "__main__":
    main()
