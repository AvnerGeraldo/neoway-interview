from controllers.process_file import ProcessFile
from helpers.logger import Logger
from database.models import SaleFile, Customer, Store
from database.types import StatusEnum


class FileTask():
    def handle(self, rawData: list):
        nextSaleFileId = SaleFile.getNextId()
        loggerInstance = Logger(nextSaleFileId)
        loggerInstance.log('Processando dados')

        processFileInstance = ProcessFile(loggerInstance)
        customers = []
        addCustomersToDb = []
        customerDb = Customer.query.all()

        try:
            for index, rowData in enumerate(rawData):
                if index == 0:
                    continue
            
                formattedData = processFileInstance.processRawData(rowData)

                if processFileInstance.isValidData(formattedData) is False:
                    continue
                
        except Exception as error:
            loggerInstance.log(str(error))
            self.__setSaleFileStatus(nextSaleFileId, StatusEnum.error)

    def __setSaleFileStatus(self, saleFileId: int, status: StatusEnum):
        hasSaleFile = SaleFile.query.filter_by(id=saleFileId)

        if hasSaleFile:
            SaleFile.update(hasSaleFile, { 'status': status })