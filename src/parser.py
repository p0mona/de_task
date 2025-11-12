import json
import copy
from constants import *
from typing import List, Dict, Tuple
import logging_config
import logging

logger = logging.getLogger(__name__)

class Parser:
    cols = []
    entity_type = ''

    def parse(self, data: List[Dict]) -> List[Tuple]:
        records = [tuple(item[col] for col in self.cols) for item in data]
        self.log()
        return records
    def log(self):
        logger.info(f"{self.entity_type} were successfully parsed.")

class LocationsParse(Parser):
    cols = [LOCATION_ID, PARENT_LOCATION_ID, LOCATION_NAME]
    entity_type = "Locations"
  
class DevicesParse(Parser):
    cols = [DEVICE_ID, DEVICE_TYPE, DEVICE_NAME, LOCATION_ID]
    entity_type = "Devices"
  
class EventsParse(Parser):
    entity_type = "Events"
    def parse(self, data: List[Dict]) -> List[Tuple]:
        records = []
        for item in data:
            details_copy = copy.deepcopy(item[DETAILS])

            if DEVICE_ID in details_copy:
                del details_copy[DEVICE_ID]
            if TIMESTAMP in details_copy:
                del details_copy[TIMESTAMP]

            record = (item[EVENT_ID], item[DETAILS][DEVICE_ID], item[DETAILS][TIMESTAMP], json.dumps(details_copy))
            records.append(record)
        self.log()
        return records
