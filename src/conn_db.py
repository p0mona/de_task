import psycopg2

def db_connection():
    try:
        connection = psycopg2.connect(
            dbname='postgres', 
            user='postgres', 
            password='postgres',
            host='localhost',
            port=5430
        )
        return connection
    except:
        return None