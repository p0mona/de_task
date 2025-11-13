import logging_config
import logging
import psycopg2
import os
from parser import *
from dotenv import load_dotenv
from open_json import open_json

logger = logging.getLogger(__name__)
load_dotenv()

class DBManager():
    def __init__(self):
        self.conn = None
        self.cursor = None

    def conn_db(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv('PGDBNAME'),
            user=os.getenv('PGUSER'),
            password=os.getenv('PGPASS'),
            host=os.getenv('PGHOST'),
            port=os.getenv('PGPORT')
        )
        self.cursor = self.conn.cursor()

    def insert_data(self, table_name, data):
        value_list = ', '.join(['%s' for _ in range(len(data[0]))])
        sql = f'INSERT INTO {table_name} VALUES ({value_list});'

        try:
            self.cursor.executemany(sql, data)
            logger.info(f"{table_name} data was successfully added")
        except:
            logger.error(f"ERROR during loading data to {table_name}.")
    
    def load_data(self, path, parser, table_name):
        data = open_json(path)
        parsed_data = parser().parse(data)
        self.insert_data(table_name, parsed_data)