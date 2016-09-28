"""
Usage:

    from logger import setup_logger

    logger = setup_logger(logfile=LOGFILE)
    logger.info("message")
"""
import logging
from tornado.log import LogFormatter as TornadoLogFormatter
import config


# the formatter
# formatter = logging.Formatter('%(name)s - %(asctime)-15s - %(levelname)s: %(message)s');
formatter = TornadoLogFormatter()


def setup_logger(name=__name__, logfile=config.LOGFILE, level=logging.DEBUG):
    """
    A utility function that you can call to set up a simple logging to the
    console. No hassles.
    """
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(level)

    if logger.handlers:
        return logger

    # create console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)  # propagate all messages

    # add the formatter to the handler
    ch.setFormatter(formatter)

    # setup logger and add the handlers
    logger.addHandler(ch)

    if logfile:
        filehandler = logging.FileHandler(logfile)
        filehandler.setLevel(logging.NOTSET)
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)

    # logger.debug("logger set up. level=%d", level)
    return logger
