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