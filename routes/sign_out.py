from bottle import post, redirect, request, response
from utils.g import _DELETE_SESSION, _RESPOND
from utils.vars import _JWT_SECRET
import jwt

##############################
@post("/sign-out")
def _():
    try:
        cookie = request.get_cookie("anarkist")
        decoded_jwt = jwt.decode(cookie, _JWT_SECRET, algorithms=["HS256"])
        _DELETE_SESSION(decoded_jwt)
        response.set_cookie("anarkist", cookie, path="/", expires=0)
        return redirect("/sign-in")
    except Exception as ex:
        print(str(ex))
        return _RESPOND(500, "Server error.")