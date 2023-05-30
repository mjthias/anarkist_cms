from bottle import post, request
import pymysql
from utils import g, validation as validate, vars as var

##############################

@post(f"{var.API_PATH}/bars")
def _():
    try:
        # VALIDATE
        session = validate.session()
        if not session:
            return g.respond(401)

        if not session["role_id"] == 1:
            return g.respond(401)

        # Input values
        bar_name, error = validate.name(request.forms.get("bar_name"))
        if error:
            return g.respond(400, {"info": error, "key": "bar_name"})

        bar_street, error = validate.name(request.forms.get("bar_street"))
        if error:
            return g.respond(400, {"info": error, "key": "bar_street"})

        bar_city, error = validate.name(request.forms.get("bar_city"))
        if error:
            return g.respond(400, {"info": error, "key": "bar_city"})

        bar_zip_code, error = validate.zip_code(request.forms.get("bar_zip_code"))
        if error:
            return g.respond(400, {"info": error, "key": "bar_zip_code"})

    except Exception as ex:
        print(str(ex))
        return g.respond(500)

    try:
        # POST TO DB
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
        INSERT INTO bars
        (bar_name, bar_street, bar_city, bar_zip_code)
        VALUES (%s, %s, %s, %s)
        """, (bar_name, bar_street, bar_city, bar_zip_code))
        bar_id = cursor.lastrowid
        db.commit()

        response_dict = {"id": bar_id, "info": "Bar was successfully created", "entry_type": "bar"}

        return g.respond(201, response_dict)

    except Exception as ex:
        print(str(ex))
        if "bar_name" in str(ex):
            return g.respond(400, {"info": "Bar already exists.", "key": "bar_name"})
        return g.respond(500)

    finally:
        cursor.close()
        db.close()
