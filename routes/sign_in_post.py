from bottle import post, redirect, request, response
from utils.g import _RESPOND
from utils.vars import _DB_CONFIG, _JWT_SECRET
import pymysql
import time
import jwt

##############################
@post("/sign-in")
def _():
    try:
        user_email = request.forms.get("user_email")
        user_password = request.forms.get("user_password")

        db_connect = pymysql.connect(**_DB_CONFIG)
        db_connect.begin()
        cursor = db_connect.cursor()

        cursor.execute("SELECT * FROM users WHERE user_email = %s LIMIT 1", (user_email))
        user = cursor.fetchone()

        if not user: return _RESPOND(400, "User does not exist.")
        if not user_password == user["user_password"]: return _RESPOND(400, "Password does not match.")

        session = {
            "fk_user_id": user["user_id"],
            "session_iat": int(time.time()),
        }

        query = """
            INSERT INTO sessions (fk_user_id, session_iat)
            VALUES(%s, %s)
        """

        cursor.execute(query, (session["fk_user_id"], session["session_iat"]))
        session["session_id"] = cursor.lastrowid

        encoded_jwt = jwt.encode(session, _JWT_SECRET, algorithm="HS256")
        response.set_cookie("anarkist", encoded_jwt, path="/")

        db_connect.commit()
        return _RESPOND(200, "Session successfully created.")
    except Exception as ex:
        print(str(ex))
        db_connect.rollback()
        return _RESPOND(500, "Server error")
    finally:
        cursor.close()
        db_connect.close()