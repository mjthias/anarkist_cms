from bottle import get, response
from vars import DB_CONFIG
import json
import pymysql

##############################

@get("/")
def _():
    try:
        db = pymysql.connect(**DB_CONFIG)
        cursor = db.cursor()
        # cursor.execute("SELECT * FROM beers")
        # cursor.execute("SELECT * FROM beer_list")
        # cursor.execute("CALL get_beer_by_name (%s)", ("american haze",))
        cursor.execute("CALL get_beer_by_fuzzy_name (%s)", ("amricn hase",))
        beers = cursor.fetchall()
        return json.dumps(beers)
    
    except Exception as ex:
        print(str(ex))
        response.status = 500
        return "Server error"

    finally:
        cursor.close()
        db.close()