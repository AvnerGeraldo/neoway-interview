from . import db

class Customer(db.Model):
    __tablename__ = 'customer'
    cpf = db.Column(db.String(11), primary_key=True, unique=True)

class Store(db.Model):
    __tablename__ = 'store'
    cnpj = db.Column(db.String(14), primary_key=True, unique=True)

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