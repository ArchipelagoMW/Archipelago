from typing import NamedTuple, Callable, List, Optional, Tuple

from BaseClasses import CollectionState, MultiWorld
from worlds.yugioh06.Locations import special


class OpponentData(NamedTuple):
    name: str
    campaignInfo: List[str]
    tier: int
    column: int
    rule: Callable[[CollectionState], bool] = lambda state: True


def get_opponents(multiworld: Optional[MultiWorld], player: Optional[int]) -> Tuple[OpponentData, ...]:
    opponents_table: List[OpponentData] = [
        # Tier 1
        OpponentData("Kuriboh", [], 1, 1),
        OpponentData("Scapegoat", [], 1, 2),
        OpponentData("Skull Servant", [], 1, 3),
        OpponentData("Watapon", [], 1, 4),
        OpponentData("White Magician Pikeru", [], 1, 5),
        # Tier 2
        OpponentData("Battery Man C", ["Quick-Finish"], 2, 1, lambda state: state.yugioh06_difficulty(player, 1)),
        OpponentData("Ojama Yellow", [], 2, 2, lambda state: state.yugioh06_difficulty(player, 1)),
        OpponentData("Goblin King", ["Quick-Finish"], 2, 3, lambda state: state.yugioh06_difficulty(player, 1)),
        OpponentData("Des Frog", ["Quick-Finish"], 2, 4, lambda state: state.yugioh06_difficulty(player, 1)),
        OpponentData("Water Dragon", ["Quick-Finish"], 2, 5, lambda state: state.yugioh06_difficulty(player, 1)),
        # Tier 3
        OpponentData("Red-Eyes Darkness Dragon", ["Quick-Finish"], 3, 1,
                     lambda state: state.yugioh06_difficulty(player, 2)),
        OpponentData("Vampire Genesis", ["Quick-Finish"], 3, 2, lambda state: state.yugioh06_difficulty(player, 2)),
        OpponentData("Infernal Flame Emperor", [], 3, 3, lambda state: state.yugioh06_difficulty(player, 2)),
        OpponentData("Ocean Dragon Lord - Neo-Daedalus", [], 3, 4, lambda state: state.yugioh06_difficulty(player, 2)),
        OpponentData("Helios Duo Megiste", ["Quick-Finish"], 3, 5, lambda state: state.yugioh06_difficulty(player, 2)),
        # Tier 4
        OpponentData("Gilford the Legend", ["Quick-Finish"], 4, 1, lambda state: state.yugioh06_difficulty(player, 3)),
        OpponentData("Dark Eradicator Warlock", ["Quick-Finish"], 4, 2,
                     lambda state: state.yugioh06_difficulty(player, 3)),
        OpponentData("Guardian Exode", [], 4, 3, lambda state: state.yugioh06_difficulty(player, 3)),
        OpponentData("Goldd, Wu-Lord of Dark World", ["Quick-Finish"], 4, 4,
                     lambda state: state.yugioh06_difficulty(player, 3)),
        OpponentData("Elemental Hero Erikshieler", ["Quick-Finish"], 4, 5,
                     lambda state: state.yugioh06_difficulty(player, 3)),
        # Tier 5
        OpponentData("Raviel, Lord of Phantasms", [], 5, 1, lambda state: state.yugioh06_difficulty(player, 4)),
        OpponentData("Horus the Black Flame Dragon LV8", [], 5, 2,
                     lambda state: state.yugioh06_difficulty(player, 4)),
        OpponentData("Stronghold", [], 5, 3,
                     lambda state: state.has("Challenge Beaten", player,
                                             multiworld.ThirdTier5CampaignBossChallenges[
                                                 player].value) and state.yugioh06_difficulty(player, 5)),
        OpponentData("Sacred Phoenix of Nephthys", [], 5, 4,
                     lambda state: state.has("Challenge Beaten", player,
                                             multiworld.FourthTier5CampaignBossChallenges[player].value)
                                   and state.yugioh06_difficulty(player, 6)),
        OpponentData("Cyber End Dragon", ["Goal"], 5, 5,
                     lambda state: state.has("Challenge Beaten", player,
                                             multiworld.FinalCampaignBossChallenges[player].value)
                                   and state.yugioh06_difficulty(player, 7)),
    ]
    return tuple(opponents_table)


def get_opponent_locations(opponent: OpponentData) -> dict[str, str]:
    location = {}
    if opponent.tier < 5:
        location[opponent.name + " Beaten"] = "Tier " + str(opponent.tier) + " Beaten"
    elif opponent.tier > 4 and opponent.column != 5:
        name = "Campaign Tier 5: Column " + str(opponent.column) + " Win"
        location[name] = special[name]
    for info in opponent.campaignInfo:
        location[opponent.name + "-> " + info] = info
    return location
