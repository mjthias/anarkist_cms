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
            return g.respond(400, {"info": error, "key": "brewery_name"})

        brewery_menu_name, error = validate.brewery_menu_name(brewery_name, request.forms.get("brewery_menu_name"))
        if error:
            return g.respond(400, {"info": error, "key": "brewery_menu_name"})

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
            return g.respond(400, {"info": "Brewery name already registered", "key": "brewery_name"})
        if "brewery_menu_name" in str(ex):
            return g.respond(400, {"info": "Brewery menu name already registered", "key": "brewery_menu_name"})
        return g.respond(500)

    finally:
        cursor.close()
        db.close()
