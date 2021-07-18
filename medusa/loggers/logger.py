from medusa.loggers.time_logger import TimeLogger
from medusa.loggers.warning_logger import WarningLogger


class Logger:
    def __init__(self):
        self.time_logger = TimeLogger()
        self.warn_logger = WarningLogger()

    def log_time(self, name=None):
        self.time_logger.log_time(name)

    def warn(self, msg):
        self.warn_logger.warn(msg)
