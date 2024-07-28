import logging


class Logger:
    """Logger object for logging to console and file"""
    def __init__(self, name: str, level: int = logging.DEBUG, filename: str = None) -> None:
        self.logger = logging.getLogger(name)
        self.logger.propagate = False
        self.logger.setLevel(level)

        formatter = logging.Formatter(
            fmt="%(asctime)s  [%(levelname)s]  %(module)s(%(lineno)d) %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        if filename:
            file_handler = logging.FileHandler(filename)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def _log(self, level: int, message: str) -> None:
        caller = self.logger.findCaller()
        filename = caller[0]
        line_number = caller[1]

        log_record = logging.LogRecord(
            filename, level, filename, line_number, message, None, None
        )

        self.logger.handle(log_record)

    def debug(self, message: str) -> None:
        self._log(logging.DEBUG, message)

    def info(self, message: str) -> None:
        self._log(logging.INFO, message)

    def warning(self, message: str) -> None:
        self._log(logging.WARNING, message)

    def error(self, message: str) -> None:
        self._log(logging.ERROR, message)

    def critical(self, message: str) -> None:
        self._log(logging.CRITICAL, message)
