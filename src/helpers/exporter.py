import json
import xml.etree.ElementTree as et
import xml.dom.minidom
from . import logging_config
import logging
import os

logger = logging.getLogger(__name__)

class Exporter():
    def __init__(self, results, output_file):
        self.results = results
        self.output_file = output_file
        
    def export(self, format):
        try:
            path = f"{self.output_file}.{format}"
            
            if os.path.exists(path):
                logger.warning(f"File {path} already exists. It will be overwritten.")

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
            results_str = json.dumps(self.results, default=str)
            results_dict = json.loads(results_str)

            with open(f"{self.output_file}.json", 'w') as f:
                json.dump(results_dict, f, ensure_ascii=False, indent=4)
            logger.info("Export to JSON was completed successfully")
        except Exception as e:
            logger.error(f'ERROR creating JSON file: {e}')
            raise

    def export_xml(self):
        try:
            root = et.Element('results')

            for id, info in self.results.items():
                query_elem = et.SubElement(root, 'query')
                query_elem.set('name', id)
                task_elem = et.SubElement(query_elem, "task")
                task_elem.text = info.get('task', '')
                results_elem = et.SubElement(query_elem, "results")

                for row in info.get('results', []):
                    row_elem = et.SubElement(results_elem, "row")

                    for key, value in row.items():
                        field_elem = et.SubElement(row_elem, key)
                        field_elem.text = str(value)      

            xml_string = et.tostring(root)
            reparsed = xml.dom.minidom.parseString(xml_string)
            pretty_xml = reparsed.toprettyxml(indent="  ")
            
            with open(f"{self.output_file}.xml", 'w') as f:
                f.write(pretty_xml)
            logger.info("Export to XML was completed successfully")

        except Exception as e:
            logger.error(f'ERROR creating XML file: {e}')
            raise
