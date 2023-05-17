from bottle import get
import utils.vars as var
import utils.g as g
import pymysql

##############################

@get(f"{var.API_PATH}/breweries")
def _():
    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM breweries")
        breweries = cursor.fetchall()
        if not breweries:
            return g.respond(204, "")
        g.respond(200, breweries)

    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error")

    finally:
        cursor.close()
        db.close()
    
