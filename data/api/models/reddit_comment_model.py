class RedditCommentModel:
    def __init__(self, submission_id, subreddit_id, created_utc, body):
        self.submission_id = submission_id
        self.subreddit_id = subreddit_id
        self.created_utc = created_utc
        self.body = body

    def __str__(self):
        return f"RedditCommentModel(submission_id={self.submission_id}, subreddit_id={self.subreddit_id}, created_utc={self.created_utc})"
