from waitress import serve
import multiprocessing

from __init__ import app

if __name__ == "__main__":
    multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn')
    serve(app, port=80, threads=1)
