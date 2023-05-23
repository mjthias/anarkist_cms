from bottle import get, view, redirect
import utils.vars as var
import utils.validation as validate
import utils.g as g
import pymysql

##############################
@get("/beer-styles")
@view("beer_styles")
def _():
    session = validate.session()
    if not session: return redirect("/sign-in")

    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        cursor = db_connect.cursor()
        
        cursor.execute("SELECT * FROM beer_styles")
        beer_styles = cursor.fetchall()

        return dict(session=session, beer_styles=beer_styles)
    
    except Exception as ex:
        print(str(ex))
        return g.error_view(500)
    
    finally:
        cursor.close()
        db_connect.close()