import logging
import os
from logging.handlers import TimedRotatingFileHandler

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")

LOG_FILE_PATH = os.path.join(LOG_DIR, "app_activity.log")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s -  [%(filename)s:%(lineno)d] - %(message)s",
    handlers=[
        TimedRotatingFileHandler(LOG_FILE_PATH, when="midnight", backupCount=30),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger()
