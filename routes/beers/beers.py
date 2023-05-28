from bottle import get, view, redirect, request
import utils.vars as var
import utils.validation as validate
import utils.g as g
import pymysql

##############################

@get("/beers")
@view("beers/index")
def _():
    # VALIDATE
    session = validate.session()
    if not session: 
        return redirect("/sign-in")
    
    limit, error = validate.limit(request.params.get("limit"))
    if error: return g.error_view(404)

    offset, error = validate.offset(request.params.get("offset"))
    if error: return g.error_view(404)

    # Get beers from DB
    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
        SELECT * FROM beers_list
        LIMIT %s, %s
        """, (offset, limit))
        beers = cursor.fetchall()

        # Render beer_list.html only?
        if request.headers.get("as_chunk"):
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
    return dict (beers = beers)
    
