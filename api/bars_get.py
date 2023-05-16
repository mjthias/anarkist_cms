from bottle import get, response
from utils.vars import _DB_CONFIG
import pymysql
import json

##############################

@get("/api/bars")
def _():
    response.content_type = 'application/json'
    query = "SELECT * FROM bars"

    # CONNNECT TO DB AND EXECUTE
    try:
        db = pymysql.connect(**_DB_CONFIG)
        cursor = db.cursor()
        cursor.execute(query)
        bars = cursor.fetchall()
        response.status = 200
        return json.dumps(bars)

    except Exception as ex:
        print(str(ex))
        response.status = 500
        return "Server error"

    finally:
        cursor.close()
        db.close()
    