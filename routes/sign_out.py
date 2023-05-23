from bottle import get, redirect, request, response
import utils.g as g
import utils.vars as var
import jwt

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