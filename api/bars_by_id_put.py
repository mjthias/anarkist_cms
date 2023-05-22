from bottle import put, request
import utils.validation as validate
import utils.vars as var
import utils.g as g
import pymysql

##############################

@put(f"{var.API_PATH}/bars/<bar_id>")
def _(bar_id):
    # VALIDATE 
    # Session
    session = validate.session()
    if not session: 
        return g.respond(401, "Unauthorized attempt.")

    # Role
    if not session["role_id"] == 1:
        return g.respond(401, "Unauthorized attempt.")

    # bar id param
    bar_id, error = validate.id(bar_id)
    if error: return g.respond(400, error)

    # Input values
    bar_name, error = validate.name(request.forms.get("bar_name"))
    if error: return g.respond(400, error)

    bar_street, error = validate.name(request.forms.get("bar_street"))
    if error: return g.respond(400, error)

    bar_city, error = validate.name(request.forms.get("bar_city"))
    if error: return g.respond(400, error)

    bar_zip_code, error = validate.zip_code(request.forms.get("bar_zip_code"))
    if error: return g.respond(400, error)

    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
        UPDATE bars
        SET bar_name = %s,
        bar_street = %s,
        bar_city = %s,
        bar_zip_code = %s
        WHERE bar_id = %s
        """, (bar_name, bar_street, bar_city, bar_zip_code, bar_id))
        counter = cursor.rowcount
        if not counter: return g.respond(204, "")
        db.commit()

        return g.respond(200, "Bar updated")

    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error")

    finally:
        cursor.close()
        db.close()
    
