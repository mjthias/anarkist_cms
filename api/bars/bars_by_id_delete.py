# pylint: disable=W0612
from bottle import delete, request
import pymysql
from utils import g, validation as validate, vars as var

##############################

@delete(f"{var.API_PATH}/bars/<bar_id>")
def _(bar_id):
    try:
        # VALIDATE
        session = validate.session()
        if not session:
            return g.respond(401)

        if not session["role_id"] == 1:
            return g.respond(401)

        # bar id param
        bar_id, error = validate.id(bar_id)
        if error:
            return g.respond(400, error)

        # Input values
        x, error = validate.confirm_deletion(request.forms.get("confirm_deletion"))
        if error:
            return g.respond(400, {"info": error, "key": "confirm_deletion"})

    except Exception as ex:
        print(str(ex))
        return g.respond(500)

    # UPDATE IN DB
    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
        DELETE FROM bars
        WHERE bar_id = %s
        """, (bar_id))
        counter = cursor.rowcount
        if not counter:
            return g.respond(204, "")
        db.commit()

        return g.respond(200, "Bar updated")

    except Exception as ex:
        print(str(ex))
        return g.respond(500)

    finally:
        cursor.close()
        db.close()
