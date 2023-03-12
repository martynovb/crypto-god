from data.api.social.reddit_api import RedditAPI

reddit_api = RedditAPI()

# get 100 submissions from the "python" subreddit
submissions = reddit_api.get_submissions("python", limit=10)

# print the titles of the submissions
for submission in submissions:
    print(submission)

# get 100 comments from the "python" subreddit
comments = reddit_api.get_comments("python", limit=10)

# print the bodies of the comments
for comment in comments:
    print(comment)