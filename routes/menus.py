import math
from bottle import get, view, redirect, request
import pymysql
from utils import g, vars as var, validation as validate

##############################

@get("/menu/<bar_id>/screen/<page_nr>")
@view("menu")
def _(bar_id, page_nr):
    # VALIDATE
    session = validate.session()
    if not session:
        return redirect("/sign-in")

    bar_id, error = validate.id(bar_id)
    if error:
        return g.error_view(404)

    page_nr, error = validate.offset(page_nr)
    if error:
        return g.error_view(404)

    try:
        db=pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()

        # GET tap counts, numbered and off the wall
        cursor.execute("""
        SELECT
            (SELECT COUNT(*) FROM taps WHERE fk_bar_id = %s AND tap_number IS NOT NULL) AS numbered_taps,
            (SELECT COUNT(*) FROM taps WHERE fk_bar_id = %s AND tap_number IS NULL) AS off_wall_taps;
        """, (bar_id, bar_id))
        counters = cursor.fetchone()

        # Calc pages to generate
        numbered_taps_pages, numbered_taps_left = divmod(counters["numbered_taps"], 14)
        off_wall_pages = math.ceil((counters["off_wall_taps"] / 2 + numbered_taps_left) / 14)

        # Calc the limits depending on page_nr + amount of numbered & non-numbered taps
        if  page_nr <= numbered_taps_pages:
            # Numbered taps only
            limit = 14
            offset = (page_nr -1) * 14
        elif off_wall_pages and page_nr == numbered_taps_pages + 1:
            # Combined page
            limit = 28 - numbered_taps_left
            offset = (page_nr -1) * 14
        elif page_nr <= numbered_taps_pages + off_wall_pages:
            # Off wall only
            limit = 28
            offset = numbered_taps_pages * 14 + 28 - numbered_taps_left
        else: return g.error_view(404)

        cursor.execute("""
        SELECT * FROM taps_list
        WHERE fk_bar_id = %s
        LIMIT %s,  %s
        """, (bar_id, offset, limit))
        taps = cursor.fetchall()

        # Return menu_content only
        if request.headers.get("as-chunk"):
            return as_chunk(taps)

        return dict(taps = taps)

    except Exception as ex:
        print(ex)
        return g.error_view(500)

    finally:
        cursor.close()
        db.close()

@view("components/menu_content")
def as_chunk(taps):
    return dict(taps=taps)
    