from sqlalchemy import TIMESTAMP, func
from flask import abort

from . import db
from .types import StatusEnum

def saveModel(modelInstance):
    try:
        db.session.add(modelInstance)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.close()
        abort(str(e), 500)

def updateModel(modelInstance, updatedData: dict):
    try:
        modelInstance.update(updatedData)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.close()
        abort(str(e), 500)

def bulkModel(objects):
    try:
        db.session.bulk_save_objects(objects)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.close()
        abort(str(e))

class Customer(db.Model):
    __tablename__ = 'customer'
    cpf = db.Column(db.String(11), primary_key=True, unique=True)

    def bulk(customers: list):
        bulkModel(customers)

class Store(db.Model):
    __tablename__ = 'store'
    cnpj = db.Column(db.String(14), primary_key=True, unique=True)

    def bulk(stores: list):
        bulkModel(stores)

class Sale(db.Model):
    __tablename__ = 'sale'
    id = db.Column(db.Integer, primary_key=True)
    private = db.Column(db.Integer, nullable=False)
    unfinished = db.Column(db.Integer, nullable=False)
    last_purchase = db.Column(db.Date, nullable=True)
    average_ticket_price = db.Column(db.Numeric(10,2), nullable=True)
    ticket_price_last_purchase = db.Column(db.Numeric(10,2), nullable=True)
    customer_id = db.Column(db.String(11), db.ForeignKey('customer.cpf'))
    most_visited_store = db.Column(db.String(14), db.ForeignKey('store.cnpj'), nullable=True)
    last_purchase_store = db.Column(db.String(14), db.ForeignKey('store.cnpj'), nullable=True)

    def save(addSale):
        saveModel(addSale)
    
    def update(SaleObject, updatedData: dict):
        updateModel(SaleObject, updatedData)

    def bulk(sales: list):
        bulkModel(sales)

class SaleFile(db.Model):
    __tablename__ = 'sale_file'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(StatusEnum), nullable=True)
    job_id = db.Column(db.String(100), nullable=True)

    def getNextId():
        maxId = db.session.query(func.max(SaleFile.id)).scalar()
        return (maxId + 1) if maxId else 1

    def save(addSaleFile):
        saveModel(addSaleFile)

    def update(SaleFileObject, updatedData: dict):
        updateModel(SaleFileObject, updatedData)

class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    created_at = db.Column(TIMESTAMP(timezone=False), default=func.now())
    sale_file_id = db.Column(db.Integer, db.ForeignKey('sale_file.id'))

    def save(addLog):
        saveModel(addLog)