import logging
import os

if not os.path.exists("logs"):
    os.mkdir("logs")

logging.basicConfig(
    level=logging.INFO, 
    filename='logs/app.log', 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)