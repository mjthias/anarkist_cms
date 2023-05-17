import requests
import utils.vars as vars

def _DEPLOY_VERCEL():
    try:
        import production
        requests.get(vars.VERCEL_DEPLOY_HOOK)
    except:
        pass
