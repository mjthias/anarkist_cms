from bottle import put, request
import utils.vars as var
import utils.validation as validate
import utils.g as g
import pymysql

##############################

@put(f"{var.API_PATH}/breweries/<brewery_id>")
def _(brewery_id):

    # VALIDATE SESSION
    session = validate.session()
    if not session:
        return g.respond(401, "Unautorized attmept.")
    
    # VALIDATE BREWERY_ID PARAM
    brewery_id, error = validate.id(brewery_id)
    if error: return g.respond(400, error)

    # VALIDATE INPUT VALUES
    brewery_name, error = validate.brewery_name(request.forms.get("brewery_name"))
    if error: return g.respond(400, error)

    # Menu_name only required if len(name) > 50
    if not request.forms.get("brewery_menu_name"):
        if len(brewery_name) > 50:
            return g.respond(400, "Brewery name is too long for menu. Please provide a short menu name")
        brewery_menu_name = brewery_name

    else:
        brewery_menu_name, error = validate.brewery_menu_name(request.forms.get("brewery_menu_name"))
        if error: return g.respond(400, error)

        if len(brewery_menu_name) > len(brewery_name):
            return g.respond(400, "Menu name can't be longer than the actual name")
    
    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
            UPDATE breweries
            SET brewery_name = %s, brewery_menu_name = %s
            WHERE brewery_id = %s
            """, (brewery_name, brewery_menu_name, brewery_id))
        counter = cursor.rowcount
        if not counter: return g.respond(204, "")
        db.commit()
        return g.respond(200, "Brewery updated")

    except Exception as ex:
        print(ex)
        if "brewery_name" in str(ex): return g.respond(400, "Brewery name already registered")
        if "brewery_menu_name" in str(ex): return g.respond(400, "Brewery menu name already registered")
        return g.respond(500, "Server error")
    
    finally:
        cursor.close()
        db.close()


    
