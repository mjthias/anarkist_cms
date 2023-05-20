from bottle import response
import pymysql
import utils.vars as var
import json

##############################
def respond(status = 400, data = "Unknown error"):
    response.content_type = 'application/json'
    response.status = status
    if type(data) is str:
        return json.dumps({ "info": data })
    return json.dumps(data)

##############################
def delete_session(session=None):
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
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
        return respond(500, "Server error.")
    finally:
        cursor.close()
        db_connect.close()

##############################
def update_session(now=0, session=None):
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
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
        print(f"Sessions updated: {counter}")
    except Exception as ex:
        print(str(ex))
        respond(500, "Server error.")
    finally:
        cursor.close()
        db_connect.close()

##############################
def format_price(value):
    seperator_index = str(value).index(".")
    if str(value)[seperator_index+1:] == "0":
        return format(value, ".0f")
    else:
        return format(value, ".2f")