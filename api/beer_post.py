from  bottle import post, request
import utils.vars as var
import utils.g as g
import utils.validation as validate
import pymysql

##############################
@post(f"{var.API_PATH}/beers")
def _():
    # VALIDATE SESSION
    session = validate.session()
    if not session: return g.respond(401, "Unauthorized attempt.")

    try:
        return g.respond(201, "Beer created")
    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error.")