import re
from datetime import datetime

from helpers.logger import Logger
from helpers.validateCpfCnpj import ValidaCpfCnpj

class ProcessFile():
    def __init__(self, LoggerInstance: Logger):
        self.Logger = LoggerInstance

    def processRawData(self, rowData: str):
        columns = self.__separateDataInColumns(rowData)
        cleanedRowData = self.__cleanRawData(columns)
        return self.__setHeaderOnData(cleanedRowData)       

    def __separateDataInColumns(self, rowData: str):
        splitSpaces = rowData.split(' ')
        return [item.strip() for item in splitSpaces if len(item.strip()) > 0]

    def __cleanRawData(self, rowData: list):
        cpf = re.sub('\D', '', rowData[0])
        private = int(rowData[1])
        unfinished = int(rowData[2])

        try:
            last_purchase = None if (rowData[3]).upper() == 'NULL' else datetime.strptime(rowData[3], '%Y-%m-%d')
        except:
            last_purchase = None
        
        average_ticket_price = None if (rowData[3]).upper() == 'NULL' else self.__formatCurrency(rowData[4])
        ticket_price_last_purchase = None if (rowData[3]).upper() == 'NULL' else self.__formatCurrency(rowData[5])
        most_visited_store = None if (rowData[3]).upper() == 'NULL' else re.sub('\D', '', rowData[6])
        last_purchase_store = None if (rowData[3]).upper() == 'NULL' else re.sub('\D', '', rowData[7])

        return [cpf, private, unfinished, last_purchase, average_ticket_price, ticket_price_last_purchase, most_visited_store, last_purchase_store]

    def __setHeaderOnData(self, rowData: list):
        return {
            'customer_id_cpf': rowData[0],
            'private': rowData[1],
            'unfinished': rowData[2],
            'last_purchase_date': rowData[3],
            'average_ticket_price': rowData[4],
            'ticket_price_last_purchase': rowData[5],
            'most_visited_store_cnpj': rowData[6],
            'last_purchase_store_cnpj': rowData[7],
        }

    def isValidData(self, data: list) -> bool:
        if data['customer_id_cpf'] is None:
            self.Logger.log('CPF is empty')
            return False

        if len(data['customer_id_cpf']) > 11:
            self.Logger.log('CPF %s is invalid' % data['customer_id_cpf'])
            return False

        if len(data['customer_id_cpf']) == 11 and ValidaCpfCnpj(data['customer_id_cpf']).valida() == False:
            self.Logger.log('CPF %s is invalid' % data['customer_id_cpf'])
            return False

        if not data['most_visited_store_cnpj'] is None:
            if len(data['most_visited_store_cnpj']) > 14 or len(data['most_visited_store_cnpj']) < 14:
                self.Logger.log('Most visited store CNPJ %s is invalid' % data['most_visited_store_cnpj'])
                return False

            if len(data['most_visited_store_cnpj']) == 14 and ValidaCpfCnpj(data['most_visited_store_cnpj']).valida() == False:
                self.Logger.log('Most visited store CNPJ %s is invalid' % data['most_visited_store_cnpj'])
                return False

        if not data['last_purchase_store_cnpj'] is None:
            if len(data['last_purchase_store_cnpj']) > 14 or len(data['last_purchase_store_cnpj']) < 14:
                self.Logger.log('Last purchase store CNPJ %s is invalid' % data['last_purchase_store_cnpj'])
                return False

            if not data['last_purchase_store_cnpj'] is None and len(data['last_purchase_store_cnpj']) == 14 and ValidaCpfCnpj(data['last_purchase_store_cnpj']).valida() == False:
                self.Logger.log('Last purchase store CNPJ %s is invalid' % data['last_purchase_store_cnpj'])
                return False

        return True
