from helpers.logger import Logger

class ProcessFile():
    def __init__(self, LoggerInstance: Logger):
        self.Logger = LoggerInstance

    def processRawData(self, rawData: list):
        self.Logger.log('Processing data')