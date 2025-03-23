# Company News Sentiment Analysis

This project analyzes the sentiment of news articles related to a company. Users can enter a company name, and the system will fetch relevant news and classify the sentiment as positive, negative, or neutral.

## Features
- Fetches real-time news about a given company
- Performs sentiment analysis using a pre-trained model
- Supports Hindi translation of news content
- Provides voice output for sentiment summary

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/sanjayvmenon/news_analysis.git
   cd news-sentiment-analysis
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. **Run the Flask API:**
   ```sh
   python app.py
   ```

4. **Run the Streamlit frontend:**
   ```sh
   streamlit run web.py
   ```

## How It Works
1. Enter a company name in the frontend.
2. The backend fetches related news articles.
3. Sentiment analysis is performed.
4. Users can translate results into Hindi and hear the sentiment summary using text-to-speech.

## Technologies Used
- **Backend:** Flask (Python)
- **Frontend:** Streamlit
- **Translation:** Google Translate API
- **Text-to-Speech:** gTTS (Google Text-to-Speech)

## License
This project is licensed under the MIT License.

---

