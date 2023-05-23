from bottle import get, view, redirect
import utils.validation as validate
import utils.vars as var
import utils.g as g
import pymysql

##############################

@get("/bars")
@view("bars/index")
def _():
    # VALIDATE SESSION
    session = validate.session()
    if not session: return redirect("/sign-in")

    # VALIDATE ROLE
    if not session["role_id"] == 1:
        return g.error_view(401)
    
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

    
