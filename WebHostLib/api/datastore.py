from typing import Any, Dict
from uuid import UUID

from flask import abort

from WebHostLib import cache
from WebHostLib.api import api_endpoints
from ..models import Room
from Utils import restricted_loads


@api_endpoints.route('/datastorage/<suuid:room_id>')
@cache.memoize(timeout=60)
def read_datastorage(room_id: UUID) -> Dict[str, str]:
    # TODO: Impliment POST method to update datastorage. This can be accomplished by:
    #       1. Importing Command from models, and commit from pony.orm
    #       2. Mimic the Command interaction from the /room post method from misc.py
    #         - This submits a command to the room, processed by the Multiserver.py ServerCommandProcessor
    #       3. Add an additonal command to ServerCommandProcessor to write to the datastorage.
    #       Currently, there is no need/want to write to the datastorage, and would require a significant lift to do so.

    room = Room.get(id=room_id)
    if room is None:
        return abort(404)
    
    datastorage = restricted_loads(room.multisave).get('stored_data',{}) if room.multisave else {}

    return datastorage
