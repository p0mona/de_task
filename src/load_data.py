import logging
import json
import os
from conn_db import db_connection
import parser

if not os.path.exists("logs"):
    os.mkdir("logs")

logging.basicConfig(
    level=logging.INFO, 
    filename='logs/load_data.log', 
    format="%(asctime)s -  %(levelname)s - %(message)s"
)

with open('data/locations', 'r', encoding='utf-8') as locations:
    locations = json.load(locations)

with open('data/devices', 'r', encoding='utf-8') as devices:
    devices = json.load(devices)
    
with open('data/events', 'r', encoding='utf-8') as events:
    events = json.load(events)

def load_data():
    connection = db_connection()
    if not connection:
        logging.error('Connection Error!')

    cursor = connection.cursor()
    try:
        cursor.executemany(
        "INSERT INTO locations VALUES (%s, %s, %s);",parser.locations_parser(locations)
        )
        logging.info("Locations data was successfully added")

        cursor.executemany(
        "INSERT INTO devices VALUES (%s, %s, %s, %s);",parser.devices_parser(devices)
        )
        logging.info("Devices data was successfully added")

        cursor.executemany(
        "INSERT INTO events VALUES (%s, %s, %s, %s);",parser.events_parser(events)
        )
        logging.info("Events data was successfully added")
        connection.commit()
    except:
        logging.error("ERROR during loading data to db")
    finally:
        connection.close()
    return

load_data()