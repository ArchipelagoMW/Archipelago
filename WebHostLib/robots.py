from WebHostLib import app
from flask import abort
from . import cache


@cache.cached()
@app.route('/robots.txt')
def robots():
    # If this host is not official, do not allow search engine crawling
    if not app.config["ASSET_RIGHTS"]:
        return app.send_static_file('robots.txt')

    # Send 404 if the host has affirmed this to be the official WebHost
    abort(404)
