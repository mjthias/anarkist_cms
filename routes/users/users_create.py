from bottle import get, view, redirect
import utils.validation as validate
import utils.g as g

##############################

@get("/users/create")
@view("users/create")
def _():
    # VALDATE SESSION
    session = validate.session()
    if not session: return redirect("/sign-in")
    # Staff no access
    if session["role_id"] == 3:
        return g.error_view(401)

    
    return dict(session = session)