from bottle import get, view, redirect
import pymysql
from utils import g, vars as var, validation as validate

##############################

@get("/bars")
@view("bars/index")
def _():
    # VALIDATE SESSION
    session = validate.session()
    if not session:
        return redirect("/sign-in")

    try:
        # VALIDATE ROLE
        if not session["role_id"] == 1:
            return g.error_view(401)

    except Exception as ex:
        print(ex)
        return g.error_view(500)

    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM bars")
        bars = cursor.fetchall()
        return dict(
            session = session,
            bars = bars
            )

    except Exception as ex:
        print(ex)
        return g.error_view(500)

    finally:
        cursor.close()
        db.close()
