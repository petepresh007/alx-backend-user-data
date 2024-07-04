#!/usr/bin/env python3
'''a module to filter'''
import logging
import re
from typing import List


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str,
        ) -> str:
    '''a function to carry out filtering'''
    return re.sub(
             f"({'|'.join(fields)})=[^{separator}]*",
             lambda m: f"{m.group(1)}={redaction}",
             message
            )


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        '''init method'''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''a function for logging records'''
        original_message = super(RedactingFormatter, self).format(record)
        return filter_datum(
                self.fields,
                self.REDACTION,
                original_message,
                self.SEPARATOR
                )


def get_logger() -> logging.Logger:
    """Creates and returns a logger with the specified configuration."""
    PII_FIELDS = ("name", "email", "phone", "ssn", "password")
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create a StreamHandler
    stream_handler = logging.StreamHandler()

    # Create and set the formatter
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(stream_handler)

    return logger
