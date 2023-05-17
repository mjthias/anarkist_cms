from bottle import get, view, response
import utils.vars as var
import pymysql
import json

##############################

@get("/beers")
@view("beers")
def _():
    try:
        db = pymysql.connect(**var.DB_CONFIG)
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
    
