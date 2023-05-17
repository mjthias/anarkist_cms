from bottle import get, view, redirect, request
import utils.g as g
import utils.validation as validate

##############################
@get("/sign-in")
@view("sign_in")
def _():
    is_signed_in = validate.session()

    if is_signed_in: 
        return redirect("/")

    return