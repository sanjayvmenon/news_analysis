from flask import Flask, request, jsonify
import spacy
from bs4 import BeautifulSoup
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import Counter
import gtts
import subprocess
from googletrans import Translator
from flask_cors import CORS
import platform

app = Flask(__name__)
CORS(app)  # Enable frontend access

#  Load spaCy for Named Entity Recognition
nlp = spacy.load("en_core_web_sm")

@app.route("/analyze", methods=["GET"])
def analyze_sentiment():
    company = request.args.get("company", "").strip().lower()
    if not company:
        return jsonify({"error": "Company name is required"}), 400

    analyzer = SentimentIntensityAnalyzer()
    translator = Translator()
    company_news = []

    for page in range(1, 6):  #  Scrape pages 1 to 5
        url = f"https://www.gadgets360.com/news/page-{page}" if page > 1 else "https://www.gadgets360.com/news"
        response = requests.get(url)

        if response.status_code != 200:
            continue  # Skip if page fails

        soup = BeautifulSoup(response.text, 'lxml')
        news = soup.find_all('div', class_='caption_box')

        for new in news:
            title_tag = new.find('span', class_='news_listing')
            link_tag = new.find('a')

            if title_tag and link_tag:
                title = title_tag.text.lower().strip()
                news_url = link_tag['href']
                if not news_url.startswith("http"):
                    news_url = "https://www.gadgets360.com" + news_url  

                if company in title:
                    sentiment_score = analyzer.polarity_scores(title)['compound']
                    sentiment = "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral"

                    #  Get full article summary
                    news_response = requests.get(news_url, headers={"User-Agent": "Mozilla/5.0"})
                    news_soup = BeautifulSoup(news_response.text, 'lxml')

                    content_div = news_soup.find('div', class_='content_text')

                    if content_div:
                        paragraphs = content_div.find_all('p')
                        full_summary = " ".join(p.text.strip() for p in paragraphs[:3])
                        summary = " ".join(full_summary.split()[:10]) + "..."  

                    else:
                        summary = "No summary available."

                    #  Store data
                    company_news.append({
                        "title": title,
                        "summary": summary,
                        "sentiment": sentiment
                    })

    if company_news:
        #  Sentiment Analysis Summary
        sentiment_counts = Counter([news["sentiment"] for news in company_news])
        overall_sentiment = (
            "Positive" if sentiment_counts["Positive"] > sentiment_counts["Negative"] else
            "Negative" if sentiment_counts["Negative"] > sentiment_counts["Positive"] else
            "Neutral"
        )

        #  Generate Final Report
        final_report = f"The latest news coverage on '{company.capitalize()}' is {overall_sentiment.lower()}."
        translated_report = translator.translate(final_report, dest="hi").text

        #  Convert Hindi Report to Speech
        tts = gtts.gTTS(translated_report, lang="hi")
        audio_file = "final_report.mp3"
        tts.save(audio_file)

        #  Play Hindi Audio (Based on OS)
        if platform.system() == "Darwin":  
            subprocess.run(["afplay", audio_file], check=True)
        elif platform.system() == "Windows":  
            subprocess.run(["start", "wmplayer", audio_file], shell=True)
        elif platform.system() == "Linux":  
            subprocess.run(["mpg321", audio_file])
            

        #  Send JSON Response
        response_data = {
            "news_articles": company_news,
            "comparative_sentiment_analysis": {
                "positive_news_count": sentiment_counts["Positive"],
                "negative_news_count": sentiment_counts["Negative"],
                "neutral_news_count": sentiment_counts["Neutral"],
                "overall_sentiment": overall_sentiment
            },
            "final_report": {
                "english": final_report,
                "hindi": translated_report
            }
        }

        return jsonify(response_data)

    return jsonify({"message": f"No news found for '{company}'"}), 404

if __name__ == "__main__":
    app.run(debug=True)