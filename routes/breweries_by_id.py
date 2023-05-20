from bottle import get, view, redirect
import utils.validation as validate
import utils.vars as var
import utils.g as g
import pymysql

##############################

@get("/breweries/<brewery_id>")
@view("single_brewery")
def _(brewery_id):
    #VALIDATE SESSION
    session = validate.session()
    if not session: return redirect("/sign-in")

    # VALIDATE ID
    brewery_id, error = validate.id(brewery_id)
    if error: return g.respond(404, "Page not found")

    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
            SELECT breweries.*, taps_list.brewery_name AS brewery_on_tap FROM breweries
            LEFT JOIN taps_list 
            ON breweries.brewery_name = taps_list.brewery_name
            WHERE brewery_id = %s
            LIMIT 1
            """, (brewery_id))
        brewery = cursor.fetchone()
    
    except Exception as ex:
        print(ex)
        return g.respond(500, "Server error")
    
    finally:
        cursor.close()
        db.close()

    if not brewery:
        return g.respond(404, "Page not found")

    return dict(
        session = session,
        brewery = brewery
        )
