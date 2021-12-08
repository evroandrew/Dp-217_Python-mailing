from loguru import logger

logger.add("error.log", format='{time} {level} {message}',
           level='DEBUG', rotation="1 week", compression="zip")
