import praw
import os
import mysql_dbconfig
import mysql_queryhandler
import mysql.connector
import random
import decimal
from datetime import date, datetime

#TODO seperate queue handler
#TODO refactor main crawler

class crawler:
    def __init__(self, handler):
        self.handler = handler
        # Get tracked stocks
        self.stocks = self.handler.get_valid_stocks()
        # Get word sentiments
        self.word_sentiments = self.handler.get_word_sentiments()
    
    def parse_comment(self, comment):
        store_comment = False
        stock = ''
        comment_score = decimal.Decimal(0.0)
        for x in comment.body.split(' '):   
            word_score = decimal.Decimal(1.0)
            if x in self.word_sentiments:
                word_score = self.word_sentiments[x]
            if x in self.stocks:           
                stock = x
                store_comment = True
                print("Found mention of {} in {}".format(x, comment.body))
            comment_score += word_score
        if store_comment:
            insert_comment = (stock, "Reddit", comment_score/len(comment.body.split(' ')), datetime.now())
            self.handler.add_to_queue(insert_comment)

if __name__ == "__main__":    
    # Initialize
    reddit = praw.Reddit('RedditSentimentAnalysisBot')
    #postIds = {}
    #comments = []
    handler = mysql_queryhandler.queryhandler(50)
    reddit_crawler = crawler(handler)

    # Process comment stream
    try:
        for submission in reddit.subreddit('wallstreetbets').stream.submissions():   
            #postIds[submission.id] = True
            submission.comments.replace_more(limit=None)
            comment_queue = submission.comments[:]  # Seed with top-level
            while comment_queue:
                comment = comment_queue.pop(0)    
                reddit_crawler.parse_comment(comment)
                #comments.append(comment)
                comment_queue.extend(comment.replies)
    except KeyboardInterrupt:
        del handler

    