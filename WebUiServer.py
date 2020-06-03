import http.server
import socketserver
import os
import socket
import threading
from functools import partial
import webbrowser

import Utils

webthread = None

PORT = 5050

Handler = partial(http.server.SimpleHTTPRequestHandler, directory=Utils.local_path(os.path.join("data", "web", "public")))


def start_server(socket_port: int, on_start=lambda: None):
    global webthread
    try:
        server = socketserver.TCPServer(("", PORT), Handler)
    except OSError:
        # In most cases "Only one usage of each socket address (protocol/network address/port) is normally permitted"
        import logging

        # If the exception is caused by our desired port being unavailable, assume the web server is already running
        # from another client instance
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', PORT)) == 0:
                logging.info("Web server is already running in another client window.")
                webbrowser.open(f'http://localhost:{PORT}?port={socket_port}')
                return

        # If the exception is caused by something else, report on it
        logging.exception("Unable to bind port for local web server. The CLI client should work in all cases.")
    else:
        print("serving at port", PORT)
        on_start()
        webthread = threading.Thread(target=server.serve_forever).start()


if __name__ == "__main__":
    start_server(5090)
