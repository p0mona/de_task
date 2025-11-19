import argparse
from . import logging_config
import logging

logger = logging.getLogger(__name__)

def arg_parse():
    parser = argparse.ArgumentParser()

    group = parser.add_argument_group('required')
    group.add_argument(
        '--locations',
        type=str,
        required=True,
        help='Path to locations JSON file'
    )
    group.add_argument(
        '--devices',
        type=str,
        required=True,
        help='Path to devices JSON file'
    )
    group.add_argument(
        '--events',
        type=str,
        required=True,
        help='Path to events JSON file'
    )
    group.add_argument(
        '--format',
        type=str,
        required=True,
        choices=['json', 'xml'],
        help='The output format for query results (json or xml)'
    )

    logger.info('Arguments are received')
    
    return parser.parse_args()