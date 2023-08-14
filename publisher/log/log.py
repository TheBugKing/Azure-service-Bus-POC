import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)
