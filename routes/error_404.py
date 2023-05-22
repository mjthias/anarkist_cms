from bottle import get, view, redirect, request
import utils.validation as validate

##############################

# @error(404)
@get("/404")
@view("error")
def _():
    session = validate.session()
    if not session: return redirect("/sign-in")
    
    error = {
        "code": 404,
        "message": "Not found.",
        "info": f"Page '{request.query.get('url')}' was not found."
    }

    return dict(session=session, error=error)