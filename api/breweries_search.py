from bottle import get, request
import utils.vars as var
import utils.validation as validate
import utils.g as g
import pymysql

##############################
@get(f"{var.API_PATH}/breweries/<brewery_name>")
def _(brewery_name=""):
    # VALIDATE SESSION/USER
    session = validate.session()
    if not session: return g.respond(401)

    # VALIDATE INPUT/QUERYSTRING VALUE
    try:
        brewery_name, error = validate.name(brewery_name)
        if error: return g.respond(400, error)
        offset, error = validate.offset(request.query.get("offset"))
        if error: return g.respond(400, error)
        limit, error = validate.limit(request.query.get("limit"))
        if error: return g.respond(400, error)
    except Exception as ex:
        print(str(ex))
        return g.respond(500)
    
    # CONNECT TO DB
    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        cursor = db_connect.cursor()

        cursor.execute("CALL get_brewery_by_fuzzy_name(%s, %s, %s)", (brewery_name, offset, limit))
        breweries = cursor.fetchall()
        if not breweries: return g.respond(204)

        return g.respond(200, breweries)
    except Exception as ex:
        print(str(ex))
        return g.respond(500)
    finally:
        cursor.close()
        db_connect.close()

