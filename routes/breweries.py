from bottle import get, view, redirect
import utils.validation as validate
import utils.vars as var
import utils.g as g
import pymysql

########################################

@get("/breweries")
@view("breweries")
def _():
    session = validate.session()
    if not session: return redirect("/sign-in")

    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
            SELECT * FROM breweries
            ORDER BY brewery_name
            """)
        breweries = cursor.fetchall()
        return dict(
            session = session,
            breweries = breweries
            )
    
    except Exception as ex:
        print(ex)
        return g.error_view(500)
    
    finally:
        cursor.close()
        db.close()
