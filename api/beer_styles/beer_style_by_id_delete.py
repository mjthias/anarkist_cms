from bottle import delete, request
import utils.g as g
import utils.vars as var
import utils.validation as validate
import pymysql

##############################
@delete(f"{var.API_PATH}/beer-styles/<beer_style_id>")
def _(beer_style_id=""):
    try:
        # VALIDATE SESSION
        session = validate.session()
        if not session: return g.respond(401)

        # VALIDATE ALLOWED KEYS
        allowed_keys = ["id", "confirm_deletion"]
        for key in request.forms.keys():
            if not key in allowed_keys: return g.respond(403, f"Forbidden key: {key}")

        # VALIDATE INPUT
        beer_style_id, error = validate.id(beer_style_id)
        if error: return g.respond(400, f"Beer style {error}")
        confirm_delete, error = validate.confirm_deletion(request.forms.get("confirm_deletion"))
        if error: return g.respond(400, error)

    except Exception as ex:
        print(str(ex))
        return g.respond(500)
    
    # CONNECT TO DB
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        cursor = db_connect.cursor()

        cursor.execute("""
            DELETE FROM beer_styles
            WHERE beer_style_id = %s
        """, (beer_style_id,))
        counter = cursor.rowcount
        if not counter: return g.respond(204)
        db_connect.commit()

        return g.respond(200, f"Successfully deleted beer style with ID: {beer_style_id}")
    except Exception as ex:
        print(str(ex))
        return g.respond(500)
    finally:
        cursor.close()
        db_connect.close()