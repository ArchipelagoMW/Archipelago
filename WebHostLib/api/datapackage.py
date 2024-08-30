from flask import abort

from Utils import restricted_loads
from WebHostLib import cache
from WebHostLib.models import GameDataPackage
from . import api_endpoints


@api_endpoints.route('/datapackage')
@cache.cached()
def get_datapackage():
    from worlds import network_data_package
    return network_data_package


@api_endpoints.route('/datapackage/<string:checksum>')
@cache.memoize(timeout=3600)
def get_datapackage_by_checksum(checksum: str):
    package = GameDataPackage.get(checksum=checksum)
    if package:
        return restricted_loads(package.data)
    return abort(404)


@api_endpoints.route('/datapackage_checksum')
@cache.cached()
def get_datapackage_checksums():
    from worlds import network_data_package
    version_package = {
        game: game_data["checksum"] for game, game_data in network_data_package["games"].items()
    }
    return version_package
