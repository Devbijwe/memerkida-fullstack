
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__,template_folder="Templates")
app.secret_key='sdx2323@3343zbhcfew3rr3343@@###$2ffr454'
db=SQLAlchemy(app)   
from config import Config
app.config.from_object(Config)
with app.app_context():
    db.create_all()
    
from views import *
# ****************************************google Login*****************************************   
 
if __name__=='__main__':
    app.run(debug=True,port=2000)