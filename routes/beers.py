from bottle import get, view, response, redirect
import utils.vars as var
import utils.validation as validate
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
        cursor.execute("SELECT * FROM beer_list")
        beers = cursor.fetchall()
        print(beers)
        return dict(beers = beers, session=session)

    except Exception as ex:
        print(str(ex))
        response.status = 500
        return "Server error"

    finally:
        cursor.close()
        db.close()
    
