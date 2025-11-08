import psycopg2
import logging
import os

if not os.path.exists("logs"):
  os.mkdir("logs")

logging.basicConfig(
  level=logging.INFO, 
  filename='logs/load_data.log', 
  format="%(asctime)s -  %(levelname)s - %(message)s"
)

try:
  connection = psycopg2.connect(
    dbname='postgres', 
    user='postgres', 
    password='postgres',
    host='localhost',
    port=5430
  )
  logging.info("Connected!")
except:
  logging.error("Connection ERROR!")