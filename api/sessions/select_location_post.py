from bottle import post, request, response
import jwt
import pymysql
from utils import g, vars as var, validation as validate

##############################
@post("/select-location")
def _():
    try:
        # VALIDATE
        session = validate.partial_session()
        if not session:
            return g.respond(401)

        bar_id, error = validate.id(request.forms.get("bar_id"))
        if error:
            return g.respond(400, error)

    except Exception as ex:
        print(str(ex))
        return g.respond(500)

    try:
        # Check if bar exists in DB
        db_conn = pymysql.connect(**var.DB_CONFIG)
        cursor = db_conn.cursor()

        if session["role_id"] == 1:
            cursor.execute("""
            SELECT * FROM bars
            WHERE bar_id = %s
            LIMIT 1
            """, (bar_id))
        else:
            cursor.execute("""
            SELECT bars.* FROM bars
            JOIN bar_access
            WHERE bar_id = %s 
            AND fk_bar_id = bar_id 
            AND fk_user_id = %s
            LIMIT 1
            """, (bar_id, session["user_id"]))
        bar = cursor.fetchone()
        if not bar:
            return g.respond(401)

        # Append bar id to session dict
        session["bar_id"] = bar_id
        for bar in session["bar_access"]:
            if bar["bar_id"] == bar_id:
                session["bar_name"] = bar["bar_name"]

        session = {
            "user_id": session["user_id"],
            "session_iat": session["session_iat"],
            "user_name": session["user_name"],
            "session_id": session["session_id"],
            "role_id": session["role_id"],
            "bar_id": session["bar_id"],
            "bar_name": session["bar_name"],
            "bar_access": session["bar_access"]
        }

        encoded_jwt = jwt.encode(session, var.JWT_SECRET, algorithm="HS256")
        response.set_cookie("anarkist", encoded_jwt, path="/")

        return g.respond(200, "Location successfully selected.")

    except Exception as ex:
        print(str(ex))
        return g.respond(500)

    finally:
        cursor.close()
        db_conn.close()
