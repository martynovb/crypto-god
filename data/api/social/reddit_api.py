import requests
import datetime
from typing import List

from data.api.models.reddit_comment_model import RedditCommentModel
from data.api.models.reddit_submission_model import RedditSubmissionModel


class RedditAPI:
    def __init__(self):
        self.base_url = "https://api.pushshift.io/reddit"

    def _get(self, endpoint, params=None):
        response = requests.get(f"{self.base_url}/{endpoint}", params=params)
        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            return None
        return response.json()

    def get_submissions(self, subreddit, before=None, after=None, limit=10, sort="score") \
            -> List[RedditSubmissionModel]:
        params = {"subreddit": subreddit, "limit": limit, "sort": sort,
                  "filter": "id,subreddit_id,created_utc,title,selftext"}
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        response = self._get("submission/search", params=params)
        if response:
            submissions = response.get("data", [])
            return list(map(lambda item: RedditSubmissionModel(item['id'], item['subreddit_id'], item['created_utc'],
                                                               item['title'], item['selftext']), submissions))

    def get_comments(self, subreddit, before=None, after=None, limit=10, sort="score") \
            -> List[RedditCommentModel]:
        params = {"subreddit": subreddit, "limit": limit, "sort": sort,
                  "filter": "id,subreddit_id,created_utc,body"}
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        response = self._get("comment/search", params=params)
        if response:
            comments = response.get("data", [])
            return list(map(lambda item: RedditCommentModel(item['id'], item['subreddit_id'], item['created_utc'],
                                                            item['body'], ), comments))
