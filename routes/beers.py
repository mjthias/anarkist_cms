from bottle import get, view, response, redirect
import utils.vars as var
import utils.validation as validate
import utils.g as g
import pymysql

##############################

@get("/beers")
@view("beers")
def _():
    session = validate.session()
    if not session: 
        return redirect("/sign-in")
    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM beers_list")
        beers = cursor.fetchall()
        print(beers)
        return dict(beers = beers, session=session)

    except Exception as ex:
        print(str(ex))
        return g.error_view(500)

    finally:
        cursor.close()
        db.close()
    
