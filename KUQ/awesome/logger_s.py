import logging
import logging.handlers

logging.basicConfig()

# logger
logger = logging.getLogger("dialog")
logger.setLevel(level=logging.DEBUG)
handler = logging.handlers.RotatingFileHandler("log/log.log", maxBytes=1024)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger_suggestions = logging.getLogger("suggestions")
logger_suggestions.setLevel(level=logging.DEBUG)
handler = logging.handlers.RotatingFileHandler("log/suggestions.log", maxBytes=1024)
logger_suggestions.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger_suggestions.addHandler(handler)


def get_logger():
    return logger


def get_logger_suggestions():
    return logger_suggestions
