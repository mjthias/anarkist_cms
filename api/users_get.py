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
    session = validate.session()
    if not session: return g.respond(401, "Unauthorized attempt.")
    if not int(session["role_id"]) in var.AUTH_USER_ROLES: return g.respond(401, "Unauthorized attempt.")
    
    bar_id, error = validate.id(str(session["bar_id"]))
    if error: return g.respond(400, error)
    offset, error = validate.offset(offset)
    if error: return g.respond(400, error)
    limit, error = validate.limit(limit)
    if error: return g.respond(400, error)

    if session["role_id"] == 1:
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