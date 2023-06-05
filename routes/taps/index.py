from bottle import get, view, redirect
import pymysql
from utils import g, vars as var, validation as validate

##############################

@get("/taps")
@view("taps/index")
def _():
    # VALIDATE SESSION
    session = validate.session()
    if not session:
        return redirect("/sign-in")

    # GET TAPS FROM DB
    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
            SELECT * FROM taps_list
            WHERE fk_bar_id = %s
            """, (session["bar_id"]))
        taps = cursor.fetchall()

        return dict(
            session = session,
            taps = taps,
            )

    except Exception as ex:
        print(ex)
        return g.respond(500)

    finally:
        cursor.close()
        db.close()
