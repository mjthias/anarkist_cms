from bottle import get, view, redirect
import utils.validation as validate
import utils.vars as var
import utils.g as g
import pymysql

##############################
@get("/beer-styles/<beer_style_id>")
@view("single_beer_style")
def _(beer_style_id):
    # VALIDATE SESSION
    session = validate.session()
    if not session: return redirect("/sign-in")

    # VALIDATE ID
    beer_style_id, error = validate.id(beer_style_id)
    if error: return g.error_view(404, "Page not found")

    # CONNECT TO DB
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        cursor = db_connect.cursor()

        cursor.execute("""
            SELECT * FROM beer_styles 
            WHERE beer_style_id = %s 
            LIMIT 1
        """, (beer_style_id,))
        beer_style = cursor.fetchone()
        if not beer_style: g.error_view(404, "Page not found")

        return dict(session=session, beer_style=beer_style)
    
    except Exception as ex:
        print(str(ex))
        return g.error_view(500, "Server error.")
    
    finally:
        cursor.close()
        db_connect.close()