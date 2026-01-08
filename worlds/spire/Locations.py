from collections import defaultdict
from enum import Enum, auto
from typing import Optional, List, Tuple, Union, NamedTuple, Set

from worlds.spire import character_list
from worlds.spire.Characters import NUM_CUSTOM

CARD_REWARD_COUNT = 13

CHAR_OFFSET = 200

class LocationType(Enum):
    Card_Reward = auto()
    Rare_Card_Reward = auto()
    Relic = auto()
    Boss_Relic = auto()
    Floor = auto()
    Campfire = auto()
    Event = auto()
    Shop = auto()
    Start = auto()
    Gold = auto()
    Potion = auto()


class LocationData(NamedTuple):
    name: str
    id: Optional[int]
    type: LocationType
    act: int
    boss: bool = False

def create_location_data() -> List[LocationData]:
    return ([LocationData(f"Reached Floor {j}", j, LocationType.Floor, min(((j-1) // 17)+1,3)) for j in range(1, 57)] +
            [LocationData(f"Card Reward {j}", j + 100, LocationType.Card_Reward, min(((j - 1) // (CARD_REWARD_COUNT // 3)) + 1, 3)) for j in range(1, CARD_REWARD_COUNT + 1)] +
            [LocationData(f"Relic {j}", j + 140, LocationType.Relic, min(((j-1) // 3)+1,3)) for j in range(1, 11)] +
            [LocationData(f"Shop Slot {j}", j + 163, LocationType.Shop, min(((j-1) // 5)+1, 3)) for j in range(1,17)] +
            [LocationData(f"Combat Gold {j}", j + 56, LocationType.Gold, min(((j-1)//6)+1,3)) for j in range(1,19)] +
            [LocationData(f"Elite Gold {j}", j + 75, LocationType.Gold, min(((j-1)//2)+1,3)) for j in range(1,8)] +
            [LocationData(f"Potion Drop {j}", j + 84, LocationType.Potion, min(((j-1)//3)+1,3)) for j in range(1,10)] +
            [LocationData('Act 1 Campfire 1', 121, LocationType.Campfire, 1),
            LocationData('Act 1 Campfire 2', 122, LocationType.Campfire, 1),
            LocationData('Act 2 Campfire 1', 123, LocationType.Campfire, 2),
            LocationData('Act 2 Campfire 2', 124, LocationType.Campfire, 2),
            LocationData('Act 3 Campfire 1', 125, LocationType.Campfire, 3),
            LocationData('Act 3 Campfire 2', 126, LocationType.Campfire, 3),
            LocationData('Rare Card Reward 1', 131, LocationType.Rare_Card_Reward, 1, True),
            LocationData('Rare Card Reward 2', 132, LocationType.Rare_Card_Reward, 2, True),
            LocationData('Boss Relic 1', 161, LocationType.Boss_Relic, 1, True),
            LocationData('Boss Relic 2', 162, LocationType.Boss_Relic, 2, True),
            LocationData('Press Start', 163, LocationType.Start, 1),
            LocationData('Boss Gold 1', 83, LocationType.Gold, 1, True),
            LocationData('Boss Gold 2', 84, LocationType.Gold, 2, True),
            LocationData('Heart Room', None, LocationType.Event, 3),
            LocationData('Act 1 Boss', None, LocationType.Event, 1),
            LocationData('Act 2 Boss', None, LocationType.Event, 2),
            LocationData('Act 3 Boss', None, LocationType.Event, 3),
    ])

def create_location_tables(vanilla_chars: List[str], extras: int) -> Tuple[dict[str, int], dict[
    Union[str, int],dict[str,LocationData]],dict[int,LocationData]]:
    loc_name_to_id = dict()
    characters_to_locs: dict[Union[str, int],dict[str, LocationData]] = defaultdict(lambda: dict())
    ids_to_data: dict[int, LocationData] = dict()
    char_num = 0

    base_location_data = create_location_data()

    ids = { x.id for x in base_location_data if x.id is not None}
    assert len(ids) == (len(base_location_data) - 4), f"{len(ids)} != {len(base_location_data)}"
    for char in vanilla_chars:
        for data in base_location_data:
            newkey = f"{char} {data.name}"
            newval = data.id + char_num*CHAR_OFFSET if data.type != LocationType.Event else data.id
            loc_name_to_id[newkey] = newval
            characters_to_locs[char][newkey] = data
            if newval is not None:
                ids_to_data[newval] = data
        char_num += 1

    for i in range(extras):
        for data in base_location_data:
            newkey = f"Custom Character {i+1} {data.name}"
            newval = data.id + char_num * CHAR_OFFSET if data.type != LocationType.Event else data.id
            loc_name_to_id[newkey] = newval
            characters_to_locs[i+1][newkey] = data
            if newval is not None:
                ids_to_data[newval] = data
        char_num += 1

    return loc_name_to_id, characters_to_locs, ids_to_data

def create_location_groups(chars_to_locs: dict[Union[str,int],dict[str,LocationData]]) -> dict[str, Set[str]]:
    act_one = set()
    act_two = set()
    act_three = set()
    act_one_boss = set()
    act_two_boss = set()

    ret = dict()

    ret["Act 1"] = act_one
    ret["Act 2"] = act_two
    ret["Act 3"] = act_three
    ret["Act 1 Boss"] = act_one_boss
    ret["Act 2 Boss"] = act_two_boss

    for key, data in chars_to_locs.items():
        char = key if type(key) == str else f"Custom Character {key+1}"
        char_act_one = set()
        char_act_two = set()
        char_act_three = set()
        char_act_one_boss = set()
        char_act_two_boss = set()
        ret[f"{char} Act 1"] = char_act_one
        ret[f"{char} Act 2"] = char_act_two
        ret[f"{char} Act 3"] = char_act_three
        ret[f"{char} Act 1 Boss"] = char_act_one_boss
        ret[f"{char} Act 2 Boss"] = char_act_two_boss
        for loc_name, loc_data in data.items():
            if loc_data.id is None:
                continue
            if loc_data.act == 1:
                char_act_one.add(loc_name)
                act_one.add(loc_name)
                if loc_data.boss:
                    char_act_one_boss.add(loc_name)
                    act_one_boss.add(loc_name)
            elif loc_data.act == 2:
                char_act_two.add(loc_name)
                act_two.add(loc_name)
                if loc_data.boss:
                    char_act_two_boss.add(loc_name)
                    act_two_boss.add(loc_name)
            elif loc_data.act == 3:
                char_act_three.add(loc_name)
                act_three.add(loc_name)

    return ret

location_table, characters_to_locs, loc_ids_to_data = create_location_tables(character_list, NUM_CUSTOM)

location_groups = create_location_groups(characters_to_locs)