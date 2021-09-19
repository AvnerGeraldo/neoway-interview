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
        stores = []
        addCustomersToDb = []
        addStoreToDb = []
        customerDb = Customer.query.all()
        storeDb = Store.query.all()

        try:
            for index, rowData in enumerate(rawData):
                if index == 0:
                    continue
            
                formattedData = processFileInstance.processRawData(rowData)

                if processFileInstance.isValidData(formattedData) is False:
                    continue

                resCustomer = self.__prepareCustomerDataToDb(customers, customerDb, formattedData['customer_id_cpf'])

                if not resCustomer is None:
                    addCustomersToDb.append(resCustomer)
                    customers.append(formattedData['customer_id_cpf'])

                for storeCnpj in [formattedData['most_visited_store_cnpj'], formattedData['last_purchase_store_cnpj']]:
                    resStore = self.__prepareStoreDataToDb(stores, storeDb, storeCnpj)

                    if not resStore is None:
                        addStoreToDb.append(resStore)
                        stores.append(storeCnpj)

        except Exception as error:
            loggerInstance.log(str(error))
            self.__setSaleFileStatus(nextSaleFileId, StatusEnum.error)

    def __setSaleFileStatus(self, saleFileId: int, status: StatusEnum):
        hasSaleFile = SaleFile.query.filter_by(id=saleFileId)

        if hasSaleFile:
            SaleFile.update(hasSaleFile, { 'status': status })

    def __prepareCustomerDataToDb(self, customerList: list, customerDb: list, cpf: str):
        if not cpf in customerList:
            try:
                if not cpf is None:
                    hasCustomer = customerDb.filter_by(cpf=cpf).first()

                    if not hasCustomer:
                        return Customer(cpf=cpf)

                return None
            except Exception as error:
                raise Exception("Erro: Não foi possível adicionar cliente com o CPF %s na base de dados. %s" % (cpf, str(error)))

    def __prepareStoreDataToDb(self, storeList: list, storeDb: list, cnpj: str):
        if not cnpj in storeList:
            try:
                if not cnpj is None:
                    hasStore = storeDb.filter_by(cnpj=cnpj).first()

                    if not hasStore:
                        return Store(cnpj=cnpj)

                return None
            except Exception as error:
                raise Exception("Erro: Não foi possível adicionar loja com o CNPJ %s na base de dados" % (cnpj, str(error)))

    