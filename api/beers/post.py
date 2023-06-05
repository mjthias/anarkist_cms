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
            return g.respond(400, {"info": error, "key": "beer_name"})

        brewery_id, error = validate.id(request.forms.get("brewery_id"))
        if error:
            return g.respond(400, {"info": f"Brewery {error}", "key": "brewer_id"})

        beer_style_id, error = validate.id(request.forms.get("beer_style_id"))
        if error:
            return g.respond(400, {"info": f"Beer style {error}", "key": "beer_style_id"})

        beer_alc, error = validate.alc(request.forms.get("beer_alc"))
        if error:
            return g.respond(400, {"info": error, "key": "beer_alc"})

        beer_price, error = validate.price(request.forms.get("beer_price"))
        if error:
            return g.respond(400, {"info": error, "key": "beer_price"})

        beer_ibu, error = validate.ibu(request.forms.get("beer_ibu"))
        if error:
            return g.respond(400, {"info": error, "key": "beer_ibu"})

        beer_ebc, error = validate.ebc(request.forms.get("beer_ebc"))
        if error:
            return g.respond(400, {"info": error, "key": "beer_ebc"})

        beer_description_en, error = validate.description(request.forms.get("beer_description_en"))
        if error:
            return g.respond(400, {"info": error, "key": "beer_description_en"})

        beer_description_dk, error = validate.description(request.forms.get("beer_description_dk"))
        if error:
            return g.respond(400, {"info": error, "key": "beer_description_dk"})

        if request.files.get("beer_image") and not request.files.get("beer_image").filename == "empty":
            beer_image, error = validate.image(request.files.get("beer_image"))
            if error:
                return g.respond(400, {"info": error, "key": "beer_image"})
        else:
            beer_image = None

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

        response_dict = {"id": beer_id, "info": "Beer was successfully created", "entry_type": "beer"}

        return g.respond(201, response_dict)

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
