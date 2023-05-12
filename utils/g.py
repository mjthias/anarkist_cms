from bottle import response
import pymysql
from utils.vars import _DB_CONFIG

##############################
def _RESPOND(status = 400, error_message = "Unknown error"):
    response.status = status
    return {
        "info": error_message
    }

##############################
def _DELETE_SESSION(session=None):
    try:
        db_connect = pymysql.connect(**_DB_CONFIG)
        cursor = db_connect.cursor()

        cursor.execute("DELETE FROM sessions WHERE session_id =%s", (session["session_id"],))
        
        counter = cursor.rowcount
        if not counter: 
            print("No sessions to delete.")
            response.set_cookie("anarkist", "", expires=0)
        
        db_connect.commit()
        print(f"Rows deleted: {counter}")
    except Exception as ex:
        print(str(ex))
        return _RESPOND(500, "Server error.")
    finally:
        cursor.close()
        db_connect.close()

##############################
def _UPDATE_SESSION(now=0, session=None):
    try:
        db_connect = pymysql.connect(**_DB_CONFIG)
        cursor = db_connect.cursor()

        cursor.execute("""
            UPDATE sessions
            SET session_iat = %s
            WHERE session_id = %s
        """, (now, session["session_id"]))

        counter = cursor.rowcount
        if not counter: 
            print("No sessions to update.")
        
        db_connect.commit()
        print(f"Rows updated: {counter}")
    except Exception as ex:
        print(str(ex))
        _RESPOND(500, "Server error.")
    finally:
        cursor.close()
        db_connect.close()