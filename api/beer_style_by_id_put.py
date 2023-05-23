from bottle import put, request
import utils.g as g
import utils.vars as var
import utils.validation as validate
import pymysql

##############################
@put(f"{var.API_PATH}/beer-styles/<beer_style_id>")
def _(beer_style_id=""):
    try:
        # VALIDATE SESSION
        session = validate.session()
        if not session: return g.respond(401)

        # VALIDATE ALLOWED KEYS
        allowed_keys = ["beer_style_id", "beer_style_name"]
        for key in request.forms.keys():
            if not key in allowed_keys: return g.respond(403, f"Forbidden key: {key}")

        # VALIDATE INPUT VALUES
        beer_style_id, error = validate.id(beer_style_id)
        if error: return g.respond(400, f"Beer style {error}")
        form_beer_style_id, error = validate.id(request.forms.get("beer_style_id"))
        if error: return g.respond(400, f"Beer style {error}")
        if not form_beer_style_id == beer_style_id: return g.respond(400, "Beer style ID's does not match.")
        beer_style_name, error = validate.name(request.forms.get("beer_style_name"))
        if error: return g.respond(400, error)
    
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
        if not counter: return g.respond(204)
        print(f"Rows updated: {counter}")
        db_connect.commit()

        cursor.execute("SELECT * FROM beer_styles WHERE beer_style_id = %s LIMIT 1", (beer_style_id,))
        beer_style = cursor.fetchone()

        return g.respond(200, beer_style)
    except Exception as ex:
        print(str(ex))
        if "beer_style_name" in str(ex): return g.respond(400, "Beer style already exists.")
        return g.respond(500)
    finally:
        cursor.close()
        db_connect.close()
