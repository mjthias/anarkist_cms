from bottle import delete, request
import utils.validation as validate
import utils.vars as var
import utils.g as g
import pymysql

##############################

@delete(f"{var.API_PATH}/bars/<bar_id>")
def _(bar_id):
    # VALIDATE 
    # Session
    session = validate.session()
    if not session: 
        return g.respond(401, "Unauthorized attempt.")

    # Role
    if not session["role_id"] == 1:
        return g.respond(401, "Unauthorized attempt.")

    # bar id param
    bar_id, error = validate.id(bar_id)
    if error: return g.respond(400, error)

    # Input values
    x, error = validate.confirm_deletion(request.forms.get("confirm_deletion"))
    if error: return g.respond(400, error)

    # Update in db
    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""
        DELETE FROM bars
        WHERE bar_id = %s
        """, (bar_id))
        counter = cursor.rowcount
        if not counter: return g.respond(204, "")
        db.commit()

        return g.respond(200, "Bar updated")

    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error")

    finally:
        cursor.close()
        db.close()
    
