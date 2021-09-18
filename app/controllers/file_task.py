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

                resCustomer = self.__prepareCustomerDataToDb(customers, customerDb, formattedData)

                if not resCustomer is None:
                    addCustomersToDb.append(resCustomer)
                    customers.append(formattedData['customer_id_cpf'])
                
        except Exception as error:
            loggerInstance.log(str(error))
            self.__setSaleFileStatus(nextSaleFileId, StatusEnum.error)

    def __setSaleFileStatus(self, saleFileId: int, status: StatusEnum):
        hasSaleFile = SaleFile.query.filter_by(id=saleFileId)

        if hasSaleFile:
            SaleFile.update(hasSaleFile, { 'status': status })

    def __prepareCustomerDataToDb(self, customerList: list, customerDb: list, data: dict):
        cpf = data['customer_id_cpf']

        if not cpf in customerList:
            try:
                if not cpf is None:
                    hasCustomer = customerDb.filter_by(cpf=cpf).first()

                    if not hasCustomer:
                        return Customer(cpf=cpf)

                return None
            except Exception as error:
                raise Exception("Error trying to add customer with CPF %s on database. %s" % (cpf, str(error)))