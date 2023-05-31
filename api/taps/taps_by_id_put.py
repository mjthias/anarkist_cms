from bottle import put, request
import pymysql
from utils import g, vars as var, validation as validate, vercel

##############################

@put(f"{var.API_PATH}/taps/<tap_id>")
def _(tap_id):
    try:
        # VALIDATE SESSION
        session = validate.session()
        if not session:
            return g.respond(401)
        bar_id = session["bar_id"]

        # VALIDATE ID PARAM
        tap_id, error = validate.id(tap_id)
        if error:
            return g.respond(400, error)

        # VALIDATE INNPUT VALS
        beer_id, error =  validate.id(request.forms.get("beer_id"))
        if error:
            return g.respond(400, error)

        tap_unavailable = bool(request.forms.get("tap_unavailable"))

    except Exception as ex:
        print(ex)
        return g.respond(500)

    try:
        # UPDATE IN DB
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
        UPDATE taps
        SET fk_beer_id = %s,
        tap_unavailable = %s
        WHERE tap_id = %s
        AND fk_bar_id = %s
        """, (beer_id, tap_unavailable, tap_id, bar_id))
        counter = cursor.rowcount
        if not counter:
            return g.respond(204)
        db.commit()

        # DEPLOY VERCEL
        vercel.deploy()

        return g.respond(200, "Tap was successfully updated.")

    except Exception as ex:
        print(ex)
        return g.respond(500)

    finally:
        cursor.close()
        db.close()
