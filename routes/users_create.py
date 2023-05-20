from bottle import get, view, redirect
import utils.validation as validate

##############################

@get("/users/create")
@view("users_create")
def _():
    # VALDATE SESSION
    session = validate.session()
    if not session: return redirect("/sign-in")
    # Staff no access
    if session["role_id"] == 3:
        return redirect("/")
    
    return dict(session = session)