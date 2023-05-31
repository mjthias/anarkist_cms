# pylint: disable=W0612
from bottle import delete, request
import pymysql
from utils import g, vars as var, validation as validate, vercel

##############################

@delete(f"{var.API_PATH}/taps/<tap_id>")
def _(tap_id):
    try:
        # VALIDATE SESSION AND ROLE - staff not allowed
        session = validate.session()
        if not session or session["role_id"] == 3:
            return g.respond(401)

        # VALIDATE ID PARAM
        tap_id, error = validate.id(tap_id)
        if error:
            return g.respond(400, error)

        # Input values
        x, error = validate.confirm_deletion(request.forms.get("confirm_deletion"))
        if error:
            return g.respond(400, {"info": error, "key": "confirm_deletion"})

    except Exception as ex:
        print(ex)
        return g.respond(500)

    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("CALL delete_tap(%s, %s)", (tap_id, session["bar_id"]))
        counter = cursor.rowcount
        if not counter:
            return g.respond(204)
        db.commit()

        # DEPLOY VERCEL
        vercel.deploy()

        return g.respond(200, "Tap deleted")

    except Exception as ex:
        print(ex)
        return g.respond(500)

    finally:
        cursor.close()
        db.close()
