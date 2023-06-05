from bottle import get, view, redirect, request
import pymysql
from utils import g, vars as var, validation as validate

##############################

@get("/beers")
@view("beers/index")
def _():
    # VALIDATE
    session = validate.session()
    if not session:
        return redirect("/sign-in")

    try:
        limit, error = validate.limit(request.params.get("limit"))
        if error:
            return g.error_view(404)

        offset, error = validate.offset(request.params.get("offset"))
        if error:
            return g.error_view(404)

        if request.params.get("name"):
            beer_name, error = validate.name(request.params.get("name"))
            if error:
                return g.error_view(204)
        else: beer_name = None

    except Exception as ex:
        print(str(ex))
        return g.error_view(500)

    # Get beers from DB
    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        if not beer_name:
            cursor.execute("""
            SELECT * FROM beers_list
            LIMIT %s, %s
            """, (offset, limit))
        else:
            cursor.execute("""
            CALL get_beers_by_fuzzy_name(%s, %s, %s)
            """, (beer_name, limit, offset))
        beers = cursor.fetchall()

        # Render beer_list.html only?
        if request.headers.get("as-chunk"):
            return as_chunk(beers)

        return dict(beers = beers, session=session)

    except Exception as ex:
        print(str(ex))
        return g.error_view(500)

    finally:
        cursor.close()
        db.close()

# Only render beer_list.html
@view("components/beer_list")
def as_chunk(beers):
    if not beers:
        return g.error_view(204)
    return dict (beers = beers)
