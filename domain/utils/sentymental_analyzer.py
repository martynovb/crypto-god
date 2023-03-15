import nltk
import spacy
from textblob import TextBlob
from spacytextblob.spacytextblob import SpacyTextBlob
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.downloader.download('vader_lexicon')
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe("spacytextblob")
sia = SentimentIntensityAnalyzer()


class SentimentalAnalyzer:

    def analyze(self, text: str):
        sentiment_tb = self._tb_analyzer(text)
        sentiment_vd = self._vd_analyzer(text)
        sentiment_sp = self._sp_analyzer(text)
        total_sentiment_evg = (sentiment_tb + sentiment_vd + sentiment_sp) / 3
        return {
            "tb": sentiment_tb,
            "vd": sentiment_vd,
            "sp": sentiment_sp,
            "total": total_sentiment_evg
        }

    def _tb_analyzer(self, text: str):
        return TextBlob(text).sentiment.polarity

    def _vd_analyzer(self, text: str):
        return sia.polarity_scores(text)['compound']

    def _sp_analyzer(self, text: str):
        return nlp(text)._.blob.polarity
