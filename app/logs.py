"""log config"""

import logging
import os
from logging.handlers import TimedRotatingFileHandler


def configure_logging(app):
    """log config"""

    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = TimedRotatingFileHandler(
        "logs/application.log", when="D", interval=1, backupCount=30
    )
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    )
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.DEBUG)
    app.logger.info("Application startup")
