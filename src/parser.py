from typing import List, Dict, Tuple
import copy
import logging
import json
import logging_config

logger = logging.getLogger(__name__)


def locations_parser(data: List[Dict]) -> List[Tuple]:
    records = []
    for item in data:
        record = (item["location_id"], item["parent_location_id"], item["location_name"])
        records.append(record)
    logger.info('Locations were successfully parsed.')
    return records

def devices_parser(data: List[Dict]) -> List[Tuple]:
    records = []
    for item in data:
        record = (item["device_id"], item["device_type"], item["device_name"], item["location_id"])
        records.append(record)
    logger.info('Devices were successfully parsed.')
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
    logger.info('Events were successfully parsed.')
    return records