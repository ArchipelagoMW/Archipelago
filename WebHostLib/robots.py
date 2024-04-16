from WebHostLib import app
from . import cache


@app.route('/robots.txt')
@cache.cached(timeout=300)
def robots():
    return app.send_static_file('robots.txt')
