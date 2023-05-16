import pymysql
import hidden

# DB CONFIGURATION
try:
    import production
    _DB_CONFIG = hidden._DB_CONFIG
except:
    _DB_CONFIG = {
        "host" : "localhost",
        "user" : "root",
        "port" : 8889,
        "password" : "root",
        "database" : "anarkist",
        "cursorclass":pymysql.cursors.DictCursor
    }

_JWT_SECRET = hidden._JWT_SECRET

# API path variable
_API_PATH = "/api/v1"

# Vercel
_VERCEL_DEPLOY_HOOK = hidden._VERCEL_DEPLOY_HOOK
