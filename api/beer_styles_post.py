from bottle import post, request
import utils.vars as var
import utils.g as g
import utils.validation as validate
import pymysql

##############################
@post(f"{var.API_PATH}/beer-styles")
def _():
    # VALIDATE SESSION
    session = validate.session()
    if not session: return g.respond(401, "Unauthorized attempt.")

    # VALIDATE INPUT VALUES
    try:
        allowed_keys = ["beer_style_name"]
        for key in request.forms.keys():
            if not key in allowed_keys: return g.respond(403, f"Forbidden key: {key}")
        
        beer_style_name, error = validate.name(request.forms.get("beer_style_name"))
        if error: return g.respond(400, error)
        
    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error.")
    
    # CONNECT TO DB
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        cursor = db_connect.cursor()

        cursor.execute("""
            INSERT INTO beer_styles
            (beer_style_name)
            VALUES(%s)
        """, (beer_style_name,))
        beer_style_id = cursor.lastrowid
        db_connect.commit()

        return g.respond(201, beer_style_id)
    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error.")
    finally:
        cursor.close()
        db_connect.close()