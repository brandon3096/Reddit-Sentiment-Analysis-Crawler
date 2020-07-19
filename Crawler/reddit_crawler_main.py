import praw
import os
import mysql_dbconfig
import mysql_queryhandler
import mysql.connector
import random
from datetime import date, datetime

#TODO use newer version of wordnet nouns
#TODO add word analysis to main crawler logic

if __name__ == "__main__":    
    # Initialize
    reddit = praw.Reddit('RedditSentimentAnalysisBot')
    postIds = {}
    comments = []
    handler = mysql_queryhandler.queryhandler(50)

    # Get tracked stocks
    stocks = handler.get_valid_stocks()

    # Get word sentiments
    

    # Process comment stream
    try:
        for submission in reddit.subreddit('wallstreetbets').stream.submissions():   
            postIds[submission.id] = True
            submission.comments.replace_more(limit=None)
            comment_queue = submission.comments[:]  # Seed with top-level
            while comment_queue:
                comment = comment_queue.pop(0)    
                for x in comment.body.split(' '):
                    if x in stocks:
                        insert_comment = (x, "Reddit", random.randrange(1, 1000), datetime.now())
                        handler.add_to_queue(insert_comment)
                        print("Found mention of {} in {}".format(x, comment.body))
                comments.append(comment)
                comment_queue.extend(comment.replies)
    except KeyboardInterrupt:
        del handler

    