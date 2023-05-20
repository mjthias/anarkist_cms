from bottle import post, request, response
import utils.vars as var
import utils.g as g
import utils.validation as validate
import bcrypt
import pymysql
import json
import jwt

##############################
@post(f"{var.API_PATH}/users")
def _():
    # VALIDATE SESSION AND USER ROLE
    session = validate.session()
    if not session: return g.respond(401, "Unauthorized attempt.")
    if session["role_id"] == 3: return g.respond(401, "Unauthorized attempt.")

    bar_id = session["bar_id"]

    # VALIDATE INPUT VALUES
    try:
        user_name, error = validate.user_name(request.forms.get("user_name"))
        if error: return g.respond(400, error)

        user_email, error = validate.email(request.forms.get("user_email"))
        if error: return g.respond(400, error)

        user_password, error = validate.password(request.forms.get("user_password"))
        if error: return g.respond(400, error)

        user_confirm_password, error = validate.confirm_password(user_password, request.forms.get("user_confirm_password"))
        if error: return g.respond(400, error)

        user_role_id, error = validate.id(request.forms.get("user_role_id"))
        if error: return g.respond(400, f"User Role {error}")

        # Admins cant create super users
        if session["role_id"] == 2 and user_role_id == 1:
            return g.respond(401, "Unauthorized attempt.")

        # GENERATE HASHED PASSWORD
        user_password_bytes = user_password.encode('utf-8')
        salt = bcrypt.gensalt()
        hash_user_password = bcrypt.hashpw(user_password_bytes, salt)
        user_password = str(hash_user_password)[2:-1]

        user = (
            user_email,
            user_name,
            user_password,
            user_role_id
        )
        
    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error.")
    
    # CONNECT TO DB
    try:
        db = pymysql.connect(**var.DB_CONFIG)
        db.begin()
        cursor = db.cursor()

        query = """
            INSERT INTO users
            (user_email,
            user_name,
            user_password,
            fk_user_role_id)
            VALUES(%s, %s, %s, %s)
        """
        cursor.execute(query, user)
        user_id = cursor.lastrowid

        # IF NEW USER IS NOT A SUPERUSER, INSERT BAR ACCESS AS WELL
        if not user_role_id == 1:
            query = """
                INSERT INTO bar_access
                (fk_bar_id,
                fk_user_id)
                VALUES(%s, %s)
            """
            cursor.execute(query, (bar_id, user_id))

        db.commit()

        return g.respond(201, user_id)
    
    except Exception as ex:
        print(str(ex))
        db.rollback()
        if "user_email" in str(ex): return g.respond(400, "Email already exists.")
        if "user_role_id" in str(ex): return g.respond(400, "User role does not exist.")
        if "bar_id" in str(ex): return g.respond(400, "Bar does not exist.")
        return g.respond(500, "Server error.")
    
    finally:
        cursor.close()
        db.close()