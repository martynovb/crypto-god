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

nltk.downloader.download('vader_lexicon')
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe("spacytextblob")
sia = SentimentIntensityAnalyzer()

reddit = praw.Reddit(client_id='VIB-kgeb_4moHcs9KpIU6A',
                     client_secret='3FgGRG_evVCX7VsotBTt7NwmQfKDFg',
                     user_agent="VIB-kgeb_4moHcs9KpIU6A/1.0 (by /u/crypto-god)")


class RedditSentimentalAnalyser:

    def fetch_submission_comments(self, submission_id):
        url = f"https://api.pushshift.io/reddit/comment/search?link_id={submission_id}&sort_type=top"

        def fetch_submission_ids_in_time_chunk(self, subreddit_name, chunk_time_interval, chunk_time_range_start):
            submissions = []
            chunk_time_range_end = chunk_time_range_start + chunk_time_interval

            # make API request
            url = f"https://api.pushshift.io/reddit/submission/search?subreddit={subreddit_name}&after={chunk_time_range_start}&before={chunk_time_range_end}&sort_type=top"
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Error {response.status_code}: {response.text}")
                return None

            # process API response
            api_response = response.json()
            for submission in api_response['data']:
                submission_id = submission['id']
                subreddit_id = submission['subreddit_id']
                created_utc = submission['created_utc']
                created_datetime = datetime.datetime.utcfromtimestamp(created_utc)
                created_datetime_str = created_datetime.isoformat()
                title = submission['title']
                selftext = submission['selftext']

                # add submission to list
                submissions.append({
                    "id": submission_id,
                    "subreddit_id": subreddit_id,
                    "created_timestamp": created_utc,
                    "created_timestamp_str": created_datetime_str,
                    "title": title,
                    "selftext": selftext,
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
            return json_obj

    def start(self, subreddits):
        reddit_analysis = []
        for subreddit_name in subreddits:
            print(f"Start sentiment analysis for subreddit: {subreddit_name}")
            query = 'selftext:crypto'
            reddit_analysis.append(self.subreddit_analyse(subreddit_name, query, 'top', 2))
        # assuming your data is stored in a variable named `results`
        with open('reddit_analysis.json', 'w') as f:
            json.dump(reddit_analysis, f)

    def subreddit_analyse(self, subreddit_name, query, sort, limit):
        top_posts = []
        data = {
            "subreddit": subreddit_name,
            "sentiment_historical_data": [
                {
                    "timestamp": datetime.utcnow().isoformat(),  # todo change to specific timerange
                    "top_posts": top_posts
                }
            ]
        }
        subreddit = reddit.subreddit(subreddit_name)
        for submission in subreddit.search(query, sort=sort, limit=limit):
            submission_content = f'{submission.title}\n{submission.selftext}'

            content_sentiment_tb = TextBlob(submission_content).sentiment.polarity
            content_sentiment_vd = sia.polarity_scores(submission_content)['compound']
            content_sentiment_sp = nlp(submission_content)._.blob.polarity
            total_title_sentiment_evg = (content_sentiment_tb + content_sentiment_vd + content_sentiment_sp) / 3

            top_comments = self.get_top_comments_analysis(submission.comments)

            top_posts.append({
                "id": submission.id,
                "timestamp": datetime.utcfromtimestamp(submission.created_utc).isoformat(),
                "top_comments": top_comments,
                "sentiment": {
                    "textblob_post_rate": content_sentiment_tb,
                    "vader_post_rate": content_sentiment_vd,
                    "spacy_post_rate": content_sentiment_sp,
                    "total_post_rate": total_title_sentiment_evg,
                    "textblob_comments_rate": sum(
                        [c['sentiment']['textblob_comments_rate'] for c in top_comments]) / len(
                        top_comments) if top_comments else 0,
                    "vader_comments_rate": sum([c['sentiment']['vader_comments_rate'] for c in top_comments]) / len(
                        top_comments) if top_comments else 0,
                    "spacy_comments_rate": sum([c['sentiment']['spacy_comments_rate'] for c in top_comments]) / len(
                        top_comments) if top_comments else 0,
                    "total_comments_rate": sum([c['sentiment']['total_comments_rate'] for c in top_comments]) / len(
                        top_comments) if top_comments else 0
                }
            })
        return data

    def get_top_comments_analysis(self, comments):
        top_comments = []
        for comment in comments:
            if isinstance(comment, MoreComments):
                continue
            comment_sentiment_tb = TextBlob(comment.body).sentiment.polarity
            comment_sentiment_vd = sia.polarity_scores(comment.body)['compound']
            comment_sentiment_sp = nlp(comment.body)._.blob.polarity
            comments_sentiment_evg = (comment_sentiment_tb + comment_sentiment_vd + comment_sentiment_sp) / 3
            top_comments.append({
                "id": comment.id,
                "sentiment": {
                    "textblob_comments_rate": comment_sentiment_tb,
                    "vader_comments_rate": comment_sentiment_vd,
                    "spacy_comments_rate": comment_sentiment_sp,
                    "total_comments_rate": comments_sentiment_evg
                }
            })
        return top_comments
