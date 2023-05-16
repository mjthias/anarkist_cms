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

        cursor.execute("SELECT * FROM sign_in_users_list WHERE user_email = %s", (user_email))
        users = cursor.fetchall()

        if not users: return _RESPOND(400, "User does not exist.")
        if not user_password == users[0]["user_password"]: return _RESPOND(400, "Password does not match.")

        session = {
            "fk_user_id": users[0]["user_id"],
            "session_iat": int(time.time()),
        }

        query = """
            INSERT INTO sessions (fk_user_id, session_iat)
            VALUES(%s, %s)
        """

        cursor.execute(query, (session["fk_user_id"], session["session_iat"]))
        db_connect.commit()

        session["session_id"] = cursor.lastrowid
        session["user_role"] = users[0]["user_role_id"]
        
    except Exception as ex:
        print(ex)
        db_connect.rollback()
        return _RESPOND(500, "Server error")
    finally:
        cursor.close()
        db_connect.close()

    if len(users) > 1 or users[0]["user_role_id"] == 1:
        encoded_jwt = jwt.encode(session, _JWT_SECRET, algorithm="HS256")
        response.set_cookie("anarkist", encoded_jwt, path="/")

        if users[0]["user_role_id"] != 1:
            bars = []
            for user in users:
                bar = {
                    "bar_id": user['bar_id'],
                    "bar_name": user['bar_name']
                }
                bars.append(bar)
            response.set_cookie("bars", bars, _JWT_SECRET, path="/")

        return redirect("/select-location")
        
    if len(users) == 1:
        session["bar_id"] = users[0]["bar_id"]
        encoded_jwt = jwt.encode(session, _JWT_SECRET, algorithm="HS256")
        response.set_cookie("anarkist", encoded_jwt, path="/")
        return redirect("/")