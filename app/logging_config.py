import logging
from logging.config import dictConfig
import json
from datetime import datetime

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "line": record.lineno,
            "message": record.getMessage()
        }
        
        # Include any extra attributes passed to the logger
        for key, value in record.__dict__.items():
            if key not in ["args", "exc_info", "exc_text", "levelname", "lineno", 
                          "module", "msecs", "msg", "name", "pathname", 
                          "process", "processName", "relativeCreated", 
                          "thread", "threadName", "asctime"]:
                log_record[key] = value
                
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_record)

# Фильтр для исключения логирования запросов к endpoint /metrics
class MetricsFilter(logging.Filter):
    def filter(self, record):
        # Проверяем, что сообщение от логгера uvicorn.access и не содержит /metrics
        if record.name == "uvicorn.access" and "/metrics" in str(record.getMessage()):
            return False
        return True

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "json": {
            "()": JsonFormatter
        }
    },
    "filters": {
        "metrics": {
            "()": MetricsFilter
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "filters": ["metrics"],
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filters": ["metrics"],
            "filename": "app.log",
            "maxBytes": 10 * 1024 * 1024,  # 10MB
            "backupCount": 5
        }
    },
    "loggers": {
        "uvicorn.error": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        },
        "uvicorn.access": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        },
        # Настройка уровня логирования для PyMongo
        "pymongo": {
            "handlers": ["console", "file"],
            "level": "WARNING",  # Изменяем уровень с DEBUG на WARNING
            "propagate": False
        },
        # Логгеры для различных компонентов PyMongo
        "pymongo.connection": {
            "level": "WARNING",
            "propagate": True
        },
        "pymongo.topology": {
            "level": "WARNING",
            "propagate": True
        },
        "pymongo.serverSelection": {
            "level": "WARNING",
            "propagate": True
        },
        "": {
            "handlers": ["console", "file"],
            "level": "INFO"
        }
    }
}

def setup_logging():
    dictConfig(LOGGING_CONFIG)