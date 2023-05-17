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
    session = validate.session()
    if not request.get_cookie("anarkist"): return g.respond(401, "Unauthorized attempt.")
    if not session["role_id"] in var.AUTH_USER_ROLES: return g.respond(401, "Unauthorized attempt.")

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
        if not user_role_id == 1:
            bar_id, error = validate.id(request.forms.get("bar_id"))
            if error: return g.respond(400, f"Bar {error}")
            if (not session["role_id"] == 1) and (not session["bar_id"] == bar_id):
                return g.respond(403, "Unauthorized attempt.")

        
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

        response.status = 201
        response.content_type = "Application/json"
        return json.dumps(user)
    except Exception as ex:
        print(str(ex))
        db_connect.rollback()
        if "user_email" in str(ex): return g.respond(400, "Email already exists.")
        if "user_role_id" in str(ex): return g.respond(400, "User role does not exists.")
        if "bar_id" in str(ex): return g.respond(400, "Bar does not exists.")
        return g.respond(500, "Server error.")
    finally:
        cursor.close()
        db_connect.close()