from bottle import put, request
import utils.g as g
import utils.vars as var
import utils.validation as validate
import pymysql
import time
import os

##############################
@put(f"{var.API_PATH}/beers/<beer_id>")
def _(beer_id=""):
    try:
        # VALIDATE SESSION/USER
        session = validate.session()
        if not session: return g.respond(401)

        # VALIDATE ALLOWED KEYS
        allowed_keys = ["beer_id", "beer_name", "beer_ebc", "beer_ibu", "beer_alc", "beer_price", "beer_image", "beer_image_name", "beer_description_en", "beer_description_dk", "brewery_id", "brewery_name", "beer_style_id", "beer_style_name"]
        for key in request.forms.keys():
            if not key in allowed_keys: return g.respond(403, f"Forbidden key: {key}")
        
        # VALIDATE INPUT VALUES
        beer_id, error = validate.id(beer_id)
        if error: return g.respond(400, f"Beer {error}")
        form_beer_id, error = validate.id(request.forms.get("beer_id"))
        if error: return g.respond(400, f"Beer {error}")
        if not form_beer_id == beer_id: return g.respond(400, "Beer ID's does not match.")
        beer_id = form_beer_id
        beer_name, error = validate.name(request.forms.get("beer_name"))
        if error: return g.respond(400, error)
        beer_ebc, error = validate.ebc(request.forms.get("beer_ebc"))
        if error: return g.respond(400, error)
        beer_ibu, error = validate.ibu(request.forms.get("beer_ibu"))
        if error: return g.respond(400, error)
        beer_alc, error = validate.alc(request.forms.get("beer_alc"))
        if error: return g.respond(400, error)
        beer_price, error = validate.price(request.forms.get("beer_price"))
        if error: return g.respond(400, error)
        beer_description_en, error = validate.description(request.forms.get("beer_description_en"))
        if error: return g.respond(400, error)
        beer_description_dk, error = validate.description(request.forms.get("beer_description_dk"))
        if error: return g.respond(400, error)
        # IF A FILE HAS BEEN UPLOADED, VALIDATE IT. ELSE SET THE VALUE TO OLD FILE NAME
        if request.files.get("beer_image") and not request.files.get("beer_image").filename == "empty":
            beer_image, error = validate.image(request.files.get("beer_image"))
            if error: return g.respond(400, error)
        else:
            beer_image = request.forms.get("beer_image_name")
        brewery_id, error = validate.id(request.forms.get("brewery_id"))
        if error: return g.respond(400, f"Brewery {error}")
        beer_style_id, error = validate.id(request.forms.get("beer_style_id"))
        if error: return g.respond(400, f"Beer style {error}")
        
    except Exception as ex:
        print(str(ex))
        return g.respond(500)

    # CONNECT TO DB
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        db_connect.begin()
        cursor = db_connect.cursor()

        # SELECT DB BEER
        cursor.execute("SELECT * FROM beers WHERE beer_id = %s LIMIT 1", (beer_id,))
        beer = cursor.fetchone()
        if not beer: return g.respond(204)

        # SAVE OLD IMAGE PATH
        beer_image_old = beer["beer_image"]

        # APPEND NEW VALUES TO BEER
        beer['beer_name'] = beer_name
        beer['fk_brewery_id'] = brewery_id
        beer['beer_ebc'] = beer_ebc
        beer['beer_ibu'] = beer_ibu
        beer['beer_alc'] = beer_alc
        beer['fk_beer_style_id'] = beer_style_id
        beer['beer_price'] = beer_price
        beer['beer_image'] = beer_image
        beer['beer_description_en'] = beer_description_en
        beer['beer_description_dk'] = beer_description_dk
        beer['beer_updated_at'] = int(time.time())
        beer['fk_beer_updated_by'] = session['user_id']

        # UPDATE BEER
        cursor.execute("""
            UPDATE beers
            SET beer_name = %s,
            fk_brewery_id = %s,
            beer_ebc = %s,
            beer_ibu = %s,
            beer_alc = %s,
            fk_beer_style_id = %s,
            beer_price = %s,
            beer_image = %s,
            beer_description_en = %s,
            beer_description_dk = %s,
            beer_updated_at = %s,
            fk_beer_updated_by = %s
            WHERE beer_id = %s
        """, (beer['beer_name'], beer['fk_brewery_id'], beer['beer_ebc'], beer['beer_ibu'], beer['beer_alc'], beer['fk_beer_style_id'], beer['beer_price'], beer['beer_image'], beer['beer_description_en'], beer['beer_description_dk'], beer['beer_updated_at'], beer['fk_beer_updated_by'], beer['beer_id']))

        counter = cursor.rowcount
        if not counter: return g.respond(204)
        print(f"Rows updated: {counter}")
        db_connect.commit()

        # REMOVE OLD BEER IMAGE FROM SYSTEM
        if not beer_image_old == "" and not beer_image_old == beer_image:
            os.remove(f"{var.IMAGE_PATH}{beer_image_old}")

        response_dict = {"name": beer_name, "info": "Beer was successfully updated."}

        return g.respond(200, response_dict)

    except Exception as ex:
        print(str(ex))
        return g.respond(500)
    finally:
        cursor.close()
        db_connect.close()