from bottle import put, request, response
import pymysql
import jwt
from utils import g, vars as var, validation as validate

##############################

@put(f"{var.API_PATH}/users/<user_id>")
def _(user_id):
    try:
        # VALIDATE SESSION/USER
        session = validate.session()
        if not session:
            return g.respond(401)

        # VALIDATE INPUT VALUES
        user_id, error = validate.id(user_id)
        if error:
            return g.respond(400, error)

        if not user_id == session["user_id"] and user_id == 3:
            return g.respond(401)

        is_own_user = session["user_id"] == user_id

        # Staffs can only update themselves
        if session["role_id"] == 3 and not is_own_user:
            return g.respond(401)

        user_email, error = validate.email(request.forms.get("user_email"))
        if error:
            return g.respond(400, {"info": error, "key": "user_email"})

        user_name, error = validate.user_name(request.forms.get("user_name"))
        if error:
            return g.respond(400, {"info": error, "key": "user_name"})

        # Admins and Supers can change user_role for other users
        if session["role_id"] != 3 and not is_own_user:
            user_role_id, error = validate.role_id(request.forms.get("user_role_id"))
            if error:
                return g.respond(400, {"info": error, "key": "user_role_id"})

            # Admins cant update role to super users
            if session["role_id"] == 2 and user_role_id == 1:
                return g.respond(401)

        else: user_role_id = None

    except Exception as ex:
        print(str(ex))
        return g.respond(500)

    # CONNECT TO DB
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        db_connect.begin()
        cursor = db_connect.cursor()

        # SELECT USER DB
        cursor.execute("""
        SELECT * FROM users_list
        WHERE user_id = %s AND user_role_id >= %s
        LIMIT 1 
        """, (user_id, session["role_id"]))
        user = cursor.fetchone()
        if not user:
            return g.respond(204)

        # IF INPUT VALUES ARE NEW, APPEND TO USER-DICT
        if user_email != user["user_email"]:
            user["user_email"] = user_email
        if user_name != user["user_name"]:
            user["user_name"] = user_name
        if user_role_id and user_role_id != user["user_role_id"]:
            # can't update own role, admins cant make super user
            if is_own_user == 3 or user_role_id == 1 and session["role_id"] == 2:
                return g.respond(401)
            user["user_role_id"] = user_role_id

        cursor.execute("""
        UPDATE users
        SET user_email = %s,
        user_name = %s,
        fk_user_role_id = %s
        WHERE user_id = %s
        """, (user["user_email"], user["user_name"], user["user_role_id"], user["user_id"]))
        counter = cursor.rowcount
        if not counter:
            return g.respond(204)

        # Rm session if other user
        if not is_own_user:
            cursor.execute("""
            DELETE FROM sessions
            WHERE fk_user_id = %s
            """, (user["user_id"]))
        else:
            session["user_email"] = user["user_email"]
            session["user_name"] = user["user_name"]
            print(session)
            encoded_jwt = jwt.encode(session, var.JWT_SECRET, algorithm="HS256")
            response.set_cookie("anarkist", encoded_jwt, path="/")

        db_connect.commit()

        response_dict = {"name": user_name, "info": "User was successfully updated."}

        return g.respond(200, response_dict)

    except Exception as ex:
        print(str(ex))
        db_connect.rollback()
        if "user_email" in str(ex):
            return g.respond(400, {"info": "Email already exists.", "key": "user_email"})
        if "user_role_id" in str(ex):
            return g.respond(400, {"info": "User role does not exist.", "key": "user_role_id"})
        if "bar_id" in str(ex):
            return g.respond(400, {"info": "Bar does not exist"})
        return g.respond(500)

    finally:
        cursor.close()
        db_connect.close()
