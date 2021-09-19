from controllers import process_file, save_file
from helpers.logger import Logger
from database.models import SaleFile, Customer, Store
from database.types import StatusEnum


class FileTask():
    def handle(self, rawData: list):
        nextSaleFileId = SaleFile.getNextId()
        loggerInstance = Logger(nextSaleFileId)
        loggerInstance.log('Processando dados')

        processFileInstance = process_file.ProcessFile(loggerInstance)
        saveFileInstance = save_file.SaveFile()
        saveFileInstance.initializingDbData()

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

            

        except Exception as error:
            loggerInstance.log(str(error))
            self.__setSaleFileStatus(nextSaleFileId, StatusEnum.error)

    def __setSaleFileStatus(self, saleFileId: int, status: StatusEnum):
        hasSaleFile = SaleFile.query.filter_by(id=saleFileId)

        if hasSaleFile:
            SaleFile.update(hasSaleFile, { 'status': status })