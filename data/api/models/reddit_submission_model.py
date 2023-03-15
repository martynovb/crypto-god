class RedditSubmissionModel:
    def __init__(self, submission_id, subreddit_id, created_utc, title, self_text):
        self.submission_id = submission_id
        self.subreddit_id = subreddit_id
        self.created_utc = created_utc
        self.title = title
        self.self_text = self_text

    def __str__(self):
        return f"RedditSubmissionModel(submission_id={self.submission_id}, subreddit_id={self.subreddit_id}, created_utc={self.created_utc}')"
