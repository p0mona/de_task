import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def db_connection():
    try:
        connection = psycopg2.connect(
            dbname = os.getenv('PGDBNAME'),
            user = os.getenv('PGUSER'),
            password = os.getenv('PGPASS'),
            host = os.getenv('PGHOST'),
            port = os.getenv('PGPORT')
        )
        return connection
    except:
        return None