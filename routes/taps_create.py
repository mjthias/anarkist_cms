from bottle import get, view, redirect
import utils.validation as validate
import utils.g as g


##############################

@get("/taps/create")
@view("taps_create")
def _():
    # VALIATE SESSION
    session = validate.session()
    if not session: return redirect("/sign-in")

    # VALIDATE ROLE
    if session["role_id"] == 3:
        return g.error_view(401, "Unauthorized attempt")
    
    return dict(session=session)

