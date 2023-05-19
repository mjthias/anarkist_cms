from bottle import put, request
import utils.g as g
import utils.vars as var
import utils.validation as validate
import pymysql

##############################
@put(f"{var.API_PATH}/users/<user_id>")
def _(user_id):
    try:
        # VALIDATE SESSION/USER
        session = validate.session()
        if not session: return g.respond(401, "Unauthorized attempt.")

        # VALIDATE ALLOWED KEYS
        allowed_keys = ["user_id", "user_name", "user_email", "user_role_id"]
        for key in request.forms.keys():
            if not key in allowed_keys: return g.respond(403, f"Forbidden key: {key}")


        # VALIDATE INPUT VALUES
        # if (not session["user_id"] == int(user_id)) and (not session["role_id"] in var.AUTH_USER_ROLES): return g.respond(401, "Unauthorized attempt.")
        user_id, error = validate.id(user_id)
        if error: return g.respond(400, error)

        is_own_user = session["user_id"] == user_id

        # Staffs can only update themselves
        if session["role_id"] == 3 and not is_own_user:
            return g.respond(401, "Unauthorized attempt  test.")
        
        user_email, error = validate.email(request.forms.get("user_email"))
        if error: return g.respond(400, error)

        user_name, error = validate.user_name(request.forms.get("user_name"))
        if error: return g.respond(400, error)
        
        # Admins and Supers can change user_role for other users
        if session["role_id"] != 3 and not is_own_user:
            user_role_id, error = validate.id(request.forms.get("user_role_id"))
            if error: return g.respond(400, f"User role {error}")

            # Admins cant update role to super users
            if session["role_id"] == 2 and user_role_id == 1:
                return g.respond(401, "Unauthorized attempt")
            
        else: user_role_id = None

    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error")
    
    # CONNECT TO DB
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        db_connect.begin()
        cursor = db_connect.cursor()

        # SELECT USER DB
        # Super users can acces super users
        if session["role_id"] == 1:
            cursor.execute("""
                SELECT * FROM users_list
                WHERE user_id = %s AND bar_id = %s
                OR user_id = %s AND user_role_id = 3
                LIMIT 1 
            """, (user_id, session["bar_id"], user_id))
        else: 
            # Other roles can't
            cursor.execute("""
                SELECT * FROM users_list
                WHERE user_id = %s AND bar_id = %s
                LIMIT 1 
            """, (user_id, session["bar_id"]))
        user = cursor.fetchone()
        if not user: return g.respond(204, "")

        # IF INPUT VALUES ARE NEW, APPEND TO USER-DICT
        if user_email != user["user_email"]: user["user_email"] = user_email
        if user_name != user["user_name"]: user["user_name"] = user_name
        # user_role_id = None if is_own_user or session-role_id = 3
        if user_role_id and user_role_id != user["user_role_id"]: user["user_role_id"] = user_role_id

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

        return g.respond(200, "User updated.")
    
    except Exception as ex:
        print(str(ex))
        db_connect.rollback()
        return g.respond(500, "Server error.")
    
    finally:
        cursor.close()
        db_connect.close()