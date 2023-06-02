from bottle import get, request, view
import pymysql
from utils import g, vars as var, validation as validate

##############################

@get(f"{var.API_PATH}/taps/notifications")
def _():
    try:
        # VALIDATE SESSION
        session = validate.session()
        if not session:
            return g.respond(401)
        bar_id = session["bar_id"]

    except Exception as ex:
        print(ex)
        return g.respond(500)

    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
        SELECT DISTINCT beer_id, beer_name 
        FROM taps_list
        WHERE fk_bar_id = %s
        AND (beer_ebc IS NULL
        OR beer_ibu IS NULL
        OR beer_image IS NULL
        OR beer_description_en IS NULL
        OR beer_description_dk IS NULL)
        """, (bar_id))
        taps = cursor.fetchall()
        db.commit()

        if request.headers.get("as-html"):
            if not taps:
                return g.error_view(204)
            return as_html(taps)

        return g.respond(200, taps)

    except Exception as ex:
        print(ex)
        return g.respond(500)

    finally:
        cursor.close()
        db.close()

@view("components/taps_notifications_list")
def as_html(taps):
    return dict(taps=taps)
    