from bottle import get
from utils.deploy_vercel import _DEPLOY_VERCEL

##############################
@get("/")
def _():
    _DEPLOY_VERCEL()
    return "Welcome!"