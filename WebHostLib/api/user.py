from flask import session, jsonify

from WebHostLib.models import *
from . import api_endpoints


@api_endpoints.route('/get_rooms')
def get_rooms():
    response = []
    for room in select(room for room in Room if room.owner == session["_id"]):
        response.append({
            "room_id": room.id,
            "seed_id": room.seed.id,
            "creation_time": room.creation_time,
            "last_activity": room.last_activity,
            "last_port": room.last_port,
            "timeout": room.timeout,
            "tracker": room.tracker,
            "players": room.seed.multidata["names"] if room.seed.multidata else [["Singleplayer"]],
        })
    return jsonify(response)


@api_endpoints.route('/get_seeds')
def get_seeds():
    response = []
    for seed in select(seed for seed in Seed if seed.owner == session["_id"]):
        response.append({
            "seed_id": seed.id,
            "creation_time": seed.creation_time,
            "players": seed.multidata.names if seed.multidata else [["Singleplayer"]],
        })
    return jsonify(response)