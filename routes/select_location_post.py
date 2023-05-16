from bottle import post, redirect, request, response
from utils.g import _RESPOND
from utils.vars import _JWT_SECRET
import utils.validation as validate
import json
import jwt

##############################
@post("/select-location")
def _():
    if not validate._SESSION(): return _RESPOND(403, "Unauthorized attempt.")
    if not request.forms.get("bars"): return _RESPOND(400, "An error occured.")

    bar_id = int(request.forms.get("bars"))
    cookie = request.get_cookie("anarkist")
    decoded_jwt = jwt.decode(cookie, _JWT_SECRET, algorithms=["HS256"])
    decoded_jwt["bar_id"] = bar_id
    encoded_jwt = jwt.encode(decoded_jwt, _JWT_SECRET, algorithm="HS256")
    response.set_cookie("anarkist", encoded_jwt, path="/")

    if request.get_cookie("bars"):
        response.set_cookie("bars", "", path="/", expires=0)

    return redirect("/")