from loguru import logger


logger.remove(handler_id=None)
logger.add("log/file_{time}.log", backtrace=True, encoding="utf8")
