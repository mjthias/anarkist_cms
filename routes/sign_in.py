from bottle import get, view, redirect, request
from utils.g import _RESPOND
from utils.vars import JWT_SECRET
import jwt

##############################
@get("/sign-in")
@view("sign_in")
def _():
    if request.get_cookie("anarkist"):
        cookie = request.get_cookie("anarkist")
        decoded_jwt = jwt.decode(cookie, JWT_SECRET, algorithms=["HS256"])

        return redirect("/")

    return 