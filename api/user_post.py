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
    # VALIDATE SESSION/USER
    session = validate.session()
    if not request.get_cookie("anarkist"): return g.respond(401, "Unauthorized attempt.")
    if not session["role_id"] in var.AUTH_USER_ROLES: return g.respond(401, "Unauthorized attempt.")

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
        # IF NEW USER IS NOT A SUPER USER
        if not user_role_id == 1:
            bar_id, error = validate.id(request.forms.get("bar_id"))
            if error: return g.respond(400, f"Bar {error}")
            # ONLY ALLOW THE CREATION OF USERS WITH ACCESS TO CHOSEN LOCATION
            if (not session["role_id"] == 1) and (not session["bar_id"] == bar_id):
                return g.respond(403, "Unauthorized attempt.")

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
        db_connect = pymysql.connect(**var.DB_CONFIG)
        db_connect.begin()
        cursor = db_connect.cursor()

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

        # IF NEW USER IS NOT A SUPERUSER, INSERT BAR ACCESS AS WELL, AND FETCH NEW USER
        if not user_role_id == 1:
            query = """
                INSERT INTO bar_access
                (fk_bar_id,
                fk_user_id)
                VALUES(%s, %s)
            """
            cursor.execute(query, (bar_id, user_id))
            cursor.execute("SELECT * FROM users_list WHERE user_id = %s AND bar_id = %s LIMIT 1", (user_id, bar_id))
        else:
            cursor.execute("SELECT * FROM users_list WHERE user_id = %s LIMIT 1", (user_id,))

        user = cursor.fetchone()
        db_connect.commit()

        return g.respond(201, user)
    except Exception as ex:
        print(str(ex))
        db_connect.rollback()
        if "user_email" in str(ex): return g.respond(400, "Email already exists.")
        if "user_role_id" in str(ex): return g.respond(400, "User role does not exist.")
        if "bar_id" in str(ex): return g.respond(400, "Bar does not exist.")
        return g.respond(500, "Server error.")
    finally:
        cursor.close()
        db_connect.close()