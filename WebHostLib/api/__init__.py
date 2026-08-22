"""API endpoints package."""
from typing import List, Tuple

from flask import Blueprint
from flask_cors import CORS

from Utils import __version__
from ..models import Seed, Slot

api_endpoints = Blueprint('api', __name__, url_prefix="/api")
cors = CORS(api_endpoints, resources={
                r"/api/version": {"origins": "*"},
                r"/api/datapackage/*": {"origins": "*"},
                r"/api/datapackage": {"origins": "*"},
                r"/api/datapackage_checksum/*": {"origins": "*"},
                r"/api/room_status/*": {"origins": "*"},
                r"/api/tracker/*": {"origins": "*"},
                r"/api/static_tracker/*": {"origins": "*"},
                r"/api/slot_data_tracker/*": {"origins": "*"}
            })


def get_players(seed: Seed) -> List[Tuple[str, str]]:
    return [(slot.player_name, slot.game) for slot in seed.slots.order_by(Slot.player_id)]

# trigger endpoint registration
from . import datapackage, generate, room, tracker, user

API_VERSION = {
    "ap_core_version": __version__,
    "tracker_api_version": str(tracker.TRACKER_VERSION)
}

@api_endpoints.route("/version")
def version() -> dict[str, str]:
    return API_VERSION
