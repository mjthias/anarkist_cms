from bottle import get, view, redirect, request
from utils.g import _RESPOND
from utils.vars import _DB_CONFIG, _JWT_SECRET
import utils.validation as validate
import pymysql

##############################
@get("/select-location")
@view("select_location")
def _():
    is_signed_in = validate._SESSION()

    if is_signed_in:
        if not request.get_cookie("bars"):
            try:
                db_connect = pymysql.connect(**_DB_CONFIG)
                cursor = db_connect.cursor()
                cursor.execute("SELECT bar_id, bar_name FROM bars")
                bars = cursor.fetchall()
            except Exception as ex:
                print(str(ex))
                return _RESPOND(500, "Server error.")
            finally:
                cursor.close()
                db_connect.close()
        else:
            bars = request.get_cookie("bars", secret=_JWT_SECRET)

        return dict(bars=bars)
    
    return redirect("/sign-in")
