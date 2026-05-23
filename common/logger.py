import logging


def 获取日志器() -> logging.Logger:
    logger = logging.getLogger("farm_move")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    return logger
