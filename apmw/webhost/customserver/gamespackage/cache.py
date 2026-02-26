import typing as t

from NetUtils import GamesPackage
from Utils import restricted_loads
from WebHostLib.models import GameDataPackage
from apmw.multiserver.gamespackage.cache import GamesPackageCache, ItemNameGroups, LocationNameGroups


class DBGamesPackageCache(GamesPackageCache):
    _static: dict[str, tuple[GamesPackage, ItemNameGroups, LocationNameGroups]]

    def __init__(self, static_games_package: dict[str, GamesPackage]) -> None:
        super().__init__()
        self._static = {game: super().get(game, games_package) for game, games_package in static_games_package.items()}

    def get(
        self,
        game: str,
        full_games_package: GamesPackage,
    ) -> tuple[GamesPackage, ItemNameGroups, LocationNameGroups]:
        # for games started on webhost, full_games_package is likely unpopulated and only has the checksum field
        cache_key = (game, full_games_package.get("checksum", None))
        cached = self._get(cache_key)
        if any(value is None for value in cached):
            row = GameDataPackage.get(checksum=full_games_package["checksum"])
            if row:  # None if rolled on >= 0.3.9 but uploaded to <= 0.3.8 ...
                return super().get(game, restricted_loads(row.data))
            return super().get(game, full_games_package)  # ... in which case full_games_package should be populated
        return t.cast(tuple[GamesPackage, ItemNameGroups, LocationNameGroups], cached)

    def get_static(self, game: str) -> tuple[GamesPackage, ItemNameGroups, LocationNameGroups]:
        return self._static[game]
