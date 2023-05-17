from bottle import get, redirect, request, response
from utils.g import _DELETE_SESSION, _RESPOND
import utils.vars as var
import jwt

##############################
@get("/sign-out")
def _():
    try:
        cookie = request.get_cookie("anarkist")
        decoded_jwt = jwt.decode(cookie, var.JWT_SECRET, algorithms=["HS256"])
        _DELETE_SESSION(decoded_jwt)
        response.set_cookie("anarkist", cookie, path="/", expires=0)
        return _RESPOND(200, "Successfully signed out.")
    except Exception as ex:
        print(str(ex))
        return _RESPOND(500, "Server error.")
    finally:
        redirect("/sign-in")