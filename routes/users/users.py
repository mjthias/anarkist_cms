from bottle import get, view, redirect, request
import pymysql
from utils import g, vars as var, validation as validate

@get("/users")
@view("users/index")
def _():
    # VALIDATE
    session = validate.session()
    if not session:
        return redirect("/sign-in")

    try:
        # redirect if role = staff (3)
        role_id=int(session["role_id"])
        if role_id == 3:
            return g.error_view(401)

        user_id=int(session["user_id"])

        limit, error = validate.limit(request.params.get("limit"))
        if error:
            return g.error_view(404)

        offset, error = validate.offset(request.params.get("offset"))
        if error:
            return g.error_view(404)

    except Exception as ex:
        print(str(ex))
        return g.error_view(500)

    # Search_term can be both be user_name and a partial email.
    if request.params.get("name"):
        search_term = request.params.get("name")
    else: search_term = None

    # GET USERS FROM DB
    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        if not search_term:
            cursor.execute("""
            SELECT * FROM users_list
            WHERE user_id != %s
            AND user_role_id >= %s
            ORDER BY bar_city
            LIMIT %s, %s
            """, (user_id, session["role_id"], offset, limit))
        else:
            cursor.execute("""
            CALL get_users_by_fuzzy_name(%s,%s,%s,%s,%s)
            """, (search_term, offset, limit, session["role_id"], session["user_id"]))

        users = cursor.fetchall()

        # Render beer_list.html only?
        if request.headers.get("as-chunk"):
            return as_chunk(users)

        return dict(session = session, users = users)

    except Exception as ex:
        print(str(ex))
        return g.error_view(500)

    finally:
        cursor.close()
        db.close()

# Only render user_list.html
@view("components/user_list")
def as_chunk(users):
    if not users:
        return g.respond(204)
    current_topic = request.params.get("current-topic")
    return dict (
        users = users,
        current_topic = current_topic,
        )
