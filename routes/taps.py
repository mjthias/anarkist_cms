from bottle import get, view, redirect
import utils.validation as validate

##############################

@get("/taps")
@view("taps")
def _():
    session = validate.session()
    if not session: return redirect("/sign-in")
    
    return dict(session = session)