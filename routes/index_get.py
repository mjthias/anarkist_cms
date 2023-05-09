from bottle import get, response
from vars import DB_CONFIG
import json
import pymysql
from datetime import datetime

##############################

@get("/")
def _():
    try:
        db = pymysql.connect(**DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM beers")
        beers = cursor.fetchall()

        for beer in beers:
            beer["beer_created_at"] = beer["beer_created_at"].strftime("%m %d %Y")
            beer["beer_updated_at"] = beer["beer_updated_at"].strftime("%m %d %Y")

        print(beers)
        return json.dumps(beers)
    
    except Exception as ex:
        print(str(ex))
        response.status = 500
        return "Server error"

    finally:
        cursor.close()
        db.close()