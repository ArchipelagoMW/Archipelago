from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GameCheck:
    event_key: str
    location_name: str


GAME_CHECKS = (
    GameCheck(
        "received_starter",
        "New Bark Town - Receive Starter",
    ),
    GameCheck(
        "received_pokegear",
        "New Bark Town - Receive Pokegear",
    ),
    GameCheck(
        "received_running_shoes",
        "Cherrygrove City - Receive Running Shoes",
    ),
    GameCheck(
        "received_map_card",
        "Cherrygrove City - Receive Map Card",
    ),
    GameCheck(
        "visited_mr_pokemon",
        "Route 30 - Visit Mr. Pokemon",
    ),
    GameCheck(
        "received_apricorn_box",
        "Route 30 - Receive Apricorn Box",
    ),
    GameCheck(
        "cleared_sprout_tower",
        "Violet City - Clear Sprout Tower",
    ),
    GameCheck(
        "defeated_falkner",
        "Violet City - Defeat Falkner",
    ),
    GameCheck(
        "received_togepi_egg",
        "Violet City - Receive Togepi Egg",
    ),
    GameCheck(
        "received_miracle_seed",
        "Route 32 - Receive Miracle Seed",
    ),
    GameCheck(
        "reached_union_cave_south_exit",
        "Union Cave - Reach South Exit",
    ),
    GameCheck(
        "cleared_slowpoke_well",
        "Azalea Town - Clear Slowpoke Well",
    ),
    GameCheck(
        "defeated_bugsy",
        "Azalea Town - Defeat Bugsy",
    ),
    GameCheck(
        "cleared_farfetchd_puzzle",
        "Ilex Forest - Clear Farfetch'd Puzzle",
    ),
    GameCheck(
        "defeated_whitney",
        "Goldenrod City - Defeat Whitney",
    ),
    GameCheck(
        "received_bicycle",
        "Goldenrod City - Receive Bicycle",
    ),
    GameCheck(
        "received_radio_card",
        "Goldenrod Radio Tower - Receive Radio Card",
    ),
    GameCheck(
        "received_kenya",
        "Route 35 - Receive Kenya",
    ),
    GameCheck(
        "received_quick_claw",
        "National Park - Receive Quick Claw",
    ),
    GameCheck(
        "defeated_rival_burned_tower",
        "Ecruteak City - Defeat Rival in Burned Tower",
    ),
    GameCheck(
        "defeated_morty",
        "Ecruteak City - Defeat Morty",
    ),
    GameCheck(
        "cleared_dance_theater",
        "Ecruteak City - Clear Dance Theater",
    ),
    GameCheck(
        "defeated_kimono_girls",
        "Ecruteak City - Defeat Kimono Girls",
    ),
    GameCheck(
        "received_good_rod",
        "Olivine City - Receive Good Rod",
    ),
    GameCheck(
        "reached_amphy",
        "Olivine Lighthouse - Reach Amphy",
    ),
    GameCheck(
        "received_secretpotion",
        "Cianwood City - Receive SecretPotion",
    ),
    GameCheck(
        "defeated_chuck",
        "Cianwood City - Defeat Chuck",
    ),
    GameCheck(
        "received_shuckle",
        "Cianwood City - Receive Shuckle",
    ),
    GameCheck(
        "defeated_jasmine",
        "Olivine City - Defeat Jasmine",
    ),
    GameCheck(
        "cleared_team_rocket_hq",
        "Mahogany Town - Clear Team Rocket HQ",
    ),
    GameCheck(
        "defeated_red_gyarados",
        "Lake of Rage - Defeat Red Gyarados",
    ),
    GameCheck(
        "defeated_pryce",
        "Mahogany Town - Defeat Pryce",
    ),
    GameCheck(
        "received_basement_key",
        "Goldenrod Underground - Receive Basement Key",
    ),
    GameCheck(
        "received_card_key",
        "Goldenrod Radio Tower - Receive Card Key",
    ),
    GameCheck(
        "cleared_radio_tower",
        "Goldenrod Radio Tower - Clear Radio Tower",
    ),
    GameCheck(
        "defeated_clair",
        "Blackthorn City - Defeat Clair",
    ),
    GameCheck(
        "defeated_victory_road_rival",
        "Victory Road - Defeat Rival",
    ),
)


event_key_to_location_name = {
    game_check.event_key: game_check.location_name
    for game_check in GAME_CHECKS
}


location_name_to_event_key = {
    game_check.location_name: game_check.event_key
    for game_check in GAME_CHECKS
}


def get_location_name_for_event_key(event_key: str) -> str | None:
    return event_key_to_location_name.get(event_key)


def get_event_key_for_location_name(location_name: str) -> str | None:
    return location_name_to_event_key.get(location_name)