# pylint: disable=W0611
import pymysql
try:
    import hidden
except:
    import hidden_expample as hidden

# DB CONFIGURATION
try:
    import production
    DB_CONFIG = hidden.DB_CONFIG
except:
    DB_CONFIG = {
        "host" : "localhost",
        "user" : "root",
        "port" : 8889,
        "password" : "root",
        "database" : "anarkist",
        "cursorclass":pymysql.cursors.DictCursor
    }

JWT_SECRET = hidden.JWT_SECRET

# API path variable
API_PATH = "/api/v1"

# Vercel
VERCEL_DEPLOY_HOOK = hidden.VERCEL_DEPLOY_HOOK

# Authorized user roles
AUTH_USER_ROLES = [1, 2]

# Name variables
NAME_MIN_LEN = 2
NAME_MAX_LEN = 100

# Image path
IMAGE_PATH = "./static/images/"
