from bottle import post, redirect, request, response
import utils.g as g
import utils.vars as var
import utils.validation as validate
import jwt

##############################
@post("/select-location")
def _():
    # VALIDATE
    session = validate.partial_session()
    if not session: return g.respond(401, "Unauthorized attempt.")

    try:
        bar_id, error = validate.id(request.forms.get("bars"))
        if error: return g.respond(400, error)

        # Append bar id to session dict
        session["bar_id"] = bar_id
        for bar in session["bar_access"]:
            if bar["bar_id"] == bar_id: 
                session["bar_name"] = bar["bar_name"]

        session = {
            "user_id": session["user_id"],
            "session_iat": session["session_iat"],
            "user_name": session["user_name"],
            "session_id": session["session_id"],
            "role_id": session["role_id"],
            "bar_id": session["bar_id"],
            "bar_name": session["bar_name"],
            "bar_access": session["bar_access"]
        }

        encoded_jwt = jwt.encode(session, var.JWT_SECRET, algorithm="HS256")
        response.set_cookie("anarkist", encoded_jwt, path="/")

        return g.respond(200, "Location successfully selected.")
    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error.")