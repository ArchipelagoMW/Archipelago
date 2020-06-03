from __future__ import annotations
import asyncio
import json
import logging
import typing

import websockets


class Node:
    endpoints: typing.List

    def __init__(self):
        self.endpoints = []

    def broadcast_all(self, msgs):
        msgs = json.dumps(msgs)
        for endpoint in self.endpoints:
            asyncio.create_task(self.send_json_msgs(endpoint, msgs))

    async def send_msgs(self, endpoint: Endpoint, msgs):
        if not endpoint.socket or not endpoint.socket.open or endpoint.socket.closed:
            return
        try:
            await endpoint.socket.send(json.dumps(msgs))
        except websockets.ConnectionClosed:
            logging.exception("Exception during send_msgs")
            await self.disconnect(endpoint)

    async def send_json_msgs(self, endpoint: Endpoint, msg: str):
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
