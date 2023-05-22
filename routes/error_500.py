from bottle import get, view, redirect, request
import utils.validation as validate

##############################

# @error(404)
@get("/500")
@view("error")
def _():
    session = validate.session()
    if not session: return redirect("/sign-in")
    
    error = {
        "code": 500,
        "message": "Server error.",
        "info": f"Page '{request.query.get('url')}' caused a server error."
    }

    return dict(session=session, error=error)