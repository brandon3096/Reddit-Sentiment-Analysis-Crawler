import praw
import os

if __name__ == "__main__":    
    reddit = praw.Reddit('RedditSentimentAnalysisBot')

    postIds = {}
    comments = []

    for submission in reddit.subreddit('me_irl').stream.submissions():   
        postIds[submission.id] = True
        submission.comments.replace_more(limit=None)
        comment_queue = submission.comments[:]  # Seed with top-level
        while comment_queue:
            comment = comment_queue.pop(0)
            print(comment.body)
            comments.append(comment)
            comment_queue.extend(comment.replies)

    print(postIds)
    print(comments)