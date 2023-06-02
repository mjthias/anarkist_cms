from bottle import get
import pymysql
from utils import g, vars as var, validation as validate

##############################

@get(f"{var.API_PATH}/taps/notifications")
def _():
    try:
        # VALIDATE SESSION
        session = validate.session()
        if not session or session["role_id"] == 3:
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
        return g.respond(200, taps)

    except Exception as ex:
        print(ex)
        return g.respond(500)

    finally:
        cursor.close()
        db.close()
    