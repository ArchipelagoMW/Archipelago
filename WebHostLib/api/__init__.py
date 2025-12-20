"""API endpoints package."""
from typing import List, Tuple

from flask import Blueprint
from flask_cors import CORS

from ..models import Seed, Slot

api_endpoints = Blueprint('api', __name__, url_prefix="/api")
cors = CORS(api_endpoints, resources={r"/api/*": {"origins": "*"}})


def get_players(seed: Seed) -> List[Tuple[str, str]]:
    return [(slot.player_name, slot.game) for slot in seed.slots.order_by(Slot.player_id)]

# trigger endpoint registration
from . import datapackage, generate, room, tracker, user
