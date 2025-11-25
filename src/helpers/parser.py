import json
import copy
from .constants import *
from typing import List, Dict, Tuple
from . import logging_config
import logging

logger = logging.getLogger(__name__)


class Parser:
    """
    Base parser class for converting JSON data to tuples

    Attributes:
        cols (list): list of column names to extract from JSON data
        entity_type (str): name for logging
    """

    cols = []
    entity_type = ""

    def parse(self, data: List[Dict]) -> List[Tuple]:
        """
        Parse JSON data into database-ready tuples

        Args:
            data (List[Dict]): list of JSON objects to parse

        Returns:
            List[Tuple]: list of tuples ready for database insertion
        """

        records = [tuple(item[col] for col in self.cols) for item in data]
        self.log()
        return records

    def log(self):
        """Log successful parsing of entities."""

        logger.info(f"{self.entity_type} were successfully parsed.")


class LocationsParse(Parser):
    """
    Parser for locations data.
    """

    cols = [LOCATION_ID, PARENT_LOCATION_ID, LOCATION_NAME]
    entity_type = "Locations"


class DevicesParse(Parser):
    """
    Parser for devices data.
    """

    cols = [DEVICE_ID, DEVICE_TYPE, DEVICE_NAME, LOCATION_ID]
    entity_type = "Devices"


class EventsParse(Parser):
    """
    Parser for events data.
    """

    entity_type = "Events"

    def parse(self, data: List[Dict]) -> List[Tuple]:
        """
        Parse events data

        Args:
            data(List[Dict]): list of event objects with details field

        Returnes:
            records(List[Tuple]): list of tuples with parsed data
        """

        records = []
        for item in data:
            details_copy = copy.deepcopy(item[DETAILS])

            if DEVICE_ID in details_copy:
                del details_copy[DEVICE_ID]
            if TIMESTAMP in details_copy:
                del details_copy[TIMESTAMP]

            record = (
                item[EVENT_ID],
                item[DETAILS][DEVICE_ID],
                item[DETAILS][TIMESTAMP],
                json.dumps(details_copy),
            )
            records.append(record)
        self.log()
        return records
