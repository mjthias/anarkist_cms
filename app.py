from bottle import get, static_file, run, default_app

##############################

# API
import api.users_get
import api.users_post
import api.users_put
import api.users_delete
import api.taps_get
import api.breweries_get
import api.bars_get

# CMS
import routes.sign_in
import routes.sign_in_post
import routes.select_location
import routes.select_location_post
import routes.sign_out
import routes.home
import routes.beers

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