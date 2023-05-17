from bottle import get, view, redirect, request, response
import utils.g as g
import utils.vars as var
import utils.validation as validate
import pymysql
import jwt

##############################
@get("/select-location")
@view("select_location")
def _():
    #VALIDATE
    session = validate.session()
    if not session:
        return redirect("/sign-in")
    
    user_id = session["user_id"]
    role_id = session["role_id"]
    
    #CONNECT TO DB
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        cursor = db_connect.cursor()
        if role_id == 1:
            cursor.execute("SELECT bar_id, bar_name FROM bars")
        else:
            cursor.execute("""
                SELECT bar_id, bar_name FROM bar_access
                JOIN bars WHERE fk_user_id = %s AND fk_bar_id = bar_id;
                """, (user_id))
        bars = cursor.fetchall()

    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error.")
    
    finally:
        cursor.close()
        db_connect.close()

    # If only 1 bar, skip selection
    if len(bars) == 1:
        session["bar_id"] = bars[0]["bar_id"]
        encoded_jwt = jwt.encode(session, var.JWT_SECRET, algorithm="HS256")
        response.set_cookie("anarkist", encoded_jwt, path="/")
        return redirect("/")
    
    return dict(bars=bars)



