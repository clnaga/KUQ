import logging

# logger
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
handler = logging.FileHandler("log1.txt", encoding='utf-8')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger_suggestions = logging.getLogger("suggestions")
logger_suggestions.setLevel(level=logging.DEBUG)
handler = logging.FileHandler("suggestions.txt", encoding='utf-8')
logger_suggestions.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger_suggestions.addHandler(handler)


def get_logger():
    return logger


def get_logger_suggestions():
    return logger_suggestions
