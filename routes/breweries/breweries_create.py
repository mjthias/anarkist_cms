from bottle import get, view, redirect
import utils.validation as validate

########################################

@get("/breweries/create")
@view("breweries/create")
def _():
    session = validate.session()
    if not session: return redirect("/sign-in")

    return dict(session = session)
