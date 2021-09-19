from database.models import Customer, Store, Sale
from helpers.db import bulkModel, saveModel, updateModel

class SaveFile():
    def __init__(self, LoggerInstance):
        self.Logger = LoggerInstance
        self.customersCpf = []
        self.storesCnpj = []
        self.customersToDb = []
        self.storesToDb = []
        self.salesToDb = []

    def addCustomerToDb(self, cpf: str):
        resCustomer = self.__prepareCustomerDataToDb(cpf)

        if not resCustomer is None:
            self.customersToDb.append(resCustomer)
            self.customersCpf.append(cpf)

    def addStoreToDb(self, cnpj: str):
        resStore = self.__prepareStoreDataToDb(cnpj)

        if not resStore is None:
            self.storesToDb.append(resStore)
            self.storesCnpj.append(cnpj)

    def addSaleToDb(self, data:dict):
        self.salesToDb.append(data)

    def save(self):
        if len(self.customersToDb) > 0:
            self.Logger.log('Salvando clientes')
            bulkModel(self.customersToDb)

        if len(self.storesToDb) > 0:
            self.Logger.log('Salvando lojas')
            bulkModel(self.storesToDb)

        self.Logger.log('Salvando ticket médio')
        for saleData in self.salesToDb:
            self.__saveSale(saleData)

    def __prepareCustomerDataToDb(self, cpf: str):
        if not cpf in self.customersCpf:
            try:
                if not cpf is None:
                    hasCustomer = Customer.query.filter_by(cpf=cpf).first()

                    if not hasCustomer:
                        return Customer(cpf=cpf)

                return None
            except Exception as error:
                raise Exception("Erro: Não foi possível adicionar cliente com o CPF %s na base de dados. %s" % (cpf, str(error)))

    def __prepareStoreDataToDb(self, cnpj: str):
        if not cnpj in self.storesCnpj:
            try:
                if not cnpj is None:
                    hasStore = Store.query.filter_by(cnpj=cnpj).first()

                    if not hasStore:
                        return Store(cnpj=cnpj)

                return None
            except Exception as error:
                raise Exception("Erro: Não foi possível adicionar loja com o CNPJ %s na base de dados" % (cnpj, str(error)))

    def __saveSale(self, saleData):
        try:
            hasSale = Sale.query.filter_by(customer_id=saleData['customer_id'])
            sale = hasSale.first()

            if not sale:
                addSale = Sale(
                    customer_id=saleData['customer_id'],
                    private=saleData['private'],
                    unfinished=saleData['unfinished'],
                    last_purchase=saleData['last_purchase'],
                    average_ticket_price=saleData['average_ticket_price'],
                    ticket_price_last_purchase=saleData['ticket_price_last_purchase'],
                    most_visited_store=saleData['most_visited_store'],
                    last_purchase_store=saleData['last_purchase_store']
                )

                saveModel(addSale)
                return True
            
            if (sale.private != saleData['private'] or sale.unfinished != saleData['unfinished'] or 
            sale.last_purchase != saleData['last_purchase'] or sale.average_ticket_price != saleData['average_ticket_price'] or
            sale.ticket_price_last_purchase != saleData['ticket_price_last_purchase'] or sale.most_visited_store != saleData['most_visited_store'] or
            sale.last_purchase_store != saleData['last_purchase_store']):
            
                updateModel(hasSale, dict(
                    customer_id=saleData['customer_id'],
                    private=saleData['private'],
                    unfinished=saleData['unfinished'],
                    last_purchase=saleData['last_purchase'],
                    average_ticket_price=saleData['average_ticket_price'],
                    ticket_price_last_purchase=saleData['ticket_price_last_purchase'],
                    most_visited_store=saleData['most_visited_store'],
                    last_purchase_store=saleData['last_purchase_store']
                ))
               
        except Exception as error:
            raise Exception("Erro: Não foi possível adcionar ticket médio com o CPF %s na base de dados. %s" % (saleData['customer_id'], str(error)))