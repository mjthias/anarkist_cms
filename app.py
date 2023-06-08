# pylint: disable=W0611,

from bottle import get, static_file, run, default_app, error
from utils import g

##############################

# API
import api.sessions.post
import api.sessions.location_post
import api.users.users_get
import api.users.user_post
import api.users.user_by_id_get
import api.users.user_by_id_put
import api.users.user_by_id_delete
import api.users.password_put
import api.breweries.get
import api.breweries.search
import api.breweries.post
import api.breweries.by_id_put
import api.breweries.by_id_delete
import api.bars.get
import api.bars.post
import api.bars.by_id_put
import api.bars.by_id_delete
import api.beers.post
import api.beers.by_id_put
import api.beers.by_id_delete
import api.beers.by_name_get
import api.taps.get
import api.taps.notification
import api.taps.post
import api.taps.by_id_put
import api.taps.by_id_delete
import api.bars.bar_access_post
import api.bars.bar_access_delete
import api.beer_styles.get
import api.beer_styles.post
import api.beer_styles.by_id_put
import api.beer_styles.by_id_delete

# CMS
import routes.sign_in
import routes.select_location
import routes.sign_out
import routes.home
import routes.bars.index
import routes.bars.create
import routes.bars.by_id
import routes.breweries.index
import routes.breweries.create
import routes.breweries.by_id
import routes.beers.index
import routes.beers.create
import routes.beers.by_id
import routes.beer_styles.index
import routes.beer_styles.create
import routes.beer_styles.by_id
import routes.taps.index
import routes.taps.create
import routes.taps.by_id
import routes.users.index
import routes.users.create
import routes.users.by_id
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
