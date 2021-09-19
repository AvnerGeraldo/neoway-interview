from controllers import process_file, save_file
from helpers.logger import Logger
from database.types import StatusEnum
from database.models import SaleFile
from helpers.db import saveModel, updateModel, getNextId

class FileTask():
    def __init__(self):
        self.saleId = None

    def createSaleFile(self):
        self.saleId = getNextId(SaleFile)
        saveModel(SaleFile())

    def handle(self, rawData: list):
        loggerInstance = Logger(self.saleId)
        loggerInstance.log('Processando dados')

        processFileInstance = process_file.ProcessFile(loggerInstance)
        saveFileInstance = save_file.SaveFile(loggerInstance)

        try:
            for index, rowData in enumerate(rawData):
                if index == 0:
                    continue
            
                formattedData = processFileInstance.processRawData(rowData)

                if processFileInstance.isValidData(formattedData) is False:
                    continue
                
                saveFileInstance.addCustomerToDb(formattedData['customer_id_cpf'])

                if formattedData['most_visited_store_cnpj'] == formattedData['last_purchase_store_cnpj']:
                    saveFileInstance.addStoreToDb(formattedData['most_visited_store_cnpj'])
                else:
                    saveFileInstance.addStoreToDb(formattedData['most_visited_store_cnpj'])
                    saveFileInstance.addStoreToDb(formattedData['last_purchase_store_cnpj'])

                saveFileInstance.addSaleToDb({
                    'private': formattedData['private'],
                    'unfinished': formattedData['unfinished'],
                    'last_purchase': formattedData['last_purchase_date'],
                    'average_ticket_price': formattedData['average_ticket_price'],
                    'ticket_price_last_purchase': formattedData['ticket_price_last_purchase'],
                    'customer_id': formattedData['customer_id_cpf'],
                    'most_visited_store': formattedData['most_visited_store_cnpj'],
                    'last_purchase_store': formattedData['last_purchase_store_cnpj']
                })

            saveFileInstance.save()
            self.setSaleFileStatus(StatusEnum.completed)
            loggerInstance.log('Processo encerrado com sucesso.')
        except Exception as error:
            loggerInstance.log(str(error))
            self.__setSaleFileStatus(StatusEnum.error)

    def setSaleFileStatus(self, status: StatusEnum, jobId: str=None):
        hasSaleFile = SaleFile.query.filter_by(id=self.saleId)

        if hasSaleFile:
            updatedData = { 'status': status }

            if jobId:
                updatedData.update({
                    'job_id': jobId
                })

            updateModel(hasSaleFile, updatedData)
        