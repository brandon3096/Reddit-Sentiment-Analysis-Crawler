import mysql_dbconfig
import table_schemas
import mysql.connector
import random
from datetime import date, datetime

class queryhandler:
    def __init__(self, queue_size=50):
        db = mysql_dbconfig.read_db_config()
        self.mysql_connection = mysql.connector.connect(**db)
        self.insert_queue = []
        self.cursor = self.mysql_connection.cursor()
        self.queue_size = queue_size

    def add_to_queue(self, data):
        self.insert_queue.append(data)
        if len(self.insert_queue) == self.queue_size:
            self.process_queue()

    def process_queue(self):
        print("Insert batch")
        schema = table_schemas.tables.schemas["comment_sentiments"] # hardcoded for now, will add support for more queues later
        insert_query = "INSERT INTO comment_sentiments " + schema[0] + " VALUES " + schema[1] + ";"
        self.cursor.executemany(insert_query, self.insert_queue)
        self.mysql_connection.commit()
        self.insert_queue = []

    def get_valid_stocks(self):
        select_query = "SELECT * FROM stocks_list;"
        self.cursor.execute(select_query)
        stock_dictionary = {}
        for (ticker, fullname) in self.cursor:
            stock_dictionary[ticker] = fullname
        return stock_dictionary

    def set_word_sentiments(self, word_sentiments):
        schema = table_schemas.tables.schemas["word_sentiments"]
        insert_query = "INSERT INTO word_sentiments " + schema[0] + " VALUES " + schema[1] + ";"
        self.cursor.executemany(insert_query, word_sentiments)
        self.mysql_connection.commit()

    def get_word_sentiments(self):
        select_query = "SELECT * FROM word_sentiments;"
        self.cursor.execute(select_query)
        word_dictionary = {}
        for (word, sentiment) in self.cursor:
            word_dictionary[word] = sentiment
        return word_dictionary

    def __del__(self):
        if len(self.insert_queue) > 0:
            self.process_queue()
        self.cursor.close()
        self.mysql_connection.close()