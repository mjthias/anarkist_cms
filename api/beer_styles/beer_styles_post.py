from bottle import post, request
import pymysql
from utils import g, vars as var, validation as validate

##############################
@post(f"{var.API_PATH}/beer-styles")
def _():
    try:
        # VALIDATE
        session = validate.session()
        if not session:
            return g.respond(401)

        # Input values
        beer_style_name, error = validate.name(request.forms.get("beer_style_name"))
        if error:
            return g.respond(400, {"info": error, "key": "beer_style_name"})

    except Exception as ex:
        print(str(ex))
        return g.respond(500)

    try:
        # POST TO DB
        db_connect = pymysql.connect(**var.DB_CONFIG)
        cursor = db_connect.cursor()
        cursor.execute("""
        INSERT INTO beer_styles
        (beer_style_name)
        VALUES(%s)
        """, (beer_style_name,))
        beer_style_id = cursor.lastrowid
        db_connect.commit()

        response_dict = {"id": beer_style_id, "info": "Beer style was successfully created", "entry_type": "beer style"}

        return g.respond(201, response_dict)

    except Exception as ex:
        print(str(ex))
        if "beer_style_name" in str(ex):
            return g.respond(400, {"info": "Beer style already exists.", "key": "beer_style_name"})
        return g.respond(500)

    finally:
        cursor.close()
        db_connect.close()
