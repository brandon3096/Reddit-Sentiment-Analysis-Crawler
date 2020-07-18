import mysql_dbconfig
import table_schemas
import mysql.connector
import random
from datetime import date, datetime

class queryhandler:
    def __init__(self, queue_size):
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

    def __del__(self):
        self.process_queue()
        self.cursor.close()
        self.mysql_connection.close()