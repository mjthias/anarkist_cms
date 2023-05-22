from bottle import get
import utils.validation as validate
import utils.g as g
import utils.vars as var
import pymysql

##############################

@get(f"{var.API_PATH}/beers/<beer_name>")
def _(beer_name):
    # VALIDATE SESSION
    # session = validate.session()
    # if not session: return g.respond(401, "Unauthorized attempt")

    #VALIDATE PARAM
    beer_name, error = validate.name(beer_name)
    if error: return g.respond(400, error)

    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
        SELECT * FROM beer_list
        WHERE beer_name LIKE CONCAT("am", "%")
        """)
        beers = cursor.fetchall()
        print(beers)
        if len(beers) == 0:
            return g.respond(204, "")
        return g.respond(200, beers)

    except Exception as ex:
        print(ex)
        return g.respond(500, "Server error")
    
    finally:
        cursor.close()
        db.close()

    

