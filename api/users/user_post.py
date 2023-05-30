# pylint: disable=W0612
from bottle import post, request
import bcrypt
import pymysql
from utils import g, vars as var, validation as validate


##############################
@post(f"{var.API_PATH}/users")
def _():
    try:
        # VALIDATE SESSION AND USER ROLE
        session = validate.session()
        if not session:
            return g.respond(401)

        if session["role_id"] == 3:
            return g.respond(401)

        bar_id = session["bar_id"]

        # VALIDATE INPUT VALUES
        user_name, error = validate.user_name(request.forms.get("user_name"))
        if error:
            return g.respond(400, {"info": error, "key": "user_name"})

        user_email, error = validate.email(request.forms.get("user_email"))
        if error:
            return g.respond(400, {"info": error, "key": "user_email"})

        user_password, error = validate.password(request.forms.get("user_password"))
        if error:
            return g.respond(400, {"info:": error, "key": "user_password"})

        user_confirm_password, error = validate.confirm_password(user_password, request.forms.get("user_confirm_password"))
        if error:
            return g.respond(400, {"info": error, "key": "user_confirm_password"})

        user_role_id, error = validate.role_id(request.forms.get("user_role_id"))
        if error:
            return g.respond(400,  {"info": error, "key": "user_role_id"})

        # Admins cant create super users
        if session["role_id"] == 2 and user_role_id == 1:
            return g.respond(401, "Unauthorized attempt.")

        # GENERATE HASHED PASSWORD
        user_password_bytes = user_password.encode('utf-8')
        salt = bcrypt.gensalt()
        hash_user_password = bcrypt.hashpw(user_password_bytes, salt)
        user_password = str(hash_user_password)[2:-1]

        user = (
            user_email,
            user_name,
            user_password,
            user_role_id
        )

    except Exception as ex:
        print(str(ex))
        return g.respond(500)

    # CONNECT TO DB
    try:
        db = pymysql.connect(**var.DB_CONFIG)
        db.begin()
        cursor = db.cursor()

        query = """
        INSERT INTO users
        (user_email,
        user_name,
        user_password,
        fk_user_role_id)
        VALUES(%s, %s, %s, %s)
        """
        cursor.execute(query, user)
        user_id = cursor.lastrowid

        # IF NEW USER IS NOT A SUPERUSER, INSERT BAR ACCESS AS WELL
        if user_role_id != 1:
            query = """
            INSERT INTO bar_access
            (fk_bar_id,
            fk_user_id)
            VALUES(%s, %s)
            """
            cursor.execute(query, (bar_id, user_id))

        db.commit()

        response_dict = {"id": user_id, "info": "User was successfully created", "entry_type": "user"}

        return g.respond(201, response_dict)

    except Exception as ex:
        print(str(ex))
        db.rollback()
        if "user_email" in str(ex):
            return g.respond(400, {"info": "Email already exists.", "key": "user_email"})
        if "user_role_id" in str(ex):
            return g.respond(400, {"info": "User role does not exist.", "key": "user_role_id"})
        if "bar_id" in str(ex):
            return g.respond(400, "Bar does not exist.")
        return g.respond(500)

    finally:
        cursor.close()
        db.close()
