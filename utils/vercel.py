# pylint: disable=C0415,W0611
import requests
from utils import vars as var

def deploy():
    try:
        import production
        requests.get(var.VERCEL_DEPLOY_HOOK, timeout=5)
    except:
        pass
