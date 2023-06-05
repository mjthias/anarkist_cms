# pylint: disable=W0612
from bottle import delete, request
import pymysql
from utils import g, vars as var, validation as validate

##############################

@delete(f"{var.API_PATH}/breweries/<brewery_id>")
def _(brewery_id):
    try:
        #VALIDATE SESSION & ROLE AUTH
        session = validate.session()
        if not session:
            return g.respond(401)

        if session["role_id"] == 3:
            return g.respond(401)

        # VALIDATE BREWERY ID PARAM
        brewery_id, error = validate.id(brewery_id)
        if error:
            return g.respond(400, error)

        # VALIDATE INPUT VALUES
        confirm_deletion, error = validate.confirm_deletion(request.forms.get("confirm_deletion"))
        if error:
            return g.respond(400, {"info": error, "key": "confirm_deletion"})

    except Exception as ex:
        print(ex)
        return g.respond(500)

    try:
        # DELETE FROM DB
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
        DELETE FROM breweries
        WHERE brewery_id = %s
        """, (brewery_id))
        counter = cursor.rowcount
        if not counter:
            return g.respond(204)
        db.commit()

        return g.respond(200, f"Brewery with id: {brewery_id}, deleted")

    except Exception as ex:
        print(ex)
        if "beers" in str(ex):
            return g.respond(403, {"info": "One or more beers references this brewery.", "key": "confirm_deletion"})
        return g.respond(500)

    finally:
        cursor.close()
        db.close()
