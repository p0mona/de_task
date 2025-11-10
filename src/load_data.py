import json
from conn_db import db_connection
import parser
import logging_config
import logging

logger = logging.getLogger(__name__)

with open('data/locations.json', 'r', encoding='utf-8') as locations:
    locations = json.load(locations)

with open('data/devices.json', 'r', encoding='utf-8') as devices:
    devices = json.load(devices)
    
with open('data/events.json', 'r', encoding='utf-8') as events:
    events = json.load(events)

def load_data():
    connection = db_connection()
    if not connection:
        logger.error('Connection Error!')

    cursor = connection.cursor()
    try:
        cursor.executemany(
        "INSERT INTO locations VALUES (%s, %s, %s);",parser.locations_parser(locations)
        )
        logger.info("Locations data was successfully added")

        cursor.executemany(
        "INSERT INTO devices VALUES (%s, %s, %s, %s);",parser.devices_parser(devices)
        )
        logger.info("Devices data was successfully added")

        cursor.executemany(
        "INSERT INTO events VALUES (%s, %s, %s, %s);",parser.events_parser(events)
        )
        logger.info("Events data was successfully added")
        connection.commit()
    except:
        logger.error("ERROR during loading data to db")
    finally:
        connection.close()
    return

load_data()