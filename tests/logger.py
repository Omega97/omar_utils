import logging


def level_to_int(level) -> int:
    if type(level) == str:
        return Logger.numbers[level]
    return level


class Logger:
    levels = [logging.NOTSET, logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
    logs = [None, logging.debug, logging.info, logging.warning, logging.error, logging.critical]
    numbers = {'nonset': 0, 'debug': 1, 'info': 2, 'warning': 3, 'error': 4, 'critical': 5}

    def __init__(self, path='report.log', level=None, log_format=None, filemode='w'):
        """
        :param path: path of the log
        :param level: logging level: 0 = NOTSET, 1 = DEBUG, 2 = INFO, 3 = WARNING, 4 = ERROR, 5 = CRITICAL
        :param log_format: log format
        :param filemode: default 'w' overwrite log file
        """
        self.logger = None
        self.path = path
        self.level = level
        self.format = log_format
        self.filemode = filemode
        self._setup()

    def _setup(self):
        """clean parameters, create and config a logger"""
        if not self.format:
            self.format = '%(levelname)s %(asctime)s - %(message)s'
        self.level = level_to_int(self.level)
        logging.basicConfig(filename=self.path,
                            level=Logger.levels[self.level],
                            format=self.format,
                            filemode=self.filemode)
        self.logger = logging.getLogger()  # root logger (no name)

    def __call__(self, message, level=None):
        """create log message"""
        level = level_to_int(level)
        if level:
            Logger.logs[level](message)


if __name__ == '__main__':

    logger = Logger(level=1)

    logger('1 debug', 'debug')
    logger('2 info', 'info')
    logger('3 worn', 'warning')
    logger('4 err', 'error')
    logger('5 crit', 'critical')
    logger('1 debug', 1)
    logger('2 info', 2)
    logger('3 worn', 3)
    logger('4 err', 4)
    logger('5 crit', 5)
