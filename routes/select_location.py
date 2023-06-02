from bottle import get, view, redirect, response
import pymysql
import jwt
from utils import g, vars as var, validation as validate

##############################
@get("/select-location")
@view("select_location")
def _():
    #VALIDATE
    session = validate.partial_session()
    if not session:
        return redirect("/sign-in")

    user_id = session["user_id"]
    role_id = session["role_id"]

    #CONNECT TO DB
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        cursor = db_connect.cursor()
        if role_id == 1:
            cursor.execute("SELECT * FROM bars")
        else:
            cursor.execute("""
                SELECT * FROM bar_access
                JOIN bars WHERE fk_user_id = %s 
                AND fk_bar_id = bar_id;
                """, (user_id))
        bars = cursor.fetchall()
        print(bars)

    except Exception as ex:
        print(str(ex))
        return g.error_view(500)

    finally:
        cursor.close()
        db_connect.close()

    # If only 1 bar, skip selection
    if len(bars) == 1:
        session["bar_id"] = bars[0]["bar_id"]
        session["bar_name"] = bars[0]["bar_name"]
        session["bar_access"] = bars
        encoded_jwt = jwt.encode(session, var.JWT_SECRET, algorithm="HS256")
        response.set_cookie("anarkist", encoded_jwt, path="/")
        return redirect("/")

    session["bar_access"] = bars
    encoded_jwt = jwt.encode(session, var.JWT_SECRET, algorithm="HS256")
    response.set_cookie("anarkist", encoded_jwt, path="/")

    return dict(bars=bars)
