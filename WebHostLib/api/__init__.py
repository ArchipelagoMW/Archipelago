"""API endpoints package."""
from typing import Dict, List

from flask import Blueprint

from ..models import Seed, Slot

api_endpoints = Blueprint('api', __name__, url_prefix="/api")


def get_players(seed: Seed) -> List[Dict[str, str]]:
    return [{"name": slot.player_name, "game": slot.game, "slot": slot.player_id} for slot in seed.slots.order_by(Slot.player_id)]

from . import datapackage, generate, room, user  # trigger registration
