import logging_config
import logging
from parser import *

logger = logging.getLogger(__name__)

def insert_data(cursor, table_name, data):
    value_list = ', '.join(['%s' for _ in range(len(data[0]))])
    sql = f'INSERT INTO {table_name} VALUES ({value_list});'

    try:
        cursor.executemany(sql, data)
        logger.info(f"{table_name} data was successfully added")
    except:
        logger.error(f"ERROR during loading data to {table_name}.")
    return 