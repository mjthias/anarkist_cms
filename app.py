# pylint: disable=W0611,

from bottle import get, static_file, run, default_app, error
from utils import g

##############################

# API
import api.sessions.sign_in_post
import api.sessions.select_location_post
import api.users.users_get
import api.users.user_post
import api.users.user_by_id_get
import api.users.user_by_id_put
import api.users.user_by_id_delete
import api.users.password_put
import api.breweries.breweries_get
import api.breweries.breweries_search
import api.breweries.breweries_post
import api.breweries.breweries_by_id_put
import api.breweries.breweries_by_id_delete
import api.bars.bars_get
import api.bars.bars_post
import api.bars.bars_by_id_put
import api.bars.bars_by_id_delete
import api.beers.beer_post
import api.beers.beer_by_id_put
import api.beers.beer_by_id_delete
import api.beers.beers_by_name_get
import api.taps.taps_get
import api.taps.taps_post
import api.taps.taps_by_id_put
import api.taps.taps_by_id_delete
import api.bars.bar_access_post
import api.bars.bar_access_delete
import api.beer_styles.beer_styles_search
import api.beer_styles.beer_styles_post
import api.beer_styles.beer_style_by_id_put
import api.beer_styles.beer_style_by_id_delete

# CMS
import routes.sign_in
import routes.select_location
import routes.sign_out
import routes.home
import routes.bars.bars
import routes.bars.bars_create
import routes.bars.bars_by_id
import routes.breweries.breweries
import routes.breweries.breweries_create
import routes.breweries.breweries_by_id
import routes.beers.beers
import routes.beers.beers_create
import routes.beers.beers_by_id
import routes.beer_styles.beer_styles
import routes.beer_styles.beer_styles_create
import routes.beer_styles.beer_style_by_id
import routes.taps.taps
import routes.taps.taps_create
import routes.taps.taps_by_id
import routes.users.users
import routes.users.users_create
import routes.users.users_by_id
import routes.menus

##############################

# Static files
@get("/static/<dir_name>/<file_name>")
def _(dir_name, file_name):
    return static_file(file_name, root=f"./static/{dir_name}")

@get("/static/images/<image>")
def _(image):
    return static_file(image, root="./static/images", mimetype="image/*")

##############################

# Non-spa error pages
@error(404)
def _(error):
    print(error)
    return g.error_view(404)

@error(500)
def _(error):
    print(error)
    return g.error_view(500)

##############################

try:
    # Prod
    import production
    application = default_app()

except:
    # Dev
    run( host="127.0.0.1", port=5555, debug=True, reloader=True )
