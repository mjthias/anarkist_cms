from bottle import get, response, request
import utils.vars as var
import utils.g as g
import utils.validation as validate
import pymysql
import json
import jwt

##############################
@get(f"{var.API_PATH}/users")
def _():
    if not request.get_cookie("anarkist"): return g.respond(403, "Unauthorized attempt.")
    cookie = request.get_cookie("anarkist")
    decoded_jwt = jwt.decode(cookie, var.JWT_SECRET, algorithms=["HS256"])
    if not int(decoded_jwt["role_id"]) in var.AUTH_USER_ROLES: return g.respond(403, "Unauthorized attempt.")
    
    bar_id, error = validate.id(str(decoded_jwt["bar_id"]))
    if error: return g.respond(400, error)
    offset = request.query.get("offset") if request.query.get("offset") else "0"
    offset, error = validate.offset(offset)
    if error: return g.respond(400, error)
    limit = request.query.get("limit") if request.query.get("limit") else "100"
    limit, error = validate.limit(limit)
    if error: return g.respond(400, error)

    if decoded_jwt["role_id"] == 1:
        where_clause = "WHERE bar_id = %s OR bar_id IS NULL"
    else:
        where_clause = "WHERE bar_id = %s"

    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        cursor = db_connect.cursor()

        cursor.execute(f"SELECT * FROM users_list {where_clause} LIMIT %s,%s", (bar_id, offset, limit))
        users = cursor.fetchall()

        counter = cursor.rowcount
        if not counter: return g.respond(204, "")

        response.status = 200
        return json.dumps(users)
    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error.")
    finally:
        cursor.close()
        db_connect.close()