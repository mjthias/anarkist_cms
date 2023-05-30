from bottle import get, view, redirect
from utils import g, validation as validate

##############################

@get("/users/create")
@view("users/create")
def _():
    # VALDATE SESSION
    session = validate.session()
    if not session:
        return redirect("/sign-in")

    # Staff no access
    if session["role_id"] == 3:
        return g.error_view(401)

    return dict(session = session)
