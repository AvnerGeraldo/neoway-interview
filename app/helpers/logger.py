from helpers.db import saveModel
from database.models import Log

class Logger():
    def __init__(self, saleFileId: int):
        self.saleFileId = saleFileId

    def log(self, message):
        logInstance = Log(
            message=message,
            sale_file_id=self.saleFileId
        )
        
        saveModel(logInstance)