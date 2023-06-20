from bottle import post, request
import pymysql
from utils import g, validation as validate, vars as var

##############################

@post(f"{var.API_PATH}/bar-access")
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
        # CONNECT TO DB
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()

        # Select user to prevent role_id 1 in bar_access
        cursor.execute("""
        SELECT fk_user_role_id FROM users
        WHERE user_id = %s
        """, (user_id))
        user = cursor.fetchone()
        if not user:
            return g.respond(204)
        if user["fk_user_role_id"] == 1:
            return g.respond(400, "Super users have access to all bars")

        # Post to DB
        cursor.execute("""
        INSERT INTO bar_access
        SET fk_user_id = %s, fk_bar_id = %s
        """, (user_id, bar_id))
        db.commit()
        return g.respond(201, "Bar access created")

    except Exception as ex:
        print(ex)
        return g.respond(500)

    finally:
        cursor.close()
        db.close()
