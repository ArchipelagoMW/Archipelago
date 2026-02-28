from typing_extensions import override

from NetUtils import GamesPackage
from Utils import restricted_loads
from apmw.multiserver.gamespackage.cache import GamesPackageCache, ItemNameGroups, LocationNameGroups


class DBGamesPackageCache(GamesPackageCache):
    _static: dict[str, tuple[GamesPackage, ItemNameGroups, LocationNameGroups]]

    def __init__(self, static_games_package: dict[str, GamesPackage]) -> None:
        super().__init__()
        self._static = {game: GamesPackageCache.get(self, game, games_package) for game, games_package in static_games_package.items()}

    @override
    def get(
        self,
        game: str,
        full_games_package: GamesPackage,
    ) -> tuple[GamesPackage, ItemNameGroups, LocationNameGroups]:
        # for games started on webhost, full_games_package is likely unpopulated and only has the checksum field
        cache_key = (game, full_games_package.get("checksum", None))
        cached = self._get(cache_key)
        if any(value is None for value in cached):
            if "checksum" not in full_games_package:
                return super().get(game, full_games_package)  # no checksum, assume fully populated

            from WebHostLib.models import GameDataPackage

            row: GameDataPackage | None = GameDataPackage.get(checksum=full_games_package["checksum"])
            if row:  # None if rolled on >= 0.3.9 but uploaded to <= 0.3.8 ...
                return super().get(game, restricted_loads(row.data))
            return super().get(game, full_games_package)  # ... in which case full_games_package should be populated

        return cached  # type: ignore # mypy doesn't understand any value is None

    @override
    def get_static(self, game: str) -> tuple[GamesPackage, ItemNameGroups, LocationNameGroups]:
        return self._static[game]
