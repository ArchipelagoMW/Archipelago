"""Custom exceptions for randomizer operations."""


class EntrancePlacementException(Exception):
    """Exception triggered when shuffled entrances fails to produce a valid world."""


class EntranceOutOfDestinations(EntrancePlacementException):
    """Exception triggered when an entrance attempted to be shuffled has no valid destinations."""


class EntranceAttemptCountExceeded(EntrancePlacementException):
    """Exception triggered when too many attempts were made to place entrances."""


class BarrelPlacementException(Exception):
    """Exception triggered when shuffled barrel minigames fails to produce a valid world."""


class BarrelOutOfMinigames(BarrelPlacementException):
    """Exception triggered when a barrel attempted to be shuffled has no valid minigames."""


class BarrelAttemptCountExceeded(BarrelPlacementException):
    """Exception triggered when too many attempts were made to place minigames."""


class KasplatPlacementException(Exception):
    """Exception triggered when shuffled kasplats minigames fails to produce a valid world."""


class KasplatOutOfKongs(KasplatPlacementException):
    """Exception triggered when a kasplat attempted to be shuffled has no valid kongs."""


class KasplatAttemptCountExceeded(KasplatPlacementException):
    """Exception triggered when too many attempts were made to place kasplats."""


class FillException(Exception):
    """Exception triggered during the fill process."""


class ItemPlacementException(FillException):
    """Exception triggered when not all items are placed from running out of reachable locations."""


class GameNotBeatableException(FillException):
    """Exception triggered when all items were placed but the game was not beatable."""


class VanillaItemsGameNotBeatableException(FillException):
    """Exception triggered when all locations have vanilla items but the game was not beatable."""


class MusicPlacementExceededMapThreshold(Exception):
    """Exception triggered when shuffled music leads to a map having too big music files."""


class MusicAttemptCountExceeded(Exception):
    """Exception triggered when too many attempts were made to place music."""


class BossOutOfLocationsException(FillException):
    """Exception triggered when there are no valid levels to put a boss."""


class CBFillFailureException(FillException):
    """Exception triggered when CB rando fails to correctly generate a valid set of groups."""


class CoinFillFailureException(FillException):
    """Exception triggered when coin rando fails to correctly generate a valid set of groups."""


class RaceCoinFillFailureException(FillException):
    """Exception triggered when race coin rando fails to correctly generate a valid set of groups."""


class SettingsIncompatibleException(FillException):
    """Exception triggered when conditions arise that are most likely a settings incompatibility."""


class PlandoIncompatibleException(FillException):
    """Exception triggered when plando settings conflict with base settings."""


class LocationsFailureException(FillException):
    """Exception triggered when not all locations are reachable after placing random locations."""
