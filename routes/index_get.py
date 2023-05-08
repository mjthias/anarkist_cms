from bottle import get

##############################

@get("/")
def _():
    return "hello"