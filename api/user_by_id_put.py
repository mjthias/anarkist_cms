from bottle import put, request, response
import utils.g as g
import utils.vars as var
import utils.validation as validate
import json
import pymysql

allowed_keys = ["user_id", "user_name", "user_email", "user_role_id"]

##############################
@put(f"{var.API_PATH}/users/<user_id>")
def _(user_id=""):
    session = validate.session()
    if not session: return g.respond(401, "Unauthorized attempt.")
    if (not session["user_id"] == int(user_id)) and (not session["role_id"] in var.AUTH_USER_ROLES): return g.respond(401, "Unauthorized attempt.")
    try:
        for key in request.forms.keys():
            if not key in allowed_keys: return g.respond(403, f"Forbidden key: {key}")
        
        user_id, error = validate.id(user_id)
        if error: return g.respond(400, error)
        form_user_id, error = validate.id(request.forms.get("user_id"))
        if error: return g.respond(400, f"User {error}")
        if not user_id == form_user_id: return g.respond(400, "The user ID's does not match.")
        user_email, error = validate.email(request.forms.get("user_email"))
        if error: return g.respond(400, error)
        user_name, error = validate.user_name(request.forms.get("user_name"))
        if error: return g.respond(400, error)
        user_role_id, error = validate.id(request.forms.get("user_role_id"))
        if error: return g.respond(400, f"User role {error}")

    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error")
    
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        db_connect.begin()
        cursor = db_connect.cursor()

        if session["role_id"] == 1:
            cursor.execute("""
                SELECT * FROM users_list 
                WHERE (user_id = %s AND bar_id = %s) 
                OR (user_id = %s AND bar_id IS NULL)
                LIMIT 1
            """, (user_id, session["bar_id"], user_id))
        else:
            cursor.execute("""
                SELECT * FROM users_list 
                WHERE user_id = %s AND bar_id = %s 
                LIMIT 1
            """, (user_id, session["bar_id"]))
        user = cursor.fetchone()
        if not user: return g.respond(204, "")

        user["user_email"] = user_email
        user["user_name"] = user_name
        if (session["role_id"] == 1) or (session["bar_id"] == user["bar_id"] and session["role_id"] == 2 and not user_role_id == 1):
            user["user_role_id"] = user_role_id

        cursor.execute("""
            UPDATE users
            SET user_email = %s,
            user_name = %s,
            fk_user_role_id = %s
            WHERE user_id = %s
        """, (user["user_email"], user["user_name"], user["user_role_id"], user["user_id"]))

        counter = cursor.rowcount
        if not counter: return g.respond(204, "")
        print(f"Rows updated: {counter}")
        db_connect.commit()

        if session["role_id"] == 1:
            cursor.execute("""
                SELECT * FROM users_list 
                WHERE (user_id = %s AND bar_id = %s) 
                OR (user_id = %s AND bar_id IS NULL)
                LIMIT 1
            """, (user_id, session["bar_id"], user_id))
        else:
            cursor.execute("""
                SELECT * FROM users_list 
                WHERE user_id = %s AND bar_id = %s 
                LIMIT 1
            """, (user_id, session["bar_id"]))
        user = cursor.fetchone()

        response.status = 200
        response.content_type = "application/json"
        return json.dumps(user)
    except Exception as ex:
        print(str(ex))
        db_connect.rollback()
        return g.respond(500, "Server error.")
    finally:
        cursor.close()
        db_connect.close()