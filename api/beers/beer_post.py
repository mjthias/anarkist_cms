import time
from  bottle import post, request
import pymysql
from utils import g, vars as var, validation as validate

##############################

@post(f"{var.API_PATH}/beers")
def _():
    try:
        # VALIDATE
        session = validate.session()
        if not session:
            return g.respond(401)

        # Input values
        beer_name, error = validate.name(request.forms.get("beer_name"))
        if error:
            return g.respond(400, error)

        brewery_id, error = validate.id(request.forms.get("brewery_id"))
        if error:
            return g.respond(400, f"Brewery {error}")

        beer_style_id, error = validate.id(request.forms.get("beer_style_id"))
        if error:
            return g.respond(400, f"Beer style {error}")

        beer_alc, error = validate.alc(request.forms.get("beer_alc"))
        if error:
            return g.respond(400, error)

        beer_price, error = validate.price(request.forms.get("beer_price"))
        if error:
            return g.respond(400, error)

        beer_ibu, error = validate.ibu(request.forms.get("beer_ibu"))
        if error:
            return g.respond(400, error)

        beer_ebc, error = validate.ebc(request.forms.get("beer_ebc"))
        if error:
            return g.respond(400, error)

        beer_description_en, error = validate.description(request.forms.get("beer_description_en"))
        if error:
            return g.respond(400, error)

        beer_description_dk, error = validate.description(request.forms.get("beer_description_dk"))
        if error:
            return g.respond(400, error)

        if request.files.get("beer_image") and not request.files.get("beer_image").filename == "empty":
            beer_image, error = validate.image(request.files.get("beer_image"))
            if error:
                return g.respond(400, error)
        else:
            beer_image = ""

        # Create beer tuple
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
            session["user_id"],
            int(time.time()),
            session["user_id"]
        )

    except Exception as ex:
        print(str(ex))
        return g.respond(500)

    # POST TO DB
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        cursor = db_connect.cursor()
        query = """
        INSERT INTO beers
        (beer_name,
        fk_brewery_id,
        beer_ebc,
        beer_ibu,
        beer_alc,
        fk_beer_style_id,
        beer_price,
        beer_image,
        beer_description_en,
        beer_description_dk,
        beer_created_at,
        fk_beer_created_by,
        beer_updated_at,
        fk_beer_updated_by)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, beer)
        beer_id = cursor.lastrowid
        db_connect.commit()

        return g.respond(201, beer_id)

    except Exception as ex:
        print(str(ex))
        return g.respond(500)

    finally:
        cursor.close()
        db_connect.close()
