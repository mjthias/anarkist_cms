from bottle import get, view, redirect
import pymysql
from utils import g, vars as var, validation as validate

##############################
@get("/beer-styles/<beer_style_id>")
@view("beer_styles/by_id")
def _(beer_style_id):
    # VALIDATE SESSION
    session = validate.session()
    if not session:
        return redirect("/sign-in")

    # VALIDATE ID
    beer_style_id, error = validate.id(beer_style_id)
    if error:
        return g.error_view(404)

    # CONNECT TO DB
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        cursor = db_connect.cursor()

        cursor.execute("""
        SELECT beer_styles.*, beer_id AS style_on_beer
        FROM beer_styles 
        LEFT JOIN beers
        ON fk_beer_style_id = beer_style_id
        WHERE beer_style_id = %s 
        LIMIT 1
        """, (beer_style_id,))
        beer_style = cursor.fetchone()
        if not beer_style:
            return g.error_view(404)
        print(beer_style)

        return dict(session=session, beer_style=beer_style)

    except Exception as ex:
        print(str(ex))
        return g.error_view(500)

    finally:
        cursor.close()
        db_connect.close()
