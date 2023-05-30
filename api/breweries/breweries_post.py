from bottle import post, request
import pymysql
from utils import g, vars as var, validation as validate

##############################

@post(f"{var.API_PATH}/breweries")
def _():
    try:
        # VALIDATE SESSION
        session = validate.session()
        if not session:
            return g.respond(401)

        # VALIDATE INPUT VALUES
        brewery_name, error = validate.brewery_name(request.forms.get("brewery_name"))
        if error:
            return g.respond(400, error)

        # Menu_name only required if len(name) > 50
        if not request.forms.get("brewery_menu_name"):
            if len(brewery_name) > 50:
                return g.respond(400, "Brewery name is too long for menu. Please provide a short menu name")
            brewery_menu_name = brewery_name

        else:
            brewery_menu_name, error = validate.brewery_menu_name(request.forms.get("brewery_menu_name"))
            if error:
                return g.respond(400, error)

            if len(brewery_menu_name) > len(brewery_name):
                return g.respond(400, "Menu name can't be longer than the actual name")

    except Exception as ex:
        print(ex)
        return g.respond(500)

    try:
        # INSERT TO DB
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
        INSERT INTO breweries
        (brewery_name, brewery_menu_name)
        VALUES (%s, %s)
        """, (brewery_name, brewery_menu_name))
        brewery_id = cursor.lastrowid
        db.commit()

        response_dict = {"id": brewery_id, "info": "Brewery was successfully created", "entry_type": "brewery"}

        return g.respond(201, response_dict)

    except Exception as ex:
        print(ex)
        if "brewery_name" in str(ex):
            return g.respond(400, "Brewery name already registered")
        if "brewery_menu_name" in str(ex):
            return g.respond(400, "Brewery menu name already registered")
        return g.respond(500)

    finally:
        cursor.close()
        db.close()
