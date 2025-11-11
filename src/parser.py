import json
import copy
from constants import *
from typing import List, Dict, Tuple
import logging_config
import logging

logger = logging.getLogger(__name__)

class Parser:
    def parse(self, data: List[Dict]) -> List[Tuple]:
        pass
    def log(self, name: str):
        logger.info(f"{name} were successfully parsed.")

class LocationsParse(Parser):
    def parse(self, data: List[Dict]) -> List[Tuple]:
        records = [(item[LOCATION_ID], item[PARENT_LOCATION_ID], item[LOCATION_NAME]) for item in data]
        self.log("Locations")
        return records
  
class DevicesParse(Parser):
    def parse(self, data: List[Dict]) -> List[Tuple]:
        records = [(item[DEVICE_ID], item[DEVICE_TYPE], item[DEVICE_NAME], item[LOCATION_ID]) for item in data]
        self.log("Devices")
        return records
  
class EventsParse(Parser):
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
        self.log("Events")
        return records
