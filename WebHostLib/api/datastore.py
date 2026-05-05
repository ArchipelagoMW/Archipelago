from typing import Any, Dict
from uuid import UUID

from flask import abort

from WebHostLib import cache
from WebHostLib.api import api_endpoints
from ..models import Room
from Utils import restricted_loads


@api_endpoints.route('/datastorage_read/<suuid:room_id>')
@cache.memoize(timeout=60)
def read_datastorage(room_id: UUID) -> Dict[str, str]:
    room = Room.get(id=room_id)
    if room is None:
        return abort(404)
    
    datastorage = restricted_loads(room.multisave).get('stored_data',{}) if room.multisave else {}

    return {
        "data_storage": datastorage
    }
