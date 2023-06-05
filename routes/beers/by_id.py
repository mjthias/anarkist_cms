from bottle import get, view, redirect
import pymysql
from utils import g, vars as var, validation as validate

##############################

@get("/beers/<beer_id>")
@view("beers/by_id")
def _(beer_id=""):
    # VALIDATE
    session = validate.session()
    if not session:
        return redirect("/sign-in")

    try:
        beer_id, error = validate.id(beer_id)
        if error:
            return g.error_view(404)

    except Exception as ex:
        print(str(ex))
        return g.error_view(500)

    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        cursor = db_connect.cursor()
        cursor.execute("""
        SELECT beers_list.*, tap_id AS beer_on_tap
        FROM beers_list
        LEFT JOIN taps_list
        ON beers_list.beer_id = taps_list.fk_beer_id
        WHERE beers_list.beer_id = %s 
        LIMIT 1
        """, (beer_id,))
        beer = cursor.fetchone()
        if not beer:
            return g.error_view(404)

        beer['beer_price'] = g.format_price(beer["beer_price"])
        beer['beer_alc'] = g.format_price(float(beer['beer_alc']))
        return dict(session = session, beer = beer)

    except Exception as ex:
        print(str(ex))
        return g.error_view(500)

    finally:
        cursor.close()
        db_connect.close()
