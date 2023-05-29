from bottle import get, view, redirect, request
import utils.validation as validate
import utils.g as g
import utils.vars as var
import pymysql

@get("/users")
@view("users/index")
def _():
    # VALIDATE
    session = validate.session()
    if not session:
        return redirect("/sign-in")
    
    # redirect if role = staff (3)
    role_id=int(session["role_id"])
    if role_id == 3:
        return g.error_view(401)
    
    user_id=int(session["user_id"])

    limit, error = validate.limit(request.params.get("limit"))
    if error: return g.error_view(404)

    offset, error = validate.offset(request.params.get("offset"))
    if error: return g.error_view(404)
    
    # GET USERS FROM DB
    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()
        # include super_users if super_user
        if role_id == 1:
            cursor.execute("""
                SELECT * FROM users_list
                WHERE user_id != %s
                ORDER BY bar_city
                LIMIT %s, %s
                """, (user_id, offset, limit))
        else:
            cursor.execute("""
                SELECT * FROM users_list
                WHERE user_id != %s AND user_role_id != 1
                ORDER BY bar_city
                LIMIT %s, %s
                """, (user_id, offset, limit))
            
        users = cursor.fetchall()

        # Render beer_list.html only?
        if request.headers.get("as_chunk"):
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
    if not users: return g.respond(204)
    current_topic = request.params.get("current-topic")
    return dict (
        users = users,
        current_topic = current_topic,
        )