from bottle import get
import utils.vars as var
import utils.g as g
import pymysql

##############################

@get(f"{var.API_PATH}/bars")
def _():
    # USED BY VERCEL - NO SESSION
    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM bars")
        bars = cursor.fetchall()
        if not bars:
            return g.respond(204)
        return g.respond(200, bars)

    except Exception as ex:
        print(str(ex))
        return g.respond(500)

    finally:
        cursor.close()
        db.close()
    
