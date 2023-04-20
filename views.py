

import io


import pandas as pd


from PIL import Image

import os

from werkzeug.utils import secure_filename
import random
import math



import json
from sqlite3 import IntegrityError
from sqlalchemy.exc import IntegrityError 
from flask import Flask, make_response,render_template,abort,session,redirect,send_file, request,flash,jsonify,Response,url_for
from jinja2 import Template
from datetime import datetime
from sqlalchemy import func, text
import uuid
from flask_mail import Mail

from PIL import Image

from docxtpl import DocxTemplate
import re


import requests
import xml.etree.ElementTree as ET


from string import Template

# google login

import pathlib
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests


from .__init__ import app,db
from .payments.ccavutil import encrypt,decrypt
from .payments.ccavResponseHandler import res
from .models import *

with open("/var/www/MemerKida/MemerKida/config.json","r") as c:
    params=json.load(c)['params']
with open("/var/www/MemerKida/MemerKida/config.json","r") as d:
    directories=json.load(d)['directories']
with open("/var/www/MemerKida/MemerKida/config.json","r") as e:
    ecxp=json.load(e)['EcomExpress']
with open("/var/www/MemerKida/MemerKida/config.json","r") as p:
    paygate=json.load(p)['paymentGateway']

# ****************************************google Login*****************************************    
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "423572210681-ig2sv7oikb9e03b4flq4k553d5ftj9bk.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://memerkida.com/callback"
)
def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()
    return wrapper

@app.route("/login/auth/google")
def login_google():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    # try:
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    # print(credentials)
    # return credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)

    token_request = google.auth.transport.requests.Request(session=cached_session)


    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    sub= id_info.get("sub")
    name = id_info.get("name")
    email = id_info.get("email")
    mobile = id_info.get("mobile")
    loggedFrom="google"
    pswd=sub
    # return id_info
    data=Customers.query.filter_by(email=email).first()
    if data is None:
        publicId = uuid.uuid4().hex
        cred=Customers(publicId=publicId,name=name,mobile=mobile,email=email,pswd=pswd,loggedFrom=loggedFrom,date=datetime.now())
        try:
            db.session.add(cred)
            db.session.commit()
            mainstr="login"
            session["user"]=publicId
            return redirect("/google/auth") 
        except:
            flash("Some error occured please reload page")
            return redirect("/login/auth")
   
    
    session["user"]=data.publicId
    
        
    # flash("Account already exists")
    return redirect("/login/auth")
    # except:
        
    #     return redirect("/login/auth")





#  ***************************************Login and logout******************************************

# login and signups       
@app.route("/<string:mainstr>/auth",methods=['GET','POST'])
def login(mainstr):
    
    if 'user' in session:
        mobile=request.form.get("mobile")
        pswd=request.form.get("pswd")

        if mainstr=="google":
            
            user=Customers.query.filter_by(publicId=session['user']).first()
        if "redirect_to" in session:
            return redirect(session["redirect_to"]) 
         
        return redirect("/")
    elif mainstr=="whatsapp":
        mobile=request.form.get("mobile")
        pswd=request.form.get("pswd")
        name=request.form.get("name")
        user=Customers.query.filter_by(mobile=mobile).first()
        loggedFrom="whatsapp"
        print("whatsapp")
        if user:
            session['user']=user.publicId
            return {
                    "code":200,
                    "msg":"You logged in as %s" %name,
                    "redirect_url":"/login/auth"
                }
        else:
            publicId = uuid.uuid4().hex
            cred=Customers(publicId=publicId,name=name,mobile=mobile,pswd=pswd,loggedFrom=loggedFrom,date=datetime.now())
            try:
                db.session.add(cred)
                db.session.commit()
                session['user']=publicId
                return {
                    "code":200,
                    "msg":"You logged in as %s" %name,
                    "redirect_url":"/login/auth"
                }
            except:
                flash("Some error occured please reload page")
            
            
    
        
            
        # user=Customers.query.filter_by(publicId=session['user']).first()
        if "redirect_to" in session:
            return redirect(session["redirect_to"]) 
         
        return redirect("/")
            
          
    else:
        mobile=request.form.get("mobile")
        pswd=request.form.get("pswd")
        loggedFrom="self"
        if request.method=="POST" and mainstr=="signup":
            name=request.form.get("username")
            email=request.form.get("email")
            user=Customers.query.filter_by(mobile=mobile).first()
            if user:
                flash("Account already exists!")
            else:
                publicId = uuid.uuid4().hex
                cred=Customers(publicId=publicId,name=name,mobile=mobile,email=email,pswd=pswd,loggedFrom=loggedFrom,date=datetime.now())
                try:
                    db.session.add(cred)
                    db.session.commit()
                    mainstr="login"
                    session['user']=publicId
                    if "redirect_to" in session:
                        return redirect(session["redirect_to"])
                    else:  
                        
                        return redirect("/")
                except:
                    flash("Some error occured please reload page")
        elif request.method=="POST" and mainstr=="login":
            user=Customers.query.filter((Customers.mobile == mobile) | (Customers.email == mobile)).first()
            if user and pswd==user.pswd:
                session['user']=user.publicId
                if "redirect_to" in session:
                    return redirect(session["redirect_to"])
                else:  
                     
                    return redirect("/")
                
            elif user and pswd!=user.pswd:
                flash("You have entered wrong password!")
            else:
                flash("Account doesn't exists!")
    
    return render_template("login2.html", page=mainstr)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")




    
    
    
    
    
    
#  *********************************CUSTOMERS***************************************************


#home page
@app.route("/",methods=['GET'])   
def home():
    # for key in directories:
    #     print(directories.get(key))
    session.permanent = True 
    carousel=Templates.query.filter_by(carousel=True).all()
    if 'admin' in session:
        return render_template("admin_home.html")
    orders=Orders.query.order_by(Orders.id.desc()).all()
    return render_template("index.html",params=params,orders=orders,carousel=carousel)

#get template categories (api)
@app.route("/get/templates/categories")
def getCategory():
    temp2=[]
    cat=[]
    t=Templates.query.order_by(Templates.price).all()
    for k in t:
        cat.append(k.category)
    for key in set(cat):
        temp=Templates.query.filter_by(category=key).first()
        temp2.append(temp.toDict())
        
    return jsonify(temp2)

# get started
@app.route('/about')
def about():
    return render_template('about.html')

# get started
@app.route('/getStarted')
def getStarted():
    return render_template('getStarted.html')


#choose cutomize by and displays tshirts
@app.route("/customize/<string:types>=ty/<string:category>=<string:seperator>",methods=['GET'])
def customize(types,category,seperator):
    load=None
    if types=="default":
        load="templates"
    elif types=="cust":
        load="editor"
    tshirts=Tshirts.query.filter_by(type="Demo",status="Active").all()
    
    return render_template("customize_type.html",seperator=seperator,types=types,tshirts=tshirts,load=load,category=category)
 
 
 
#  ************************************************************************************
#1) customize by memerkida
# shows templates 
@app.route("/templates/<string:tshirtId>=t//<string:category>=cat",methods=['GET'])   
def templates(tshirtId,category):
    # print(category)
    if category=="all" or category=="All":
        templates=Templates.query.order_by(Templates.id.desc()).all()
    else:
        templates=Templates.query.order_by(Templates.id.desc()).filter_by(category=category).all()
    return render_template("templates.html",params=params,tshirtId=tshirtId,templates=templates)



#  ************************************************************************************
# 2) customize by yourself
# opens editor
@app.route("/editor/<string:tshirtId>=t/<string:category>=cat",methods=['GET'])
def edits(tshirtId,category):
    tshirt=Tshirts.query.filter_by(publicId=tshirtId).first()
    if 'user' in session:
        
        return render_template("edit123.html",tshirt=tshirt)
    else:
        flash("You need to Login First..")
        session["redirect_to"]="/editor/%s=t/%s=cat" %(tshirtId,category)
        return redirect("/login/auth")
    
   
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
                app.config['UPLOAD_FOLDER']= os.path.abspath(params['base_url']+params['editImagesUpload'])
                printImg = Image.open(printImg.stream)
                printImgName="cust"+str(data.publicId)+"No"+str(len(uploads))+"Images.png" 
                printImg.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(printImgName) ))   
                printImg=secure_filename(printImgName) 
                app.config['UPLOAD_FOLDER']= os.path.abspath(params['base_url']+params['editTshirtUpload'])
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


# order
@app.route("/<string:tshirtId>=t/<string:printId>=p/<string:type>/<string:source>/order",methods=['GET','POST'])   
def orderNow(tshirtId,printId,type,source):
    if 'user' in session:
        data=Customers.query.filter_by(publicId=session['user']).first()
        if request.method=="POST":
            tshirtImg=0
            printImg=0 
            theme=0
            
            paymentId=0
            quantity=request.form.get("quantity")
            colour= request.form.get("colour")
            theme= request.form.get("theme")
            size=request.form.get("size")
            price=request.form.get("price")
            details=request.form.get("details")
            
            if source=="noCart":
                if type=="default":
                    tshirt=Tshirts.query.filter_by(publicId=tshirtId,type="Demo",status="Active").first()
                    if tshirt:
                        tshirtImg=tshirt.img
                    template=Templates.query.filter_by(publicId=printId).first()
                    if theme=="dark":
                        printImg=template.darkTemplate
                    elif theme=="light":
                        printImg=template.lightTemplate
                   
                    price=int(quantity)* int( template.price)
                    # print(price)
                    
                       
                    
                elif type =="customize":
                    uploads=Edituploads.query.filter_by(custId=session['user'],publicId=printId).first()
                    if uploads:
                        tshirtImg=uploads.tshirtImg
                        printImg=uploads.printImg
            elif source=="cart":
                cartId=tshirtId
                # print(cartId)
                cart=Carts.query.filter_by(custId=data.publicId,publicId=cartId).first()
                
                if cart is None:
                    return render_template('page_not_found.html'), 404
                    
                tshirtId=cart.tshirtId
              
                if type=="default":
                    tshirt=Tshirts.query.filter_by(publicId=cart.tshirtId,type="Demo",status="Active").first()  
                    if tshirt:
                        tshirtImg=tshirt.img
                    template=Templates.query.filter_by(publicId=printId).first()
                    if cart.theme=="dark":
                        printImg=template.darkTemplate
                    elif cart.theme=="light":
                        printImg=template.lightTemplate
                   
                elif type=="customize":
                    uploads=Edituploads.query.filter_by(custId=data.publicId,publicId=cart.printId).first()
                   
                    if uploads:
                        tshirtImg=uploads.tshirtImg
                        printImg=uploads.printImg
                    
                size=cart.size
                price=cart.price
                colour=cart.colour
                quantity=cart.quantity
                price=cart.price
                type=cart.type
                theme=cart.theme
            publicId = uuid.uuid4()
            status="Pls Complete Order"
            order=Orders.query.filter_by(custId=data.publicId,status=status,quantity=quantity,colour=colour,size=size,tshirtImg=tshirtImg,type=type,theme=theme,printImg=printImg,price=price,delivered=False).first()
            if order:
                print(order)
                flash("This Order has been already placed..")
                orderId=order.publicId
                source="cart"
                
                
                # return redirect("/%s/payments" %(orderId))
            else:
                cred=Orders(publicId=publicId,custId=data.publicId,status=status,quantity=quantity,colour=colour,size=size,tshirtImg=tshirtImg,type=type,theme=theme,printImg=printImg,details=details,price=price,delivered=False,date=datetime.now())
                # try:
                db.session.add(cred)
                
                flash("Pls confirm your order by providing details..")
                orderId=publicId
                db.session.commit()   
                try:
                    addtoCart("remove",data.publicId,cartId)
                except:
                    pass
                  
                return redirect("/%s/address" %(orderId))
                # except IntegrityError:
                #     flash("Some error occured. Please reload page and try again..")
            return redirect("/%s=t/%s=p/%s/%s/order" %(tshirtId,printId,type,source))
        if source=="noCart":
            theme=""  
            cartId=0
            quantity=1
            dark_post_name=None
           
            if type=="default":
                template=Templates.query.filter_by(publicId=printId).first()
                
                post=template.lightTemplate
            
                post_name=template.lightTshirt
                dark_post_name=template.darkTshirt
            
                price=template.price
            
                tshirt=Tshirts.query.filter_by(publicId=tshirtId).first()
                
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
            # try:
            #     cart=Carts.query.filter_by(custId=data.publicId ,tshirtId=tshirtId ,printId=printId,type=type).first()  
            # except: 
            cart=Carts.query.filter_by(custId=data.publicId ,publicId=tshirtId).first()  
            if cart is None:
                return redirect("/error")
                
        
            tshirt=Tshirts.query.filter_by(publicId=cart.tshirtId,type="Demo",status="Active").first()   
            dark_post_name=None
            if type=="default":
                if tshirt:
                    tshirtImg=tshirt.img
                    
                template=Templates.query.filter_by(publicId=printId).first()
                if cart.theme=="dark":
                    printImg=template.darkTemplate
                    post=template.darkTemplate
                    post_name=template.darkTshirt
                elif cart.theme=="light":
                    printImg=template.lightTemplate
                    post=template.lightTemplate
                    post_name=template.lightTshirt
                price=template.price
                
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
            theme=cart.theme
           
    
        return render_template("orderNow.html",dark_post_name=dark_post_name,theme=theme,neck=neck,sleeve=sleeve,
                               cartId=cartId,colour=colour,size=size, quantity=quantity, price=price,tshirtId=tshirtId,
                               post_name=post_name,printId=printId,type=type,source=source,title=title,description=description)
        
    else:
        session["redirect_to"]="/%s=t/%s=p/default/noCart/order" %(tshirtId,printId)
     
        return redirect("/login/auth")


# similar post (api)
@app.route("/get/<string:id>/<string:types>/similar",methods=['GET'])
def similar_post(id,types):
    if 'user' in session:
        similar_templates=[]
        data=Customers.query.filter_by(publicId=session['user']).first()
        try:
            if types=="default":
                # if source=="cart":
                #     cart=Carts.query.filter_by(publicId=id).first()
                #     id=cart.printId   
                template=Templates.query.filter_by(publicId=id).first()
                category=template.category
                keywords=template.keywords.capitalize().split(" ")
                        
            else:
                category="Marathi"
                keywords=["couple","anime","avenger","game","marathi","fashion","chai","sigma"]
            
            similar= Templates.query.filter_by(category=category).all()
            for key in keywords:
                similar+= Templates.query.filter(Templates.keywords.contains(key)).all()
            
            for key in set(similar): 
                similar_templates.append(key.toDict())
        except:
            return   {"code":404,
                    "total":len(similar_templates),
                    "response":similar_templates
                    }
              
        return{
            "code":200,
            "total":len(similar_templates),
             "response":similar_templates
        }
                     
    return{
        "code":404,
        "total":0,
             "response":[]
    }
 

# modifies address
@app.route("/<string:orderId>/address",methods=['GET','POST'])
def address(orderId):
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
            checkMob=Customers.query.filter_by(mobile=mobile).first()
            
            # if checkMob:
            #     flash("Mobile Number already exists pls try with another number")
            #     return redirect("/%s/address" %orderId)
            try:
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
            except:
                flash("Mobile Number already exists pls try with another number")
                return redirect("/%s/address" %orderId)
                
            return redirect("/%s/checkout" %(orderId))
        # flash("Pls confirm your order by providing details..")
        indian_states = [    "Andhra Pradesh",    "Arunachal Pradesh",    "Assam",    "Bihar",    "Chhattisgarh",    "Goa",    "Gujarat",    "Haryana",    "Himachal Pradesh",    "Jharkhand",    "Karnataka",    "Kerala",    "Madhya Pradesh",    "Maharashtra",    "Manipur",    "Meghalaya",    "Mizoram",    "Nagaland",    "Odisha",    "Punjab",    "Rajasthan",    "Sikkim",    "Tamil Nadu",    "Telangana",    "Tripura",    "Uttar Pradesh",    "Uttarakhand",    "West Bengal",    "Andaman and Nicobar Islands",    "Chandigarh",    "Dadra and Nagar Haveli and Daman and Diu",    "Lakshadweep",    "Delhi",    "Puducherry",    "Jammu and Kashmir",    "Ladakh"]
        return render_template("address.html",orderId=orderId,indian_states=indian_states)
    else:
        session["redirect_to"]="%s/address" %orderId
                  
        return redirect("/login/auth")

# checkout
@app.route("/<string:orderId>/checkout",methods=['GET','POST'])
def checkout(orderId):
    if 'user' in session:
        
        data=Customers.query.filter_by(publicId=session['user']).first()
        order=Orders.query.filter_by(custId=data.publicId,publicId=orderId).first()
        print(order.printImg)
        if order.type=="default":
            
            template=Templates.query.filter_by(lightTemplate=order.printImg).first()
        
        check={}
        if order and data:
            check["name"]=data.name
            check["mobile"]=data.mobile
            check["email"]=data.email
            check["address1"]=data.address1
            check["address2"]=data.address2
            check["city"]=data.city
            check["state"]=data.state
            check["zip"]=data.zip
            check["printImg"]=template.lightTemplate if order.type=="default" else order.printImg
            check["tshirtImg"]=template.lightTshirt if order.type=="default" else order.tshirtImg 
            check["order"]=order
            # check["payMethods"]="cod"
            check["subtotal"]=order.price
            check["shipping"]=0 # 25 if str(check["state"]).lower()=="maharashtra" else 40
            check["cod"]=0  #25  if check["payMethods"]=="cod"  else 0
            check["total"]=int(check["shipping"])+int(check["subtotal"])+ int(check["cod"])

        if request.method=="POST" and data and order:
            name=check["name"]
            mobile=check["mobile"]
            address1=check["address1"]
            address2=check["address2"]
            city=check["city"]
            state=check["state"]
            zip=check["zip"]
            subtotal=check["subtotal"]
            charges=int(check["shipping"])+ int(check["cod"])
            total=int(check["shipping"])+int(check["subtotal"])+ int(check["cod"])
            payMethods=request.form.get("payMethods") 
            orderId=order.publicId
            custId=data.publicId
            publicId = uuid.uuid4()
            status="pending"
            payment=Payments.query.filter_by(orderId=orderId).first()
            if payment is None:
                try:
                    cred=Payments(publicId=publicId,custId=custId,orderId=orderId,payMethods=payMethods,status=status,subtotal=subtotal,charges=charges,total=total,name=name,mobile=mobile,address1=address1,address2=address2,city=city,state=state,zip=zip,date=datetime.now())
                    db.session.add(cred)
                    order=Orders.query.filter_by(publicId=orderId).first()
                    order.paymentId=publicId
                    order.status="Order Received and will be Dispatched soon"
                    db.session.commit()
                    if payMethods=="online":
                        return redirect("/ccavRequestHandler/%s" %(orderId))
                    flash("Your order is successfully placed..")
                    title="You recieved Order on "+params['mainTitle']
                    msg= "Your received new order kindly check it.." 
                    to="22devendrabijwe@gmail.com", "vitthaltangade6@gmail.com"
                    try:
                        sendMail(title,msg,to)
                    except:
                        pass
                    return redirect("/order/%s/success"%(orderId))
                except:
                    flash("order already placed")
                
            elif  payment.payMethods=="online" and payment.transactionId is None :
                if payMethods=="online":
                    return redirect("/ccavRequestHandler/%s" %(orderId))
                else:
                    flash("Do not change payment methods")
                    
                
            else:
                flash("This order is already in Queue")
                
         
        return render_template("checkout.html",check=check)
    else:
        session["redirect_to"]="%s/checkout" %orderId
                  
        return redirect("/login/auth")

@app.route('/order/<string:orderId>/success',methods=['GET','POST'])
def order_success(orderId):
    
    data=None
    try:
        if 'user' in session:
            user=Customers.query.filter_by(publicId=session['user']).first()

            if request.method=="POST":
                # accessCode = paygate['access_code']
                # workingKey = paygate['working_key']
                # plainText = res(request.form['encResp'],workingKey)
                # order_id=plainText["order_id"]
                # name=plainText["billing_ name"]
                # tracking_id=plainText["tracking_id"]
                # bank_ref_no=plainText["bank_ref_no"]
                # order_status=plainText["order_status"]
                # failure_message=plainText["failure_message"]
                # payment_mode=plainText["payment_mode"]
                # order_id=plainText["order_id"]
                # amount=plainText["amount"]
                # currency=plainText["currency"]
                # custId=session["user"]
                # publicId = uuid.uuid4().hex
                # trans=Transaction.query.filter_by(custId=session["user"],orderId=order_id).first()
                # if trans is None or  (trans.order_status).lower() is not "success":
                #     cred=Transaction(publicId=publicId,custId=custId,orderId=order_id,name=name,tracking_id=tracking_id,bank_ref_no=bank_ref_no,amount=amount,order_status=order_status,currency=currency,payment_mode=payment_mode,failure_message=failure_message,date=datetime.now())
                #     db.session.add(cred)
                #     db.session.commit()
                # return plainText
                pass
            ord=Orders.query.filter_by(custId=user.publicId,publicId=orderId).first()
            if ord:
                pay=Payments.query.filter_by(orderId=ord.publicId).first()
                if user and ord and pay:
                    if pay.payMethods=="online":
                        payMethods="You already paid Online."
                    else:
                        payMethods="Cash on Delivery"
                
                    data={
                        "name" :user.name,
                        "orderId":ord.publicId,
                        "address":pay.address1+", "+pay.address2+ ", "+pay.city+ ", "+pay.state+ ", "+str(pay.zip)+".",
                        "payMethods":payMethods
                    }
        else: 
            data={
                    "name" :"",
                    "orderId":"",
                    "address":"",
                    "payMethods":""
                }
    except:
        data={
                "name" :"",
                "orderId":"",
                "address":"",
                "payMethods":""
            }
    return render_template("order_success.html" ,ordData=data)
    
        


# get address of customer (api)
@app.route('/order/get/address',methods=['GET'])
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


# track item (api)
@app.route("/get/tracking/<string:orderId>")
def tracking(orderId):
    Arr = {"code":400}
    if "user" in session:
        
        order=Orders.query.filter_by(custId=session["user"],publicId=orderId).first()
        if order:
            url="https://plapi.ecomexpress.in/track_me/api/mawbd/?username=%s&password=%s&awb=%s" %(ecxp["username"],ecxp["password"],order.trackingId)
            
            response = requests.get(url = url)
            try:
        
                xml_data = response.content
            

                root = ET.fromstring(xml_data)
                Arr["code"]=200
            
                
                for key in root[0]:
                    
                    if key.findall("[@name='expected_date']"):
                        Arr["expected_date"]=key.text
                    if key.findall("[@name='status']"):
                        Arr["status"]=key.text
                    if key.findall("[@name='awb_number']"):
                        Arr["awb_number"]=key.text
                    if key.findall("[@name='scans']"):
                        Arr2=[]
                        
                        for key2 in key:
                            for key3 in key2:
                                if key3.findall("[@name='updated_on']"):
                                    updated_on=key3.text
                                if key3.findall("[@name='status']"):
                                    status=key3.text
                                if key3.findall("[@name='reason_code']"):
                                    reason_code=key3.text
                                if key3.findall("[@name='updated_on']"):
                                    updated_on=key3.text
                                if key3.findall("[@name='scan_status']"):
                                    scan_status=key3.text
                                if key3.findall("[@name='location']"):
                                    location=key3.text
                                if key3.findall("[@name='location_city']"):
                                    location_city=key3.text
                                if key3.findall("[@name='city_name']"):
                                    city_name=key3.text
                                if key3.findall("[@name='location_type']"):
                                    location_type=key3.text
                                if key3.findall("[@name='Employee']"):
                                    Employee=key3.text
                                if key3.findall("[@name='reason_code_number']"):
                                    reason_code_number=key3.text
                            Arr2.append({"updated_on":updated_on,"reason_code_number":reason_code_number,"Employee":Employee,"location_type":location_type,
                                    "scan_status":scan_status,"city_name":city_name,"location":location,"status":status,
                                    "location_city":location_city,"reason_code":reason_code})
                        
                        Arr["tracking"]=Arr2
            except :
                pass
        else:
             Arr["code"]=400
    return Arr
    
    
#*********************************************Payment Gateways****************************************************************************    
    






@app.route('/ccavResponseHandler/', methods=['GET', 'POST'])
def ccavResponseHandler():
    
    accessCode = paygate['access_code']
    workingKey = paygate['working_key']
    plainText = res(request.form['encResp'],workingKey)
    order_id=plainText["order_id"]
    name=plainText["billing_ name"]
    tracking_id=plainText["tracking_id"]
    bank_ref_no=plainText["bank_ref_no"]
    order_status=plainText["order_status"]
    failure_message=plainText["failure_message"]
    payment_mode=plainText["payment_mode"]
    order_id=plainText["order_id"]
    amount=plainText["amount"]
    currency=plainText["currency"]
    
    
    return plainText

@app.route('/ccavRequestHandler/<string:orderId>', methods=['GET', 'POST'])
def handlePayReq(orderId):
    
    accessCode = paygate['access_code']
    workingKey = paygate['working_key']
    if "user" in session:
        data=Customers.query.filter_by(publicId=session["user"]).first()
        ord=Orders.query.filter_by(custId=data.publicId,publicId=orderId).first()
        pay=Payments.query.filter_by(orderId=ord.publicId).first()
        if pay.transactionId :
            flash("alraedy done payment")
            return redirect("%s/checkout"%(orderId))
        p_merchant_id = paygate['merchant_id']
        p_order_id = ord.publicId
        p_currency = paygate['currency']
        p_amount = str(pay.total)
        p_redirect_url = paygate['base_url']+"/order/%s/success"%(orderId)
        p_cancel_url = paygate['cancel_url']+"/%s/checkout" %(orderId)
        p_language = paygate['language']
        p_billing_name = data.name
        p_billing_address =data.address1+" "+data.address2
        p_billing_city = data.city
        p_billing_state = data.state
        p_billing_zip = str(data.zip)
        p_billing_country = "India"
        p_billing_tel = str(data.mobile)
        P_billing_email=data.email
        p_merchant_param1 ="7666230646"
        p_merchant_param2 = "22devendrabijwe@gmail.com"
        p_merchant_param3 = "9370899965"
        
        p_customer_identifier = data.publicId
        # print("merchant",p_merchant_id,accessCode,workingKey)
        

        merchant_data='merchant_id='+p_merchant_id+'&'+'order_id='+p_order_id + '&' + "currency=" + p_currency + '&' + 'amount=' + p_amount+'&'+'redirect_url='+p_redirect_url+'&'+'cancel_url='+p_cancel_url+'&'+'language='+p_language+'&'+'billing_name='+p_billing_name+'&'+'billing_address='+p_billing_address+'&'+'billing_city='+p_billing_city+'&'+'billing_state='+p_billing_state+'&'+'billing_zip='+p_billing_zip+'&'+'billing_country='+p_billing_country+'&'+'billing_tel='+p_billing_tel+'&'+'billing_email'+P_billing_email+'&'+'merchant_param1='+p_merchant_param1+'&'+'merchant_param2='+p_merchant_param2+'&'+'merchant_param3='+p_merchant_param3+'&'+'customer_identifier='+p_customer_identifier+'&'
        print(merchant_data)
             
        encryption = encrypt(merchant_data,workingKey)

        html = '''\
    <html>
    <head>
        <title>Sub-merchant checkout page</title>
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
    </head>
    <body>
    <form id="nonseamless" method="post" name="redirect" action="https://secure.ccavenue.com/transaction/transaction.do?command=initiateTransaction" > 
            <input type="hidden" id="encRequest" name="encRequest" value=$encReq>
            <input type="hidden" name="access_code" id="access_code" value=$xscode>
            <script language='javascript'>document.redirect.submit();</script>
    </form>    
    </body>
    </html>
    '''
        fin = Template(html).safe_substitute(encReq=encryption,xscode=accessCode)
                
        return fin	


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
                template=Templates.query.filter_by(publicId=key.printId).first()
                
                if key.theme=="dark":
                    printImg=template.darkTemplate
                    tshirtImg=template.darkTshirt
                elif key.theme=="light":
                    printImg=template.lightTemplate
                    tshirtImg=template.lightTshirt
                    
                   
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
                "theme":key.theme,   
                 "printId":key.printId,   
                "tshirtId":key.tshirtId     
            }
            Arr.append(item)
            # print(Arr)
            # for key in Arr:
            #     print(key["printImg"]," , ",key["tshirtImg"])
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
            theme=request.form.get("theme")
            type= request.form.get("type")
            print(printId ," , ",tshirtId)
            if mainstr=='add':    
                cart=Carts.query.filter_by(custId=data.publicId,theme=theme ,tshirtId=tshirtId ,printId=printId,type=type).first()
                if cart is None:
                    cred=Carts(publicId=publicId,custId=data.publicId,theme=theme ,tshirtId=tshirtId,colour=colour,size=size,type=type,printId=printId,details=details,price=price,quantity=quantity,date=datetime.now())
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
        Arr=[]
        data=Customers.query.filter_by(publicId=session['user']).first()
        orders=Orders.query.filter_by(custId=data.publicId).order_by(Orders.date.desc()).all()
        # for key in orders:
        #     if key.paymentId:
        #         payment=Payments.query.filter_by(publicId=key.paymentId).first()
        #         Arr.append({
        #             "subtotal":payment.subtotal,
        #             "charges":payment.charges,
        #             "total":payment.total,
        #             "transactionId":payment.subtotal,
        #             "orders":key
                    
        #         })
        #     print(Arr)
            
        return render_template("orders.html",orders=orders )
    else:
        session["redirect_to"]="/orders=view"
        return redirect("/login/auth")
 

# shows edited images
@app.route("/imgviewer",methods=['GET','POST'])   
def imgViewer():
    if 'user' in session:
        imgEdits=Edituploads.query.filter_by(custId=session['user']).order_by(Edituploads.date.desc()).all()
        return render_template("imageviewer.html",imgEdits=imgEdits)
    else:
        session["redirect_to"]="/"
        return redirect("/login/auth")
  
# shows account detals          
@app.route('/account/<string:publicId>',methods=['GET','POST'])
def account(publicId):
    if 'user' in session:
        user=Customers.query.filter_by(publicId=session['user']).first()
        if user:
            return render_template('account.html',user=user)
        return render_template('page_not_found.html'), 404 
    session["redirect_to"]="/"
    return redirect("/login/auth")
   

#  *****************************************Sharing and Caring****************************************
  #chats
@app.route("/chats" ,methods=["GET","POST"])
def chats():
    if  'user' in session:
        data=Customers.query.filter_by(publicId=session['user']).first()
        if request.method=="POST":
            msg=request.form.get("msg")
            receiver= "0"
            sender=data.publicId
            custId=data.publicId
            cred=Chats(sender=sender,msg=msg,receiver=receiver,custId=custId,date=datetime.utcnow())
            db.session.add(cred)
            db.session.commit()
        
        chats=Chats.query.filter_by(custId=data.publicId).all()
        Arr=[]
        for key in chats:
            Arr.append(key.toDict())
        
        return {
            "code":200,
            "data":Arr
        }
        
    return {
            "code":400,
            "data":None
        }
        
    

#share tshirts
@app.route("/d/shares/<string:shareId>",methods=['GET'])   
def shares(shareId):
    
    return redirect("/customize/default=ty/%s=car" %(shareId))


  
#  *****************************************ADMIN****************************************

  #chats
@app.route("/admin/chats/<string:userId>" ,methods=["GET","POST"])
def chatsByAdmin(userId):
    if 'admin' in session:
        data=Customers.query.filter_by(publicId=userId).first()
        if request.method=="POST":
            msg=request.form.get("msg")
            receiver= data.publicId
            sender="0"
            custId=data.publicId
            cred=Chats(sender=sender,msg=msg,receiver=receiver,custId=custId,date=datetime.utcnow())
            db.session.add(cred)
            db.session.commit()
        
        chats=Chats.query.filter_by(custId=data.publicId).all()
        Arr=[]
        for key in chats:
            Arr.append(key.toDict())
        
        return {
            "code":200,
            "data":Arr
        }
        
    return {
            "code":400,
            "data":None
        }
        
    
# admin shows inbox  
# @app.route("/admin/inbox", methods=['GET'])
# def admin_inbox():
#     if "admin" in session:
#         chats = db.session.query(
#         Chats,
#         func.max(Chats.date).label('max_date')
#         ).group_by(Chats.custId).join(Customers).order_by(text('max_date DESC')).all()

#         chat_dict = {}
#         for chat, max_date in chats:
#             if chat.custId in chat_dict:
#                 chat_dict[chat.custId]['chats'].append(chat)
#             else:
#                 chat_dict[chat.custId] = {
#                     'chats': [chat],
#                     'name': chat.customer.name,
#                     'userId': chat.custId
#                 }

#         chat_list = sorted(chat_dict.values(), key=lambda x: x['chats'][0].date, reverse=True)
#         return render_template("admin_inbox.html", chats=chat_list)


@app.route("/admin/inbox", methods=['GET'])
def admin_inbox():
    if "admin" in session:
        # chats = db.session.query(
        #     Chats.id.label('chats_id'),
        #     Chats.custId.label('chats_custId'),
        #     Chats.sender.label('chats_sender'),
        #     Chats.receiver.label('chats_receiver'),
        #     Chats.msg.label('chats_msg'),
        #     Chats.date.label('chats_date'),
        #     func.max(Chats.date).label('max_date')
        # ).group_by(Chats.custId).order_by(text('max_date DESC')).all()
        chats = db.session.query(
        Chats.id.label('chats_id'),
        Chats.custId.label('chats_custId'),
        Chats.sender.label('chats_sender'),
        Chats.receiver.label('chats_receiver'),
        Chats.msg.label('chats_msg'),
        Chats.date.label('chats_date'),
        func.max(Chats.date).label('max_date')
    ).group_by(
        Chats.id,
        Chats.custId,
        Chats.sender,
        Chats.receiver,
        Chats.msg,
        Chats.date
    ).join(Customers).order_by(text('max_date DESC')).all()

        chat_dict = {}
        for chat in chats:
            customer = Customers.query.filter_by(publicId=chat.chats_custId).first()
            if customer:
                if chat.chats_custId in chat_dict:
                    chat_dict[chat.chats_custId]['chats'].append(chat)
                else:
                    chat_dict[chat.chats_custId] = {
                        'chats': [chat],
                        'name': customer.name,
                        'userId': chat.chats_custId
                    }

        chat_list = sorted(chat_dict.values(), key=lambda x: x['chats'][0].chats_date, reverse=True)
        return render_template("admin_inbox.html", chats=chat_list)


# admin tshirt modifier
@app.route("/tshirt/<string:ty>/<string:action>/<string:id>=id/<string:sid>=sid/<string:fid>=fid",methods=['GET','POST'])
def tshirtAdder(ty,action,id,sid,fid):   
    if "admin" in session:
        publicId = uuid.uuid4().hex
        if request.method=="POST" and action=="add":
            app.config['UPLOAD_FOLDER']= os.path.abspath(params['base_url']+params['tshirtUpload'])
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
                path=os.path.join(os.path.abspath(params['base_url']+params['tshirtUpload']), secure_filename(imgName))
                try:
                    os.remove(path,dir_fd=None)
                except:
                    pass
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
            # itemsArr=[]
            # payments=Payments.query.order_by(Payments.date.desc()).all()
            # # print(payments)
            # for key in payments:
            #     ord=Orders.query.filter_by(paymentId=key.publicId).first()
            #     print(ord)
            #     itemsArr.append(ord)
            itemsArr=Orders.query.filter(Orders.paymentId != None).order_by(Orders.date.desc()).all()   
            
        else:
            itemsArr=Orders.query.filter(Orders.paymentId != None).filter_by(publicId=pid).all()   
            
            if request.method=="Post":
                if orders.deliverd==True:
                    return redirect("/generate/invoice/%s/%s")%(0,orders.publicId)
    elif str=="customers":
        if pid=="0":
            itemsArr=Customers.query.order_by(Customers.id.desc()).all()
        else:
            itemsArr=Customers.query.filter_by(publicId=pid).all()   
            
    elif str=="payments":
        if pid=="0":
            itemsArr=Payments.query.order_by(Payments.id.desc()).all()
        else:
            itemsArr=Payments.query.filter_by(custId=pid).all()   
            
    elif str=="messages":
        if pid=="0":
            itemsArr=Chats.query.order_by(Chats.date.desc()).all()
        else:
            itemsArr=Chats.query.filter_by(publicId=pid).all()   
            
    for item in itemsArr:
        
        Arr.append(item.toDict()) 
       
    return jsonify(Arr)

# admin shows products
@app.route("/admin/products",methods=['GET','POST'])   
def admin_products():
    return render_template("admin_products.html")
 
# admin shows statistics  
@app.route("/admin/statistics",methods=['GET','POST'])   
def admin_stats():
    return render_template("admin_statistics.html")

# admin shows order   
@app.route("/admin/orders",methods=['GET','POST'])   
def admin_orders():
    return render_template("admin_orders.html")


    
 # admin shows features  
@app.route("/admin/features")   
def admin_features():
    if "admin" in session:
        features=Customize.query.all()
        return render_template("admin_features.html",features=features
                               )
# admin edits features  
@app.route("/admin/features/<string:operation>/<string:id>", methods=['GET', 'POST'])   
def admin_features_edit(operation, id):
    if "admin" in session:
        app.config['UPLOAD_FOLDER'] = os.path.abspath(params['base_url'] + params['customizeUpload'])
        if request.method == "POST" and operation == "edit":
            feature_name = request.form.get("feature_name")
            status = request.form.get("status")
            public_id = uuid.uuid4().hex
            value = request.files.get("value")
            
            if value:
                try:
                    feature = Customize.query.filter_by(publicId=id).first()
                    delete_img = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(feature.value))
                    os.remove(delete_img, dir_fd=None)
                except:
                    pass
                img_name = feature_name + str(public_id) + value.filename
                value.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(img_name)))
                value = secure_filename(img_name)
            else:
                value = request.form.get("value")
                
            # try:
            if id == "0":
                cred = Customize(publicId=public_id, feature_name=feature_name, value=value, status=status)
                db.session.add(cred)
            else:
                feature = Customize.query.filter_by(publicId=id).first()
                feature.feature_name = feature_name
                feature.status = status
                if value:
                    
                    feature.value = value
            db.session.commit()
            return redirect("/admin/features")
            # except:
            #     flash("Feature with this name already exists")
        
        feature = None if id == "0" else Customize.query.filter_by(publicId=id).first()
        if feature and operation == "delete":
            try:
                if feature.value:
                    delete_img = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(feature.value))
                    os.remove(delete_img, dir_fd=None)
                db.session.delete(feature)
                db.session.commit()
                flash("Feature deleted successfully")
                
            except:
                flash("Unauthorized")
            return redirect("/admin/features")
        return render_template("admin_features_edit.html", feature=feature, id=id)

               
    

# admin shows customers   
@app.route("/admin/customers",methods=['GET','POST'])   
def admin_customers():
    cust=Customers.query.order_by(Customers.date.desc()).all()
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
           
                
            df = pd.read_sql(query.statement, query.session.bind)
            excel_file = io.BytesIO()
            df.to_excel(excel_file, index=False)
            excel_file.seek(0)
            return send_file(excel_file, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                as_attachment=True, attachment_filename=exportData.capitalize()+'_Date_'+str(datetime.date(datetime.now()))+'.xlsx')
        
            
            #     df = pd.read_sql(query.statement, query.session.bind)
            #     df.to_excel(exportData.capitalize()+'_Date_'+str( datetime.date(datetime.now()))+'.xlsx', index=False)
            #     return send_file(exportData.capitalize()+'_Date_'+str(datetime.date(datetime.now()))+'.xlsx')
               
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
  
# admin templates
@app.route("/admin/templates/<string:opt>/<string:id>", methods=['GET','POST'])
def templateAdd(opt,id):
    if 'admin' in session:
        if opt=="add":
            
            if request.method=='POST':
                publicId = uuid.uuid4().hex 
                title=request.form.get("title")
                category=request.form.get("category")
                keywords=request.form.get("keywords")
                price=request.form.get("price")
                lightTemplate=request.files["lightTemplate"]
                lightTshirt=request.files["lightTshirt"]
                lightBG=request.form.get("lightBG")
                darkTemplate=request.files["darkTemplate"]
                darkTshirt=request.files["darkTshirt"]
                darkBG=request.form.get("darkBG")
                carousel=request.form.get("carousel")
                if carousel=="False":
                    carousel=False
                elif carousel=="True":
                    carousel=True
                else:
                    carousel=carousel
                if id =="0":
                    app.config['UPLOAD_FOLDER']= os.path.abspath(params['base_url']+params['samplePostImgUpload'])
                    lightTemplateName="lightTemplate"+str(publicId)+lightTemplate.filename
                    lightTemplate.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(lightTemplateName)))
                    darkTemplateName="darkTemplate"+str(publicId)+darkTemplate.filename
                    darkTemplate.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(darkTemplateName)))
                    
                    app.config['UPLOAD_FOLDER']= os.path.abspath(params['base_url']+params['samplePostTshirtUpload'])
                    lightTshirtName="lightTshirts"+str(publicId)+lightTshirt.filename
                    lightTshirt.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(lightTshirtName)))
                    darkTshirtName="darkTshirts"+str(publicId)+darkTshirt.filename
                    darkTshirt.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(darkTshirtName)))
                    if not keywords:
                        keywords=""
                        
                    cred=Templates(publicId=publicId,carousel=carousel,title=title,category=category,keywords=keywords,price=price,lightTemplate=secure_filename(lightTemplateName),lightTshirt=secure_filename(lightTshirtName),
                                lightBG=lightBG,darkTemplate=secure_filename(darkTemplateName),darkTshirt=secure_filename(darkTshirtName),darkBG=darkBG,date=datetime.now())
                    db.session.add(cred)
                    db.session.commit()
                else:
                    template=Templates.query.filter_by(publicId=id).first()
                    if template:
                        app.config['UPLOAD_FOLDER']= os.path.abspath(params['base_url']+params['samplePostImgUpload'])
                        if darkTemplate:
                            darkTemplateDel=os.path.join(os.path.join(app.config['UPLOAD_FOLDER']), secure_filename(template.darkTemplate))
                            try:
                            
                                os.remove(darkTemplateDel,dir_fd=None)
                               
                            except:
                                pass
                            darkTemplateName="darkTemplate"+str(publicId)+darkTemplate.filename
                            darkTemplate.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(darkTemplateName)))
                            
                        if lightTemplate:
                            lightTemplateDel=os.path.join(os.path.join(app.config['UPLOAD_FOLDER']), secure_filename(template.lightTemplate))
                            try:
                            
                                os.remove(lightTemplateDel,dir_fd=None)
                                
                            except:
                                pass
                            lightTemplateName="lightTemplate"+str(publicId)+lightTemplate.filename
                            lightTemplate.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(lightTemplateName)))
                            template.lightTemplate=secure_filename(lightTemplateName)
                            
                        app.config['UPLOAD_FOLDER']= os.path.abspath(params['base_url']+params['samplePostTshirtUpload'])
                        if darkTshirt:
                            darkTshirtDel=os.path.join(os.path.join(app.config['UPLOAD_FOLDER']), secure_filename(template.darkTshirt))
                            try:
                                os.remove(darkTshirtDel,dir_fd=None)
                            except:
                                pass
                            darkTshirtName="darkTshirts"+str(publicId)+darkTshirt.filename
                            darkTshirt.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(darkTshirtName)))
                            template.darkTshirt=secure_filename(darkTshirtName)
                            
                        if lightTshirt:
                            lightTshirtDel=os.path.join(os.path.join(app.config['UPLOAD_FOLDER']), secure_filename(template.lightTshirt))
                            try:
                                os.remove(lightTshirtDel,dir_fd=None)
                            except:
                                pass
                            lightTshirtName="lightTshirts"+str(publicId)+lightTshirt.filename
                            lightTshirt.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(lightTshirtName)))
                            template.lightTshirt=secure_filename(lightTshirtName)
                  
                        
                        
                        template.title=title
                        template.category=category
                        template.keywords=keywords
                        template.price=price
                        
                        
                        template.darkBG=darkBG
                        
                        
                        template.lightBG=lightBG
                        
                    
                        
                        template.carousel=carousel
                        template.date=datetime.now()
                        db.session.commit()   
                        
                return redirect("/admin/templates/view/0")
            if id=="0":
                template=None
            else:
                template=Templates.query.filter_by(publicId=id).first()
                
            return render_template("template_adder.html",id=id,opt=opt,template=template)
   
        if opt=="delete":
            templates=Templates.query.filter_by(publicId=id).all() 
            if templates:
                for key in templates:
                    app.config['UPLOAD_FOLDER']= os.path.abspath(params['base_url']+params['samplePostImgUpload'])
                    darkTemplateDel=os.path.join(os.path.join(app.config['UPLOAD_FOLDER']), secure_filename(key.darkTemplate))
                    lightTemplateDel=os.path.join(os.path.join(app.config['UPLOAD_FOLDER']), secure_filename(key.lightTemplate))
                    app.config['UPLOAD_FOLDER']= os.path.abspath(params['base_url']+params['samplePostTshirtUpload'])
                    darkTshirtDel=os.path.join(os.path.join(app.config['UPLOAD_FOLDER']), secure_filename(key.darkTshirt))
                    lightTshirtDel=os.path.join(os.path.join(app.config['UPLOAD_FOLDER']), secure_filename(key.lightTshirt))
                    try:
                        os.remove(darkTemplateDel,dir_fd=None)
                        os.remove(lightTemplateDel,dir_fd=None)
                        os.remove(darkTshirtDel,dir_fd=None)
                        os.remove(lightTshirtDel,dir_fd=None)
                    except:
                        pass
                    db.session.delete(key)
                db.session.commit()
            
        if opt=="view":
            templates=Templates.query.order_by(Templates.id.desc()).all()
        templates=Templates.query.order_by(Templates.id.desc()).all()
        return render_template("admin_post.html",templates=templates)
    return redirect("/admin")
    
    


#  **************************************ERRORS**********************************************

# handles error 400
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html',error=error), 404

# handles error 400
@app.route("/error")
def error():
    error=400
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
                    "paymentStatus":"pending",
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
    session["redirect_to"]="/"
    return redirect("/login/auth")
    

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
    orderFlag=False
    customize=Customize.query.all()
    if 'user' in session:
        data=Customers.query.filter_by(publicId=session['user']).first()
        order=Orders.query.filter_by(custId=session['user']).all()
        
        for key in order:
            if key.paymentId==None:
                orderFlag=True
                break
            
        # print(orderFlag)
    elif 'admin' in session:
        data=Admin.query.filter_by(email=session['admin']).first()
    return dict(params=params,data=data,orderFlag=orderFlag,customize=customize)  