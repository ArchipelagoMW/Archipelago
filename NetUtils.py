from __future__ import annotations
import asyncio
import logging
import typing
from html.parser import HTMLParser
from json import loads, dumps

import websockets


class Node:
    endpoints: typing.List
    dumper = staticmethod(dumps)
    loader = staticmethod(loads)

    def __init__(self):
        self.endpoints = []
        super(Node, self).__init__()

    def broadcast_all(self, msgs):
        msgs = self.dumper(msgs)
        for endpoint in self.endpoints:
            asyncio.create_task(self.send_encoded_msgs(endpoint, msgs))

    async def send_msgs(self, endpoint: Endpoint, msgs: typing.Iterable[typing.Sequence[str, typing.Optional[dict]]]):
        if not endpoint.socket or not endpoint.socket.open or endpoint.socket.closed:
            return
        try:
            await endpoint.socket.send(self.dumper(msgs))
        except websockets.ConnectionClosed:
            logging.exception("Exception during send_msgs")
            await self.disconnect(endpoint)

    async def send_encoded_msgs(self, endpoint: Endpoint, msg: str):
        if not endpoint.socket or not endpoint.socket.open or endpoint.socket.closed:
            return
        try:
            await endpoint.socket.send(msg)
        except websockets.ConnectionClosed:
            logging.exception("Exception during send_msgs")
            await self.disconnect(endpoint)

    async def disconnect(self, endpoint):
        if endpoint in self.endpoints:
            self.endpoints.remove(endpoint)


class Endpoint:
    socket: websockets.WebSocketServerProtocol

    def __init__(self, socket):
        self.socket = socket

    async def disconnect(self):
        raise NotImplementedError


class HTMLtoColoramaParser(HTMLParser):
    def get_colorama_text(self, input_text: str) -> str:
        self.feed(input_text)
        self.close()
        data = self.data
        self.reset()
        return data

    def handle_data(self, data):
        self.data += data

    def handle_starttag(self, tag, attrs):
        if tag in {"span", "div", "p"}:
            for attr in attrs:
                subtag, data = attr
                if subtag == "style":
                    for subdata in data.split(";"):
                        if subdata.startswith("color"):
                            color = subdata.split(":", 1)[-1].strip()
                            if color in color_codes:
                                self.data += color_code(color)
                                self.colored = tag

    def handle_endtag(self, tag):
        if tag == self.colored:
            self.colored = False
            self.data += color_code("reset")

    def reset(self):
        super(HTMLtoColoramaParser, self).reset()
        self.data = ""
        self.colored = False

    def close(self):
        super(HTMLtoColoramaParser, self).close()
        if self.colored:
            self.handle_endtag(self.colored)


color_codes = {'reset': 0, 'bold': 1, 'underline': 4, 'black': 30, 'red': 31, 'green': 32, 'yellow': 33, 'blue': 34,
               'magenta': 35, 'cyan': 36, 'white': 37, 'black_bg': 40, 'red_bg': 41, 'green_bg': 42, 'yellow_bg': 43,
               'blue_bg': 44, 'purple_bg': 45, 'cyan_bg': 46, 'white_bg': 47}


def color_code(*args):
    return '\033[' + ';'.join([str(color_codes[arg]) for arg in args]) + 'm'


def color(text, *args):
    return color_code(*args) + text + color_code('reset')


CLIENT_UNKNOWN = 0
CLIENT_READY = 10
CLIENT_PLAYING = 20
CLIENT_GOAL = 30