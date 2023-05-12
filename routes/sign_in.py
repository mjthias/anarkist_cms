from bottle import get, view, redirect, request
from utils.g import _RESPOND
import utils.validation as validate

##############################
@get("/sign-in")
@view("sign_in")
def _():
    is_signed_in = validate._SESSION()

    if is_signed_in: 
        return redirect("/")

    return