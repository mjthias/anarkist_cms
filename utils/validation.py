from bottle import response, request
import jwt
import time
import pymysql
import re
import utils.vars as var
import utils.g as g

##############################

def partial_session():
    if request.get_cookie("anarkist"):
        cookie = request.get_cookie("anarkist")
        decoded_jwt = jwt.decode(cookie, var.JWT_SECRET, algorithms=["HS256"])
        return decoded_jwt
    else:
        return False

##############################

def session():
    valid_session_keys = ['user_id', 'session_iat', 'user_name', 'session_id', 'role_id', 'bar_id', 'bar_name', 'bar_access']
    now = int(time.time())
    day_in_seconds = 864000

    if request.get_cookie("anarkist"):
        cookie = request.get_cookie("anarkist")
        decoded_jwt = jwt.decode(cookie, var.JWT_SECRET, algorithms=["HS256"])

        if not list(decoded_jwt.keys()) == valid_session_keys: return False

        try:
            db_connect = pymysql.connect(**var.DB_CONFIG)
            cursor = db_connect.cursor()

            cursor.execute("SELECT * FROM sessions WHERE session_id = %s LIMIT 1", (decoded_jwt["session_id"],))
            session = cursor.fetchone()
            if not session: 
                response.set_cookie("anarkist", cookie, expires=0)
                return False
        except Exception as ex:
            print(str(ex))
            return False
        finally:
            cursor.close()
            db_connect.close()

        session_iat = int(decoded_jwt["session_iat"])
        seconds_since_session_creation = now-session_iat

        if seconds_since_session_creation > day_in_seconds:
            g.delete_session(decoded_jwt)
            response.set_cookie("anarkist", cookie, expires=0)
            return False
        else:
            g.update_session(now, decoded_jwt)
            decoded_jwt["session_iat"] = now
            encoded_jwt = jwt.encode(decoded_jwt, var.JWT_SECRET, algorithm="HS256")
            response.set_cookie("anarkist", encoded_jwt, path="/")
            return decoded_jwt

    else:
        return False
    
##############################

def limit(value):
    if not value: return 100, None
    pattern = '^[1-9][0-9]*|(-1$)'
    invalid_message = "Limit must be a positive integer or '-1'."
    if not re.match(pattern, value): return None, invalid_message
    return int(value), None

##############################

def offset(value):
    if not value: return 0, None
    pattern = '^[0-9]*$'
    invalid_message = "Offset must be a positive integer."
    if not re.match(pattern, value): return None, invalid_message
    return int(value), None

##############################

def id(value):
    pattern = '^[1-9][0-9]*$'
    missing_message = "ID is missing."
    invalid_message = "ID must be a positive integer."
    if not value: return None, missing_message
    if not re.match(pattern, value): return None, invalid_message
    return int(value), None

##############################
def email(value):
    pattern = '^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    missing_message = "Email is missing."
    invalid_message = "Email is invalid"

    if not value: return None, missing_message
    value = value.strip()
    if not re.match(pattern, value): return None, invalid_message
    return str(value), None

##############################
def password(value):
    pattern = '^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'
    missing_message = "Password is missing."
    invalid_message = "Password must contain at least one uppercase letter, one lowercase letter, one digit, and a special character (#?!@$%^&*-)."
    if not value: return None, missing_message
    if not re.match(pattern, value): return None, invalid_message
    return str(value), None

##############################
def confirm_password(value1, value2):
    missing_message = "Confirm password is missing."
    mismatch_message = "Passwords does not match."
    if not value2: return None, missing_message
    value2, invalid_message = password(value2)
    if invalid_message: return None, invalid_message
    if not value1 == value2: return None, mismatch_message
    return str(value2), None

##############################
def user_name(value):
    missing_message = "User name is missing."
    invalid_min_message = f"User name must be at least {var.NAME_MIN_LEN} characters."
    invalid_max_message = f"User name must be less than {var.NAME_MAX_LEN} characters."
    if not value: return None, missing_message
    value = value.strip()
    if len(value) < var.NAME_MIN_LEN: return None, invalid_min_message
    if len(value) > var.NAME_MAX_LEN: return None, invalid_max_message
    value = value.capitalize()
    return str(value), None

##############################
def confirm_deletion(value):
    missing_message = "Confirm deletion is missing."
    invalid_message = "Please type 'DELETE' in all caps."
    if not value: return None, missing_message
    if not value == "DELETE": return None, invalid_message
    return str(value), None