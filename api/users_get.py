from bottle import get, response, request
from utils.vars import _DB_CONFIG, _API_PATH, _JWT_SECRET
from utils.g import _RESPOND
import pymysql
import json
import jwt

authorized_user_roles = [1, 2]

##############################
@get(f"{_API_PATH}/users")
def _():
    if not request.get_cookie("anarkist"): return _RESPOND(403, "Unauthorized attempt.")
    cookie = request.get_cookie("anarkist")
    decoded_jwt = jwt.decode(cookie, _JWT_SECRET, algorithms=["HS256"])
    if not int(decoded_jwt["user_role"]) in authorized_user_roles: return _RESPOND(403, "Unauthorized attempt.")
    
    try:
        db_connect = pymysql.connect(**_DB_CONFIG)
        cursor = db_connect.cursor()

        limit = int(request.query.get("limit")) if request.query.get("limit") else 10
        offset = int(request.query.get("offset")) if request.query.get("offset") else 0
        if int(decoded_jwt["user_role"]) == 1:
            where_clause = "WHERE bar_id = %s OR bar_id IS NULL"
        else:
            where_clause = "WHERE bar_id = %s"

        bar_id = int(decoded_jwt["bar_id"])
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