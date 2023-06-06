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
            return g.respond(400, {"info": error, "key": "confirm_deletion"})

    except Exception as ex:
        print(str(ex))
        return g.respond(500)

    # CONNECT TO DB
    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()

        # Admins can only delete other users within bar where access_count = 1
        if session["role_id"] == 2 and session["user_id"] != user_id:
            cursor.execute("""
            SELECT users_list.bar_id, COUNT(bar_access.fk_bar_id) AS access_count
            FROM users_list
            JOIN bar_access ON fk_user_id = user_id
            WHERE user_id = %s
            AND bar_id = %s
            LIMIT 1
            """, (user_id, session["bar_id"]))
            user = cursor.fetchone()
            if not user:
                g.respond(204)
            if user["access_count"] > 1:
                return g.respond(401)

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
