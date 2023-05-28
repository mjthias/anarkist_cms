from bottle import get, view, redirect, request
import utils.validation as validate
import utils.vars as var
import utils.g as g
import pymysql

########################################

@get("/breweries")
@view("breweries/index")
def _():
    session = validate.session()
    if not session: return redirect("/sign-in")

    limit, error = validate.limit(request.params.get("limit"))
    if error: return g.error_view(404)

    offset, error = validate.offset(request.params.get("offset"))
    if error: return g.error_view(404)

    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
            SELECT * FROM breweries
            ORDER BY brewery_name
            LIMIT %s, %s
            """, (offset, limit))
        breweries = cursor.fetchall()

        # Render beer_list.html only?
        if request.headers.get("as_chunk"):
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
    return dict (breweries = breweries)