from bottle import get, view, redirect, response
import utils.validation as validate
import utils.g as g
import utils.vars as var
import pymysql

@get("/users/<search_user_id>")
@view("single_user")
def _(search_user_id):
    # VALIDATE
    session = validate.session()
    if not session:
        return redirect("/sign-in")
    
    search_user_id, error = validate.id(search_user_id)
    if error:
        return g.respond(404, "Page not found")
    
    # Extract needed values from session
    role_id=int(session["role_id"])
    bar_id=int(session["bar_id"])
    user_id=int(session["user_id"])

    # role = staffs can only access their own user
    if role_id == 3 and user_id != search_user_id:
        return redirect("/")

    # SELECT USER FROM DB
    try:
        db = pymysql.connect(**var.DB_CONFIG)
        cursor = db.cursor()

        # FOR SUPER USERS
        if role_id == 1:
            cursor.execute("""
                SELECT * FROM `users_list` 
                WHERE bar_id = %s
                AND user_id = %s
                OR user_role_id = 1 
                AND user_id = %s
                LIMIT 1;
                """, (bar_id, search_user_id, search_user_id))
            user = cursor.fetchone()

            # If searched user != super_user, bar_access needed
            if user and user["user_role_id"] != "1":
                cursor.execute("""
                    SELECT bar_id, bar_name 
                    FROM bar_access
                    JOIN bars
                    WHERE fk_user_id = %s 
                    AND fk_bar_id = bar_id
                    """, (search_user_id))
                bar_access = cursor.fetchall()
                user["bar_access"] = bar_access

                cursor.execute("SELECT * FROM BARS")
                bars = cursor.fetchall()

        # NON-SUPER-USERS
        else:
            cursor.execute("""
                SELECT * FROM `users_list` 
                WHERE bar_id = %s AND user_id = %s
                LIMIT 1;
                """, (bar_id, search_user_id))
            user = cursor.fetchone()

        return dict(
                user = user,
                search_user_id = search_user_id,
                session = session,
                bars=bars,
                )

    except Exception as ex:
        print(str(ex))
        return g.respond(500, "Server error")

    finally:
        cursor.close()
        db.close()