from bottle import get, request, view
import pymysql
from utils import g, vars as var, validation as validate

##############################

@get(f"{var.API_PATH}/beers")
def _():
    try:
        # VALIDATE SESSION
        session = validate.session()
        if not session:
            return g.respond(401)

        # VALIDATE PARAM
        beer_name, error = validate.name(request.params.get("name"))
        if error:
            return g.respond(400, error)

    except Exception as ex:
        print(ex)
        return g.respond(500)

    try:
        # SELECT FROM DB
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
        CALL get_beers_by_fuzzy_name(%s, 10, 0)
        """, (beer_name))
        beers = cursor.fetchall()

        # Return as rendered html
        if request.headers.get("as-html"):
            return as_html(beers)

        return g.respond(200, beers)

    except Exception as ex:
        print(ex)
        return g.respond(500)

    finally:
        cursor.close()
        db.close()

@view("components/beer_search_results")
def as_html(beers):
    return dict(beers= beers)
