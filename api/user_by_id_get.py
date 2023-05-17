from bottle import get, response, request
import utils.vars as var
import utils.g as g
import utils.validation as validate
import pymysql
import json
import jwt

##############################
@get(f"{var.API_PATH}/users/<user_id>")
def _(user_id=""):
    if not request.get_cookie("anarkist"): return g.respond(401, "Unauthorized attempt.")
    cookie = request.get_cookie("anarkist")
    decoded_jwt = jwt.decode(cookie, var.JWT_SECRET, algorithms=["HS256"])
    # Something with vars.AUTH_USER_ROLES

    try:
        user_id, error = validate.id(user_id)
        if error: return g.respond(400, error)

        response.status = 200
        response.content_type = "application/json"
        return user_id
    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error.")