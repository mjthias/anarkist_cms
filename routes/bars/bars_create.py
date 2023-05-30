from bottle import get, view, redirect
from utils import g, validation as validate

##############################

@get("/bars/create")
@view("bars/create")
def _():
    # VALIDATE SESSION
    session = validate.session()
    if not session:
        return redirect("/sign-in")

    # VALIDATE ROLE
    if not session["role_id"] == 1:
        return g.error_view(401)

    return dict(session = session)
