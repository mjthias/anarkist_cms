from bottle import post, redirect, request, response
import utils.g as g
import utils.vars as var
import utils.validation as validate
import json
import jwt

##############################
@post("/select-location")
def _():
    if not validate.session(): return g.respond(403, "Unauthorized attempt.")
    if not request.forms.get("bars"): return g.respond(400, "An error occured.")

    bar_id = int(request.forms.get("bars"))
    cookie = request.get_cookie("anarkist")
    decoded_jwt = jwt.decode(cookie, var.JWT_SECRET, algorithms=["HS256"])
    decoded_jwt["bar_id"] = bar_id
    encoded_jwt = jwt.encode(decoded_jwt, var.JWT_SECRET, algorithm="HS256")
    response.set_cookie("anarkist", encoded_jwt, path="/")

    if request.get_cookie("bars"):
        response.set_cookie("bars", "", path="/", expires=0)

    return redirect("/")