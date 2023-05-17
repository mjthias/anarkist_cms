from bottle import get, request, response
from utils.vars import _DB_CONFIG
import utils.validation as validate
import pymysql
import json

##############################

@get("/api/taps")
def _():
    response.content_type = 'application/json'

    # VALIDATE INPUT VLAUES
    bar_id = request.query.get("bar-id")
    if bar_id and not validate.id(bar_id):
        response.status = 400
        return json.dumps({"error": "Bar-id must be a positive integer"})
    
    limit = request.query.get("limit")
    if limit and not validate.limit(limit):
        response.status = 400
        return json.dumps({"error": "Limit must be -1 or a postive integer"})
    if not limit:
        limit = 100

    offset = request.query.get("offset")
    if offset and not validate.offset(offset):
        response.status = 400
        return json.dumps({"error": "Offset must 0 or a positive integer"})
    if not offset:
        offset = 0

    # BUILD QUERY
    # init values
    params = {}
    where_clause = ""
    limit_clause = ""

    # exlude limits if limit=-1
    if limit != "-1":
        limit_clause = "LIMIT %(limit)s OFFSET %(offset)s"
        params["limit"] = int(limit)
        params["offset"] = int(offset)

    # set where_clause if bar_id
    if bar_id:
        where_clause = "WHERE fk_bar_id = %(bar_id)s"
        params["bar_id"] = int(bar_id)

    # build query
    query = f"""
    SELECT * FROM taps_list
    {where_clause}
    ORDER BY tap_number
    {limit_clause}
    """

    # CONNNECT TO DB AND EXECUTE
    try:
        db = pymysql.connect(**_DB_CONFIG)
        cursor = db.cursor()
        cursor.execute(query, params)
        if limit == "1":
            taps = cursor.fetchone()
        else:    
            taps = cursor.fetchall()

        response.status = 200
        return json.dumps(taps)

    except Exception as ex:
        print(str(ex))
        response.status = 500
        return "Server error"

    finally:
        cursor.close()
        db.close()
    
