from bottle import put, request
import utils.g as g
import utils.vars as var
import utils.validation as validate
import pymysql
import bcrypt

##############################
@put(f"{var.API_PATH}/users/<user_id>/reset-password")
def _(user_id=""):
    # VALIDATE USER
    session = validate.session()
    if not session: return g.respond(401, "Unauthorized attempt.")
    if (not session["user_id"] == int(user_id) and (not session["role_id"] == 1)): return g.respond(401, "Unauthorized attempt.")

    # VALIDATE INPUT VALUES
    allowed_keys = ["user_id", "user_password", "user_new_password", "user_confirm_new_password"]
    try:
        for key in request.forms.keys():
            if not key in allowed_keys: return g.respond(403, f"Forbidden key: {key}")
        
        user_id, error = validate.id(user_id)
        if error: return g.respond(400, f"User {error}")
        form_user_id, error = validate.id(request.forms.get("user_id"))
        if error: return g.respond(400, f"User {error}")
        if not user_id == form_user_id: return g.respond(400, "The user ID's does not match.")
        user_password, error = validate.password(request.forms.get("user_password"))
        if error: return g.respond(400, error)
        user_new_password, error = validate.password(request.forms.get("user_new_password"))
        if error: return g.respond(400, error)
        user_confirm_new_password, error = validate.confirm_password(user_new_password, request.forms.get("user_confirm_new_password"))
        if error: return g.respond(400, error)
        
    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error.")
    
    # CONNECT TO DB
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        db_connect.begin()
        cursor = db_connect.cursor()

        cursor.execute("SELECT * FROM users WHERE user_id = %s LIMIT 1", (user_id,))
        user = cursor.fetchone()
        if not user: return g.respond(204, "")

        # VALIDATE PASSWORD
        user_password_bytes = user_password.encode("utf-8")
        user_new_password_bytes = user_new_password.encode("utf-8")
        if not bcrypt.checkpw(user_password_bytes, str(user["user_password"]).encode("utf-8")):
            return g.respond(400, "Incorrect password.")

        # GENERATE NEW HASHED PASSWORD
        salt = bcrypt.gensalt()
        hash_user_new_password = bcrypt.hashpw(user_new_password_bytes, salt)
        user_new_password = str(hash_user_new_password)[2:-1]

        # UPDATE USER IN DB
        cursor.execute("""
            UPDATE users
            SET user_password = %s
            WHERE user_id = %s
        """, (user_new_password, user_id))

        counter = cursor.rowcount
        if not counter: return g.respond(204, "")
        print(f"Rows updated: {counter}")
        db_connect.commit()

        return g.respond(200, "Password was successfully updated.")
    except Exception as ex:
        print(str(ex))
        db_connect.rollback()
        return g.respond(500, "Server error.")
    finally:
        cursor.close()
        db_connect.close()