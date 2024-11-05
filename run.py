# run.py
import os
import sys
from dotenv import load_dotenv

# My Stuff
from don import create_app
from don.utils.logger import logger, configure_logger

# Configure the custom logger
configure_logger()
logger.info("Logger configured.")

# Load environment variables
logger.info("Loading environment variables...")
load_dotenv()

# Load host, port, and debug settings from environment variables
HOST = os.getenv("APP_HOST", "0.0.0.0")
PORT = int(os.getenv("APP_PORT", 5024))
DEBUG = os.getenv("APP_DEBUG", "false").lower() == "true"

app = create_app()

if __name__ == "__main__":
    logger.info("Starting Flask application...")
    try:
        app.run(host=HOST, port=PORT, debug=DEBUG)
    except Exception as e:
        logger.exception("Application failed to start.")
