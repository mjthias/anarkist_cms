from bottle import get, view, redirect
import utils.validation as validate
import utils.g as g
import utils.vars as var
import pymysql

@get("/users")
@view("users")
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
                """, (user_id))
        else:
            cursor.execute("""
                SELECT * FROM users_list
                WHERE user_id != %s AND user_role_id != 1
                ORDER BY bar_city
                """, (user_id))
            
        users = cursor.fetchall()
        return dict(session = session, users = users)

    except Exception as ex:
        print(str(ex))
        return g.error_view(500)

    finally:
        cursor.close()
        db.close()