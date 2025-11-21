import json
import xml.etree.ElementTree as et
import xml.dom.minidom
from . import logging_config, constants
import logging
import os

logger = logging.getLogger(__name__)

class Exporter():
    '''
    This class exports results of SQL queries depending on the selected format (json or xml)

    Attributes:
        results(dict): query results from Executor.run()
        output_file(str): base filename for output
    '''

    def __init__(self, results: dict, output_file: str):
        self.results = results
        self.output_file = output_file
        
    def export(self, format: str):
        '''
        This function provides the general logic for export 
        (checking for the presence of a file with the same name, overwriting if found)
        and calling the function to export the file in the previously selected format

        Args:
            format(str): output format (json or xml)
        '''
        
        try:
            path = f"{self.output_file}.{format}"
            
            if os.path.exists(path):
                logger.warning(f"File {path} already exists. It will be overwritten.")

            method_name = constants.FORMATS.get(format)
            export_method = getattr(self, method_name)
            export_method()
            
            logger.info('Export completed successfully')
        except Exception as e:
            logger.error(f'Export ERROR: {e}')
            raise

    def export_json(self):
        '''
        This function serializes the data received after executing the SQL query 
        and writes it to the corresponding JSON file.
        '''
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
        '''
        Builds XML structure from query results, adds proper indentation
        for readability, and saves to file with XML declaration.
        '''
        
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
