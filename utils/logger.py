from loguru import logger
import sys


def get_logger():
    logger.remove()
    logger.add(
        sys.stdout,
        colorize=True,
        format="<level>{level}</level>:     <blue>{module}:{file}:{line}</blue> | <level>{message}</level>",
    )
    return logger
