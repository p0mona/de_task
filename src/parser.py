from typing import List, Dict, Tuple
import copy
import logging
import json
import os

if not os.path.exists("logs"):
    os.mkdir("logs")

logging.basicConfig(
    level=logging.INFO, 
    filename='logs/parser.log', 
    format="%(asctime)s -  %(levelname)s - %(message)s"
)

def locations_parser(data: List[Dict]) -> List[Tuple]:
    records = []
    for item in data:
        record = (item["location_id"], item["parent_location_id"], item["location_name"])
        records.append(record)
    logging.info('Locations were successfully parsed.')
    return records

def devices_parser(data: List[Dict]) -> List[Tuple]:
    records = []
    for item in data:
        record = (item["device_id"], item["device_type"], item["device_name"], item["location_id"])
        records.append(record)
    logging.info('Devices were successfully parsed.')
    return records

def events_parser(data: List[Dict]) -> List[Tuple]:
    records = []
    for item in data:
        details_copy = copy.deepcopy(item['details'])

        if 'device_id' in details_copy:
            del details_copy["device_id"]
        if 'timestamp' in details_copy:
            del details_copy["timestamp"]

        record = (item["event_id"], item["details"]["device_id"], item["details"]["timestamp"], json.dumps(details_copy))
        records.append(record)
    logging.info('Events were successfully parsed.')
    return records