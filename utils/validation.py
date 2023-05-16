from bottle import response, request
import jwt
import time
import pymysql
import re
from utils.vars import _DB_CONFIG, _JWT_SECRET
from utils.g import _DELETE_SESSION, _UPDATE_SESSION, _RESPOND

##############################

def _SESSION():
    now = int(time.time())
    day_in_seconds = 864000

    if request.get_cookie("anarkist"):
        cookie = request.get_cookie("anarkist")
        decoded_jwt = jwt.decode(cookie, _JWT_SECRET, algorithms=["HS256"])

        try:
            db_connect = pymysql.connect(**_DB_CONFIG)
            cursor = db_connect.cursor()

            cursor.execute("SELECT * FROM sessions WHERE session_id = %s LIMIT 1", (decoded_jwt["session_id"],))
            session = cursor.fetchone()
            if not session: 
                response.set_cookie("anarkist", cookie, expires=0)
                return False
        except Exception as ex:
            print(str(ex))
            return _RESPOND(500, "Server error.")
        finally:
            cursor.close()
            db_connect.close()

        session_iat = int(decoded_jwt["session_iat"])
        seconds_since_session_creation = now-session_iat

        if seconds_since_session_creation > day_in_seconds:
            _DELETE_SESSION(decoded_jwt)
            response.set_cookie("anarkist", cookie, expires=0)
        else:
            _UPDATE_SESSION(now, decoded_jwt)
            decoded_jwt["session_iat"] = now
            encoded_jwt = jwt.encode(decoded_jwt, _JWT_SECRET, algorithm="HS256")
            response.set_cookie("anarkist", encoded_jwt, path="/")
            return True

    else:
        return False
    
##############################

def _LIMIT(value):
    pattern = '^[1-9][0-9]*|(-1$)'
    invalid_message = "Limit must be a positive integer or '-1'."
    if not re.match(pattern, value): return None, invalid_message
    return int(value), None

##############################

def _OFFSET(value):
    pattern = '^[0-9]*$'
    invalid_message = "Offset must be a positive integer."
    if not re.match(pattern, value): return None, invalid_message
    return int(value), None

##############################

def _ID(value):
    pattern = '^[1-9][0-9]*$'
    invalid_message = "ID must be a positive integer."
    if not re.match(pattern, value): return None, invalid_message
    return int(value), None