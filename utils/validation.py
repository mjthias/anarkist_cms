# pylint: disable=W1401,W0622
import imghdr
import uuid
import os
import re
import time
from bottle import response, request
import jwt
import pymysql
from utils import g, vars as var

##############################

def partial_session():
    if request.get_cookie("anarkist"):
        cookie = request.get_cookie("anarkist")
        decoded_jwt = jwt.decode(cookie, var.JWT_SECRET, algorithms=["HS256"])
        return decoded_jwt

    return False

##############################

def session():
    valid_session_keys = ['user_id', 'session_iat', 'user_name', 'session_id', 'role_id', 'bar_id', 'bar_name', 'bar_access']
    now = int(time.time())
    day_in_seconds = 864000

    if request.get_cookie("anarkist"):
        cookie = request.get_cookie("anarkist")
        decoded_jwt = jwt.decode(cookie, var.JWT_SECRET, algorithms=["HS256"])

        for key in valid_session_keys:
            if key not in decoded_jwt:
                return False

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

        g.update_session(now, decoded_jwt)
        decoded_jwt["session_iat"] = now
        encoded_jwt = jwt.encode(decoded_jwt, var.JWT_SECRET, algorithm="HS256")
        response.set_cookie("anarkist", encoded_jwt, path="/")
        return decoded_jwt

    return False

##############################

def limit(value):
    invalid_message = "Limit must be a positive integer or '-1'."
    if value in (0, '0'):
        return None, invalid_message
    if not value:
        return 50, None
    pattern = '^[1-9][0-9]*|(-1$)'
    value = str(value)
    if not re.match(pattern, value):
        return None, invalid_message
    return int(value), None

##############################

def offset(value):
    if not value:
        return 0, None
    pattern = '^[0-9]*$'
    invalid_message = "Offset must be a positive integer."
    value = str(value)
    if not re.match(pattern, value):
        return None, invalid_message
    return int(value), None

##############################

def id(value):
    pattern = '^[1-9][0-9]*$'
    missing_message = "ID is missing."
    invalid_message = "ID must be a positive integer."
    invalid_max_message = "ID can't be higher than 18446744073709551615."
    if not value:
        return None, missing_message
    value = str(value)
    if not re.match(pattern, value):
        return None, invalid_message
    if int(value) > 18446744073709551615:
        return None, invalid_max_message
    return int(value), None

##############################

def role_id(value):
    missing_message = "Role id is missing."
    invalid_message = "Role id must be a integer between 1 and 3."
    if not value:
        return None, missing_message

    try:
        if int(value) < 1 or int(value) > 3:
            return None, invalid_message

    except:
        return None, invalid_message
    return int(value), None

##############################
def email(value):
    pattern = '^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,3}))$'
    missing_message = "Email is missing."
    invalid_message = "Email is invalid"
    if not value:
        return None, missing_message
    value = value.strip()
    if not re.match(pattern, value):
        return None, invalid_message
    value = value.lower()
    return str(value), None

##############################
def password(value):
    pattern = '^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'
    missing_message = "Password is missing."
    invalid_message = "Password must contain at least one uppercase letter, one lowercase letter, one digit, and a special character (#?!@$%^&*-)."
    invalid_max_message = "Passwords can't extend 72 characters"
    if not value:
        return None, missing_message
    if not re.match(pattern, value):
        return None, invalid_message
    if len(value) > 72:
        return None, invalid_max_message
    return str(value), None

##############################
def confirm_password(value1, value2):
    missing_message = "Confirm password is missing."
    mismatch_message = "Passwords does not match."
    if not value2:
        return None, missing_message
    value2, invalid_message = password(value2)
    if invalid_message:
        return None, invalid_message
    if not value1 == value2:
        return None, mismatch_message
    return str(value2), None

##############################
def user_name(value):
    value = str(value)
    missing_message = "User name is missing."
    invalid_min_message = f"User name must be at least {var.NAME_MIN_LEN} characters."
    invalid_max_message = f"User name must be less than {var.NAME_MAX_LEN} characters."
    invalid_message = "Names can only consist of alphabetic characters, spaces and '-'"
    if not value:
        return None, missing_message
    value = value.strip()
    if len(value) < var.NAME_MIN_LEN:
        return None, invalid_min_message
    if len(value) > var.NAME_MAX_LEN:
        return None, invalid_max_message
    pattern = "^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$"
    if not re.match(pattern, value):
        return None, invalid_message
    return str(value), None

##############################
def brewery_name(value):
    missing_message = "Brewery name is missing."
    invalid_min_message = f"Brewery name must be at least {var.NAME_MIN_LEN} characters."
    invalid_max_message = f"Brewery name must be less than {var.NAME_MAX_LEN} characters."
    invalid_message = "Brewery name can only consist of alphabetic characters, spaces and '-'"
    if not value:
        return None, missing_message
    value = value.strip()
    if len(value) < var.NAME_MIN_LEN:
        return None, invalid_min_message
    if len(value) > var.NAME_MAX_LEN:
        return None, invalid_max_message
    pattern = "^[a-zA-Z0-9àáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$"
    if not re.match(pattern, value):
        return None, invalid_message
    return str(value), None

##############################
def brewery_menu_name(value1, value2):
    name_too_long_message = "Brewery name is too long for menu. Please provide a short menu name."
    if not value2:
        if len(value1) > 50:
            return None, name_too_long_message
        return value1, None

    menu_name_too_long_message = "Menu name can't be longer than the actual name."
    invalid_min_message = f"Brewery menu name must be at least {var.NAME_MIN_LEN} characters."
    invalid_max_message = "Brewery menu name must be less than 50 characters."
    invalid_message = "Brewery menu name can only consist of alphabetic characters, spaces and '-'"
    value2 = value2.strip()
    if len(value2) > len(value1):
        return None, menu_name_too_long_message
    if len(value2) < var.NAME_MIN_LEN:
        return None, invalid_min_message
    if len(value2) > 50:
        return None, invalid_max_message
    pattern = "^[a-zA-Z0-9àáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$"
    if not re.match(pattern, value2):
        return None, invalid_message
    return str(value2), None

##############################
def confirm_deletion(value):
    missing_message = "Confirm deletion is missing."
    invalid_message = "Please type 'DELETE' in all caps."
    if not value:
        return None, missing_message
    if not value == "DELETE":
        return None, invalid_message
    return str(value), None

##############################
def name(value):
    missing_message = "Name is missing."
    invalid_min_message = f"Name must be at least {var.NAME_MIN_LEN} characters."
    invalid_max_message = f"Name must be less than {var.NAME_MAX_LEN} characters."
    if not value:
        return None, missing_message
    value = value.strip()
    if len(value) < var.NAME_MIN_LEN:
        return None, invalid_min_message
    if len(value) > var.NAME_MAX_LEN:
        return None, invalid_max_message
    return str(value), None

##############################
def street(value):
    pattern = '^[A-Za-zÆØÅæøå]{0,}[ ]{1}[1-9]{1}[0-9A-Za-z \,\.]{0,}$'
    missing_message = "Street is missing."
    invalid_min_message = f"Street must be at least {var.NAME_MIN_LEN} characters."
    invalid_max_message = f"Street must be less than {var.NAME_MAX_LEN} characters."
    invalid_message = "Street must contain at least 1 character and 1 digit."
    if not value:
        return None, missing_message
    value = value.strip()
    if len(value) < var.NAME_MIN_LEN:
        return None, invalid_min_message
    if len(value) > var.NAME_MAX_LEN:
        return None, invalid_max_message
    if not re.match(pattern, value):
        return None, invalid_message
    return str(value), None

##############################
def city(value):
    pattern = '^[A-Za-zÆØÅæøå]{0,}[\s]?[A-Za-zÆØÅæøå]{0,}$'
    missing_message = "City is missing."
    invalid_min_message = f"City must be at least {var.NAME_MIN_LEN} characters."
    invalid_max_message = f"City must be less than {var.NAME_MAX_LEN} characters."
    invalid_message = "City can only contain alphabetical characters."
    if not value:
        return None, missing_message
    value = value.strip()
    if len(value) < var.NAME_MIN_LEN:
        return None, invalid_min_message
    if len(value) > var.NAME_MAX_LEN:
        return None, invalid_max_message
    if not re.match(pattern, value):
        return None, invalid_message
    return str(value), None

##############################
def zip_code(value):
    if not value:
        return None, "Zip code missing"
    pattern = '^[1-9][0-9]{3}$'
    invalid_message = "Zip code is a 4 digit integer, between 1000 and 9990"
    if not re.match(pattern, value):
        return None, invalid_message
    if int(value) > 9990:
        return None, invalid_message
    return str(value), None

##############################
def ebc(value):
    if not value:
        return None, None
    pattern = '^[0-9]*$'
    invalid_message = "EBC must be an integer between 1 and 600."
    if not re.match(pattern, value):
        return None, invalid_message
    if int(value) > 600:
        return None, invalid_message
    if int(value) < 1:
        return None, invalid_message
    return str(value), None

##############################
def ibu(value):
    if not value:
        return None, None
    pattern = '^[0-9]*$'
    invalid_message = "IBU must be an integer between 1 and 600."
    if not re.match(pattern, value):
        return None, invalid_message
    if int(value) > 600:
        return None, invalid_message
    if int(value) < 1:
        return None, invalid_message
    return str(value), None

##############################
def alc(value):
    missing_message = "Alcohol percentage is missing"
    invalid_min_message = "Alcohol percentage must be a positive value."
    invalid_max_message = "Alcohol percentage must be less than 100."
    if not value:
        return None, missing_message
    value = str(value).replace(",", ".")
    value = float(value)
    if value < 0:
        return None, invalid_min_message
    if value > 100:
        return None, invalid_max_message
    return format(value, '.2f'), None

##############################
def price(value):
    missing_message = "Price is missing."
    invalid_message = "Price must be at least 0 DKK."
    if not value:
        return None, missing_message
    value = str(value).replace(",", ".")
    try:
        value = float(value)
    except:
        return None, invalid_message

    if value < 0:
        return None, invalid_message
    return value, None

##############################
def description(value):
    if not value:
        return None, None
    pattern = "^[a-zA-Z0-9àáâäãåæąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÆÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$"
    min_len = 2
    max_len = 500
    invalid_min_message = f"Description must be more than {min_len} characters."
    invalid_max_message = f"Description must be less than {max_len} characters."
    invalid_message = 'Description can only have alphanumeric characters, and the special characters ",.-\'".'
    value = value.strip()
    if len(value) < min_len:
        return None, invalid_min_message
    if len(value) > max_len:
        return None, invalid_max_message
    if not re.match(pattern, value):
        return None, invalid_message
    return value, None

##############################
def image(image):
    allowed_file_types = [".png", ".jpeg", ".jpg"]
    file_name, file_extension = os.path.splitext(image.filename)

    if file_extension not in allowed_file_types:
        return None, "Filetype is not allowed."
    if file_extension == ".jpg":
        file_extension = ".jpeg"

    file_name = f"{str(uuid.uuid4())}{file_extension}"
    file_path = f"{var.IMAGE_PATH}{file_name}"
    image.save(file_path)
    imghdr_extension = imghdr.what(file_path)
    if not file_extension == f".{imghdr_extension}":
        os.remove(file_path)
        return None, "Suspicious image."
    return file_name, None
    