from bottle import get, static_file, run, default_app

##############################

# Routes
import routes.sign_in
import routes.sign_in_post
import routes.sign_out
import routes.home
import routes.beers

# API
...

##############################

# Static files
@get("/static/<dir_name>/<file_name>")
def _(dir_name, file_name):
    return static_file(file_name, root=f"./static/{dir_name}")

##############################


try:
    # Prod
    import production
    application = default_app()
except:
    # Dev
    run( host="127.0.0.1", port=5555, debug=True, reloader=True )