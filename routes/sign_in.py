# pylint: disable=R1710
from bottle import get, view, redirect
from utils import validation as validate

##############################
@get("/sign-in")
@view("sign_in")
def _():
    session = validate.session()

    if session:
        return redirect("/")

    return
