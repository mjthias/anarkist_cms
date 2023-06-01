from bottle import get, request
import pymysql
from utils import g, vars as var, validation as validate

##############################

@get(f"{var.API_PATH}/taps")
def _():
    try:
        # VALIDATE VALUES (limits)
        limit, error = validate.limit(request.query.get("limit"))
        if error:
            return g.respond(400, error)

        offset, error = validate.offset(request.query.get("offset"))
        if error:
            return g.respond(400, error)

        # BUILD QUERY
        # init values
        params = {}
        limit_clause = ""

        # exlude limits if limit=-1
        if limit != -1:
            limit_clause = "LIMIT %(limit)s OFFSET %(offset)s"
            params["limit"] = limit
            params["offset"] = offset

        # build query
        query = f"""
        SELECT * FROM taps_list
        ORDER BY tap_number
        {limit_clause}
        """

    except Exception as ex:
        print(str(ex))
        return g.respond(500)

    # CONNNECT TO DB AND EXECUTE
    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute(query, params)
        if limit == 1:
            taps = cursor.fetchone()
        else:
            taps = cursor.fetchall()
        if not taps:
            return g.respond(204)

        return g.respond(200, taps)

    except Exception as ex:
        print(str(ex))
        return g.respond(500)

    finally:
        cursor.close()
        db.close()
