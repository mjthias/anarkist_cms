from bottle import delete, request, response
import utils.g as g
import utils.vars as var
import utils.validation as validate
import jwt
import json
import pymysql

allowed_keys = ["user_id", "confirm_deletion"]

##############################
@delete(f"{var.API_PATH}/users/<user_id>")
def _(user_id=""):
    session = validate.session()
    if not session: return g.respond(401, "Unauthorized attempt.")
    if (not session["user_id"] == int(user_id)) and (not session["role_id"] in var.AUTH_USER_ROLES): return g.respond(401, "Unauthorized attempt.")

    try:
        for key in request.forms.keys():
            if not key in allowed_keys: return g.respond(403, f"Forbidden key: {key}")
        
        user_id, error = validate.id(user_id)
        if error: return g.respond(400, f"User {error}")
        form_user_id, error = validate.id(request.forms.get("user_id"))
        if error: return g.respond(400, f"User {error}")
        if not user_id == form_user_id: return g.respond(400, "The user ID's does not match.")
        confirm_deletion, error = validate.confirm_deletion(request.forms.get("confirm_deletion"))
        if error: return g.respond(400, error)
        
    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error")
    
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        cursor = db_connect.cursor()

        cursor.execute("DELETE FROM users WHERE user_id = %s;", (user_id,))

        counter = cursor.rowcount
        if not counter: g.respond(204, "")
        db_connect.commit()

        response.status = 200
        response.content_type = "application/json"
        return g.respond(200, f"Successfully deleted user with ID: {user_id}")
    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error.")
    finally:
        cursor.close()
        db_connect.close()