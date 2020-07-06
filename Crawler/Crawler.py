import praw
import os

if __name__ == "__main__":    
    reddit = praw.Reddit('RedditSentimentAnalysisBot')

    postIds = []
    comments = []

    for submission in reddit.subreddit('me_irl').stream.submissions():   
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            print(comment.body)
            #comments.append(comment)

    print("BEANS")