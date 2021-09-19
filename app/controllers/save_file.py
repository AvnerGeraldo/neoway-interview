from database.models import Customer, Store

class SaveFile():
    def __init__(self):
        self.customersCpf = []
        self.storesCnpj = []
        self.customersToDb = []
        self.storesToDb = []
        self.salesToDb = []
        self.customerDbData = None
        self.storeDbData = None

    def initializingDbData(self):
        self.customerDbData = Customer.query.all()
        self.storeDbData = Store.query.all()

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
        self.addSaleToDb.append(data)

    def __prepareCustomerDataToDb(self, cpf: str):
        if not cpf in self.customersCpf:
            try:
                if not cpf is None:
                    hasCustomer = self.customerDbData.filter_by(cpf=cpf).first()

                    if not hasCustomer:
                        return Customer(cpf=cpf)

                return None
            except Exception as error:
                raise Exception("Erro: Não foi possível adicionar cliente com o CPF %s na base de dados. %s" % (cpf, str(error)))

    def __prepareStoreDataToDb(self, cnpj: str):
        if not cnpj in self.storesCnpj:
            try:
                if not cnpj is None:
                    hasStore = self.storeDbData.filter_by(cnpj=cnpj).first()

                    if not hasStore:
                        return Store(cnpj=cnpj)

                return None
            except Exception as error:
                raise Exception("Erro: Não foi possível adicionar loja com o CNPJ %s na base de dados" % (cnpj, str(error)))