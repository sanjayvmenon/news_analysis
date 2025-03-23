import streamlit as st
import requests

st.title("📢 Company News Sentiment Analysis")

#  User input for company name
company_name = st.text_input("Enter a company name")

if st.button("Analyze News"):
    with st.spinner("Fetching data..."):
        try:
            response = requests.get(f"http://127.0.0.1:5000/analyze?company={company_name}")
            if response.status_code == 200:
                data = response.json()

                #  Display news articles
                st.subheader("📰 News Articles & Sentiments:")
                for i, article in enumerate(data["news_articles"], start=1):
                    st.write(f"**{i}. {article['title']}**")
                    st.write(f"   - Summary: {article['summary']}")
                    st.write(f"   - Sentiment: {article['sentiment']}")
                    st.write("------")

                #  Display sentiment analysis
                st.subheader("📊 Comparative Sentiment Analysis:")
                st.json(data["comparative_sentiment_analysis"])

                #  Display final report
                st.subheader("📢 Final Report:")
                st.write(f"**English:** {data['final_report']['english']}")
                st.write(f"**Hindi:** {data['final_report']['hindi']}")

            else:
                st.error("No News.")

        except requests.exceptions.RequestException as e:
            st.error("Error connecting to API.")