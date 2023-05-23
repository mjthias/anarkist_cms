from bottle import get, view, redirect
import utils.validation as validate
import utils.vars as var
import utils.g as g
import pymysql

##############################

@get("/bars/create")
@view("bars_create")
def _():
    # VALIDATE SESSION
    session = validate.session()
    if not session: return redirect("/sign-in")

    # VALIDATE ROLE
    if not session["role_id"] == 1:
        return g.error_view(401)
    
    return dict(session = session)

