from bottle import get, redirect, request, response
import utils.g as g
import utils.vars as var
import jwt

##############################
@get("/sign-out")
def _():
    try:
        cookie = request.get_cookie("anarkist")
        decoded_jwt = jwt.decode(cookie, var.JWT_SECRET, algorithms=["HS256"])
        g.delete_session(decoded_jwt)
        response.set_cookie("anarkist", cookie, path="/", expires=0)
        return g.respond(200, "Successfully signed out.")
    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error.")
    finally:
        redirect("/sign-in")