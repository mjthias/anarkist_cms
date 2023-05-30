# pylint: disable=W0612
from bottle import delete, request
import pymysql
from utils import g, vars as var, validation as validate

##############################

@delete(f"{var.API_PATH}/users/<user_id>")
def _(user_id):
    try:
        # VALIDATE SESSION/USER
        session = validate.session()
        if not session:
            return g.respond(401)

        # VALIDATE INPUT VALUES
        user_id, error = validate.id(user_id)
        if error:
            return g.respond(400, f"User {error}")

        # Staffs can only delete themselves
        if session["role_id"] == 3 and session["user_id"] != user_id:
            return g.respond(401)

        # type 'DELETE' to confirm
        confirm_deletion, error = validate.confirm_deletion(request.forms.get("confirm_deletion"))
        if error:
            return g.respond(400, error)

    except Exception as ex:
        print(str(ex))
        return g.respond(500)

    # CONNECT TO DB
    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()

        # Admins can only delete users within bar
        if session["role_id"] == 2:
            cursor.execute("""
            SELECT bar_id FROM users_list
            WHERE user_id = %s
            AND bar_id = %s
            LIMIT 1
            """, (user_id, session["bar_id"]))
            user = cursor.fetchone()
            if not user:
                g.respond(204)

        cursor.execute("""
            DELETE FROM users 
            WHERE user_id = %s
            AND fk_user_role_id >= %s
            """, (user_id, session["role_id"]))

        counter = cursor.rowcount
        print(counter)
        if not counter:
            return g.respond(204)
        db.commit()

        return g.respond(200, f"Successfully deleted user with ID: {user_id}")

    except Exception as ex:
        print(str(ex))
        return g.respond(500)

    finally:
        cursor.close()
        db.close()
