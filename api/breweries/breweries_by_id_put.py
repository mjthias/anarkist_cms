from bottle import put, request
import pymysql
from utils import g, vars as var, validation as validate, vercel

##############################

@put(f"{var.API_PATH}/breweries/<brewery_id>")
def _(brewery_id):
    try:
        # VALIDATE SESSION
        session = validate.session()
        if not session:
            return g.respond(401)

        # VALIDATE BREWERY_ID PARAM
        brewery_id, error = validate.id(brewery_id)
        if error:
            return g.respond(400, error)

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
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
        UPDATE breweries
        SET brewery_name = %s, brewery_menu_name = %s
        WHERE brewery_id = %s
        """, (brewery_name, brewery_menu_name, brewery_id))
        counter = cursor.rowcount
        if not counter:
            return g.respond(204)
        db.commit()

        # IF ON TAP, DEPLOY VERCEL
        cursor.execute("""
        SELECT tap_id FROM taps_list
        WHERE fk_brewery_id = %s
        LIMIT 1
        """, (brewery_id))
        tap = cursor.fetchone()
        if tap:
            vercel.deploy()

        response_dict = {"name": brewery_name, "info": "Brewery was successfully updated."}

        return g.respond(200, response_dict)

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
