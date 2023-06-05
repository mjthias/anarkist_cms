# pylint: disable=W0612
from bottle import delete, request
import pymysql
from utils import g, vars as var, validation as validate

##############################
@delete(f"{var.API_PATH}/beer-styles/<beer_style_id>")
def _(beer_style_id=""):
    try:
        # VALIDATE
        session = validate.session()
        if not session or session['role_id'] == 3:
            return g.respond(401)

        # Input values
        beer_style_id, error = validate.id(beer_style_id)
        if error:
            return g.respond(400, f"Beer style {error}")

        confirm_delete, error = validate.confirm_deletion(request.forms.get("confirm_deletion"))
        if error:
            return g.respond(400, {"info": error, "key": "confirm_deletion"})

    except Exception as ex:
        print(str(ex))
        return g.respond(500)

    # DELETE FROM DB
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        cursor = db_connect.cursor()
        cursor.execute("""
            DELETE FROM beer_styles
            WHERE beer_style_id = %s
        """, (beer_style_id,))
        counter = cursor.rowcount
        if not counter:
            return g.respond(204)
        db_connect.commit()

        return g.respond(200, f"Successfully deleted beer style with ID: {beer_style_id}")

    except Exception as ex:
        print(str(ex))
        if "beers" in str(ex):
            return g.respond(403, {"info": "One or more beers references this beer style.", "key": "confirm_deletion"})
        return g.respond(500)

    finally:
        cursor.close()
        db_connect.close()
