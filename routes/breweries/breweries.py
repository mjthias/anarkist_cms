from bottle import get, view, redirect, request
import pymysql
from utils import g, vars as var, validation as validate

########################################

@get("/breweries")
@view("breweries/index")
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
            brewery_name, error = validate.brewery_name(request.params.get("name"))
            if error:
                return g.error_view(204)
        else: brewery_name = None

    except Exception as ex:
        print(ex)
        return g.error_view(500)

    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        if not brewery_name:
            cursor.execute("""
            SELECT * FROM breweries
            ORDER BY brewery_name
            LIMIT %s, %s
            """, (offset, limit))
        else:
            cursor.execute("""
            CALL get_brewery_by_fuzzy_name(%s, %s, %s)
            """, (brewery_name, offset, limit))

        breweries = cursor.fetchall()

        # Render beer_list.html only?
        if request.headers.get("as-chunk"):
            return as_chunk(breweries)

        return dict(
            session = session,
            breweries = breweries
            )

    except Exception as ex:
        print(ex)
        return g.error_view(500)

    finally:
        cursor.close()
        db.close()


# Only render breweries_list.html
@view("components/breweries_list")
def as_chunk(breweries):
    if not breweries:
        return g.error_view(204)
    current_topic = request.params.get("current-topic")
    return dict (
        breweries = breweries,
        current_topic = current_topic,
        )
