from conn_db import db_connection
from parser import *
import logging_config
import logging
from open_json import open_json
from insert_data import insert_data

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
        insert_data(cursor, 'locations', LocationsParse().parse(locations))
        insert_data(cursor, 'devices', DevicesParse().parse(devices))
        insert_data(cursor, 'events', EventsParse().parse(events))
        connection.commit()
    finally:
        connection.close()
    return

load_data()