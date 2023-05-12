from bottle import run, default_app

##############################

import routes.sign_in
import routes.sign_in_post
import routes.sign_out
import routes.home
import routes.beers

##############################

try:
    # Prod
    import production
    application = default_app()
except:
    # Dev
    run( host="127.0.0.1", port=5555, debug=True, reloader=True )