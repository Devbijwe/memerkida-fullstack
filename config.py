from sqlalchemy_utils import database_exists, create_database
import json

with open("/var/www/MemerKida/MemerKida/config.json", "r") as c:
    params = json.load(c)["params"]

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if params["local_server"]:
        SQLALCHEMY_DATABASE_URI = params["local_url"]
    else:
        if not database_exists(params["prod_url"]):
            create_database(params["prod_url"])
        SQLALCHEMY_DATABASE_URI = params["prod_url"]
