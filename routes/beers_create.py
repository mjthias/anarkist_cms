from bottle import get, view, redirect
import utils.validation as validate

##############################
@get("/beers/create")
@view("beers_create")
def _():
    
    # VALIDATE SESSION
    session = validate.session()
    if not session: return redirect("/sign-in")
    
    return dict(session=session)