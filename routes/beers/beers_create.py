from bottle import get, view, redirect
from utils import validation as validate

##############################
@get("/beers/create")
@view("beers/create")
def _():

    # VALIDATE SESSION
    session = validate.session()
    if not session:
        return redirect("/sign-in")

    return dict(session=session)
