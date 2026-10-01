import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
