"""API endpoints package."""
from typing import List, Tuple

from flask import Blueprint

from ..models import Seed

api_endpoints = Blueprint('api', __name__, url_prefix="/api")


def get_players(seed: Seed) -> List[Tuple[str, str]]:
    return [(slot.player_name, slot.game) for slot in seed.slots]


from . import datapackage, generate, room, user  # trigger registration
