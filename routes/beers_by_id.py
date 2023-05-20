from bottle import get, view, response, redirect
import utils.vars as var
import utils.validation as validate
import utils.g as g
import pymysql

##############################

@get("/beers/<beer_id>")
@view("single_beer")
def _(beer_id=""):
    session = validate.session()
    if not session:
        return redirect("/sign-in")

    try:
        beer_id, error = validate.id(beer_id)
        if error: return g.respond(400, error)
    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error.")
    
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        cursor = db_connect.cursor()
        cursor.execute("SELECT * FROM beer_list WHERE beer_id = %s LIMIT 1", (beer_id,))
        beer = cursor.fetchone()
        beer['beer_price'] = g.format_price(beer["beer_price"])
        beer['beer_alc'] = g.format_price(float(beer['beer_alc']))
        
    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error.")
    finally:
        cursor.close()
        db_connect.close()

    if not beer: 
        return redirect("/404")
    return dict(session = session, beer = beer)