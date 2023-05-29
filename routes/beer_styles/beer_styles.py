from bottle import get, view, redirect, request
import utils.vars as var
import utils.validation as validate
import utils.g as g
import pymysql

##############################
@get("/beer-styles")
@view("beer_styles/index")
def _():
    session = validate.session()
    if not session: return redirect("/sign-in")

    limit, error = validate.limit(request.params.get("limit"))
    if error: return g.error_view(404)

    offset, error = validate.offset(request.params.get("offset"))
    if error: return g.error_view(404)

    try:
        db_connect = pymysql.connect(**var.DB_CONFIG)
        cursor = db_connect.cursor()
        
        cursor.execute("""
        SELECT * FROM beer_styles
        LIMIT %s, %s
        """, (offset, limit))
        beer_styles = cursor.fetchall()

        # Render beer_styles_list.html only?
        if request.headers.get("as_chunk"):
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
    if not beer_styles: return g.respond(204)
    current_topic = request.params.get("current-topic")
    return dict(
        beer_styles=beer_styles,
        current_topic = current_topic,
        )
