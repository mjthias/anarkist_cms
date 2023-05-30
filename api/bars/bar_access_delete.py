from bottle import delete, request
import pymysql
from utils import g, validation as validate, vars as var

##############################

@delete(f"{var.API_PATH}/bar-access")
def _():
    try:
        # VALIDATE
        session = validate.session()
        if not session:
            return g.respond(401)

        # Staffs are 401
        if session["role_id"] == 3:
            return g.respond(401)

        bar_id = session["bar_id"]

        user_id, error = validate.id(request.forms.get("user_id"))
        if error:
            return g.respond(400, f"User {error}")

    except Exception as ex:
        print(ex)
        return g.respond(500)

    try:
        # DELETE FROM DB
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
        DELETE FROM bar_access
        WHERE fk_user_id = %s
        AND fk_bar_id = %s
        """, (user_id, bar_id))
        counter = cursor.rowcount
        if not counter:
            return g.respond(204)
        db.commit()

        return g.respond(200, "Access deleted")

    except Exception as ex:
        print(ex)
        return g.respond(500)

    finally:
        cursor.close()
        db.close()
