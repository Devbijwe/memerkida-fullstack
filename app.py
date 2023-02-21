
from ast import Pass
import io
from optparse import Option
import time
import pandas as pd
import pyqrcode
import png
import tempfile
from captcha.image import ImageCaptcha
from PIL import Image
from itertools import product
import os
from tokenize import String
from werkzeug.utils import secure_filename
import random
import math
import secrets
import string
import docx
from docx2pdf import convert
import json
from sqlite3 import IntegrityError
from sqlalchemy.exc import IntegrityError 
from flask import Flask,render_template,session,redirect,send_file, request,flash,jsonify,Response,url_for
from jinja2 import Template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
import uuid
from flask_mail import Mail
import cv2
from sqlalchemy.orm import load_only
from PIL import ImageEnhance,Image,ImageFilter
import base64
from docxtpl import DocxTemplate
import re
import xlwt
from sqlalchemy_utils import database_exists, create_database


with open("config.json","r") as c:
    params=json.load(c)['params']
with open("config.json","r") as d:
    directories=json.load(d)['directories']


app=Flask(__name__,template_folder="Templates")
app.secret_key='sdx2323@3343zbhcfew3rr3343@@###$2ffr454'


if (params['local_server']):
    app.config['SQLALCHEMY_DATABASE_URI']=params['local_url']
else:
    if not database_exists(params['prod_url']):
        create_database(params['prod_url'])
    app.config['SQLALCHEMY_DATABASE_URI']=params['prod_url']

db=SQLAlchemy(app)    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    
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
    colour=db.Column(db.String(50),nullable=False)
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
    mobile=db.Column(db.String(15),nullable=False,unique=True)
    pswd=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(75),nullable=True)
    loggedFrom=db.Column(db.String(20),nullable=False)
    address1=db.Column(db.String(200),nullable=True)
    address2=db.Column(db.String(200),nullable=True)
    city=db.Column(db.String(50),nullable=True)
    state=db.Column(db.String(75),nullable=True)
    zip=db.Column(db.Integer,nullable=True)
    date=db.Column(db.DateTime, default=datetime.now(),nullable=True)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    
class Templates(db.Model):
    __tablename__ = 'templates'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,unique=True)
    publicId=db.Column(db.String(50),nullable=False)
    postId=db.Column(db.Integer,nullable=False)
    queSet=db.Column(db.String(5),nullable=False)
    que=db.Column(db.String(5),nullable=False)
    inputType=db.Column(db.String(20),nullable=False)
    date=db.Column(db.DateTime, default=datetime.now(),nullable=True)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    
class Answers(db.Model):
    __tablename__ = 'answers'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,unique=True)
    publicId=db.Column(db.String(50),nullable=False)
    custId=db.Column(db.String(50),nullable=False)
    postId=db.Column(db.Integer,nullable=False)
    tshirtId=db.Column(db.Integer,nullable=False)
    queset=db.Column(db.Integer,nullable=False)
    que=db.Column(db.Integer,nullable=False)
    answer=db.Column(db.String(200),nullable=False)
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
    paymentId=db.Column(db.String(25),nullable=True,unique=True)
    paymentStatus=db.Column(db.String(50),nullable=True)
    type=db.Column(db.String(25),nullable=False)
    tshirtImg=db.Column(db.String(200),nullable=False)
    printImg=db.Column(db.String(200),nullable=False)
    answerId=db.Column(db.String(50),nullable=False)
    details=db.Column(db.String(500),nullable=True)
    quantity=db.Column(db.Integer,nullable=True)
    price=db.Column(db.String(10),nullable=False)
    colour=db.Column(db.String(25),nullable=False)
    size=db.Column(db.String(10),nullable=False)
    invoice=db.Column(db.String(200),nullable=False)
    delivered=db.Column(db.String(10),nullable=False)
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
    answerId=db.Column(db.String(50),nullable=False)
    details=db.Column(db.String(200),nullable=False)
    colour=db.Column(db.String(25),nullable=True)
    size=db.Column(db.String(25),nullable=True)
    price=db.Column(db.Integer,nullable=False)
    quantity=db.Column(db.Integer,nullable=True) 
    date=db.Column(db.DateTime, default=datetime.now(),nullable=True) 
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }  
    
with app.app_context():
    db.create_all()
    
#  *********************************CUSTOMERS***************************************************

#home page
@app.route("/",methods=['GET','POST'])   
def home():
    # for key in directories:
    #     print(directories.get(key))
    if 'admin' in session:
        return render_template("admin_home.html")
    orders=Orders.query.order_by(Orders.id.desc()).all()
    return render_template("index.html",params=params,orders=orders)
# get started
@app.route('/about')
def about():
    return render_template('about.html')

# get started
@app.route('/getStarted')
def getStarted():
    return render_template('getStarted.html')

#choose cutomize by and displays tshirts
@app.route("/customize/<string:types>=ty",methods=['GET','POST'])
def customize(types):
    load=None
    if types=="default":
        load="templates"
    elif types=="cust":
        load="editor"
    tshirts=Tshirts.query.filter_by(type="Demo",status="Active").all()
    
    return render_template("customize_type.html",types=types,tshirts=tshirts,load=load)
 
 
 
#  ************************************************************************************
#1) customize by memerkida
# shows templates 
@app.route("/templates/<string:tshirtId>=t",methods=['GET','POST'])   
def memeType(tshirtId):
    Arr=[]
    data0=Templates.query.filter_by(queSet=0,inputType="0").order_by(Templates.postId.asc()).all()
    for key in data0:
        tshirt=None
        data1=Templates.query.filter_by(postId=key.postId ,queSet=0,inputType="1").first()
        if data1:
            tshirt=data1.que
        item={
            "publicId":key.publicId,
            "postId":key.postId,
            "post":key.que,
            "tshirt":tshirt 
        }
        Arr.append(item)
        
    return render_template("templates.html",params=params,data0=data0,tshirtId=tshirtId,Arr=Arr)


# displays questions for template  
@app.route("/queDisplay/<string:tshirtId>=t/<string:printId>=p", methods=['GET','POST'])
def queDisp(tshirtId,printId):
    if 'user' in session :
        data=Customers.query.filter_by(publicId=session['user']).first()
        if data and request.method=='POST':
            app.config['UPLOAD_FOLDER']= os.path.abspath("../"+params['ImgAnswers'])
            publicId = uuid.uuid4().hex
            custId=data.publicId
            template=Templates.query.filter_by(queSet=0,publicId=printId).first()
            
            postId=template.publicId
             
            print(postId)
            # ans1werImg1=request.files["ans1werImg1"]
            ans1werText1=request.form.get("ans1werText1")
            # ans1werImg2=request.files["ans1werImg2"]
            ans1werText2=request.form.get("ans1werText2")
            # ans1werImg3=request.files["ans1werImg3"]
            ans1werText3=request.form.get("ans1werText3")
            # ans1werImg4=request.files["ans1werImg4"]
            ans1werText4=request.form.get("ans1werText4")
            # ans1werImg5=request.files["ans1werImg5"]
            ans1werText5=request.form.get("ans1werText5")
            # ans1werImg6=request.files["ans1werImg6"]
            ans1werText6=request.form.get("ans1werText6")
            # ans1werImg7=request.files["ans1werImg7"]
            ans1werText7=request.form.get("ans1werText7")
            # ans1werImg8=request.files["ans1werImg8"]
            ans1werText8=request.form.get("ans1werText8")
            # ans1werImg9=request.files["ans1werImg9"]
            ans1werText9=request.form.get("ans1werText9")
            # ans1werImg10=request.files["ans1werImg10"]
            ans1werText10=request.form.get("ans1werText10")
            # ans2werImg1=request.files["ans2werImg1"]
            ans2werText1=request.form.get("ans2werText1")
            # ans2werImg2=request.files["ans2werImg2"]
            ans2werText2=request.form.get("ans2werText2")
            # ans2werImg3=request.files["ans2werImg3"]
            ans2werText3=request.form.get("ans2werText3")
            # ans2werImg4=request.files["ans2werImg4"]
            ans2werText4=request.form.get("ans2werText4")
            # ans2werImg5=request.files["ans2werImg5"]
            ans2werText5=request.form.get("ans2werText5")
            # ans2werImg6=request.files["ans2werImg6"]
            ans2werText6=request.form.get("ans2werText6")
            # ans2werImg7=request.files["ans2werImg7"]
            ans2werText7=request.form.get("ans2werText7")
            # ans2werImg8=request.files["ans2werImg8"]
            ans2werText8=request.form.get("ans2werText8")
            # ans2werImg9=request.files["ans2werImg9"]
            ans2werText9=request.form.get("ans2werText9")
            # ans2werImg10=request.files["ans2werImg10"]
            ans2werText10=request.form.get("ans2werText10")
            
            if ans1werText1:
                cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=1,que=1,answer=ans1werText1,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans1werText2:
                cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=1,que=2,answer=ans1werText2,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans1werText3:
                cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=1,que=3,answer=ans1werText3,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans1werText4:
                cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=1,que=4,answer=ans1werText4,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans1werText5:
                cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=1,que=5,answer=ans1werText5,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans1werText6:
                cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=1,que=6,answer=ans1werText6,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans1werText7:
                cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=1,que=7,answer=ans1werText7,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans1werText8:
                cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=1,que=8,answer=ans1werText8,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans1werText9:
                cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=1,que=9,answer=ans1werText9,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans1werText10:
                cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=1,que=10,answer=ans1werText10,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans2werText1:
                cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=2,que=1,answer=ans2werText1,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans2werText2:
                cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=2,que=2,answer=ans2werText2,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans2werText3:
                cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=2,que=3,answer=ans2werText3,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans2werText4:
                cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=2,que=4,answer=ans2werText4,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans2werText5:
                cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=2,que=5,answer=ans2werText5,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans2werText6:
                cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=2,que=6,answer=ans2werText6,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans2werText7:
                cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=2,que=7,answer=ans2werText7,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans2werText8:
                cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=2,que=8,answer=ans2werText8,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans2werText9:
                cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=2,que=9,answer=ans2werText9,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans2werText10:
                cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=2,que=10,answer=ans2werText10,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
                  
            
            try:
                ans1werImg1=request.files["ans1werImg1"]
                if ans1werImg1:
                    ImgName="ans1wer1ImgPost=" +f'{postId}'+"User="+f'{custId}'+ans1werImg1.filename
                    ans1werImg1.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=1,que=1,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans1werImg2=request.files["ans1werImg2"]
                if ans1werImg2:
                    ImgName="ans1wer2ImgPost=" +f'{postId}'+"User="+f'{custId}'+ans1werImg2.filename
                    ans1werImg2.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=1,que=2,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans1werImg3=request.files["ans1werImg3"]
                if ans1werImg3:
                    ImgName="ans1wer3ImgPost=" +f'{postId}'+"User="+f'{custId}'+ans1werImg3.filename
                    ans1werImg3.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=1,que=3,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans1werImg4=request.files["ans1werImg4"]
                if ans1werImg4:
                    ImgName="ans1wer4ImgPost=" +f'{postId}'+"User="+f'{custId}'+ans1werImg4.filename
                    ans1werImg4.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=1,que=4,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans1werImg5=request.files["ans1werImg5"]
                if ans1werImg5:
                    ImgName="ans1wer5ImgPost=" +f'{postId}'+"User="+f'{custId}'+ans1werImg5.filename
                    ans1werImg5.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=1,que=5,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans1werImg6=request.files["ans1werImg6"]
                if ans1werImg6:
                    ImgName="ans1wer6ImgPost=" +f'{postId}'+"User="+f'{custId}'+ans1werImg6.filename
                    ans1werImg6.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=1,que=6,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans1werImg7=request.files["ans1werImg7"]
                if ans1werImg7:
                    ImgName="ans1wer7ImgPost=" +f'{postId}'+"User="+f'{custId}'+ans1werImg7.filename
                    ans1werImg7.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=1,que=7,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans1werImg8=request.files["ans1werImg8"]
                if ans1werImg8:
                    ImgName="ans1wer8ImgPost=" +f'{postId}'+"User="+f'{custId}'+ans1werImg8.filename
                    ans1werImg8.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=1,que=8,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans1werImg9=request.files["ans1werImg9"]
                if ans1werImg9:
                    ImgName="ans1wer9ImgPost=" +f'{postId}'+"User="+f'{custId}'+ans1werImg9.filename
                    ans1werImg9.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=1,que=9,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans1werImg10=request.files["ans1werImg10"]
                if ans1werImg10:
                    ImgName="ans1wer10ImgPost=" +f'{postId}'+"User="+f'{custId}'+ans1werImg10.filename
                    ans1werImg10.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=1,que=10,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans2werImg1=request.files["ans2werImg1"]
                if ans2werImg1:
                    ImgName="ans2wer1ImgPost=" +f'{postId}'+"User="+f'{custId}'+ans2werImg1.filename
                    ans2werImg1.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=2,que=1,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans2werImg2=request.files["ans2werImg2"]
                if ans2werImg2:
                    ImgName="ans2wer2ImgPost=" +f'{postId}'+"User="+f'{custId}'+ans2werImg2.filename
                    ans2werImg2.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=2,que=2,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans2werImg3=request.files["ans2werImg3"]
                if ans2werImg3:
                    ImgName="ans2wer3ImgPost=" +f'{postId}'+"User="+f'{custId}'+ans2werImg3.filename
                    ans2werImg3.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=2,que=3,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans2werImg4=request.files["ans2werImg4"]
                if ans2werImg4:
                    ImgName="ans2wer4ImgPost=" +f'{postId}'+"User="+f'{custId}'+ans2werImg4.filename
                    ans2werImg4.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=2,que=4,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans2werImg5=request.files["ans2werImg5"]
                if ans2werImg5:
                    ImgName="ans2wer5ImgPost=" +f'{postId}'+"User="+f'{custId}'+ans2werImg5.filename
                    ans2werImg5.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=2,que=5,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans2werImg6=request.files["ans2werImg6"]
                if ans2werImg6:
                    ImgName="ans2wer6ImgPost=" +f'{postId}'+"User="+f'{custId}'+ans2werImg6.filename
                    ans2werImg6.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=2,que=6,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans2werImg7=request.files["ans2werImg7"]
                if ans2werImg7:
                    ImgName="ans2wer7ImgPost=" +f'{postId}'+"User="+f'{custId}'+ans2werImg7.filename
                    ans2werImg7.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=2,que=7,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans2werImg8=request.files["ans2werImg8"]
                if ans2werImg8:
                    ImgName="ans2wer8ImgPost=" +f'{postId}'+"User="+f'{custId}'+ans2werImg8.filename
                    ans2werImg8.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=2,que=8,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans2werImg9=request.files["ans2werImg9"]
                if ans2werImg9:
                    ImgName="ans2wer9ImgPost=" +f'{postId}'+"User="+f'{custId}'+ans2werImg9.filename
                    ans2werImg9.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=2,que=9,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans2werImg10=request.files["ans2werImg10"]
                if ans2werImg10:
                    ImgName="ans2wer10ImgPost=" +f'{postId}'+"User="+f'{custId}'+ans2werImg10.filename
                    ans2werImg10.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(publicId=publicId,custId=custId,postId=postId,tshirtId=tshirtId,queset=2,que=10,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass  
            flash("submitted successfully....")
            data0=Templates.query.filter_by(publicId=printId,queSet=0,inputType="0").first()
            answerId=publicId
            return render_template("address.html",answerId=answerId,post_name=data0.que,tshirtId=tshirtId,printId=printId,postId=postId,type="default",source="noCart")
      
            return render_template("prodReview.html",post_name=data0.que,tshirtId=tshirtId,printId=printId,postId=postId,type="default",source="noCart")
        else:
            questionsContType0=""
            questionsContType1=[]
            questionsContType2=[]
            data0=Templates.query.filter_by(publicId=printId,queSet=0).first()
            data1=Templates.query.filter_by(publicId=printId,queSet=1).all()
            if data0:
                questionsContType0=data0
                
            if data1:
                for key in data1:
                    questionsContType1.append(key)

            data2=Templates.query.filter_by(publicId=printId,queSet=2).all()
            if data2:
                for key in data2:
                    questionsContType2.append(key)
            return render_template("queDisplay.html",queCont0=questionsContType0,queCont1=questionsContType1,queCont2=questionsContType2,tshirtId=tshirtId,printId=printId)
    else:
        flash("You need to Login First..")
        return redirect("/login=ty/%s/%s=queDisplay" %(tshirtId, printId))

#  ************************************************************************************
# 2) customize by yourself
# opens editor
@app.route("/editor/<string:tshirtId>=t",methods=['GET','POST'])
def edits(tshirtId):
    tshirt=Tshirts.query.filter_by(publicId=tshirtId).first()
    if 'user' in session:
        
        return render_template("edit123.html",tshirt=tshirt)
    else:
        flash("You need to Login First..")
       
        return redirect("/login=ty/0/%s=editor" %tshirtId)
   
# saves edited img (api)
@app.route("/saveImg/<string:sortStr>=type",methods=['GET','POST'])
def saveImg(sortStr):
    if "user" in session:
        if request.method=="POST":
            sorter=sortStr
            data=Customers.query.filter_by(publicId=session['user']).first()
            tshirtImg= request.files.get('tshirtImg')
            printImg= request.files.get('printImg')
            tshirtId= request.form.get('tshirtId')
            uploads=Edituploads.query.filter_by(custId=session['user']).all()
       
            if printImg and tshirtImg:
                app.config['UPLOAD_FOLDER']= os.path.abspath("../"+params['editImagesUpload'])
                printImg = Image.open(printImg.stream)
                printImgName="cust"+str(data.publicId)+"No"+str(len(uploads))+"Images.png" 
                printImg.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(printImgName) ))   
                printImg=secure_filename(printImgName) 
                app.config['UPLOAD_FOLDER']= os.path.abspath("../"+params['editTshirtUpload'])
                tshirtImg= Image.open(tshirtImg.stream)
                tshirtImgName="cust"+str(data.publicId)+"No"+str(len(uploads))+"Tshirt.png"
                tshirtImg.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(tshirtImgName) )) 
                tshirtImg=secure_filename(tshirtImgName) 
                publicId = uuid.uuid4().hex
                # print( publicId)
                try:
                    cred=Edituploads(publicId=publicId,custId=data.publicId,sorter=sorter,tshirtId=tshirtId,tshirtImg=secure_filename(tshirtImg), printImg=secure_filename(printImg),details="ok",date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
                    flash("%s has been saved successfully..." %sorter)
                    imgUp=Edituploads.query.filter_by(custId=session["user"]).order_by(Edituploads.id.desc()).first()
                    id=imgUp.publicId
                    return {
                        "status":"ok",
                        "uploaded":"all",
                        "tshirtId":tshirtId,
                        "printId":id
                    }
                except:
                    flash("%s has not been saved..." %sorter)   
    return {
        "status":"failed",
        "uploaded":"nothing" ,
        "tshirtId":0,
        "printId":0
    }
    

#  *************************************ORDER PROCEDURE**********************************************


# modifies address
@app.route("/<string:tshirtId>=t/<string:printId>=p/<string:answerId>=a/<string:type>/<string:source>/address",methods=['GET','POST'])
def address(tshirtId,printId,answerId,type,source):
    if 'user' in session:
        data=Customers.query.filter_by(publicId=session['user']).first()
        if request.method=="POST" and data:
            name=request.form.get("name")
            mobile=request.form.get("mobile")
            email=request.form.get("email")
            address1=request.form.get("address1")
            address2=request.form.get("address2")
            city=request.form.get("city")
            state=request.form.get("state")
            zip=request.form.get("zip")
            data.username=name
            data.mobile=mobile
            data.address1=address1
            data.city=city
            data.state=state
            data.zip=zip
            if address2:
                data.address2=address2
            if email:
                data.email=email
            db.session.commit()
            return redirect("/%s=t/%s=p/%s=a/%s/%s/checkout" %(tshirtId,printId,answerId,type,source))
           
            # return redirect("/%s=t/%s=p/payments/%s/%s" %(tshirtId,printId,type,source))
    
        return render_template("address.html",answerId=answerId, data=data,tshirtId=tshirtId,printId=printId,type=type,source=source)
    else:
        return redirect("/login=ty/0/0=view")

# get address of customer (api)
@app.route('/checkout/get/address',methods=['GET'])
def getAddress():
    if 'user' in session:
        user=Customers.query.filter_by(publicId=session['user']).first()
        if user:
            return {
                "code":200,
                "name":user.name,
                "address1":user.address1,
                "address2":user.address2,
                "city":user.city,
                "state":user.state,
                "zip":user.zip,
            }
    return{
         "code":400
    }

# checkout
@app.route("/<string:tshirtId>=t/<string:printId>=p/<string:answerId>=a/<string:type>/<string:source>/checkout",methods=['GET','POST'])   
def checkout(tshirtId,printId,answerId,type,source):
    if 'user' in session:
        data=Customers.query.filter_by(publicId=session['user']).first()
        if request.method=="POST":
            tshirtImg=0
            printImg=0 
            paymentStatus="pending"
            paymentId=0
            quantity=request.form.get("quantity")
            colour= request.form.get("colour")
            size=request.form.get("size")
            price=request.form.get("price")
            details=request.form.get("details")
            print("ok")
            if source=="noCart":
                if type=="default":
                    answerId=answerId
                    tshirt=Tshirts.query.filter_by(publicId=tshirtId,type="Demo",status="Active").first()
                    if tshirt:
                        tshirtImg=tshirt.img
                    template=Templates.query.filter_by(queSet=0,publicId=printId).all()
                    for key in template:
                        
                        if key.inputType=="0":
                            printImg=key.que
                        elif key.inputType=="1":
                            tshirt=key.que
                        elif key.inputType=="price":
                            pass
                    
                elif type =="customize":
                    uploads=Edituploads.query.filter_by(custId=session['user'],publicId=printId).first()
                    if uploads:
                        tshirtImg=uploads.tshirtImg
                        printImg=uploads.printImg
            elif source=="cart":
                cartId=tshirtId
                cart=Carts.query.filter_by(custId=data.publicId,publicId=cartId).first()
                tshirtId=cart.tshirtId
                print(cart.printId)
                if type=="default":
                    tshirt=Tshirts.query.filter_by(publicId=cart.tshirtId,type="Demo",status="Active").first()  
                    if tshirt:
                        tshirtImg=tshirt.img
                        template=Templates.query.filter_by(queSet=0,publicId=cart.printId).all()
                    for key in template:
                        if key.inputType=="0":
                           
                            printImg=key.que
                        # elif key2.inputType=="1":
                        #     tshirt=key2.que
                        # elif key2.inputType=="price":
                        #     price=key2.que
                   
                elif type=="customize":
                    uploads=Edituploads.query.filter_by(custId=data.publicId,publicId=cart.printId).first()
                    print(uploads)
                    if uploads:
                        tshirtImg=uploads.tshirtImg
                        printImg=uploads.printImg
                    
                size=cart.size
                price=cart.price
                colour=cart.colour
                quantity=cart.quantity
                price=cart.price
                type=cart.type
                answerId=cart.answerId
                
                
                
                
            publicId = uuid.uuid4()
            order=Orders.query.filter_by(custId=data.publicId,quantity=quantity,colour=colour,size=size,tshirtImg=tshirtImg,type=type,answerId=answerId,printImg=printImg,price=price,delivered=False).first()
            if order:
                print(order)
                flash("This Order has been already placed..")
                orderId=order.publicId
                source="cart"
                
                # return redirect("/%s/payments" %(orderId))
            else:
                cred=Orders(publicId=publicId,custId=data.publicId,quantity=quantity,colour=colour,size=size,tshirtImg=tshirtImg,type=type,answerId=answerId,printImg=printImg,details=details,price=price,paymentStatus=paymentStatus,paymentId=paymentId,delivered=False,date=datetime.now())
                try:
                    db.session.add(cred)
                    db.session.commit()
                    flash("This Order has been submitted..")
                    orderId=publicId
                    return redirect("/orders=view")
                except IntegrityError:
                    flash("Some error occured. Please reload page and try again..")
            return redirect("/%s=t/%s=p/%s=a/%s/%s/checkout" %(tshirtId,printId,answerId,type,source))
        if source=="noCart":
            cartId=0
            quantity=1
            if type=="default":
                template=Templates.query.filter_by(queSet=0,publicId=printId).all()
                for key in template:
                    if key.inputType=="0":
                        post=key.que
                    elif key.inputType=="1":
                        post_name=key.que
                    elif key.inputType=="price":
                        price=key.que
            
                tshirt=Tshirts.query.filter_by(publicId=tshirtId).first()
                print(tshirt)
                # return render_template("address.html",post_name=data0.que,tshirtId=tshirtId,printId=printId,postId=postId,type="default",source="noCart")
            else:
                uploads=Edituploads.query.filter_by(custId=session['user'],publicId=printId).first()
                tshirt=Tshirts.query.filter_by(publicId=tshirtId).first()
                if  uploads:
                    tshirtId= uploads.tshirtId
                    printId=printId
                    post_name=uploads.tshirtImg
                    price=tshirt.price   
            if tshirt:
                colour=re.sub(' +', '', tshirt.colour).capitalize().split(",")
                size=re.sub(' +', '', tshirt.size).upper().split(",")
                description=tshirt.description
                title=tshirt.name
                sleeve=tshirt.sleeve
                neck=tshirt.neck
                # print("colour :",colour,"size:",size,"price:",price)
        else:
            try:
                cart=Carts.query.filter_by(custId=data.publicId ,tshirtId=tshirtId ,printId=printId,type=type).first()  
            except: 
                cart=Carts.query.filter_by(custId=data.publicId ,publicId=tshirtId).first()  
           
            tshirt=Tshirts.query.filter_by(publicId=cart.tshirtId,type="Demo",status="Active").first()
        
              
               
            if type=="default":
                if tshirt:
                    tshirtImg=tshirt.img
                
                template=Templates.query.filter_by(queSet=0,publicId=cart.printId).all()
                for key in template:
                    if key.inputType=="0":
                        post=key.que
                    elif key.inputType=="1":
                        post_name=key.que
                    elif key.inputType=="price":
                        price=key.que
        
            elif type=="customize":
                uploads=Edituploads.query.filter_by(custId=data.publicId,publicId=cart.printId).first()
                if uploads:
                    tshirtImg=uploads.tshirtImg
                    post_name=uploads.tshirtImg
                    printImg=uploads.printImg
            price=cart.price
            size=cart.size
            colour=cart.colour
            title=cart.details
            description=tshirt.description
            cartId=cart.publicId
            quantity=cart.quantity
            sleeve=tshirt.sleeve
            neck=tshirt.neck 
            answerId=cart.answerId
        return render_template("checkout.html",answerId=answerId,neck=neck,sleeve=sleeve,cartId=cartId,colour=colour,size=size, quantity=quantity, price=price,tshirtId=tshirtId,post_name=post_name,printId=printId,type=type,source=source,title=title,description=description)
        
    else:
       return redirect("/login=ty/0/0=prod")

# payments
@app.route("/<string:orderId>/payments",methods=['GET','POST'])
def payments(orderId):
    if 'user' in session:
        data=Customers.query.filter_by(publicId=session['user']).first()
        if request.method=="POST":
           
           
            return redirect("/%s/payments" %(orderId))
                    
            return redirect("/orders=view")
        return render_template("payments.html",orderId)
    else:
        return redirect("/login=ty/0/0=view")
 
 

#  **********************************CARTS***********************************************
# shows cart
@app.route("/carts",methods=['GET','POST'])   
def carts():
    if 'user' in session:
        Arr=[]
        tshirtImg, printImg=None,None
        data=Customers.query.filter_by(publicId=session['user']).first()
        carts=Carts.query.order_by(Carts.date.desc()).filter_by(custId=data.publicId).all()
        for key in carts:
            if key.type=="default":
                tshirt=Tshirts.query.filter_by(publicId=key.tshirtId,type="Demo",status="Active").first()  
                if tshirt:
                    tshirtImg=tshirt.img
                template=Templates.query.filter_by(queSet=0,publicId=key.printId).all()
                for key2 in template:
                    if key2.inputType=="0":
                        printImg=key2.que
                    # elif key2.inputType=="1":
                    #     tshirt=key2.que
                    # elif key2.inputType=="price":
                    #     price=key2.que
                   
            elif key.type=="customize":
                uploads=Edituploads.query.filter_by(custId=data.publicId,publicId=key.printId).first()
                
                if uploads:
                    tshirtImg=uploads.tshirtImg
                    printImg=uploads.printImg
            # print(key.tshirtId, "   " ,key.printId)       
            item={
                 "publicId":key.publicId,
                "type":key.type,
                "tshirtImg":tshirtImg,
                "printImg":printImg,
                "price":key.price,
                "quantity":key.quantity,
                "details":key.details,   
                 "colour":key.colour,
                "size":key.size,   
                "date":key.date,  
                "answerId":key.answerId,   
                 "printId":key.printId,   
                "tshirtId":key.tshirtId     
            }
            Arr.append(item)
            # print(Arr)
        return render_template("carts.html",carts=Arr)
 
# adds item to carts   (api)
@app.route("/cart/<string:mainstr>/<string:custId>/<string:cartId>",methods=['GET','POST'])
def addtoCart(mainstr,custId,cartId): 
    if 'user' in session:
        data=Customers.query.filter_by(publicId=custId).first()
        if request.method=="POST":
            publicId = uuid.uuid4().hex 
            tshirtId= request.form.get("tshirtId")
            printId= request.form.get("printId")
            details= request.form.get("details")
            colour= request.form.get("colour")
            size= request.form.get("size")
            price= request.form.get("price")
            quantity= request.form.get("quantity")
            answerId=request.form.get("answerId")
            type= request.form.get("type")
            print(printId ," , ",tshirtId)
            if mainstr=='add':    
                cart=Carts.query.filter_by(custId=data.publicId,answerId=answerId ,tshirtId=tshirtId ,printId=printId,type=type).first()
                if cart is None:
                    cred=Carts(publicId=publicId,custId=data.publicId,answerId=answerId ,tshirtId=tshirtId,colour=colour,size=size,type=type,printId=printId,details=details,price=price,quantity=quantity,date=datetime.now())
                    try:
                        db.session.add(cred)
                        db.session.commit()
                        msg="Item added to cart successfully.."
                        code=200
                    except IntegrityError:
                        msg="Some error occured. Please reload page and try again.."
                        code=400
                else:
                    
                    # cart.quantity+=int(quantity)
                    # cart.price+=int(price)
                    
                    db.session.commit()
                    msg="Item is already in cart.." #so we increase its quantity by 1
                    code=200            
        if mainstr=='remove':
            cart=Carts.query.filter_by(custId=data.publicId ,publicId=cartId).first()
            db.session.delete(cart)
            db.session.commit()
            msg="Item is removed from cart.." #so we increase its quantity by 1
            code=200      
    return {
        "code":code,
        "msg":msg
    }
    
                
       
 

# updates cart quantity   (api)
@app.route("/cart/quantity/edit/<string:cartId>/<string:plusminus>/<publicId>", methods=["GET",'POST'])
def cartQuantity(publicId,cartId,plusminus):
    
    if  'user' in session:
        cust=Customers.query.filter_by(publicId=session['user']).first()
        if cust:
            data=Carts.query.filter_by(publicId=cartId,custId=cust.publicId).first()
            if plusminus=='plus':
                data.price=data.price+data.price/ data.quantity
                data.quantity=data.quantity+1
            elif plusminus=='minus':
                if data.quantity==1:
                    data.quantity=1
                    data.price=data.price
                else:
                    data.price=data.price-data.price/ data.quantity
                    data.quantity=data.quantity-1
            
            db.session.commit()
            data=Carts.query.filter_by(publicId=cartId,custId=cust.publicId).first()
            
            return {
                "status":"success",
                "code":200,
                "quantity":data.quantity,
                 "price":data.price
            }
   
    return {
        "status":"failure",
        "code":400,
        "quantity":None,
        "price":None
    }  


# shows orders
@app.route("/orders=<string:action>",methods=['GET','POST'])   
def orders(action):
    if "user" in session:
        data=Customers.query.filter_by(publicId=session['user']).first()
        orders=Orders.query.filter_by(custId=data.publicId).order_by(Orders.date.desc()).all()
        return render_template("orders.html",orders=orders )
    else:
        return redirect("/login=ty/0/0=home")
 
# shows edited images
@app.route("/imgviewer",methods=['GET','POST'])   
def imgViewer():
    if 'user' in session:
        imgEdits=Edituploads.query.filter_by(custId=session['user']).order_by(Edituploads.date.desc()).all()
        return render_template("imageviewer.html",imgEdits=imgEdits)
    else:
        return redirect("/login=ty/0/0=home")
  
# shows account detals          
@app.route('/account/<string:publicId>',methods=['GET','POST'])
def account(publicId):
    if 'user' in session:
        user=Customers.query.filter_by(publicId=session['user']).first()
        if user:
            return render_template('account.html',user=user)
        return render_template('page_not_found.html'), 404 
    return redirect("/login=ty/0/0=view")
  
  
#  *****************************************ADMIN****************************************
# admin tshirt modifier
@app.route("/tshirt/<string:ty>/<string:action>/<string:id>=id/<string:sid>=sid/<string:fid>=fid",methods=['GET','POST'])
def tshirtAdder(ty,action,id,sid,fid):   
    if "admin" in session:
        publicId = uuid.uuid4().hex
        if request.method=="POST" and action=="add":
            app.config['UPLOAD_FOLDER']= os.path.abspath("../"+params['tshirtUpload'])
            tshirtId=request.form.get("tshirtId")
            sid=request.form.get("sid")
            name=request.form.get("name")
            description=request.form.get("description")
            status=request.form.get("status")
            type=request.form.get("type")
            sleeve=request.form.get("sleeve")
            neck=request.form.get("neck")
            img=request.files["img"]
            price=request.form.get("price")
            colour=request.form.get("colour")
            size=request.form.get("size")
            if img:
                imgName="Id" +f'{tshirtId}'+"type"+f'{type}'+str(random.randint(1, 1000)) +img.filename
                img.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(imgName)))  
                
            if  ty=="Demo":
                if fid=="0":
                    cred=Tshirts(publicId=publicId,tshirtId=tshirtId,subId=sid,name=name,description=description,price=price,colour=colour,
                                size=size,status=status,sleeve=sleeve,neck=neck,type="Demo",img=secure_filename(imgName),date=datetime.now())
                    try:
                        db.session.add(cred)
                    except:
                        flash("some error occured. please reload the page")
                
                else:
                    tshirts=Tshirts.query.filter_by(type="Demo",tshirtId=fid).first()
                    tshirts.tshirtId=tshirtId
                    tshirts.subId=sid
                    tshirts.name=name
                    tshirts.description=description
                    tshirts.status=status
                    tshirts.sleeve=sleeve
                    tshirts.neck=neck
                    tshirts.colour=colour
                    tshirts.size=size
                    tshirts.price=price
                    tshirts.type="Demo"
                    if img:
                        tshirts.img=secure_filename(imgName)
                    
                
                db.session.commit()
                flash("Uploaded")
                return redirect("/tshirt/Demo/view/0=id/0=sid/0=fid")
                    
                    
            elif ty=="Sell":
               
                if fid=="0":
                    cred=Tshirts(publicId=publicId,tshirtId=tshirtId,subId=sid,name=name,description=description,price=price,colour=colour,
                            size=size,status=status,sleeve=sleeve,neck=neck,type=type,img=secure_filename(imgName),date=datetime.now())
                    try:
                        db.session.add(cred)
                    except:
                        flash("some error occured. please reload the page")
                else:
                    tshirts=Tshirts.query.filter_by(type="Sell",tshirtId=id,subId=fid).first()
                    tshirts.tshirtId=tshirtId
                    tshirts.subId=sid
                    tshirts.name=name
                    tshirts.description=description
                    tshirts.status=status
                    tshirts.type=type
                    tshirts.price=price
                    tshirts.colour=colour
                    tshirts.size=size
                    tshirts.sleeve=sleeve 
                    tshirts.neck=neck
                    if img:
                        tshirts.img=secure_filename(imgName)
                    
                db.session.commit()
                flash("Uploaded")
                return redirect("/tshirt/Sell/view/%s=id/0=sid/0=fid" %id)           
        elif request.method=="GET" and action=="add":
            tdata=None
            data1=Tshirts.query.filter_by(type="Demo").order_by(Tshirts.tshirtId.desc()).first()
            data2=Tshirts.query.filter_by(type="Sell",tshirtId=id).order_by(Tshirts.subId.desc()).first()
            if ty=="Demo":
                 if int(sid)==0 and int(id)>0 and int(fid)>0:
                     tshirts=Tshirts.query.filter_by(type="Demo",tshirtId=fid,subId=0).first()
                 else:
                    tshirts=Tshirts.query.filter_by(type="Demo").all()
                        
                    if data1:
                        id=int(data1.tshirtId)+1
                    else:
                        id=1 
            elif ty=="Sell":
                if int(sid)>0 and int(id)>0 and int(fid)>0:
                    tshirts=Tshirts.query.filter_by(type="Sell",tshirtId=id,subId=fid).first()
                    id=id
                    sid=fid
            
                else: 
                    tshirts=Tshirts.query.filter_by(type="Sell",tshirtId=id).all()
                    tdata=Tshirts.query.filter_by(type="Demo",tshirtId=id).first()
                    id=id
                    if data2:
                        sid=int(data2.subId)+1
                    else:
                        sid=1  
                
                
            
            return render_template("tshirt_adder.html",tshirts=tshirts,sid=int(sid),type=ty,id=int(id),fid=int(fid),tdata=tdata) 
        elif action =="view":
            data1=Tshirts.query.filter_by(type="Demo").order_by(Tshirts.tshirtId.desc()).first()
            data2=Tshirts.query.filter_by(type="Sell",tshirtId=id).order_by(Tshirts.subId.desc()).first()
            if ty=="Demo":
                tshirts=Tshirts.query.filter_by(type="Demo").all()
                if data1:
                    id=int(data1.tshirtId)+1
                else:
                    id=0    
            elif ty=="Sell":
                tshirts=Tshirts.query.filter_by(type="Sell",tshirtId=id).all()
                id=id
                if data2:
                    sid=int(data2.subId)+1
                else:
                    sid=1  
            # print(tshirts)
        elif action=="Delete":
            if ty=="Demo":
                tcheck=Tshirts.query.filter_by(type="Demo",tshirtId=id,subId=0).first()
                if tcheck:
                    tshirts=Tshirts.query.filter_by(tshirtId=id).all()
            else:
                tshirts=Tshirts.query.filter_by(type=str(ty),tshirtId=id,subId=sid).all()
            
            for key in tshirts:
                imgName=key.img
                path=os.path.join(os.path.abspath("../"+params['tshirtUpload']), secure_filename(imgName))
                os.remove(path,dir_fd=None)
                db.session.delete(key)
                db.session.commit()
            return redirect("/tshirt/%s/view/%s=id/0=sid/0=fid" %(ty,id))
            
        return render_template("tshirt_display.html",type=ty,tshirts=tshirts,id=int(id),sid=int(sid),fid=int(fid))
        
    else:
        return redirect("/")     



# admin get data for customers and orders  (api)
@app.route("/admin/get/<string:str>/<string:pid>=pid",methods=['GET','POST'])   
def admin_get_data(str,pid):
    Arr = []
    if str=="orders":
        if pid=="0":
            itemsArr=Orders.query.order_by(Orders.date.desc()).all()
           
        else:
            itemsArr=Orders.query.filter_by(publicId=pid).all()   
            
            if request.method=="Post":
                if orders.deliverd==True:
                    return redirect("/generate/invoice/%s/%s")%(0,orders.publicId)
    elif str=="customers":
        if pid=="0":
            itemsArr=Customers.query.order_by(Customers.id.desc()).all()
        else:
            itemsArr=Customers.query.filter_by(publicId=pid).all()   
            
    for item in itemsArr:
        
        Arr.append(item.toDict()) 
       
    return jsonify(Arr)

# admin shows products
@app.route("/admin/products",methods=['GET','POST'])   
def admin_products():
    return render_template("admin_products.html")
 
# admin shows order   
@app.route("/admin/orders",methods=['GET','POST'])   
def admin_orders():
    return render_template("admin_orders.html")

# admin shows order   
@app.route("/admin/customers",methods=['GET','POST'])   
def admin_customers():
    cust=Customers.query.all()
    return render_template("admin_customers.html",customers=cust)

# get excel sheets for data (api)
@app.route("/admin/export/<string:exportType>/<string:exportData>",methods=['GET','POST'])   
def admin_get_excel(exportType,exportData):
    if "admin" in session:
        if exportType=="excel":
            if exportData=="customers":
                query = db.session.query(Customers)
            elif exportData=="orders":
                query = db.session.query(Orders)
            elif exportData=="templates":
                query = db.session.query(Templates)
            elif exportData=="tshirts":
                query = db.session.query(Tshirts)
            try:
                df = pd.read_sql(query.statement, query.session.bind)
                df.to_excel(exportData.capitalize()+'_Date_'+str( datetime.date(datetime.now()))+'.xlsx', index=False)
                return send_file(exportData.capitalize()+'_Date_'+str(datetime.date(datetime.now()))+'.xlsx')
            except:
                pass
    return render_template('page_not_found.html'), 404


# admin home page
@app.route("/admin",methods=['GET','POST'])
def admin():
    if 'admin' in session:
        data=Admin.query.filter_by(email=session['admin']).first()
        return render_template("admin.html",data=data)
    else:
        return redirect("/adminLogin")

# admin login   
@app.route("/adminLogin",methods=['GET','POST'])   
def adminLogin():
    if request.method=="POST":
        name=request.form.get("name")
        username=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password")
        data=Admin.query.filter_by(email=email).first()
        if data and data.password==password:
            session['admin']=data.email
            return redirect("/")
    return render_template("adminLogin.html")
  

# admin modifies questios for templates
@app.route("/queAdder/<string:type>/<string:postId>=p/<string:id>=v/<string:modifier>=m", methods=['GET','POST'])
def queAdd(type,id,postId,modifier):
    Quetype1=[]
    Quetype2=[]
    item=[]
    que=[]
    post,tshirt,price=None,None,None
    postId=postId
    publicId = uuid.uuid4().hex
    if modifier=="0":
        if request.method=='POST':
            app.config['UPLOAD_FOLDER']= os.path.abspath("../"+params['samplePostImgUpload'])
            
            input1Que1=request.form.get("input1Que1")
            input1Type1=request.form.get("input1Type1")
            input1Que2=request.form.get("input1Que2")
            input1Type2=request.form.get("input1Type2")
            input1Que3=request.form.get("input1Que3")
            input1Type3=request.form.get("input1Type3")
            input1Que4=request.form.get("input1Que4")
            input1Type4=request.form.get("input1Type4")
            input1Que5=request.form.get("input1Que5")
            input1Type5=request.form.get("input1Type5")
            input1Que6=request.form.get("input1Que6")
            input1Type6=request.form.get("input1Type6")
            input1Que7=request.form.get("input1Que7")
            input1Type7=request.form.get("input1Type7")
            input1Que8=request.form.get("input1Que8")
            input1Type8=request.form.get("input1Type8")
            input1Que9=request.form.get("input1Que9")
            input1Type9=request.form.get("input1Type9")
            input1Que10=request.form.get("input1Que10")
            input1Type10=request.form.get("input1Type10")
            input2Que1=request.form.get("input2Que1")
            input2Type1=request.form.get("input2Type1")
            input2Que2=request.form.get("input2Que2")
            input2Type2=request.form.get("input2Type2")
            input2Que3=request.form.get("input2Que3")
            input2Type3=request.form.get("input2Type3")
            input2Que4=request.form.get("input2Que4")
            input2Type4=request.form.get("input2Type4")
            input2Que5=request.form.get("input2Que5")
            input2Type5=request.form.get("input2Type5")
            input2Que6=request.form.get("input2Que6")
            input2Type6=request.form.get("input2Type6")
            input2Que7=request.form.get("input2Que7")
            input2Type7=request.form.get("input2Type7")
            input2Que8=request.form.get("input2Que8")
            input2Type8=request.form.get("input2Type8")
            input2Que9=request.form.get("input2Que9")
            input2Type9=request.form.get("input2Type9")
            input2Que10=request.form.get("input2Que10")
            input2Type10=request.form.get("input2Type10")
            try:
                samplePostPhoto=request.files["samplePostPhoto"]
                if samplePostPhoto:
                    ImgName="sp"+str(postId)+samplePostPhoto.filename
                    samplePostPhoto.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Templates (publicId=publicId, postId=postId,queSet=0 ,que=secure_filename(ImgName),inputType="0",date=datetime.now()) #input type 0 for post
                    db.session.add(cred)
                    db.session.commit()
                    type="main"
            except :
                flash("some error oocured")
                
            try:
                app.config['UPLOAD_FOLDER']= os.path.abspath("../"+params['samplePostTshirtUpload'])
                samplePostTshirt=request.files["samplePostTshirt"]
                if samplePostTshirt:
                    ImgName="st"+str(postId)+samplePostTshirt.filename
                    samplePostTshirt.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Templates(publicId=publicId,postId=postId,queSet=0 ,que=secure_filename(ImgName),inputType="1",date=datetime.now()) #input type 1 for tshirt
                    db.session.add(cred)
                    db.session.commit()
                    type="main"
            except :
                flash("some error oocured")
            try:
                samplePostPrice=request.form.get("samplePostPrice")
                if samplePostPrice:
                    cred=Templates(publicId=publicId,postId=postId,queSet=0,que=samplePostPrice,inputType="price",date=datetime.now()) #input type price for price
                    db.session.add(cred)
                    db.session.commit()
                    type="main"
            except :
                flash("some error oocured")
            if input1Que1 and input1Type1 :
                cred=Templates(publicId=publicId,postId=postId,queSet=1 , que=input1Que1,inputType=input1Type1,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
            if input1Que2 and input1Type2 :
                cred=Templates(publicId=publicId,postId=postId,queSet=1 , que=input1Que2,inputType=input1Type2,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
            if input1Que3 and input1Type3 :
                cred=Templates(publicId=publicId,postId=postId,queSet=1 , que=input1Que3,inputType=input1Type3,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
            if input1Que4 and input1Type4 :
                cred=Templates(publicId=publicId,postId=postId,queSet=1 , que=input1Que4,inputType=input1Type4,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
            if input1Que5 and input1Type5 :
                cred=Templates(publicId=publicId,postId=postId,queSet=1 , que=input1Que5,inputType=input1Type5,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
            if input1Que6 and input1Type6 :
                cred=Templates(publicId=publicId,postId=postId,queSet=1 , que=input1Que6,inputType=input1Type6,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
            if input1Que7 and input1Type7 :
                cred=Templates(publicId=publicId,postId=postId,queSet=1 , que=input1Que7,inputType=input1Type7,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
            if input1Que8 and input1Type8 :
                cred=Templates(publicId=publicId,postId=postId,queSet=1 , que=input1Que8,inputType=input1Type8,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
            if input1Que9 and input1Type9 :
                cred=Templates(publicId=publicId,postId=postId,queSet=1 , que=input1Que9,inputType=input1Type9,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
            if input1Que10 and input1Type10 :
                cred=Templates(publicId=publicId,postId=postId,queSet=1 , que=input1Que10,inputType=input1Type10,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
            if input2Que1 and input2Type1 :
                cred=Templates(publicId=publicId,postId=postId,queSet=2 , que=input2Que1,inputType=input2Type1,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
            if input2Que2 and input2Type2 :
                cred=Templates(publicId=publicId,postId=postId,queSet=2 , que=input2Que2,inputType=input2Type2,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
            if input2Que3 and input2Type3 :
                cred=Templates(publicId=publicId,postId=postId,queSet=2 , que=input2Que3,inputType=input2Type3,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
            if input2Que4 and input2Type4 :
                cred=Templates(publicId=publicId,postId=postId,queSet=2 , que=input2Que4,inputType=input2Type4,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
            if input2Que5 and input2Type5 :
                cred=Templates(publicId=publicId,postId=postId,queSet=2 , que=input2Que5,inputType=input2Type5,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
            if input2Que6 and input2Type6 :
                cred=Templates(publicId=publicId,postId=postId,queSet=2 , que=input2Que6,inputType=input2Type6,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
            if input2Que7 and input2Type7 :
                cred=Templates(publicId=publicId,postId=postId,queSet=2 , que=input2Que7,inputType=input2Type7,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
            if input2Que8 and input2Type8 :
                cred=Templates(publicId=publicId,postId=postId,queSet=2 , que=input2Que8,inputType=input2Type8,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
            if input2Que9 and input2Type9 :
                cred=Templates(publicId=publicId,postId=postId,queSet=2 , que=input2Que9,inputType=input2Type9,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
            if input2Que10 and input2Type10 :
                cred=Templates(publicId=publicId,postId=postId,queSet=2 , que=input2Que10,inputType=input2Type10,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
    else:
        
        data=Templates.query.filter_by(postId=modifier).order_by(Templates.postId.desc()).all()
        
        
        for key in data:
            if key.inputType=="0":
                post=key.que
            elif key.inputType=="1":
                tshirt=key.que
            elif key.inputType=="price":
                price=key.que
            else:
                if id==key.queSet:
                    item={
                        "que":key.que,
                        "inputType":key.inputType
                    }
                    print(item)
                    que.append(item)
    
    if type=="display":
        
        data0=Templates.query.filter_by(queSet=0,inputType="0").order_by(Templates.postId.desc()).all()
        nextPostId=Templates.query.filter_by(queSet=0).order_by(Templates.postId.desc()).first()
  
        data1=Templates.query.filter_by(queSet=1).order_by(Templates.postId.desc()).all()
        data2=Templates.query.filter_by(queSet=2).order_by(Templates.postId.desc()).all()
        return render_template("admin_post.html",modifier=modifier,type=type,srNo=id,postId=postId,posts=data0,data1=data1,data2=data2,nextPostId=nextPostId.postId+1) 
    elif type=="delete":
        data=Templates.query.filter_by(postId=postId).order_by(Templates.postId.desc()).all()
        for key in data:
            db.session.delete(key)
            db.session.commit()
        flash("deleted post succsessfully")
        return redirect("/queAdder/display/1=p/1=v/0=m")
            
    return render_template("queAdder.html",que=que,post=post,tshirt=tshirt,price=price,modifier=modifier,type=type,srNo=id,postId=postId,postData=item)


#  ***************************************Login and logout******************************************



# login and signups       
@app.route("/<string:mainstr>=ty/<string:srNo1>/<string:srNo>=<string:action>",methods=['GET','POST'])
def login(mainstr,srNo1,srNo,action):
    if 'user' in session:
        return redirect("/")
    else:
        mobile=request.form.get("mobile")
        pswd=request.form.get("pswd")
        loggedFrom="self"
        if request.method=="POST" and mainstr=="signup":
            name=request.form.get("username")
            data=Customers.query.filter_by(mobile=mobile).first()
            if data:
                flash("Account already exists!")
            else:
                publicId = uuid.uuid4().hex
                cred=Customers(publicId=publicId,name=name,mobile=mobile,pswd=pswd,loggedFrom=loggedFrom,date=datetime.now())
                try:
                    db.session.add(cred)
                    db.session.commit()
                    mainstr="login"
                except:
                    flash("Some error occured please reload page")
        elif request.method=="POST" and mainstr=="login":
            data=Customers.query.filter_by(mobile=mobile).first()
            if data and pswd==data.pswd:
                session['user']=data.publicId
                if action=='queDisplay':
                    return redirect("/queDisplay/%s=t/%s=p"  %(srNo1 ,srNo))  
                elif action=='editor':
                    return redirect("/editor/%s=t"  %(srNo))     
                else:  
                     
                    return redirect("/")
                
            elif data and pswd!=data.pswd:
                flash("You have entered wrong password!")
            else:
                flash("Account doesn't exists!")
    return render_template("login.html", page=mainstr,action=action,srNo1=srNo1,srNo=srNo)

# logout
@app.route("/logout",methods=['GET','POST'])   
def logout():
    if 'admin' in session:
        session.pop('admin')
        flash("Admin has been logged out...")
        return redirect("/adminLogin")
    if 'user' in session:
        session.pop('user')
        flash("Your Account has been logged out...")
    return redirect('/')

#  **************************************ERRORS**********************************************

# handles error 400
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html',error=error), 404


#  ***************************************UNUSED*******************************************
# otp generator 
@app.route("/generate/otp/for=<publicId>",methods=['GET','POST'])   
def otpGen(publicId):
    if 'user' in session:
        user=Customers.query.filter_by(publicId=session['user']).first()
        digits=[i for i in range(0,10)]
        otp=""
        for i in range(6):
            index=math.floor(random.random()*10)
            otp+=str(digits[index])
        title="You recieved new otp from "+params['mainTitle']
        msg= "Your otp is <b><u>%s</u></b> please confirm your order." %(otp)
        to=user.email
        response= sendMail(title,msg,to)
        print(response)
        return {"otp": otp,
           "response":response["status-code"]
        }
    
# send email for otp    
@app.route("/send/title=<string:title>&msg=<string:msg>&to=<string:to>",methods=['GET','POST'])
def sendMail(title,msg,to):
    app.config.update(
    MAIL_SERVER ='smtp.gmail.com',
    MAIL_PORT ='587',
    MAIL_USE_TLS= True,
    MAIL_USERNAME=params['gmail_user'],
    MAIL_PASSWORD=params['gmail_pswd']
    )
    mail=Mail(app)
    try:
        mail.send_message(
        title,
        sender=params['gmail_user'],
        recipients=[to],
        body=msg,
        html=msg)
        return {
            "status":"success",
            "status-code":200,
            "msg":"sent successfully"
        }
    except:
        return {
            "status":"failed",
            "status-code":400,
            "msg":"not sent! give another shot..."
        }

# generate invoice
@app.route('/generate/invoice/<string:publicId>/<string:orderId>',methods=['GET','POST'])
def genInvoice(publicId,orderId):
    if 'user' in session:
        app.config['UPLOAD_FOLDER']= os.path.abspath("../"+directories['invoices'])
        data=Customers.query.filter_by(publicId=session['user']).first()
        order=Orders.query.filter_by(publicId=orderId).first()
        if order.invoice:
            path=os.path.join(os.path.join(app.config['UPLOAD_FOLDER']), secure_filename(order.invoice))
            try:
                os.remove(path,dir_fd=None)
            except:
                pass
        invoiceId=uuid.uuid4().hex
        invoiceDate=datetime.now()
        custName=data.name
        custAddress=data.address1+", "+data.address2+", \n"+data.city+", "+data.state+", "+str(data.zip)
        custMob=data.mobile
        custEmail=data.email
        comName=params["mainTitle"]
        comPhone=params["phone"]
        comEmail=params["gmail_user"]
        comAddress=params["address"]
        orderId=order.publicId
        paymentStatus=order.paymentStatus
        paymentId=order.paymentId
        state=data.state
        shippingCompany="Dev Shippers"
        orderDate=order.date
        invoice_list = []
        def add_item():
            qty = int(order.quantity)
            desc = order.details
            size = order.size
            colour = order.colour
            price = int(order.price)/int(order.quantity)
            line_total = qty*price
            invoice_item = [qty, desc,size,colour, price, line_total]
            invoice_list.append(invoice_item)
            
        def generate_invoice():
            doc = DocxTemplate("invoice template.docx")
            subtotal = sum(item[5] for item in invoice_list) 
            if subtotal>=1000:
                gstrate = 0.12
            else:
                gstrate=0
            shippingCharges=50
            total = subtotal*(1+gstrate)+ shippingCharges
            
            doc.render({
                    "invoiceId":invoiceId,
                    "invoiceDate" :invoiceDate,
                    "custName":custName, 
                    "custAddress":custAddress,
                    "custMob":custMob ,
                    "custEmail": custEmail,
                    "comName":comName ,
                    "comPhone":comPhone ,
                    "comEmail":comEmail,
                    "comAddress":comAddress ,
                    "orderId":orderId ,
                    "paymentId": paymentId,
                    "paymentStatus":paymentStatus,
                    "state": state,
                    "shippingCompany": shippingCompany,
                    "orderDate":orderDate   ,          
                    "invoice_list": invoice_list,
                    "shippingCharges":shippingCharges,
                    "subtotal":subtotal,
                    "gst":str(subtotal*gstrate)+"("+str(gstrate*100)+"%)",
                    "total":total})
           
            doc_name =secure_filename( "INVOICE_"+str(invoiceId) + ".docx")
            doc.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(doc_name)))
            order.invoice=(secure_filename(doc_name))
            db.session.commit()
            return doc_name
        add_item()
        doc_name=generate_invoice()
        
        return {
            "code":200,
            "status":"success",
            "filename":secure_filename(doc_name)
            
        }
    return redirect("/login=ty/0/0=view")

# downloads invoice
@app.route('/download/invoice/<string:publicId>/<string:orderId>')
def downInvoice(publicId,orderId):
    if 'user' in session:
        app.config['UPLOAD_FOLDER']= os.path.abspath("../"+directories['invoices'])
        data=Customers.query.filter_by(publicId=session['user']).first()
        order=Orders.query.filter_by(publicId=orderId).first()
        if order.invoice:
            path=os.path.join(os.path.join(app.config['UPLOAD_FOLDER']), secure_filename(order.invoice))
            try:
                return send_file(path, as_attachment=True)
            except Exception as e:
                pass
            
        genInvoice(publicId,orderId)
        return redirect("/download/invoice/%s/%s"%(publicId,orderId))

@app.context_processor
def inject_user():
    data=None
    if 'user' in session:
        data=Customers.query.filter_by(publicId=session['user']).first()
    elif 'admin' in session:
        data=Admin.query.filter_by(email=session['admin']).first()
    return dict(params=params,data=data)   
if __name__=='__main__':
    app.run(debug=True,port=2000)