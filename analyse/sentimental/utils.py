import nltk
import spacy
from textblob import TextBlob
from spacytextblob.spacytextblob import SpacyTextBlob
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.downloader.download('vader_lexicon')
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe("spacytextblob")
sia = SentimentIntensityAnalyzer()


def text_sentimental_analysis(text):
    sentiment_tb = TextBlob(text).sentiment.polarity
    sentiment_vd = sia.polarity_scores(text)['compound']
    sentiment_sp = nlp(text)._.blob.polarity
    total_sentiment_evg = (sentiment_tb + sentiment_vd + sentiment_sp) / 3
    return {
        "tb": sentiment_tb,
        "vd": sentiment_vd,
        "sp": sentiment_sp,
        "total": total_sentiment_evg
    }
