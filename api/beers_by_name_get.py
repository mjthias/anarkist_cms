from bottle import get, request, view
import utils.validation as validate
import utils.g as g
import utils.vars as var
import pymysql

##############################

@get(f"{var.API_PATH}/beers")
def _():
    # VALIDATE SESSION
    session = validate.session()
    if not session: return g.respond(401, "Unauthorized attempt")

    #VALIDATE PARAM
    beer_name, error = validate.name(request.params.get("name"))
    if error: return g.respond(400, error)

    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
        CALL get_beers_by_fuzzy_name(%s, 10, 0)
        """, (beer_name))
        beers = cursor.fetchall()

        if request.headers.get("as_html"):
            return as_html(beers)
        
        return g.respond(200, beers)

    except Exception as ex:
        print(ex)
        return g.respond(500, "Server error")
    
    finally:
        cursor.close()
        db.close()

@view("components/beer_search_results")
def as_html(beers):
    return dict(beers= beers)

    

