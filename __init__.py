
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
import json

with open("/var/www/MemerKida/MemerKida/config.json", "r") as c:
    params = json.load(c)["params"]


app=Flask(__name__,template_folder="Templates")
app.secret_key='sdx2323@3343zbhcfew3rr3343@@###$2ffr454'
 
# from .config import Config
# app.config.from_object(Config)
# if params["local_server"]:
#     app.config["SQLALCHEMY_DATABASE_URI"] = params["local_url"]
# else:
#     if not database_exists(params["prod_url"]):
#         create_database(params["prod_url"])
#     app.config["SQLALCHEMY_DATABASE_URI"] = params["prod_url"]
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://memerkida:500-Memerkida@92.242.187.59/memerkida"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db=SQLAlchemy(app)  
with app.app_context():
    db.create_all()
    
from .views import *

if __name__=='__main__':
    app.run(debug=True,port=5000)