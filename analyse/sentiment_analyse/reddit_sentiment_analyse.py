import praw
import nltk
import spacy
from textblob import TextBlob
from spacytextblob.spacytextblob import SpacyTextBlob
from nltk.sentiment import SentimentIntensityAnalyzer

from praw.models import MoreComments
import json
import requests
import time
import datetime

from analyse.sentiment_analyse.utils import text_sentimental_analysis

nltk.downloader.download('vader_lexicon')
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe("spacytextblob")
sia = SentimentIntensityAnalyzer()

reddit = praw.Reddit(client_id='VIB-kgeb_4moHcs9KpIU6A',
                     client_secret='3FgGRG_evVCX7VsotBTt7NwmQfKDFg',
                     user_agent="VIB-kgeb_4moHcs9KpIU6A/1.0 (by /u/crypto-god)")


class RedditSentimentalAnalyser:

    def fetch_comments_in_time_chunk(self, subreddit_name, chunk_time_interval, chunk_time_range_start, limit):
        comments = []
        chunk_time_range_end = chunk_time_range_start + chunk_time_interval
        # make API request
        url = f"https://api.pushshift.io/reddit/comment/search?subreddit={subreddit_name}&after={chunk_time_range_start}&before={chunk_time_range_end}&filter=id,subreddit_id,created_utc,body&sort=score&limit={limit}"
        # print(f"requesting...\n${url}")
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            return None

        # process API response
        api_response = response.json()
        for submission in api_response["data"]:
            submission_id = submission["id"]
            subreddit_id = submission["subreddit_id"]
            created_utc = submission["created_utc"]
            created_datetime = datetime.datetime.utcfromtimestamp(created_utc)
            created_datetime_str = created_datetime.isoformat()
            body = submission["body"]

            # add submission to list
            comments.append({
                "id": submission_id,
                "subreddit_id": subreddit_id,
                "subreddit": subreddit_name,
                "created_timestamp": created_utc,
                "created_timestamp_str": created_datetime_str,
                "sentimental": text_sentimental_analysis(body)
            })

        # create JSON object
        json_obj = {
            "chunk_time_range_start": chunk_time_range_start,
            "chunk_time_range_end": chunk_time_range_start,
            "chunk_time_range_start_str": datetime.datetime.utcfromtimestamp(chunk_time_range_start).isoformat(),
            "chunk_time_range_end_str": datetime.datetime.utcfromtimestamp(chunk_time_range_end).isoformat(),
            "submissions": comments
        }
        print(json_obj)
        return comments

    def fetch_submission_in_time_chunk(self, subreddit_name, chunk_time_interval, chunk_time_range_start, limit):
        submissions = []
        chunk_time_range_end = chunk_time_range_start + chunk_time_interval

        # make API request
        url = f"https://api.pushshift.io/reddit/submission/search?subreddit={subreddit_name}&after={chunk_time_range_start}&before={chunk_time_range_end}&filter=id,subreddit_id,created_utc,title,selftext&sort=score&limit={limit}"
        # print(f"requesting...\n${url}")
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            return None

        # process API response
        api_response = response.json()
        for submission in api_response["data"]:
            submission_id = submission["id"]
            subreddit_id = submission["subreddit_id"]
            created_utc = submission["created_utc"]
            created_datetime = datetime.datetime.utcfromtimestamp(created_utc)
            created_datetime_str = created_datetime.isoformat()
            title = submission["title"]
            self_text = submission["selftext"]

            if self_text != "" and self_text[0] == "[":
                self_text = ""

            # add submission to list
            submissions.append({
                "id": submission_id,
                "subreddit_id": subreddit_id,
                "subreddit": subreddit_name,
                "created_timestamp": created_utc,
                "created_timestamp_str": created_datetime_str,
                "sentimental": text_sentimental_analysis(f"{title} {self_text}"),
            })

        # create JSON object
        json_obj = {
            "chunk_time_range_start": chunk_time_range_start,
            "chunk_time_range_end": chunk_time_range_start,
            "chunk_time_range_start_str": datetime.datetime.utcfromtimestamp(chunk_time_range_start).isoformat(),
            "chunk_time_range_end_str": datetime.datetime.utcfromtimestamp(chunk_time_range_end).isoformat(),
            "submissions": submissions
        }
        print(json_obj)
        return submissions

    def analyse(self, subreddits, start_date, end_date, chunk_time_interval, limit, ):
        reddit_analysis = []
        for subreddit_name in subreddits:
            print(f"Start sentiment analysis for subreddit: {subreddit_name}")
            sentiment_historical_data = []
            fetch_count = int((end_date - start_date) / chunk_time_interval)
            chunk_time_range_start = start_date
            chunk_time_range_end = chunk_time_range_start + chunk_time_interval
            for i in range(fetch_count):
                time.sleep(3)
                submissions = self.fetch_submission_in_time_chunk(subreddit_name, chunk_time_interval,
                                                                  chunk_time_range_start, limit)
                time.sleep(3)
                comments = self.fetch_comments_in_time_chunk(subreddit_name, chunk_time_interval,
                                                             chunk_time_range_start, limit)
                chunk = {
                    "chunk_time_range_start": chunk_time_range_start,
                    "chunk_time_range_end": chunk_time_range_end,
                    "chunk_time_range_start_str": datetime.datetime.utcfromtimestamp(
                        chunk_time_range_start).isoformat(),
                    "chunk_time_range_end_str": datetime.datetime.utcfromtimestamp(chunk_time_range_end).isoformat(),
                    "submissions": submissions,
                    "comments": comments,
                    "submissions_sentimental": {},
                    "comments_sentimental": {},
                    "total_sentimental": {
                        'tb': 0.0,
                        'vd': 0.0,
                        'sp': 0.0,
                        'total': 0.0
                    },
                }

                total_submissions = len(chunk['submissions'])
                total_comments = len(chunk['comments'])
                submissions_sentimental_sum = {
                    'tb': 0.0,
                    'vd': 0.0,
                    'sp': 0.0,
                    'total': 0.0
                }
                comments_sentimental_sum = {
                    'tb': 0.0,
                    'vd': 0.0,
                    'sp': 0.0,
                    'total': 0.0
                }

                for submission in chunk['submissions']:
                    for k, v in submission['sentimental'].items():
                        submissions_sentimental_sum[k] += v
                chunk['submissions_sentimental'] = {k: v / total_submissions for k, v in
                                                    submissions_sentimental_sum.items()}

                for comment in chunk['comments']:
                    for k, v in comment['sentimental'].items():
                        comments_sentimental_sum[k] += v
                chunk['comments_sentimental'] = {k: v / total_comments for k, v in
                                                 comments_sentimental_sum.items()}

                for k in chunk['comments_sentimental'].keys():
                    chunk['total_sentimental'][k] = (chunk['submissions_sentimental'][k] +
                                                     chunk['comments_sentimental'][k]) / 2

                sentiment_historical_data.append(chunk)
                chunk_time_range_start = chunk_time_range_start + chunk_time_interval
                chunk_time_range_end = chunk_time_range_start + chunk_time_interval
            reddit_analysis.append(
                {"subreddit": subreddit_name, "sentiment_historical_data": sentiment_historical_data})

        # assuming your data is stored in a variable named `results`
        with open('reddit_analysis.json', 'w') as f:
            json.dump(reddit_analysis, f)
