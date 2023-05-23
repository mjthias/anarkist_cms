from bottle import put, request
import utils.g as g
import utils.vars as var
import utils.validation as validate
import pymysql
import bcrypt

##############################

@put(f"{var.API_PATH}/users/reset-password")
def _():
    try:
        # VALIDATE
        # Session
        session = validate.session()
        if not session: return g.respond(401)

        user_id = session["user_id"]

        # Keys allowed
        allowed_keys = ["user_password", "user_new_password", "user_confirm_new_password"]
        for key in request.forms.keys():
            if not key in allowed_keys: return g.respond(403, f"Forbidden key: {key}")
        
        # Current password
        user_password, error = validate.password(request.forms.get("user_password"))
        if error: return g.respond(400, error)

        # New password
        user_new_password, error = validate.password(request.forms.get("user_new_password"))
        if error: return g.respond(400, error)

        # Password to confirm
        user_confirm_new_password, error = validate.confirm_password(user_new_password, request.forms.get("user_confirm_new_password"))
        if error: return g.respond(400, error)
        
    except Exception as ex:
        print(str(ex))
        return g.respond(500)
    
    # CONNECT TO DB
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        db_connect.begin()
        cursor = db_connect.cursor()

        # Select the user
        cursor.execute("SELECT * FROM users WHERE user_id = %s LIMIT 1", (user_id,))
        user = cursor.fetchone()
        if not user: return g.respond(204)

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

        # No user affected
        counter = cursor.rowcount
        if not counter: return g.respond(204)
        
        db_connect.commit()
        return g.respond(200, "Password was successfully updated.")
    
    except Exception as ex:
        print(str(ex))
        db_connect.rollback()
        return g.respond(500)
    
    finally:
        cursor.close()
        db_connect.close()