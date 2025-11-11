from conn_db import db_connection
from parser import *
import logging_config
import logging
from open_json import open_json

logger = logging.getLogger(__name__)

locations = open_json('data/locations.json')
devices = open_json('data/devices.json')
events = open_json('data/events.json')

def load_data():
    connection = db_connection()
    if not connection:
        logger.error('Connection Error!')

    cursor = connection.cursor()
    try:
        cursor.executemany(
        "INSERT INTO locations VALUES (%s, %s, %s);", LocationsParse().parse(locations)
        )
        logger.info("Locations data was successfully added")

        cursor.executemany(
        "INSERT INTO devices VALUES (%s, %s, %s, %s);", DevicesParse().parse(devices)
        )
        logger.info("Devices data was successfully added")

        cursor.executemany(
        "INSERT INTO events VALUES (%s, %s, %s, %s);", EventsParse().parse(events)
        )
        logger.info("Events data was successfully added")
        connection.commit()
    except:
        logger.error("ERROR during loading data to db")
    finally:
        connection.close()
    return

load_data()