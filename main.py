
from ast import Pass
from optparse import Option
import time
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
import secrets
import string
import json
from sqlite3 import IntegrityError
from sqlalchemy.exc import IntegrityError 
from flask import Flask,render_template,session,redirect,request,flash,jsonify
from jinja2 import Template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import cv2
from sqlalchemy.orm import load_only
from PIL import ImageEnhance,Image,ImageFilter

with open("config.json","r") as c:
    params=json.load(c)['params']

app=Flask(__name__,template_folder="Templates")
app.secret_key='sdx2323@3343zbhcfew3rr3343@@###$2ffr454'
if (params['local_server']):
    app.config['SQLALCHEMY_DATABASE_URI']=params['local_url']
else:
    app.config['SQLALCHEMY_DATABASE_URI']=params['prod_url']

db=SQLAlchemy(app)    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
class Editorval(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    cid=db.Column(db.Integer,nullable=False)
    brightness=db.Column(db.String(5),nullable=True)
    contrast=db.Column(db.String(5),nullable=True)
    colour=db.Column(db.String(5),nullable=True)
    sharpness=db.Column(db.String(5),nullable=True)
    blur=db.Column(db.String(5),nullable=True)
    date=db.Column(db.String(12),nullable=True)
    
class Memes(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    meme=db.Column(db.String(500),nullable=False)
    date=db.Column(db.String(12),nullable=True)
class Tshirts(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    colour=db.Column(db.String(50),nullable=False)
    sleeves=db.Column(db.String(20),nullable=False)
    neck=db.Column(db.String(20),nullable=False)
    date=db.Column(db.String(12),nullable=True)
class Customers(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(30),nullable=False)
    mobile=db.Column(db.String(15),nullable=False)
    pswd=db.Column(db.String(20),nullable=False)
    address1=db.Column(db.String(200),nullable=True)
    address2=db.Column(db.String(200),nullable=True)
    city=db.Column(db.String(50),nullable=True)
    state=db.Column(db.String(75),nullable=True)
    zip=db.Column(db.Integer,nullable=True)
    date=db.Column(db.String(12),nullable=True)
class Quetypes(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    postId=db.Column(db.String(20),nullable=False)
    queType1=db.Column(db.JSON,nullable=False)
    queType2=db.Column(db.JSON,nullable=True)
    sampleImg=db.Column(db.String(50),nullable=True)
    date=db.Column(db.String(12),nullable=True)
class Questions(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    postId=db.Column(db.Integer,nullable=False)
    queSet=db.Column(db.String(5),nullable=False)
    que=db.Column(db.String(5),nullable=False)
    inputType=db.Column(db.String(20),nullable=False)
    date=db.Column(db.String(12),nullable=True)
class Answers(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    userId=db.Column(db.Integer,nullable=False)
    postId=db.Column(db.Integer,nullable=False)
    queset=db.Column(db.Integer,nullable=False)
    que=db.Column(db.Integer,nullable=False)
    answer=db.Column(db.String(200),nullable=False)
    date=db.Column(db.String(12),nullable=True)
class Admin(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    username=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(75),nullable=False)
    password=db.Column(db.String(50),nullable=False)
    secretkey=db.Column(db.String(100),nullable=False)
    date=db.Column(db.String(12),nullable=True)
    
with app.app_context():
    db.create_all()

@app.route("/admin",methods=['GET','POST'])   
def admin():
    if 'admin' in session:
        data=Admin.query.filter_by(email=session['admin']).first()
        return render_template("admin.html",data=data)
    else:
        return redirect("/adminLogin")
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
            return redirect("/admin")
            
    return render_template("adminLogin.html")
    
@app.route("/queDisplay/<string:str>=view", methods=['GET','POST'])
def queDisp(str):
    if 'user' in session :
        data=Customers.query.filter_by(id=session['user']).first()
        if data and request.method=='POST':
            app.config['UPLOAD_FOLDER']= os.path.abspath("../"+params['ImgAnswers'])
        
       
            print(data)
            userId=data.id
            postId=str
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
                cred=Answers(userId=userId,postId=postId,queset=1,que=1,answer=ans1werText1,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans1werText2:
                cred=Answers(userId=userId,postId=postId,queset=1,que=2,answer=ans1werText2,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans1werText3:
                cred=Answers(userId=userId,postId=postId,queset=1,que=3,answer=ans1werText3,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans1werText4:
                cred=Answers(userId=userId,postId=postId,queset=1,que=4,answer=ans1werText4,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans1werText5:
                cred=Answers(userId=userId,postId=postId,queset=1,que=5,answer=ans1werText5,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans1werText6:
                cred=Answers(userId=userId,postId=postId,queset=1,que=6,answer=ans1werText6,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans1werText7:
                cred=Answers(userId=userId,postId=postId,queset=1,que=7,answer=ans1werText7,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans1werText8:
                cred=Answers(userId=userId,postId=postId,queset=1,que=8,answer=ans1werText8,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans1werText9:
                cred=Answers(userId=userId,postId=postId,queset=1,que=9,answer=ans1werText9,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans1werText10:
                cred=Answers(userId=userId,postId=postId,queset=1,que=10,answer=ans1werText10,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans2werText1:
                cred=Answers(userId=userId,postId=postId,queset=2,que=1,answer=ans2werText1,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans2werText2:
                cred=Answers(userId=userId,postId=postId,queset=2,que=2,answer=ans2werText2,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans2werText3:
                cred=Answers(userId=userId,postId=postId,queset=2,que=3,answer=ans2werText3,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans2werText4:
                cred=Answers(userId=userId,postId=postId,queset=2,que=4,answer=ans2werText4,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans2werText5:
                cred=Answers(userId=userId,postId=postId,queset=2,que=5,answer=ans2werText5,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans2werText6:
                cred=Answers(userId=userId,postId=postId,queset=2,que=6,answer=ans2werText6,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans2werText7:
                cred=Answers(userId=userId,postId=postId,queset=2,que=7,answer=ans2werText7,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans2werText8:
                cred=Answers(userId=userId,postId=postId,queset=2,que=8,answer=ans2werText8,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans2werText9:
                cred=Answers(userId=userId,postId=postId,queset=2,que=9,answer=ans2werText9,date=datetime.now())
                db.session.add(cred)
                db.session.commit()

            if ans2werText10:
                cred=Answers(userId=userId,postId=postId,queset=2,que=10,answer=ans2werText10,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
                  
            # postId=str(postId)
            try:
                ans1werImg1=request.files["ans1werImg1"]
                if ans1werImg1:
                    ImgName="ans1wer1ImgPost=" +f'{postId}'+"User="+f'{userId}'+ans1werImg1.filename
                    ans1werImg1.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(userId=userId,postId=postId,queset=1,que=1,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans1werImg2=request.files["ans1werImg2"]
                if ans1werImg2:
                    ImgName="ans1wer2ImgPost=" +f'{postId}'+"User="+f'{userId}'+ans1werImg2.filename
                    ans1werImg2.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(userId=userId,postId=postId,queset=1,que=2,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans1werImg3=request.files["ans1werImg3"]
                if ans1werImg3:
                    ImgName="ans1wer3ImgPost=" +f'{postId}'+"User="+f'{userId}'+ans1werImg3.filename
                    ans1werImg3.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(userId=userId,postId=postId,queset=1,que=3,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans1werImg4=request.files["ans1werImg4"]
                if ans1werImg4:
                    ImgName="ans1wer4ImgPost=" +f'{postId}'+"User="+f'{userId}'+ans1werImg4.filename
                    ans1werImg4.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(userId=userId,postId=postId,queset=1,que=4,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans1werImg5=request.files["ans1werImg5"]
                if ans1werImg5:
                    ImgName="ans1wer5ImgPost=" +f'{postId}'+"User="+f'{userId}'+ans1werImg5.filename
                    ans1werImg5.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(userId=userId,postId=postId,queset=1,que=5,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans1werImg6=request.files["ans1werImg6"]
                if ans1werImg6:
                    ImgName="ans1wer6ImgPost=" +f'{postId}'+"User="+f'{userId}'+ans1werImg6.filename
                    ans1werImg6.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(userId=userId,postId=postId,queset=1,que=6,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans1werImg7=request.files["ans1werImg7"]
                if ans1werImg7:
                    ImgName="ans1wer7ImgPost=" +f'{postId}'+"User="+f'{userId}'+ans1werImg7.filename
                    ans1werImg7.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(userId=userId,postId=postId,queset=1,que=7,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans1werImg8=request.files["ans1werImg8"]
                if ans1werImg8:
                    ImgName="ans1wer8ImgPost=" +f'{postId}'+"User="+f'{userId}'+ans1werImg8.filename
                    ans1werImg8.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(userId=userId,postId=postId,queset=1,que=8,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans1werImg9=request.files["ans1werImg9"]
                if ans1werImg9:
                    ImgName="ans1wer9ImgPost=" +f'{postId}'+"User="+f'{userId}'+ans1werImg9.filename
                    ans1werImg9.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(userId=userId,postId=postId,queset=1,que=9,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans1werImg10=request.files["ans1werImg10"]
                if ans1werImg10:
                    ImgName="ans1wer10ImgPost=" +f'{postId}'+"User="+f'{userId}'+ans1werImg10.filename
                    ans1werImg10.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(userId=userId,postId=postId,queset=1,que=10,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans2werImg1=request.files["ans2werImg1"]
                if ans2werImg1:
                    ImgName="ans2wer1ImgPost=" +f'{postId}'+"User="+f'{userId}'+ans2werImg1.filename
                    ans2werImg1.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(userId=userId,postId=postId,queset=2,que=1,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans2werImg2=request.files["ans2werImg2"]
                if ans2werImg2:
                    ImgName="ans2wer2ImgPost=" +f'{postId}'+"User="+f'{userId}'+ans2werImg2.filename
                    ans2werImg2.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(userId=userId,postId=postId,queset=2,que=2,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans2werImg3=request.files["ans2werImg3"]
                if ans2werImg3:
                    ImgName="ans2wer3ImgPost=" +f'{postId}'+"User="+f'{userId}'+ans2werImg3.filename
                    ans2werImg3.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(userId=userId,postId=postId,queset=2,que=3,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans2werImg4=request.files["ans2werImg4"]
                if ans2werImg4:
                    ImgName="ans2wer4ImgPost=" +f'{postId}'+"User="+f'{userId}'+ans2werImg4.filename
                    ans2werImg4.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(userId=userId,postId=postId,queset=2,que=4,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans2werImg5=request.files["ans2werImg5"]
                if ans2werImg5:
                    ImgName="ans2wer5ImgPost=" +f'{postId}'+"User="+f'{userId}'+ans2werImg5.filename
                    ans2werImg5.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(userId=userId,postId=postId,queset=2,que=5,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans2werImg6=request.files["ans2werImg6"]
                if ans2werImg6:
                    ImgName="ans2wer6ImgPost=" +f'{postId}'+"User="+f'{userId}'+ans2werImg6.filename
                    ans2werImg6.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(userId=userId,postId=postId,queset=2,que=6,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans2werImg7=request.files["ans2werImg7"]
                if ans2werImg7:
                    ImgName="ans2wer7ImgPost=" +f'{postId}'+"User="+f'{userId}'+ans2werImg7.filename
                    ans2werImg7.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(userId=userId,postId=postId,queset=2,que=7,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans2werImg8=request.files["ans2werImg8"]
                if ans2werImg8:
                    ImgName="ans2wer8ImgPost=" +f'{postId}'+"User="+f'{userId}'+ans2werImg8.filename
                    ans2werImg8.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(userId=userId,postId=postId,queset=2,que=8,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans2werImg9=request.files["ans2werImg9"]
                if ans2werImg9:
                    ImgName="ans2wer9ImgPost=" +f'{postId}'+"User="+f'{userId}'+ans2werImg9.filename
                    ans2werImg9.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(userId=userId,postId=postId,queset=2,que=9,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass
            
            try:
                ans2werImg10=request.files["ans2werImg10"]
                if ans2werImg10:
                    ImgName="ans2wer10ImgPost=" +f'{postId}'+"User="+f'{userId}'+ans2werImg10.filename
                    ans2werImg10.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ImgName)))
                    cred=Answers(userId=userId,postId=postId,queset=2,que=10,answer=secure_filename(ImgName),date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
            except KeyError:
                pass  
            flash("submitted successfully....")
            data0=Questions.query.filter_by(postId=postId,queSet=0).first()
            return render_template("prodReview.html",post_name=data0.que,postId=postId)
        else:
            questionsContType0=""
            questionsContType1=[]
            questionsContType2=[]
            data0=Questions.query.filter_by(postId=str,queSet=0).first()
            data1=Questions.query.filter_by(postId=str,queSet=1).all()
            if data0:
                questionsContType0=data0
                
            if data1:
                for key in data1:
                    questionsContType1.append(key)

            data2=Questions.query.filter_by(postId=str,queSet=2).all()
            if data2:
                for key in data2:
                    questionsContType2.append(key)
                    
     
            return render_template("queDisplay.html",queCont0=questionsContType0,queCont1=questionsContType1,queCont2=questionsContType2,srNo=str)
    else:
        flash("You need to Login First..")
        return redirect("/login=ty/%s=queDisplay" %str)
app.route("/prodRev/<string:srNo>=rev", methods=['GET','POST'])
def prodRev(srNo):
    if 'user' in session:
       data=Customers.query.filter_by(id=session['user'])
        
    
    data0=Questions.query.filter_by(postId=srNo,queSet=0).first()
    return render_template("prodReview.html",post_name=data0.que)

@app.route("/queAdder/<string:type>/<string:postId>=p/<string:id>=v", methods=['GET','POST'])
def queAdd(type,id,postId):
    Quetype1=[]
    Quetype2=[]
    postId=postId
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
                cred=Questions(postId=postId,queSet=0 ,que=secure_filename(ImgName),inputType=0,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
                type="main"
        except KeyError:
            pass
        if input1Que1 and input1Type1 :
            cred=Questions(postId=postId,queSet=1 , que=input1Que1,inputType=input1Type1,date=datetime.now())
            db.session.add(cred)
            db.session.commit()
        if input1Que2 and input1Type2 :
            cred=Questions(postId=postId,queSet=1 , que=input1Que2,inputType=input1Type2,date=datetime.now())
            db.session.add(cred)
            db.session.commit()
        if input1Que3 and input1Type3 :
            cred=Questions(postId=postId,queSet=1 , que=input1Que3,inputType=input1Type3,date=datetime.now())
            db.session.add(cred)
            db.session.commit()
        if input1Que4 and input1Type4 :
            cred=Questions(postId=postId,queSet=1 , que=input1Que4,inputType=input1Type4,date=datetime.now())
            db.session.add(cred)
            db.session.commit()
        if input1Que5 and input1Type5 :
            cred=Questions(postId=postId,queSet=1 , que=input1Que5,inputType=input1Type5,date=datetime.now())
            db.session.add(cred)
            db.session.commit()
        if input1Que6 and input1Type6 :
            cred=Questions(postId=postId,queSet=1 , que=input1Que6,inputType=input1Type6,date=datetime.now())
            db.session.add(cred)
            db.session.commit()
        if input1Que7 and input1Type7 :
            cred=Questions(postId=postId,queSet=1 , que=input1Que7,inputType=input1Type7,date=datetime.now())
            db.session.add(cred)
            db.session.commit()
        if input1Que8 and input1Type8 :
            cred=Questions(postId=postId,queSet=1 , que=input1Que8,inputType=input1Type8,date=datetime.now())
            db.session.add(cred)
            db.session.commit()
        if input1Que9 and input1Type9 :
            cred=Questions(postId=postId,queSet=1 , que=input1Que9,inputType=input1Type9,date=datetime.now())
            db.session.add(cred)
            db.session.commit()
        if input1Que10 and input1Type10 :
            cred=Questions(postId=postId,queSet=1 , que=input1Que10,inputType=input1Type10,date=datetime.now())
            db.session.add(cred)
            db.session.commit()
        if input2Que1 and input2Type1 :
            cred=Questions(postId=postId,queSet=2 , que=input2Que1,inputType=input2Type1,date=datetime.now())
            db.session.add(cred)
            db.session.commit()
        if input2Que2 and input2Type2 :
            cred=Questions(postId=postId,queSet=2 , que=input2Que2,inputType=input2Type2,date=datetime.now())
            db.session.add(cred)
            db.session.commit()
        if input2Que3 and input2Type3 :
            cred=Questions(postId=postId,queSet=2 , que=input2Que3,inputType=input2Type3,date=datetime.now())
            db.session.add(cred)
            db.session.commit()
        if input2Que4 and input2Type4 :
            cred=Questions(postId=postId,queSet=2 , que=input2Que4,inputType=input2Type4,date=datetime.now())
            db.session.add(cred)
            db.session.commit()
        if input2Que5 and input2Type5 :
            cred=Questions(postId=postId,queSet=2 , que=input2Que5,inputType=input2Type5,date=datetime.now())
            db.session.add(cred)
            db.session.commit()
        if input2Que6 and input2Type6 :
            cred=Questions(postId=postId,queSet=2 , que=input2Que6,inputType=input2Type6,date=datetime.now())
            db.session.add(cred)
            db.session.commit()
        if input2Que7 and input2Type7 :
            cred=Questions(postId=postId,queSet=2 , que=input2Que7,inputType=input2Type7,date=datetime.now())
            db.session.add(cred)
            db.session.commit()
        if input2Que8 and input2Type8 :
            cred=Questions(postId=postId,queSet=2 , que=input2Que8,inputType=input2Type8,date=datetime.now())
            db.session.add(cred)
            db.session.commit()
        if input2Que9 and input2Type9 :
            cred=Questions(postId=postId,queSet=2 , que=input2Que9,inputType=input2Type9,date=datetime.now())
            db.session.add(cred)
            db.session.commit()
        if input2Que10 and input2Type10 :
            cred=Questions(postId=postId,queSet=2 , que=input2Que10,inputType=input2Type10,date=datetime.now())
            db.session.add(cred)
            db.session.commit()
        
    return render_template("queAdder.html",type=type,srNo=id,postId=postId)


@app.route("/<string:mainstr>=ty/<string:srNo>=<string:action>",methods=['GET','POST'])
def login(mainstr,srNo,action):
    if 'user' in session:
        return redirect("/")
    else:
        mobile=request.form.get("mobile")
        pswd=request.form.get("pswd")
        if request.method=="POST" and mainstr=="signup":
            username=request.form.get("username")
            data=Customers.query.filter_by(mobile=mobile).first()
            if data:
                flash("Account already exists!")
            else:
                cred=Customers(username=username,mobile=mobile,pswd=pswd,date=datetime.now())
                db.session.add(cred)
                db.session.commit()
                mainstr="login"
        elif request.method=="POST" and mainstr=="login":
            data=Customers.query.filter_by(mobile=mobile).first()
            if data and pswd==data.pswd:
                session['user']=data.id
                if action=='queDisplay':
                    return redirect("/queDisplay/%s=view" %srNo)       
                    
                return redirect("/")
                
            elif data and pswd!=data.pswd:
                flash("You have entered wrong password!")
            else:
                flash("Account doesn't exists!")
    return render_template("login.html", page=mainstr,action=action,srNo=srNo)

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
       
@app.route("/",methods=['GET','POST'])   
def home():
    # flash("testing")
    # return render_template("card2.html",params=params)
    return render_template("index.html",params=params)

@app.route("/memeType",methods=['GET','POST'])   
def memeType():
    data0=Questions.query.filter_by(queSet=0).order_by(Questions.postId.asc()).all()
    # return render_template("card2.html",params=params)
    return render_template("card2.html",params=params,data0=data0)

@app.route("/customize/<string:types>=ty",methods=['GET','POST'])
def customize(types):
    
    return render_template("html.html",types=types)


@app.route("/customize/<string:types>=ty/<string:subTypes>=sbty")
def subcustomize(types,subTypes):
    return render_template("subcustomize.html",types=types,subTypes=subTypes)

@app.route("/uploader/<string:val>=val",methods=['GET','POST'])
def uploads(val):
    
    return render_template("tp.html")

@app.route("/payments",methods=['GET','POST'])
def payments():
    if 'user' in session:
        return render_template("payments.html")
    else:
        return redirect("/login=ty/0=view")
@app.route("/address=confirm",methods=['GET','POST'])
def address():
    if 'user' in session:
        data=Customers.query.filter_by(id=session['user']).first()
        if request.method=="POST" and data:
            name=request.form.get("name")
            mobile=request.form.get("mobile")
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
            db.session.commit()
            return redirect("/payments")
    
        return render_template("address.html", data=data)
    else:
        return redirect("/login=ty/0=view")
        

@app.route("/editor",methods=['GET','POST'])
def edits():
    return render_template("mainEditor.html")



@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html',error=error), 404



@app.route('/slide')
def slide():
    return render_template('slide.html')
@app.route('/getStarted')
def getStarted():
    return render_template('document.html')
@app.route("/cards")
def cards():
    return render_template("cards.html")
@app.route('/feedbackhome')
def feedbackhome():
    return render_template('feedbackhome.html')
@app.route('/footer')
def footer():
    return render_template('footer.html')
@app.context_processor
def inject_user():
    data=None
    if 'user' in session:
        data=Customers.query.filter_by(id=session['user']).first()
    return dict(params=params,data=data)   
if __name__=='__main__':
    app.run(debug=True,port=2000)