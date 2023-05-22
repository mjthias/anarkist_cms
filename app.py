from bottle import get, static_file, run, default_app, error, view

##############################

# API
import api.sign_in_post
import api.select_location_post
import api.users_get
import api.user_post
import api.user_by_id_get
import api.user_by_id_put
import api.user_by_id_delete
import api.password_put
import api.taps_get
import api.breweries_get
import api.breweries_search
import api.breweries_post
import api.breweries_by_id_put
import api.breweries_by_id_delete
import api.bars_get
import api.beer_post
import api.beer_by_id_put
import api.beer_by_id_delete
import api.bar_access_post
import api.bar_access_delete
import api.beer_styles_search
import api.beer_styles_post
import api.beer_style_by_id_put
import api.beer_style_by_id_delete

# CMS
import routes.sign_in
import routes.select_location
import routes.sign_out
import routes.home
import routes.breweries
import routes.breweries_create
import routes.breweries_by_id
import routes.beers
import routes.beers_create
import routes.beers_by_id
import routes.beer_styles
import routes.beer_styles_create
import routes.beer_style_by_id
import routes.taps
import routes.users
import routes.users_create
import routes.users_by_id
import routes.error_404
import routes.error_500

##############################

# Static files
@get("/static/<dir_name>/<file_name>")
def _(dir_name, file_name):
    return static_file(file_name, root=f"./static/{dir_name}")

@get("/static/images/<image>")
def _(image):
    return static_file(image, root="./static/images", mimetype="image/*")

##############################


try:
    # Prod
    import production
    application = default_app()
except:
    # Dev
    run( host="127.0.0.1", port=5555, debug=True, reloader=True )