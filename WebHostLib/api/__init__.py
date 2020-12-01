"""API endpoints package."""
from uuid import UUID

from flask import Blueprint, abort

from ..models import Room

api_endpoints = Blueprint('api', __name__, url_prefix="/api")

from . import generate

# unsorted/misc endpoints

@api_endpoints.route('/room_status/<suuid:room>')
def room_info(room: UUID):
    room = Room.get(id=room)
    if room is None:
        return abort(404)
    return {"tracker": room.tracker,
            "players": room.seed.multidata["names"],
            "last_port": room.last_port,
            "last_activity": room.last_activity,
            "timeout": room.timeout}