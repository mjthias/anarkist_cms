from bottle import get, view

##############################
@get("/")
@view("home")
def _():
    user = {"user_name": "Super User"}
    return dict(user=user)