from bottle import get, response, request
from utils.vars import _AUTH_USER_ROLES, _DB_CONFIG, _API_PATH, _JWT_SECRET
from utils.g import _RESPOND
import utils.validation as validate
import pymysql
import json
import jwt

##############################
@get(f"{_API_PATH}/users")
def _():
    if not request.get_cookie("anarkist"): return _RESPOND(403, "Unauthorized attempt.")
    cookie = request.get_cookie("anarkist")
    decoded_jwt = jwt.decode(cookie, _JWT_SECRET, algorithms=["HS256"])
    if not int(decoded_jwt["user_role"]) in _AUTH_USER_ROLES: return _RESPOND(403, "Unauthorized attempt.")
    
    bar_id, error = validate._ID(str(decoded_jwt["bar_id"]))
    if error: return _RESPOND(400, error)
    offset = request.query.get("offset") if request.query.get("offset") else "0"
    offset, error = validate._OFFSET(offset)
    if error: return _RESPOND(400, error)
    limit = request.query.get("limit") if request.query.get("limit") else "100"
    limit, error = validate._LIMIT(limit)
    if error: return _RESPOND(400, error)

    if decoded_jwt["user_role"] == 1:
        where_clause = "WHERE bar_id = %s OR bar_id IS NULL"
    else:
        where_clause = "WHERE bar_id = %s"

    try:
        db_connect = pymysql.connect(**_DB_CONFIG)
        cursor = db_connect.cursor()

        cursor.execute(f"SELECT * FROM users_list {where_clause} LIMIT %s,%s", (bar_id, offset, limit))
        users = cursor.fetchall()

        counter = cursor.rowcount
        if not counter: return _RESPOND(204, "")

        response.status = 200
        return json.dumps(users)
    except Exception as ex:
        print(str(ex))
        return _RESPOND(500, "Server error.")
    finally:
        cursor.close()
        db_connect.close()