import praw
import os
import mysql_dbconfig
import mysql_queryhandler
import mysql.connector
import random
from datetime import date, datetime

if __name__ == "__main__":    
    reddit = praw.Reddit('RedditSentimentAnalysisBot')

    postIds = {}
    comments = []
    handler = mysql_queryhandler.queryhandler(10)
    count = 0    

    try:
        for submission in reddit.subreddit('me_irl').stream.submissions():   
            print("New submission")
            postIds[submission.id] = True
            submission.comments.replace_more(limit=None)
            comment_queue = submission.comments[:]  # Seed with top-level
            while comment_queue:
                comment = comment_queue.pop(0)                
                insert_comment = ("TEST"+str(count), "Reddit", random.randrange(1, 1000), datetime.now())
                handler.add_to_queue(insert_comment)
                comments.append(comment)
                comment_queue.extend(comment.replies)
                print("Push to queue: ", count)
                count += 1
    except KeyboardInterrupt:
        del handler

    