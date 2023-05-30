from bottle import put, request
import pymysql
from utils import g, validation as validate, vars as var

##############################

@put(f"{var.API_PATH}/bars/<bar_id>")
def _(bar_id):
    # VALIDATE
    session = validate.session()
    if not session:
        return g.respond(401)

    if not session["role_id"] == 1:
        return g.respond(401)

    # bar id param
    bar_id, error = validate.id(bar_id)
    if error:
        return g.respond(400, error)

    # Input values
    bar_name, error = validate.name(request.forms.get("bar_name"))
    if error:
        return g.respond(400, error)

    bar_street, error = validate.name(request.forms.get("bar_street"))
    if error:
        return g.respond(400, error)

    bar_city, error = validate.name(request.forms.get("bar_city"))
    if error:
        return g.respond(400, error)

    bar_zip_code, error = validate.zip_code(request.forms.get("bar_zip_code"))
    if error:
        return g.respond(400, error)

    # UPDATE IN DB
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
        if not counter:
            return g.respond(204)
        db.commit()

        response_dict = {"name": bar_name, "info": "Bar was successfully updated."}
        return g.respond(200, response_dict)

    except Exception as ex:
        print(str(ex))
        return g.respond(500)

    finally:
        cursor.close()
        db.close()
