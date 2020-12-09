import logging
import sys

LOGGER = logging.getLogger("pyevo")

LOGGER.setLevel(logging.INFO)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stdout_handler.setFormatter(formatter)
LOGGER.addHandler(stdout_handler)
