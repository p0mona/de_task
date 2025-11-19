from helpers import DBManager
from . import logging_config
import logging

logger = logging.getLogger(__name__)

db = DBManager()

class Executor():
    def __init__(self, db):
        self.db = db

    def run(self):
        all_results = {}

        try:
            result_1 = self.db.execute_query(
                '''SELECT a.location_name
                FROM locations a
                LEFT JOIN locations b ON a.location_id=b.parent_location_id
                WHERE b.location_id IS NULL
                GROUP BY a.location_id;'''
            )
            all_results['query 1'] = {
                'name': 'query 1',
                'task': 'Select all location_names that don’t have any sublocations. (self join).',
                'results': result_1
            }
            logger.info(f'Query 1 executed, {len(result_1)} results returned')

            result_2 = self.db.execute_query(
                '''SELECT root.location_name, 
                COALESCE(lev3.location_name, lev2.location_name, root.location_name )
                FROM locations root
                LEFT JOIN locations lev2 ON lev2.parent_location_id=root.location_id
                LEFT JOIN locations lev3 ON lev3.parent_location_id=lev2.location_id 
                GROUP BY root.location_name, lev2.location_name, lev3.location_name ,root.location_id 
                ORDER BY root.location_id;'''
            )
            all_results['query 2'] = {
                'name': 'query 2',
                'task': 'List all location_names and its lowest sublocation.',
                'results': result_2
            }
            logger.info(f'Query 2 executed, {len(result_2)} results returned')

            result_3 = self.db.execute_query(
                '''SELECT e.event_id
                FROM events e
                JOIN devices d ON d.device_id = e.device_id 
                WHERE d.device_type='Smart Lamp' 
                AND (e.details ->> 'new_status') = 'on'
                AND (e.details ->> 'brightness')::int > 80;'''
            )
            all_results['query 3'] = {
                'name': 'query 3',
                'task': "Find all event_id’s for 'Smart Lamp' devices where the new_status was 'on' and the brightness was greater than 80.",
                'results': result_3
            }
            logger.info(f'Query 3 executed, {len(result_3)} results returned')

            result_4 = self.db.execute_query(
                '''SELECT avg((e.details ->> 'brightness')::int) AS brightness, l.location_name 
                FROM events e
                JOIN devices d ON d.device_id = e.device_id
                JOIN locations l ON d.location_id = l.location_id 
                WHERE d.device_type = 'Smart Lamp'
                AND e.details ->> 'new_status' = 'on'
                GROUP BY l.location_name;'''
            )
            all_results['query 4'] = {
                'name': 'query 4',
                'task': "Calculate the average brightness for all 'Smart Lamp' 'on' events, grouped by location_name.",
                'results': result_4
            }
            logger.info(f'Query 4 executed, {len(result_4)} results returned')

            result_5 = self.db.execute_query(
                '''SELECT l.location_name
                FROM locations l
                JOIN devices d ON d.location_id = l.location_id 
                JOIN events e ON d.device_id = e.device_id
                WHERE e.details -> 'leak_detected' = 'true';'''
            )
            all_results['query 5'] = {
                'name': 'query 5',
                'task': "List location_names that have any device that detected a leak.",
                'results': result_5
            }
            logger.info(f'Query 5 executed, {len(result_5)} results returned')

            result_6 = self.db.execute_query(
                '''SELECT l.location_name, d.device_name
                FROM locations l
                JOIN devices d ON d.location_id = l.location_id 
                LEFT JOIN events e ON d.device_id = e.device_id
                WHERE e.event_id IS NULL;'''
            )
            all_results['query 6'] = {
                'name': 'query 6',
                'task': "Select all location_names and its device_names that don’t have any events.",
                'results': result_6
            }
            logger.info(f'Query 6 executed, {len(result_6)} results returned')
            
            result_7 = self.db.execute_query(
                '''SELECT l.location_name
                FROM locations l
                JOIN devices d ON d.location_id = l.location_id
                WHERE d.device_type = 'Smart Lamp'
                GROUP BY l.location_name 
                ORDER BY count(d.device_type ) DESC
                LIMIT 3;'''
            )
            all_results['query 7'] = {
                'name': 'query 7',
                'task': "Find 3 location_names with the highest amount of 'Smart Lamp' devices, and its amount.",
                'results': result_7
            }
            logger.info(f'Query 7 executed, {len(result_7)} results returned')

            result_8 = self.db.execute_query(
                '''SELECT l.location_name, avg((e.details ->> 'temperature')::float) AS average
                FROM locations l
                JOIN devices d ON d.location_id = l.location_id 
                JOIN events e ON d.device_id = e.device_id
                WHERE e.details ->> 'alert' = 'high_temp'
                GROUP BY l.location_name;'''
            )
            all_results['query 8'] = {
                'name': 'query 8',
                'task': "Calculate the average temperature for each location where alert = 'high_temp'.",
                'results': result_8
            }
            logger.info(f'Query 8 executed, {len(result_8)} results returned')

            result_9 = self.db.execute_query(
                '''SELECT l.location_name, d.device_type,  sum((e.details -> 'person_count')::int)
                FROM locations l
                JOIN devices d ON d.location_id = l.location_id 
                JOIN events e ON d.device_id = e.device_id
                WHERE e.details ->> 'person_count' IS NOT NULL
                GROUP BY l.location_name, d.device_type
                ORDER BY sum((e.details -> 'person_count')::int)
                OFFSET 4;'''
            )
            all_results['query 9'] = {
                'name': 'query 9',
                'task': "Retrieve the total number of people (person_count) for each location and device type, excluding entries with zero values.",
                'results': result_9
            }
            logger.info(f'Query 9 executed, {len(result_9)} results returned')

            result_10 = self.db.execute_query(
                '''SELECT tab1.device_id
                FROM (
                    SELECT 
                    ROW_NUMBER() OVER (
                        PARTITION BY device_id
                        ORDER BY 'timestamp'
                    ) AS rn,
                    device_id, details ->> 'new_status' AS status
                    FROM events
                    WHERE details ->> 'new_status' IS NOT NULL
                ) AS tab1
                WHERE tab1.rn=1 AND tab1.status = 'off' '''
            )
            all_results['query 10'] = {
                'name': 'query 10',
                'task': "Retrieve the device_id of devices for which the very first recorded event (by timestamp) had a status of 'off'.",
                'results': result_10
            }
            logger.info(f'Query 10 executed, {len(result_10)} results returned')
        
        except Exception as e:
            logger.error(f'Executing queries ERROR: {e}')
            raise

        return all_results