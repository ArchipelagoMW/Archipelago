from WebHostLib import app
from . import cache


@cache.cached()
@app.route('/robots.txt')
def robots():
    return app.send_static_file('robots.txt')
