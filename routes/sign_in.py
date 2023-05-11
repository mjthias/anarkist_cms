from bottle import get, view

##############################
@get("/sign-in")
@view("sign_in")
def _():
    return 