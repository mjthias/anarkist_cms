# pylint: disable=R1710,C0123
import json
from bottle import response, view, request
import pymysql
from utils import vars as var

##############################
def respond(status = 400, data = None):
    if not data:
        data = set_response_message(status)
    response.content_type = 'application/json'
    response.status = status
    if type(data) is str:
        return json.dumps({ "info": data })
    return json.dumps(data)

##############################
@view("error")
def error_view(status=404, info = None):
    if not info:
        info  = set_response_message(status)
    error = {}
    error["code"] = status
    error["info"] = info
    error["page_url"] = request.path
    response.status = status
    return dict(error = error)

##############################
def set_response_message(status):
    if status == 404:
        return "Page not found"
    if status == 400:
        return "Client error"
    if status == 401:
        return "Access denied"
    if status == 500:
        return "Server error"
    if status == 204:
        return ""
    if status == 201:
        return "Row created"
    if status == 200:
        return "Success"
    return "No message"

##############################
def delete_session(session=None):
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        cursor = db_connect.cursor()

        cursor.execute("""
        DELETE FROM sessions WHERE session_id =%s
        """, (session["session_id"],))

        counter = cursor.rowcount
        if not counter:
            response.set_cookie("anarkist", "", expires=0)

        db_connect.commit()
        return

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
    return format(value, ".2f")

##############################
def to_menu_name(value):
    return value.replace("å", "aa").replace("Å", "Aa").replace("ø", "oe").replace("Ø", "Oe").replace("æ", "ae").replace("Æ", "Ae").replace("ö", "o").replace("Ö", "O")
    