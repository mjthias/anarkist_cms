import math
from bottle import get, view, redirect
import pymysql
from utils import g, vars as var, validation as validate

##############################

@get("/bars/<bar_id>")
@view("bars/by_id")
def _(bar_id):
    # VALIDATE SESSION
    session = validate.session()
    if not session:
        return redirect("/sign-in")

    # VALIDATE ROLE
    if not session["role_id"] == 1:
        return g.error_view(401)

    # VALIDATE BAR ID
    bar_id, error = validate.id(bar_id)
    if error:
        return g.error_view(404)

    # GET BAR FROM DB
    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
        SELECT bars.*, 
        (SELECT COUNT(*) FROM taps WHERE fk_bar_id = bars.bar_id AND tap_number IS NOT NULL) AS numbered_taps,
        (SELECT COUNT(*) FROM taps WHERE fk_bar_id = bars.bar_id AND tap_number IS NULL) AS off_wall_taps
        FROM bars
        WHERE bar_id = %s
        LIMIT 1;
        """, (bar_id))
        bar = cursor.fetchone()
        if not bar:
            return g.error_view(404)

        # Calc generated screens
        screens_nr = math.ceil((bar["numbered_taps"] + bar["off_wall_taps"] / 2) / 14)

        return dict(
            session = session,
            bar = bar,
            screens_nr = screens_nr
            )

    except Exception as ex:
        print(ex)
        return g.error_view(500)

    finally:
        cursor.close()
        db.close()
