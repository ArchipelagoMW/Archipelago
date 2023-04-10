from __future__ import annotations
import logging
import asyncio
import urllib.parse
import sys
import typing
import time
import functools

import ModuleUpdate
ModuleUpdate.update()

import websockets

import Utils


from MultiServer import CommandProcessor
from NetUtils import Endpoint, decode, NetworkItem, encode, JSONtoTextParser, \
    ClientStatus, Permission, NetworkSlot, RawJSONtoTextParser
from Utils import Version, stream_input, async_start
from worlds import network_data_package, AutoWorldRegister
from CommonClient import CommonContext
import os

class GalaxyContext(CommonContext):