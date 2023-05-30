from bottle import get, request
import pymysql
from utils import g, vars as var, validation as validate

##############################

@get(f"{var.API_PATH}/users")
def _():
    try:
        # VALIDATE SESSION/USER
        session = validate.session()
        if not session:
            return g.respond(401, "Unauthorized attempt.")

        if int(session["role_id"]) not in var.AUTH_USER_ROLES:
            return g.respond(401, "Unauthorized attempt.")

        # VALIDATE INPUT/QUERYSTRING VALUES
        user_id, error = validate.id(str(session["user_id"]))
        if error:
            return g.respond(400, f"User {error}")

        bar_id, error = validate.id(str(session["bar_id"]))
        if error:
            return g.respond(400, f"Bar {error}")

        offset, error = validate.offset(request.query.get("offset"))
        if error:
            return g.respond(400, error)

        limit, error = validate.limit(request.query.get("limit"))
        if error:
            return g.respond(400, error)

    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error.")

    # CONNECT TO DB
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        cursor = db_connect.cursor()

        # INCLUDE SUPER USERS IF SUPER USER
        if session["role_id"] == 1:
            cursor.execute("""
            SELECT * FROM users_list
            WHERE bar_id = %s 
            OR user_role_id = 1 AND user_id != %s
            LIMIT %s,%s
            """, (bar_id, user_id, offset, limit))
        else:
            cursor.execute("""
            SELECT * FROM users_list
            WHERE bar_id = %s AND user_id != %s
            LIMIT %s,%s
            """, (bar_id, user_id, offset, limit))

        users = cursor.fetchall()
        counter = cursor.rowcount
        if not counter:
            return g.respond(204, "")

        return g.respond(200, users)

    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error.")

    finally:
        cursor.close()
        db_connect.close()
