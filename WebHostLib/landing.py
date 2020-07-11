from flask import render_template
from WebHostLib import app, cache


@cache.memoize(timeout=300)
@app.route('/', methods=['GET', 'POST'])
def landing():
    return render_template("landing.html")
