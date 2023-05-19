from bottle import post, request
import utils.vars as var
import utils.validation as validate
import utils.g as g
import pymysql

##############################

@post(f"{var.API_PATH}/bar-access")
def _():
    try:
        # VALIDATE
        session = validate.session()
        if not session: return g.respond(401, "Unauthorized attempt.")

        # Staffs are 401
        if session["role_id"] == 3: return g.respond(401, "Unauthorized attempt.")

        bar_id = session["bar_id"]

        user_id, error = validate.id(request.forms.get("user_id"))
        if error: return g.respond(400, f"User {error}")

    except Exception as ex:
        print(ex)
        g.respond(500, "Server error.")

    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
        INSERT INTO bar_access
        SET fk_user_id = %s, fk_bar_id = %s
        """, (user_id, bar_id))
        db.commit()
        return g.respond(200, "Bar access created.")

    except Exception as ex:
        print(ex)
        g.respond(500, "Server error")
    
    finally:
        cursor.close()
        db.close()