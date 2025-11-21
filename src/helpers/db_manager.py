from helpers.parser import Parser
from . import logging_config
import logging
import psycopg2
import os
from dotenv import load_dotenv
from .open_json import open_json

logger = logging.getLogger(__name__)
load_dotenv()

class DBManager():
    '''
    A class for working with a database: connecting to a database, inserting data, 
    uploading data, and executing queries.
    '''
    
    def __init__(self):
        self.conn = None
        self.cursor = None

    def conn_db(self):
        '''
        Connect with database using environment variables
        '''
        
        self.conn = psycopg2.connect(
            dbname=os.getenv('PGDBNAME'),
            user=os.getenv('PGUSER'),
            password=os.getenv('PGPASS'),
            host=os.getenv('PGHOST'),
            port=os.getenv('PGPORT')
        )
        self.cursor = self.conn.cursor()

    def insert_data(self, table_name: str, data: list):
        '''
        Insert records into specified database table

        Args:
            table_name(str): name of a target name
            data(list): list of tuples containing data records
        '''

        value_list = ', '.join(['%s' for _ in range(len(data[0]))])
        sql = f'INSERT INTO {table_name} VALUES ({value_list});'

        try:
            self.cursor.executemany(sql, data)
            logger.info(f"{table_name} data was successfully added")
        except:
            logger.error(f"ERROR during loading data to {table_name}.")
    
    def load_data(self, path: str, parser: type[Parser], table_name: str):
        '''
        Upload data into specified database table

        Args:
            path(str): path to the json file
            parser(class): selected parser for data parsing
            table_name(str): name of a target name
        '''
        
        data = open_json(path)
        parsed_data = parser().parse(data)
        self.insert_data(table_name, parsed_data)

    def execute_query(self, query: str) -> list:
        '''
        Execute SQL query and return results as list of dictionaries

        Args:
            query(str): SQL query string to execute

        Returns:
            data(list): list of dictionaries where keys are column names and values are row data
        '''

        self.cursor.execute(query)
        cols = [desc[0] for desc in self.cursor.description]
        rows = self.cursor.fetchall()
        data = [dict(zip(cols, row)) for row in rows]

        return data