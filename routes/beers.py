from bottle import get, view, response
from utils.vars import _DB_CONFIG
import pymysql
import json

##############################

@get("/beers")
@view("beers")
def _():
    try:
        db = pymysql.connect(**_DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM beers")
        beers = cursor.fetchall()
        user = {"user_name": "Super User"}
        # return json.dumps(beers)
        print(beers)
        return dict(beers = beers, user=user)

    except Exception as ex:
        print(str(ex))
        response.status = 500
        return "Server error"

    finally:
        cursor.close()
        db.close()
    
