from bottle import get, view, redirect
import pymysql
from utils import g, vars as var, validation as validate

##############################

@get("/breweries/<brewery_id>")
@view("breweries/by_id")
def _(brewery_id):
    #VALIDATE SESSION
    session = validate.session()
    if not session:
        return redirect("/sign-in")

    try:
        # VALIDATE ID
        brewery_id, error = validate.id(brewery_id)
        if error:
            return g.error_view(404)

    except Exception as ex:
        print(ex)
        return g.error_view(500)

    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
        SELECT breweries.*, taps_list.brewery_name AS brewery_on_tap
        FROM breweries
        LEFT JOIN taps_list 
        ON breweries.brewery_name = taps_list.brewery_name
        WHERE brewery_id = %s
        LIMIT 1
        """, (brewery_id))
        brewery = cursor.fetchone()

        if not brewery:
            return g.error_view(404)

        return dict(
            session = session,
            brewery = brewery
            )

    except Exception as ex:
        print(ex)
        return g.error_view(500)

    finally:
        cursor.close()
        db.close()
