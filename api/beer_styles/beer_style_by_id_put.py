from bottle import put, request
import pymysql
from utils import g, vars as var, validation as validate, vercel

##############################
@put(f"{var.API_PATH}/beer-styles/<beer_style_id>")
def _(beer_style_id=""):
    try:
        # VALIDATE
        session = validate.session()
        if not session:
            return g.respond(401)

        # Input values
        beer_style_id, error = validate.id(beer_style_id)
        if error:
            return g.respond(400, f"Beer style {error}")

        form_beer_style_id, error = validate.id(request.forms.get("beer_style_id"))
        if error:
            return g.respond(400, f"Beer style {error}")

        if form_beer_style_id != beer_style_id:
            return g.respond(400, "Beer style ID's does not match.")

        beer_style_name, error = validate.name(request.forms.get("beer_style_name"))
        if error:
            return g.respond(400, {"info": error, "key": "beer_style_name"})

    except Exception as ex:
        print(str(ex))
        return g.respond(500)

    # CONNECT TO DB
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        cursor = db_connect.cursor()
        cursor.execute("""
        UPDATE beer_styles
        SET beer_style_name = %s
        WHERE beer_style_id = %s
        """, (beer_style_name, beer_style_id))
        counter = cursor.rowcount
        if not counter:
            return g.respond(204)
        db_connect.commit()

        # IF STYLE ON TAP, DEPLOY VERCEL
        cursor.execute("""
        SELECT tap_id FROM taps_list
        WHERE fk_beer_style_id = %s
        LIMIT 1
        """, (beer_style_id))
        tap = cursor.fetchone()
        if tap:
            vercel.deploy()

        response_dict = {"name": beer_style_name, "info": "Beer style was successfully updated."}
        return g.respond(200, response_dict)

    except Exception as ex:
        print(str(ex))
        if "beer_style_name" in str(ex):
            return g.respond(400, {"info": "Beer style already exists.", "key": "beer_style_name"})
        return g.respond(500)

    finally:
        cursor.close()
        db_connect.close()
