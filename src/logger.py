import logging

logger = logging.getLogger("steam-to-calendar")
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter("%(asctime)s::%(levelname)s::%(message)s"))
logger.addHandler(stream_handler)
