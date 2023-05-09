import pymysql
import hidden

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