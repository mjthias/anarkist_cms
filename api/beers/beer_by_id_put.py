import time
import os
from bottle import put, request
import pymysql
from utils import g, vars as var, validation as validate, vercel

##############################

@put(f"{var.API_PATH}/beers/<beer_id>")
def _(beer_id):
    try:
        # VALIDATE
        session = validate.session()
        if not session:
            return g.respond(401)

        # Input values
        beer_id, error = validate.id(beer_id)
        if error:
            return g.respond(400, {"info": f"Beer {error}", "key": "beer_style_id"})

        form_beer_id, error = validate.id(request.forms.get("beer_id"))
        if error:
            return g.respond(400, {"info": f"Beer {error}", "key": "beer_style_id"})

        if form_beer_id != beer_id:
            return g.respond(400, "Beer ID's does not match.")
        beer_id = form_beer_id

        beer_name, error = validate.name(request.forms.get("beer_name"))
        if error:
            return g.respond(400, {"info": error, "key": "beer_name"})

        beer_ebc, error = validate.ebc(request.forms.get("beer_ebc"))
        if error:
            return g.respond(400, {"info": error, "key": "beer_ebc"})

        beer_ibu, error = validate.ibu(request.forms.get("beer_ibu"))
        if error:
            return g.respond(400, {"info": error, "key": "beer_ibu"})

        beer_alc, error = validate.alc(request.forms.get("beer_alc"))
        if error:
            return g.respond(400, {"info": error, "key": "beer_alc"})

        beer_price, error = validate.price(request.forms.get("beer_price"))
        if error:
            return g.respond(400, {"info": error, "key": "beer_price"})

        beer_description_en, error = validate.description(request.forms.get("beer_description_en"))
        if error:
            return g.respond(400, {"info": error, "key": "beer_description_en"})

        beer_description_dk, error = validate.description(request.forms.get("beer_description_dk"))
        if error:
            return g.respond(400, {"info": error, "key": "beer_description_dk"})

        # IF A IMAGE HAS BEEN UPLOADED, VALIDATE IT. ELSE SET THE VALUE TO OLD FILE NAME
        if request.files.get("beer_image") and not request.files.get("beer_image").filename == "empty":
            beer_image, error = validate.image(request.files.get("beer_image"))
            if error:
                return g.respond(400, {"info": error, "key": "beer_image"})
        else:
            beer_image = request.forms.get("beer_image_name")
        if not beer_image:
            beer_image = None

        brewery_id, error = validate.id(request.forms.get("brewery_id"))
        if error:
            return g.respond(400, {"info": f"Brewery {error}", "key": "brewer_id"})

        beer_style_id, error = validate.id(request.forms.get("beer_style_id"))
        if error:
            return g.respond(400, {"info": f"Beer style {error}", "key": "beer_style_id"})

    except Exception as ex:
        print(str(ex))
        return g.respond(500)

    # CONNECT TO DB
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        db_connect.begin()
        cursor = db_connect.cursor()

        # SELECT DB BEER_IMAGE
        cursor.execute("""
        SELECT beer_image FROM beers 
        WHERE beer_id = %s LIMIT 1
        """, (beer_id,))
        beer_image_old = cursor.fetchone()['beer_image']

        # APPEND NEW VALUES TO BEER
        beer = (
            beer_name,
            brewery_id,
            beer_ebc,
            beer_ibu,
            beer_alc,
            beer_style_id,
            beer_price,
            beer_image,
            beer_description_en,
            beer_description_dk,
            int(time.time()),
            session['user_id'],
            beer_id
        )

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
        """, beer)

        counter = cursor.rowcount
        if not counter:
            return g.respond(204)
        db_connect.commit()

        # CALL ASTRO HOOK IF BEER ON TAP
        cursor.execute("""
        SELECT tap_id FROM taps
        WHERE fk_beer_id = %s
        LIMIT 1
        """, (beer_id))
        tap = cursor.fetchone()
        if tap:
            vercel.deploy()

        # REMOVE OLD BEER IMAGE FROM SYSTEM
        if not beer_image_old is None and not beer_image_old == beer_image:
            os.remove(f"{var.IMAGE_PATH}{beer_image_old}")

        response_dict = {"name": beer_name, "info": "Beer was successfully updated."}

        return g.respond(200, response_dict)

    except Exception as ex:
        print(str(ex))
        if "beer_name" in str(ex):
            return g.respond(400, {"info": "Beer already exists", "key": "beer_name"})
        if "fk_brewery_id" in str(ex):
            return g.respond(400, {"info": "Brewery does not exist", "key": "brewery_name"})
        if "fk_beer_style_id" in str(ex):
            return g.respond(400, {"info": "Beer style does not exist", "key": "beer_style_name"})
        return g.respond(500)

    finally:
        cursor.close()
        db_connect.close()
