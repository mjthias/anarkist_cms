from bottle import get, view, redirect
from utils import g, validation as validate

##############################

@get("/taps/create")
@view("taps/create")
def _():
    # VALIATE SESSION
    session = validate.session()
    if not session:
        return redirect("/sign-in")

    # VALIDATE ROLE
    if session["role_id"] == 3:
        return g.error_view(401)

    return dict(session=session)
