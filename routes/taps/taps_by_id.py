from bottle import get, view, redirect
import pymysql
from utils import g, vars as var, validation as validate

##############################

@get("/taps/<tap_id>")
@view("taps/by_id")
def _(tap_id):
    # VALIDATE SESSION
    session = validate.session()
    if not session:
        return redirect("/sign-in")

    try:
        # VALIDATE ID PARAM
        tap_id, error = validate.id(tap_id)
        if error:
            return g.error_view(404)

    except Exception as ex:
        print(ex)
        return g.error_view(500)

    # GET TAP FROM DB
    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
            SELECT * FROM taps_list
            WHERE tap_id = %s
            AND fk_bar_id = %s
            LIMIT 1
            """, (tap_id, session["bar_id"]))
        tap = cursor.fetchone()
        if not tap:
            return g.error_view(404)

        return dict(
            session = session,
            tap = tap,
            )

    except Exception as ex:
        print(ex)
        return g.error_view(500)

    finally:
        cursor.close()
        db.close()
