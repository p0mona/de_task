import json
import xml.etree.ElementTree as et
from . import logging_config
import logging

logger = logging.getLogger(__name__)

class Exporter():
    def __init__(self, results, output_file):
        self.results = results
        self.output_file = output_file
        
    def export(self, format):
        try:
            if format == 'json':
                self.export_json()
            elif format == 'xml':
                self.export_xml()
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            logger.info('Export completed successfully')
        except Exception as e:
            logger.error(f'Export ERROR: {e}')
            raise

    def export_json(self):
        try: 
            with open(f"{self.output_file}.json", 'w') as f:
                json.dump(self.results, f)
            logger.info("Export to JSON was completed successfully")
        except Exception as e:
            logger.error(f'ERROR creating JSON file: {e}')
            raise

    def export_xml(self):
        try:
            root = et.Element('results')

            for id, info in self.results.items():
                query_elem = et.SubElement(root, 'query')
                task_elem = et.SubElement(query_elem, "task")
                task_elem.text = info.get('task', '')
                results_elem = et.SubElement(query_elem, "results")

                for row in info.get('results', []):
                    row_elem = et.SubElement(results_elem, "row")

                    for key, value in row.items():
                        field_elem = et.SubElement(row_elem, key)
                        field_elem.text = str(value)        
        
            et.ElementTree(root).write(
                f"{self.output_file}.xml", 
                encoding='utf-8', 
                xml_declaration=True
            )
            logger.info("Export to XML was completed successfully")

        except Exception as e:
            logger.error(f'ERROR creating XML file: {e}')
            raise
