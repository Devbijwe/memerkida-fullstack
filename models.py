
from .__init__ import db
from datetime import datetime
from sqlalchemy import inspect

class Customize(db.Model):
    __tablename__ = 'customize'
    id=db.Column(db.Integer,primary_key=True)
    publicId=db.Column(db.String(50),nullable=False)
    feature_name=db.Column(db.String(100),nullable=False)
    value=db.Column(db.String(200),nullable=True)
    status=db.Column(db.String(20),nullable=True)
    date=db.Column(db.DateTime, default=datetime.now(),nullable=True)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    

class Tshirts(db.Model):
    __tablename__ = 'tshirts'
    id=db.Column(db.Integer,primary_key=True)
    publicId=db.Column(db.String(50),nullable=False)
    tshirtId=db.Column(db.Integer,nullable=False)
    subId=db.Column(db.Integer,nullable=False)
    type=db.Column(db.String(20),nullable=False)
    name=db.Column(db.String(100),nullable=False)
    description=db.Column(db.String(200),nullable=False)
    price=db.Column(db.String(11),nullable=False)
    img=db.Column(db.String(100),nullable=False)
    colour=db.Column(db.String(200),nullable=False)
    sleeve=db.Column(db.String(50),nullable=False)
    size=db.Column(db.String(100),nullable=False)
    neck=db.Column(db.String(50),nullable=False)
    status=db.Column(db.String(20),nullable=False)
    date=db.Column(db.DateTime, default=datetime.now(),nullable=True)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    
class Customers(db.Model):
    __tablename__ = 'customers'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,unique=True)
    publicId=db.Column(db.String(50),nullable=False,unique=True)
    name=db.Column(db.String(50),nullable=False)
    mobile=db.Column(db.String(15),nullable=True,unique=True)
    pswd=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(75),nullable=True)
    loggedFrom=db.Column(db.String(20),nullable=False)
    address1=db.Column(db.String(200),nullable=True)
    address2=db.Column(db.String(200),nullable=True)
    city=db.Column(db.String(50),nullable=True)
    state=db.Column(db.String(50),nullable=True)
    zip=db.Column(db.Integer,nullable=True)
    date=db.Column(db.DateTime, default=datetime.now(),nullable=True)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

class Templates(db.Model):
    __tablename__ = 'templates'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,unique=True)
    publicId=db.Column(db.String(50),nullable=False,unique=True)
    title=db.Column(db.String(250),nullable=False)
    category=db.Column(db.String(50),nullable=False)
    keywords=db.Column(db.String(100),nullable=True)
    price=db.Column(db.String(10),nullable=False)
    lightTemplate=db.Column(db.String(200),nullable=False)
    lightTshirt=db.Column(db.String(200),nullable=False)
    lightBG=db.Column(db.String(50),nullable=False)
    darkTemplate=db.Column(db.String(200),nullable=False)
    darkTshirt=db.Column(db.String(200),nullable=False)
    darkBG=db.Column(db.String(50),nullable=False)
    carousel=db.Column(db.Boolean, default=False,nullable=False)
    date=db.Column(db.DateTime, default=datetime.now(),nullable=True)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    

class Admin(db.Model):
    __tablename__ = 'admin'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,unique=True)
    publicId=db.Column(db.String(50),nullable=False,unique=True)
    name=db.Column(db.String(50),nullable=False)
    username=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(75),nullable=False,unique=True)
    password=db.Column(db.String(50),nullable=False)
    secretkey=db.Column(db.String(100),nullable=False)
    date=db.Column(db.DateTime, default=datetime.now(),nullable=True)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    
class Orders(db.Model):
    __tablename__ = 'orders'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,unique=True)
    publicId=db.Column(db.String(50),nullable=False,unique=True)
    custId=db.Column(db.String(50),nullable=False)
    paymentId=db.Column(db.String(50),nullable=True,unique=True)
    trackingId=db.Column(db.String(50),nullable=True,unique=True)
    type=db.Column(db.String(25),nullable=False)
    tshirtImg=db.Column(db.String(200),nullable=False)
    printImg=db.Column(db.String(200),nullable=False)
    theme=db.Column(db.String(20),nullable=False)
    details=db.Column(db.String(500),nullable=True)
    quantity=db.Column(db.Integer,nullable=True)
    price=db.Column(db.String(10),nullable=False)
    colour=db.Column(db.String(25),nullable=False)
    size=db.Column(db.String(10),nullable=False)
    invoice=db.Column(db.String(200),nullable=True)
    status=db.Column(db.String(50),nullable=True)
    delivered=db.Column(db.String(10),nullable=False)
    date=db.Column(db.DateTime, default=datetime.now(),nullable=True)   
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    
class Payments(db.Model):
    __tablename__ = 'payments'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,unique=True)
    publicId=db.Column(db.String(50),nullable=False,unique=True)
    custId=db.Column(db.String(50),nullable=False)
    orderId=db.Column(db.String(50),nullable=False,unique=True)
    transactionId=db.Column(db.String(50),nullable=True,unique=True)
    payMethods=db.Column(db.String(50),nullable=False)
    name=db.Column(db.String(75),nullable=False)
    mobile=db.Column(db.String(15),nullable=False)
    address1=db.Column(db.String(200),nullable=False)
    address2=db.Column(db.String(200),nullable=False)
    city=db.Column(db.String(50),nullable=False)
    state=db.Column(db.String(50),nullable=False)
    zip=db.Column(db.Integer,nullable=False)
    subtotal=db.Column(db.Integer,nullable=False)
    charges=db.Column(db.Integer,nullable=False)
    total=db.Column(db.Integer,nullable=False)
    status=db.Column(db.String(20),nullable=False)
    date=db.Column(db.DateTime, default=datetime.now(),nullable=True)   
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

class Transaction(db.Model):
    __tablename__ = 'transaction'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,unique=True)
    publicId=db.Column(db.String(50),nullable=False,unique=True)
    custId=db.Column(db.String(50),nullable=False)
    orderId=db.Column(db.String(50),nullable=False,unique=True)
    name=db.Column(db.String(75),nullable=False)
    tracking_id=db.Column(db.String(15),nullable=True)
    bank_ref_no=db.Column(db.String(75),nullable=True)
    amount=db.Column(db.String(15),nullable=True)
    order_status=db.Column(db.String(20),nullable=True)
    currency=db.Column(db.String(5),nullable=True)
    payment_mode=db.Column(db.String(20),nullable=True)
    failure_message=db.Column(db.String(100),nullable=True)
    
   
    date=db.Column(db.DateTime, default=datetime.now(),nullable=True)   
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    
class Edituploads(db.Model):
    __tablename__ = 'edituploads'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,unique=True)
    publicId=db.Column(db.String(50),nullable=False,unique=True)
    custId=db.Column(db.String(50),nullable=True)
    sorter=db.Column(db.String(20),nullable=True)
    tshirtId=db.Column(db.String(50),nullable=True)
    tshirtImg=db.Column(db.String(200),nullable=True)
    printImg=db.Column(db.String(200),nullable=True)
    details=db.Column(db.String(100),nullable=False)
    date=db.Column(db.DateTime, default=datetime.now(),nullable=True) 
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }  
     
class Carts(db.Model):
    __tablename__ = 'carts'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,unique=True)
    publicId=db.Column(db.String(50),nullable=False,unique=True)
    custId=db.Column(db.String(50),nullable=False)
    type=db.Column(db.String(25),nullable=False)
    tshirtId=db.Column(db.String(50),nullable=False)
    printId=db.Column(db.String(50),nullable=False)
    theme=db.Column(db.String(20),nullable=False)
    details=db.Column(db.String(200),nullable=False)
    colour=db.Column(db.String(25),nullable=True)
    size=db.Column(db.String(25),nullable=True)
    price=db.Column(db.Integer,nullable=False)
    quantity=db.Column(db.Integer,nullable=True) 
    date=db.Column(db.DateTime, default=datetime.now(),nullable=True) 
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }  

class Chats(db.Model):
    __tablename__ = 'chats'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,unique=True)
    custId=db.Column(db.String(50),db.ForeignKey('customers.publicId'),nullable=False)
    sender=db.Column(db.String(50),nullable=False)
    receiver=db.Column(db.String(50),nullable=False)
    msg=db.Column(db.String(250),nullable=False)
    date=db.Column(db.DateTime, default=datetime.now(),nullable=True)
    customer = db.relationship('Customers', backref='chats')
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

