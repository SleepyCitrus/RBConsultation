import logging


def logger(cls):
    """
    Injects a logger instance into the decorated class.
    """
    # Use the class's module and name to create a scoped logger name
    logger_name = f"{cls.__module__}.{cls.__name__}"
    cls.logger = logging.getLogger(logger_name)
    cls.logger.setLevel(logging.INFO)
    return cls
