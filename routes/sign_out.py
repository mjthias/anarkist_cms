# pylint: disable=W0150
from bottle import get, redirect, request, response
import jwt
from utils import g, vars as var

##############################

@get("/sign-out")
def _():
    try:
        cookie = request.get_cookie("anarkist")
        session = jwt.decode(cookie, var.JWT_SECRET, algorithms=["HS256"])
        g.delete_session(session)
        response.set_cookie("anarkist", cookie, path="/", expires=0)

    except Exception as ex:
        print(str(ex))

    finally:
        return redirect("/sign-in")
