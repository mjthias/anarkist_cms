from bottle import post, redirect, request, response
import utils.g as g
import utils.vars as var
import utils.validation as validate
import pymysql
import time
import jwt
import bcrypt

##############################
@post("/sign-in")
def _():
    # VALIDATE INPUT VALUES
    try:
        user_email, error = validate.email(request.forms.get("user_email"))
        if error: return g.respond(400, error)
        user_password, error = validate.password(request.forms.get("user_password"))
        if error: return g.respond(400, error)
        user_password_bytes = user_password.encode('utf-8')

    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error.")

    # CONNTECT TO DB
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        db_connect.begin()
        cursor = db_connect.cursor()

        # Get users from db
        cursor.execute("SELECT * FROM sign_in_users_list WHERE user_email = %s", (user_email))
        users = cursor.fetchall()

        # Validate password
        if not users: return g.respond(400, "Invalid email or password.")
        if not bcrypt.checkpw(user_password_bytes, str(users[0]['user_password']).encode('utf-8')): 
            return g.respond(400, "Invalid email or password.")

        # Create session
        session = {
            "user_id": users[0]["user_id"],
            "session_iat": int(time.time()),
        }

        # Insert to DB
        query = """
            INSERT INTO sessions (fk_user_id, session_iat)
            VALUES(%s, %s)
        """
        cursor.execute(query, (session["user_id"], session["session_iat"]))
        db_connect.commit()

        # Append the remaininig values to session-dict
        session["session_id"] = cursor.lastrowid
        session["role_id"] = users[0]["user_role_id"]

    except Exception as ex:
        print(ex)
        db_connect.rollback()
        return g.respond(500, "Server error")
    
    finally:
        cursor.close()
        db_connect.close()


    encoded_jwt = jwt.encode(session, var.JWT_SECRET, algorithm="HS256")
    response.set_cookie("anarkist", encoded_jwt, path="/")
    return redirect("/select-location")