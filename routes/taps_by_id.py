from bottle import get, view, redirect
import utils.validation as validate
import utils.vars as var
import utils.g as g
import pymysql

##############################

@get("/taps/<tap_id>")
@view("single_tap")
def _(tap_id):
    # VALIDATE SESSION
    session = validate.session()
    if not session: return redirect("/sign-in")

    # VALIDATE ID PARAM
    tap_id, error = validate.id(tap_id)
    if error: g.respond(404, "Page not found")

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

        print(tap)

        if not tap: return g.respond(404, "Page not found")
        
        return dict(
            session = session,
            tap = tap,
            )

    except Exception as ex:
        print(ex)
        return g.respond(500, "Server error")
    
    finally:
        cursor.close()
        db.close()