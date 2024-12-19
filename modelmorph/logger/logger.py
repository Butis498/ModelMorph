import logging
import os


class Logger:
    def __init__(self, log_file: str,verbose=False):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.verbose = verbose
        try:
            handler = logging.FileHandler(log_file)
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        except Exception as e:
            print(f"Error initializing logger: {e}")

    def log(self, message: str, level: str = 'info'):
        if level == 'debug':
            self.logger.debug(message)
        elif level == 'info':
            self.logger.info(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        elif level == 'critical':
            self.logger.critical(message)
        else:
            self.logger.info(message)

        if self.verbose:
            print(f"{level.upper()}: {message}")

    def log_exception(self, message: str):
        self.logger.exception(message)