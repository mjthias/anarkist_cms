from bottle import get, view, redirect, request
import utils.g as g
import utils.validation as validate

##############################
@get("/sign-in")
@view("sign_in")
def _():
    session = validate.session()

    if session: 
        return redirect("/")

    return