from bottle import get, response, request
import utils.vars as var
import utils.g as g
import utils.validation as validate
import pymysql

##############################
@get(f"{var.API_PATH}/users/<user_id>")
def _(user_id=""):
    # VALIDATE SESSION/USER
    session = validate.session()
    if not session: return g.respond(401, "Unauthorized attempt.")
    if (not session["user_id"] == int(user_id)) and (not session["role_id"] in var.AUTH_USER_ROLES): return g.respond(401, "Unauthorized attempt.")

    # VALIDATE INPUT VALUES
    try:
        user_id, error = validate.id(user_id)
        if error: return g.respond(400, f"User {error}")
        bar_id, error = validate.id(str(session["bar_id"]))
        if error: return g.respond(400, f"Bar {error}")

    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error.")
    
    # CONNECT TO DB
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        cursor = db_connect.cursor()

        # INCLUDE SUPER USERS AND USERS WITHOUT A BAR IF SUPER USER
        if session["role_id"] == 1:
            cursor.execute("""
                SELECT * FROM users_list 
                WHERE (user_id = %s AND bar_id = %s) 
                OR (user_id = %s AND bar_id IS NULL)
                LIMIT 1
            """, (user_id, bar_id, user_id))
        else:
            cursor.execute("""
                SELECT * FROM users_list 
                WHERE user_id = %s AND bar_id = %s 
                LIMIT 1
            """, (user_id, bar_id))
        user = cursor.fetchone()
        if not user: return g.respond(204, "")

        return g.respond(200, user)
    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error")
    finally:
        cursor.close()
        db_connect.close()