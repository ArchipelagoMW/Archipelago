from Options import Toggle, Range, Choice, Option
import typing


class LocalUndergroundLakeKey(Toggle):
    """Local Key for Underground Lake Room"""
    display_name = "Place Key for Underground Lake Room locally"

Shivers_options: typing.Dict[str, type(Option)] = {
    "local_key_for_underground_lake_room": LocalUndergroundLakeKey
}