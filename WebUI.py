import http.server
import logging
import os
import socket
import socketserver
import threading
import webbrowser
import asyncio
from functools import partial

from NetUtils import Node
from MultiClient import Context
import Utils

logger = logging.getLogger("WebUIRelay")


class WebUiClient(Node):
    def __init__(self):
        super().__init__()
        self.manual_snes = None

    @staticmethod
    def build_message(msg_type: str, content: dict) -> dict:
        return {'type': msg_type, 'content': content}

    def log_info(self, message, *args, **kwargs):
        self.broadcast_all(self.build_message('info', message))
        logger.info(message, *args, **kwargs)

    def log_warning(self, message, *args, **kwargs):
        self.broadcast_all(self.build_message('warning', message))
        logger.warning(message, *args, **kwargs)

    def log_error(self, message, *args, **kwargs):
        self.broadcast_all(self.build_message('error', message))
        logger.error(message, *args, **kwargs)

    def log_critical(self, message, *args, **kwargs):
        self.broadcast_all(self.build_message('critical', message))
        logger.critical(message, *args, **kwargs)

    def send_chat_message(self, message):
        self.broadcast_all(self.build_message('chat', message))

    def send_connection_status(self, ctx: Context):
        asyncio.create_task(self._send_connection_status(ctx))

    async def _send_connection_status(self, ctx: Context):
        cache = Utils.persistent_load()
        cached_address = cache.get("servers", {}).get("default", None)
        server_address = ctx.server_address if ctx.server_address else cached_address if cached_address else None

        self.broadcast_all(self.build_message('connections', {
            'snesDevice': ctx.snes_attached_device[1] if ctx.snes_attached_device else None,
            'snes': ctx.snes_state,
            'serverAddress': server_address,
            'server': 1 if ctx.server is not None and not ctx.server.socket.closed else 0,
        }))

    def send_device_list(self, devices):
        self.broadcast_all(self.build_message('availableDevices', {
            'devices': devices,
        }))

    def poll_for_server_ip(self):
        self.broadcast_all(self.build_message('serverAddress', {}))

    def notify_item_sent(self, finder, recipient, item, location, i_am_finder: bool, i_am_recipient: bool):
        self.broadcast_all(self.build_message('itemSent', {
            'finder': finder,
            'recipient': recipient,
            'item': item,
            'location': location,
            'iAmFinder': 1 if i_am_finder else 0,
            'iAmRecipient': 1 if i_am_recipient else 0,
        }))

    def notify_item_found(self, finder: str, item: str, location: str, i_am_finder: bool):
        self.broadcast_all(self.build_message('itemFound', {
            'finder': finder,
            'item': item,
            'location': location,
            'iAmFinder': 1 if i_am_finder else 0,
        }))

    def notify_item_received(self, finder: str, item: str, location: str, item_index: int, queue_length: int):
        self.broadcast_all(self.build_message('itemReceived', {
            'finder': finder,
            'item': item,
            'location': location,
            'itemIndex': item_index,
            'queueLength': queue_length,
        }))

    def send_hint(self, finder, recipient, item, location, found, i_am_finder: bool, i_am_recipient: bool,
                  entrance_location: str = None):
        self.broadcast_all(self.build_message('hint', {
            'finder': finder,
            'recipient': recipient,
            'item': item,
            'location': location,
            'found': int(found),
            'iAmFinder': int(i_am_finder),
            'iAmRecipient': int(i_am_recipient),
            'entranceLocation': entrance_location,
        }))

    def send_game_info(self, ctx: Context):
        self.broadcast_all(self.build_message('gameInfo', {
            'serverVersion': Utils.__version__,
            'hintCost': ctx.hint_cost,
            'checkPoints': ctx.check_points,
            'forfeitMode': ctx.forfeit_mode,
            'remainingMode': ctx.remaining_mode,
        }))

    def send_location_check(self, ctx: Context, last_check: str):
        self.broadcast_all(self.build_message('locationCheck', {
            'totalChecks': len(ctx.locations_checked),
            'hintPoints': ctx.hint_points,
            'lastCheck': last_check,
        }))


class WaitingForUiException(Exception):
    pass


web_thread = None
PORT = 5050


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_request(self, code='-', size='-'):
        pass

    def log_message(self, format, *args):
        pass

    def log_date_time_string(self):
        pass


Handler = partial(RequestHandler,
                  directory=Utils.local_path("data", "web", "public"))


def start_server(socket_port: int, on_start=lambda: None):
    global web_thread
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
        web_thread = threading.Thread(target=server.serve_forever).start()
