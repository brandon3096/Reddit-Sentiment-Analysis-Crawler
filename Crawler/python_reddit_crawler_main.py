import praw
import os
import python_mysql_dbconfig
import mysql.connector

if __name__ == "__main__":    
    reddit = praw.Reddit('RedditSentimentAnalysisBot')

    postIds = {}
    comments = []

    count = 0

    for submission in reddit.subreddit('me_irl').stream.submissions():   
        print("New submission")
        postIds[submission.id] = True
        submission.comments.replace_more(limit=None)
        comment_queue = submission.comments[:]  # Seed with top-level
        while comment_queue:
            comment = comment_queue.pop(0)
            print(comment.body)
            comments.append(comment)
            comment_queue.extend(comment.replies)
            count += 1
            if (count == 5):
                break
        if (count == 5):
                break

    # Connect to DB
    db = python_mysql_dbconfig.read_db_config()
    mysql_connection = mysql.connector.connect(**db)

    query = "SELECT * FROM stocks_list"
    cursor = mysql_connection.cursor()

    cursor.execute(query)
    ticker = ""
    fullname = ""

    for (ticker, fullname) in cursor:
      print("{}: {}".format(ticker, fullname))

    cursor.close()
    mysql_connection.close()