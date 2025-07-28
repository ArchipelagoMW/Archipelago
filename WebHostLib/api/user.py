from flask import session, jsonify
from pony.orm import select

from WebHostLib import to_url
from WebHostLib.models import Room, Seed
from . import api_endpoints, get_players


@api_endpoints.route('/get_rooms')
def get_rooms():
    response = []
    for room in select(room for room in Room if room.owner == session["_id"]):
        response.append({
            "room_id": to_url(room.id),
            "seed_id": to_url(room.seed.id),
            "creation_time": room.creation_time,
            "last_activity": room.last_activity,
            "last_port": room.last_port,
            "timeout": room.timeout,
            "tracker": to_url(room.tracker),
        })
    return jsonify(response)


@api_endpoints.route('/get_seeds')
def get_seeds():
    response = []
    for seed in select(seed for seed in Seed if seed.owner == session["_id"]):
        response.append({
            "seed_id": to_url(seed.id),
            "creation_time": seed.creation_time,
            "players": get_players(seed),
        })
    return jsonify(response)
