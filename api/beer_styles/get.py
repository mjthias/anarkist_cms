from bottle import get, request, view
import pymysql
from utils import g, vars as var, validation as validate

##############################
@get(f"{var.API_PATH}/beer-styles/<beer_style_name>")
def _(beer_style_name=""):
    try:
        # VALIDATE
        session = validate.session()
        if not session:
            return g.respond(401)

        # Input values
        beer_style_name, error = validate.name(beer_style_name)
        if error:
            return g.respond(400, error)

        offset, error = validate.offset(request.query.get("offset"))
        if error:
            return g.respond(400, error)

        limit, error = validate.limit(request.query.get("limit"))
        if error:
            return g.respond(400, error)

    except Exception as ex:
        print(str(ex))
        return g.respond(500)

    try:
        # SELECT FROM DB
        db_connect = pymysql.connect(**var.DB_CONFIG)
        cursor = db_connect.cursor()
        cursor.execute("""
        CALL get_beer_style_by_fuzzy_name(%s, %s, %s)
        """, (beer_style_name, offset, limit))
        beer_styles = cursor.fetchall()

        # Return as rendered html
        if request.headers.get("as-html"):
            return as_html(beer_styles, beer_style_name)

        if not beer_styles:
            return g.respond(204)

        return g.respond(200, beer_styles)

    except Exception as ex:
        print(str(ex))
        return g.respond(500)

    finally:
        cursor.close()
        db_connect.close()

@view("components/beer_styles_search_results")
def as_html(beer_styles, search_term):
    return dict(
        beer_styles=beer_styles,
        search_term=search_term
        )
