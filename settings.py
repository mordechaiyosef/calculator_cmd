import logging

# Set the logging level to DEBUG
LEVEL = logging.DEBUG
# log to the console and file
logging.basicConfig(
    level=LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="calculator.log",
)

logger = logging.getLogger(__name__)
