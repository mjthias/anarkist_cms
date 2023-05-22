from bottle import get, view, redirect
import utils.validation as validate
import utils.vars as var
import utils.g as g
import pymysql

##############################

@get("/bars/<bar_id>")
@view("single_bar")
def _(bar_id):
    # VALIDATE SESSION
    session = validate.session()
    if not session: return redirect("/sign-in")

    # VALIDATE ROLE
    if not session["role_id"] == 1:
        return redirect("/")
    
    # VALIDATE BAR ID
    bar_id, error = validate.id(bar_id)
    if error: return g.respond(404, "Page not found")
    
    # GET BAR FROM DB
    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
        SELECT * FROM bars
        WHERE bar_id = %s
        LIMIT 1
        """, (bar_id))
        bar = cursor.fetchone()
        if not bar: return g.respond(404, "Page not found")
        
        return dict(
            session = session,
            bar = bar
            )

    except Exception as ex:
        print(ex)
        return g.respond(500, "Server error")

    finally:
        cursor.close()
        db.close()

    

