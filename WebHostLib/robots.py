from WebHostLib import app
from flask import abort
import os
import Utils
from . import cache


@cache.cached()
@app.route('/robots.txt')
def robots():
    configpath = os.path.abspath("config.yaml")
    if not os.path.exists(configpath):
        configpath = os.path.abspath(Utils.user_path('config.yaml'))

    if os.path.exists(configpath) and not app.config["TESTING"]:
        import yaml
        app.config.from_file(configpath, yaml.safe_load)

    # If this host is not official, do not allow search engine crawling
    if not app.config["ASSET_RIGHTS"]:
        return app.send_static_file('robots.txt')

    # Send 404 if this is the
    abort(404)
