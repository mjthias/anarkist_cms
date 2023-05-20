from bottle import delete, request
import utils.vars as var
import utils.validation as validate
import utils.g as g
import pymysql

##############################

@delete(f"{var.API_PATH}/breweries/<brewery_id>")
def _(brewery_id):
    #VALIDATE SESSION & ROLE AUTH
    session = validate.session()
    if not session:
        return g.respond(401, "Unautorized attempt")
    
    if session["role_id"] == 3:
        return g.respond(401, "Unautorized attempt")
    
    # VALIDATE BREWERY ID PARAM
    brewery_id, error = validate.id(brewery_id)
    if error: return g.respond(400, error)

    # VALIDATE INPUT VALUES
    confirm_deletion, error = validate.confirm_deletion(request.forms.get("confirm_deletion"))
    if error: return g.respond(400, error)

    # DELETE FROM DB
    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
            DELETE FROM breweries
            WHERE brewery_id = %s
            """, (brewery_id))
        counter = cursor.rowcount
        if not counter: return g.respond(204, "")
        db.commit()

        return g.respond(200, f"Brewery with id: {brewery_id}, deleted")

    except Exception as ex:
        print(ex)
        return g.respond(500, "Server error")
    
    finally:
        cursor.close()
        db.close()



