import logging
import os
from logging import handlers

class Logger:
    def __init__(self, name, logLevel, filename=""):
        MAX_BYTES = 100000 # 100KByte
        BACKUP_COUNET = 10

        level = logging.DEBUG
        errorMessages = []
        
        levelList = {"DEBUG": logging.DEBUG, "INFO": logging.INFO, "WARN": logging.WARN, "ERROR": logging.ERROR, "CRITICAL": logging.CRITICAL}
        if logLevel in levelList:
            level = levelList[logLevel]
        else:
            errorMessages.append("Logger.__init__() {} is not in the list".format(logLevel))

        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(level)
        formatter = logging.Formatter("[%(asctime)s] [%(process)d] [%(name)s] [%(levelname)s] %(message)s")

        # 種順出力
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self.__logger.addHandler(handler)

        # ログファイル出力
        if(filename != ""):
            dirname = os.path.dirname(filename)
            os.makedirs(dirname, exist_ok=True)
            handler = handlers.RotatingFileHandler(filename, maxBytes = MAX_BYTES, backupCount = BACKUP_COUNET)
            handler.setLevel(level)
            handler.setFormatter(formatter)
            self.__logger.addHandler(handler)

        self.debug("Logger.__init__()")
        for errorMessage in errorMessages:
            self.error(errorMessage)
        self.info("Logger.__init__() initialeze log level: {}".format(level))

    def debug(self, msg):
        self.__logger.debug(msg)

    def info(self, msg):
        self.__logger.info(msg)

    def warn(self, msg):
        self.__logger.warning(msg)

    def error(self, msg):
        self.__logger.error(msg)

    def critical(self, msg):
        self.__logger.critical(msg)