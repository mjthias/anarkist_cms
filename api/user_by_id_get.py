from bottle import get, response, request
import utils.vars as var
import utils.g as g
import utils.validation as validate
import pymysql
import json
import jwt

##############################
@get(f"{var.API_PATH}/users/<user_id>")
def _(user_id=""):
    if not request.get_cookie("anarkist"): return g.respond(401, "Unauthorized attempt.")
    cookie = request.get_cookie("anarkist")
    decoded_jwt = jwt.decode(cookie, var.JWT_SECRET, algorithms=["HS256"])
    session_user_id = int(decoded_jwt["user_id"])
    session_role_id = int(decoded_jwt["user_role"])
    session_bar_id = int(decoded_jwt["bar_id"])
    if (not session_user_id == int(user_id)) and (not session_role_id in var.AUTH_USER_ROLES): return g.respond(401, "Unauthorized attempt.")

    try:
        user_id, error = validate.id(user_id)
        if error: return g.respond(400, f"User {error}")
        bar_id, error = validate.id(str(session_bar_id))
        if error: return g.respond(400, f"Bar {error}")

    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error.")
    
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        cursor = db_connect.cursor()

        if session_role_id == 1:
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