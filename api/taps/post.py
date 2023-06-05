from bottle import post, request
import pymysql
from utils import g, vars as var, validation as validate, vercel

##############################

@post(f"{var.API_PATH}/taps")
def _():
    try:
        # VALIDATE SESSION AND ROLE - staff not allowed
        session = validate.session()
        if not session or session["role_id"] == 3:
            return g.respond(401)
        bar_id = session["bar_id"]

        # VALIDATE BEER ID
        beer_id, error =  validate.id(request.forms.get("beer_id"))
        if error:
            return g.respond(400, error)

        is_off_wall = bool(request.forms.get("tap_off_the_wall"))

    except Exception as ex:
        print(ex)
        return g.respond(500)

    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
        CALL insert_tap(%s, %s, %s)
        """, (is_off_wall, beer_id, bar_id))
        new_tap_id = cursor.fetchone()["tap_id"]
        db.commit()

        # DEPLOY VERCEL
        vercel.deploy()

        response_dict = {"id": new_tap_id, "info": "Tap was successfully created", "entry_type": "tap"}
        return g.respond(201, response_dict)

    except Exception as ex:
        print(ex)
        return g.respond(500)

    finally:
        cursor.close()
        db.close()
    