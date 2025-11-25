import argparse
from . import logging_config, constants
import logging

logger = logging.getLogger(__name__)


def arg_parse() -> argparse.Namespace:
    """
    Parse command line arguments

    Returns:
        object with parsed command line arguments with attributes:
        locations, devices, events, format
    """
    parser = argparse.ArgumentParser()

    group = parser.add_argument_group("required")
    group.add_argument(
        "--locations", type=str, required=True, help="Path to locations JSON file"
    )
    group.add_argument(
        "--devices", type=str, required=True, help="Path to devices JSON file"
    )
    group.add_argument(
        "--events", type=str, required=True, help="Path to events JSON file"
    )
    group.add_argument(
        "--format",
        type=str,
        required=True,
        choices=constants.FORMATS.keys(),
        help="The output format for query results (json or xml)",
    )

    logger.info("Arguments are received")

    return parser.parse_args()
