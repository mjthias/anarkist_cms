from bottle import delete
import utils.vars as var
import utils.validation as validate
import utils.g as g
import pymysql

##############################

@delete(f"{var.API_PATH}/taps/<tap_id>")
def _(tap_id):
    # VALIDATE SESSION
    session = validate.session()
    if not session: return g.respond(401, "Unauthorized attempt")

    # VALIDATE ROLE
    if session["role_id"] == 3:
        return g.respond(401, "Unauthorized attempt")
    
    # VALIDATE ID PARAM
    tap_id, error = validate.id(tap_id)
    if error: return g.respond(400, error)

    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("CALL delete_tap(%s, %s)", (tap_id, session["bar_id"]))
        counter = cursor.rowcount
        if not counter: return g.respond(204, "")
        db.commit()
        return g.respond(200, "Tap deleted")

    except Exception as ex:
        print(ex)
        return g.respond(500, "Server error")

    finally:
        cursor.close()
        db.close()


