from bottle import post, redirect, request, response
import utils.g as g
import utils.vars as var
import utils.validation as validate
import json
import jwt

##############################
@post("/select-location")
def _():
    # VALIDATE
    session = validate.session()
    if not session: return g.respond(403, "Unauthorized attempt.")

    bar_id, error = validate.id(request.forms.get("bars"))
    if error: return g.respond(400, error)

    # Append bar id to session dict
    session["bar_id"] = bar_id
    encoded_jwt = jwt.encode(session, var.JWT_SECRET, algorithm="HS256")
    response.set_cookie("anarkist", encoded_jwt, path="/")

    return redirect("/")