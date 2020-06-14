from waitress import serve

from __init__ import app

if __name__ == "__main__":
    serve(app, port=80, threads=1)
