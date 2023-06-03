import time
from bottle import post, request, response
import pymysql
import jwt
import bcrypt
from utils import g, vars as var, validation as validate

##############################
@post("/sign-in")
def _():
    # VALIDATE INPUT VALUES
    try:
        user_email, error = validate.email(request.forms.get("user_email"))
        if error:
            return g.respond(400, error)

        user_password, error = validate.password(request.forms.get("user_password"))
        if error:
            return g.respond(400, error)
        user_password_bytes = user_password.encode('utf-8')

    except Exception as ex:
        print(str(ex))
        return g.respond(500)

    try:
        # POST TO DB
        db_connect = pymysql.connect(**var.DB_CONFIG)
        cursor = db_connect.cursor()

        # Get users from db
        cursor.execute("""
        SELECT * FROM users 
        WHERE user_email = %s
        LIMIT 1
        """, (user_email))
        user = cursor.fetchone()

        # Validate password
        if not user or not bcrypt.checkpw(user_password_bytes, str(user['user_password']).encode('utf-8')):
            return g.respond(400, "Invalid email or password.")

        # Create session
        session = {
            "user_id": user["user_id"],
            "session_iat": int(time.time()),
        }

        # Insert to DB
        cursor.execute("""
        CALL insert_session(%s,%s)
        """, (session["user_id"], session["session_iat"]))
        session["session_id"] = cursor.fetchone()["session_id"]
        db_connect.commit()

        # Append the remaininig values to session-dict
        session["user_name"] = user["user_name"]
        session["role_id"] = user["fk_user_role_id"]

        encoded_jwt = jwt.encode(session, var.JWT_SECRET, algorithm="HS256")
        response.set_cookie("anarkist", encoded_jwt, path="/")
        return g.respond(201, "Successfully signed in.")

    except Exception as ex:
        print(ex)
        return g.respond(500)

    finally:
        cursor.close()
        db_connect.close()
