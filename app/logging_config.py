import logging
from pythonjsonlogger import jsonlogger

def setup_logging():
    handler = logging.StreamHandler()
    fmt = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s"
    )
    handler.setFormatter(fmt)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers = [handler]