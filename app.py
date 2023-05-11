from bottle import run, default_app

##############################

import routes.sign_in

##############################

try:
    # Prod
    import production
    application = default_app()
except:
    # Dev
    run( host="127.0.0.1", port=5555, debug=True, reloader=True )