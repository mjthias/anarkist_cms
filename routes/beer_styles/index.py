from bottle import get, view, redirect, request
import pymysql
from utils import g, vars as var, validation as validate

##############################
@get("/beer-styles")
@view("beer_styles/index")
def _():
    # VALIDATE
    session = validate.session()
    if not session:
        return redirect("/sign-in")

    limit, error = validate.limit(request.params.get("limit"))
    if error:
        return g.error_view(404)

    offset, error = validate.offset(request.params.get("offset"))
    if error:
        return g.error_view(404)

    if request.params.get("name"):
        beer_style_name, error = validate.name(request.params.get("name"))
        if error:
            return g.error_view(204)
    else: beer_style_name = None

    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        cursor = db_connect.cursor()
        # No name search param
        if not beer_style_name:
            cursor.execute("""
            SELECT * FROM beer_styles
            LIMIT %s, %s
            """, (offset, limit))
        # Name search param
        else:
            cursor.execute("""
            CALL get_beer_style_by_fuzzy_name(%s,%s,%s)
            """, (beer_style_name, offset, limit))

        beer_styles = cursor.fetchall()

        # Render beer_styles_list.html only?
        if request.headers.get("as-chunk"):
            return as_chunk(beer_styles)

        return dict(session=session, beer_styles=beer_styles)

    except Exception as ex:
        print(str(ex))
        return g.error_view(500)

    finally:
        cursor.close()
        db_connect.close()

# Only render beer_styles_list.html
@view("components/beer_styles_list")
def as_chunk(beer_styles):
    if not beer_styles:
        return g.error_view(204)
    current_topic = request.params.get("current-topic")
    return dict(
        beer_styles=beer_styles,
        current_topic = current_topic,
        )
