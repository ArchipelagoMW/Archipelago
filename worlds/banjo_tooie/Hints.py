import re
from typing import List, Union
from dataclasses import dataclass
from BaseClasses import ItemClassification, Location, LocationProgressType
from worlds.AutoWorld import World
from .Options import HintClarity, AddSignpostHintsToArchipelagoHints
from .Items import moves_table, bk_moves_table, progressive_ability_table
from .Locations import MumboTokenBoss_table, MumboTokenGames_table, MumboTokenJinjo_table, all_location_table, WorldUnlocks_table
from .Names import locationName

TOTAL_HINTS = 61

@dataclass
class HintData:
    text: str # The displayed text in the game.
    location_id: Union[int, None] = None
    location_player_id: Union[int, None] = None
    should_add_hint: bool = False

class Hint:
    world: World
    location: Location

    def __init__(self, world: World, location: Location):
        self.world = world
        self.location = location

    # TODO: have some fun with Grunty's rhymes here
    @property
    def hint_data(self) -> HintData:
        if self.world.options.hint_clarity == HintClarity.option_clear:
            text = self.__clear_hint_text
        else:
            text = self.__cryptic_hint_text

        return HintData(text, self.location.address, self.location.player, self.__should_add_hint)

    @property
    def one_of_a_kind(self) -> bool:
        if not self.location.item.advancement:
            return False

        count = 0
        for item in self.world.multiworld.itempool:
            if item.player == self.location.player and item.name == self.location.item.name:
                count += 1
                if count > 1:
                    return False
        return count == 1

    def __format_location(self, capitalize: bool) -> str:
        if self.location.player == self.world.player:
            return f"{'Your' if capitalize else 'your'} {self.location.name}"

        return f"{Hint.__player_id_to_name(self.world, self.location.player)}'s {Hint.__sanitize_text(self.location.name)}"

    def __format_item(self, capitalize: bool) -> str:
        if self.location.item.player == self.world.player:
            return f"{'Your' if capitalize else 'your'} {Hint.__sanitize_text(self.location.item.name)}"

        return f"{Hint.__player_id_to_name(self.world, self.location.item.player)}'s {Hint.__sanitize_text(self.location.item.name)}"

    @property
    def __clear_hint_text(self) -> str:
        return f"{self.__format_location(capitalize=True)} has {self.__format_item(capitalize=False)}."

    @property
    def __cryptic_hint_text(self) -> str:
        formatted_location = self.__format_location(capitalize=True)

        if self.one_of_a_kind:
            return f"{formatted_location} has a legendary one-of-a-kind item."
        if self.location.item.classification == ItemClassification.progression:
            return f"{formatted_location} has a wonderful item."
        if self.location.item.classification == ItemClassification.progression_skip_balancing:
            return f"{formatted_location} has a great item."
        if self.location.item.classification == ItemClassification.useful:
            return f"{formatted_location} has a good item."
        if self.location.item.classification == ItemClassification.filler:
            return f"{formatted_location} has a useless item."
        if self.location.item.classification == ItemClassification.trap:
            return f"{formatted_location} has a bad item."

        # Not sure what actually fits in a multi-flag classification
        return f"{formatted_location} has a weiiiiiird item."

    @property
    def __should_add_hint(self) -> bool:
        hint_clarity = self.world.options.hint_clarity
        if hint_clarity == HintClarity.option_cryptic:
            return False

        ap_hinting = self.world.options.add_signpost_hints_to_ap

        if ap_hinting == AddSignpostHintsToArchipelagoHints.option_always:
            return True

        if ap_hinting == AddSignpostHintsToArchipelagoHints.option_progression:
            return self.location.item.advancement

        # option_never
        return False

    @staticmethod
    def __player_id_to_name(world: World, player: int) -> str:
        return Hint.__sanitize_text(world.multiworld.player_name[player])

    @staticmethod
    def __sanitize_text(text: str) -> str:
        N = 18
        text = text.replace('_', ' ')

        words = text.split()
        modified_words = []

        for word in words:
            if len(word) > N:
                # Try to split by PascalCase (uppercase letters within the word)
                split_by_pascal = re.sub(r'([a-z])([A-Z])', r'\1 \2', word)

                if word != split_by_pascal:
                    modified_words.append(split_by_pascal)
                else:
                    forced_split = ' '.join(word[i:i+N] for i in range(0, len(word), N))
                    modified_words.append(forced_split)
            else:
                modified_words.append(word)

        return ' '.join(modified_words)


def generate_hints(world: World):
    hints: List[Hint] = []

    generate_move_hints(world, hints)
    generate_slow_locations_hints(world, hints)

    hint_data = [hint.hint_data for hint in hints]

    generate_joke_hints(world, hint_data)

    world.random.shuffle(hint_data)
    world.hints = dict(zip(get_signpost_location_ids(), hint_data))

def generate_joke_hints(world: World, hints: List[HintData]):
    # Fills the rest of the signposts with jokes.
    if len(hints) == TOTAL_HINTS:
        return
    generate_suggestion_hint(world, hints)
    generate_forced_joke_hint(world, hints)
    generate_generic_joke_hint(world, hints)

def generate_forced_joke_hint(world: World, hint_datas: List[HintData]):
    if len(hint_datas) == TOTAL_HINTS:
        return
    hint_datas.append(HintData(f"Sorry {world.player_name}, but we are not adding that feature in this game."))

def generate_generic_joke_hint(world: World, hint_datas: List[HintData]):
    selected_jokes = (world.random.choices([
        "A hint is what you want, but instead here's a taunt.",
        "This is an information signpost.",
        "This joke hint features no newline.",
        "Press \x86 to read this signpost.", # That's the B button
        "Banjo-Kazooie: Grunty's Revenge is a collectathon that was released on the GBA.",
        "Did you know that Banjo-Kazooie had 2 mobile games? Me neither.",
        "After collecting all 9 black jinjos, enter their house for a happy sound.",
        "Made you look!",
        "Developer jjjj12212 was a good developer... until he got shot with an arrow in the knee.",

        # The following are quotes from other video games (or something inspired from them).
        "Thank you Banjo, but your hint is on another signpost!",
        "It's dangerous to go alone, read this!",
        "I like shorts! They're comfy and easy to wear!",
        "Press F to pay respects.",
        "Press \x86 to doubt.",
        "The sign is a lie",
        "When life gives you wood, don't make signs! Make life take the wood back! Get mad!",
    ], k = TOTAL_HINTS - len(hint_datas)))

    for joke in selected_jokes:
        hint_datas.append(HintData(joke))

def generate_suggestion_hint(world: World, hint_datas: List[HintData]):
    non_tooie_player_names = [world.player_name for world in world.multiworld.worlds.values() if world.game != "Banjo-Tooie"]
    if not non_tooie_player_names:
        return
    hint = "You should suggest {} to try the Banjo-Tooie Randomizer.".format(world.random.choice(non_tooie_player_names))
    hint_datas.append(HintData(hint))

def generate_slow_locations_hints(world: World, hints: List[Hint]):
    already_hinted = [hint.location.name for hint in hints\
                      if hint.location.player == world.player]

    worst_locations_names = [location_name for location_name in get_worst_location_names(world)\
                             if location_name not in already_hinted]
    bad_location_names = [location_name for location_name in get_bad_location_names(world)\
                             if location_name not in already_hinted]

    local_hint_location_names = already_hinted + worst_locations_names + bad_location_names

    def get_weight(hint: Hint) -> int:
        if hint.one_of_a_kind:
            return 20
        elif hint.location.item.classification == ItemClassification.progression:
            return 10
        elif hint.location.item.classification == ItemClassification.progression_skip_balancing:
            return 5

        return 1

    worst_hints = [Hint(world, get_location_by_name(world, location_name))\
                for location_name in worst_locations_names if get_location_by_name(world, location_name)]
    worst_weights = [10 + get_weight(hint) for hint in worst_hints]

    bad_hints = [Hint(world, get_location_by_name(world, location_name))\
                for location_name in bad_location_names if get_location_by_name(world, location_name)]
    bad_weights = [get_weight(hint) for hint in worst_hints]

    hint_shuffled = list(zip(bad_hints, bad_weights)) + list(zip(worst_hints, worst_weights))
    hint_shuffled = sorted(hint_shuffled, key=lambda x: world.random.random() / x[1])

    new_hints = [elem for elem, _ in hint_shuffled]
    new_hints = new_hints[:world.options.signpost_hints - len(hints)]
    hints.extend(new_hints)

    # At this point, we went through all the bad locations, and we still don't have enough hints.
    # So we just hint random locations in our own world that have not been picked.
    remaining_locations = [location for location in get_player_hintable_locations(world) if location.name not in local_hint_location_names]
    world.random.shuffle(remaining_locations)

    while len(hints) < world.options.signpost_hints:
        hints.append(Hint(world, remaining_locations.pop()))


def get_worst_location_names(world: World):
    worst_location_names = []

    worst_location_names.extend([
        locationName.JIGGYMT5,

        locationName.JIGGYGM5,

        locationName.JIGGYWW2,
        locationName.JIGGYWW3,
        locationName.JIGGYWW4,
        locationName.JIGGYWW7,

        locationName.JIGGYJR7,
        locationName.JIGGYJR9,

        locationName.JIGGYTD3,
        locationName.JIGGYTD7,

        locationName.JIGGYGI1,
        locationName.JIGGYGI2,
        locationName.JIGGYGI3,
        locationName.JIGGYGI4,

        locationName.JIGGYHP1,
        locationName.JIGGYHP5,
        locationName.JIGGYHP9,

        locationName.JIGGYCC1,
        locationName.JIGGYCC7,

        locationName.SCRAT,
    ])

    if world.options.randomize_jinjos:
        worst_location_names.extend([
            locationName.JIGGYIH7,
            locationName.JIGGYIH8,
            locationName.JIGGYIH9,

            locationName.JINJOGI3,
            locationName.JINJOGI5,
        ])

    if world.options.randomize_glowbos:
        worst_location_names.extend([
            locationName.GLOWBOMEG,
        ])

    if world.options.randomize_cheato:
        worst_location_names.extend([
            locationName.CHEATOWW3,
            locationName.CHEATOJR1,
            locationName.CHEATOGI3,
            locationName.CHEATOCC1,
        ])

    # The 5 most expensive silos
    if world.options.randomize_moves:
        sorted_silos = [k for k, v in sorted(world.jamjars_siloname_costs.items(), key=lambda item: item[1])]
        for _ in range(5):
            worst_location_names.append(sorted_silos.pop())

    if world.options.cheato_rewards:
        worst_location_names.extend([
            locationName.CHEATOR4,
            locationName.CHEATOR5,
        ])

    if world.options.honeyb_rewards:
        worst_location_names.extend([
            locationName.HONEYBR5,
        ])

    return worst_location_names

def get_bad_location_names(world: World):
    bad_location_names = []

    bad_location_names.extend([
        locationName.JIGGYMT1,
        locationName.JIGGYMT3,

        locationName.JIGGYGM2,
        locationName.JIGGYGM5,

        locationName.JIGGYWW1,
        locationName.JIGGYWW5,

        locationName.JIGGYJR1,
        locationName.JIGGYJR3,

        locationName.JIGGYTD2,
        locationName.JIGGYTD9,

        locationName.JIGGYGI6,
        locationName.JIGGYGI9,

        locationName.JIGGYHP3,
        locationName.JIGGYHP6,
        locationName.JIGGYHP8,
        locationName.JIGGYHP10,

        locationName.JIGGYCC4,

        locationName.SCRUT,
        locationName.SCRAT,
    ])

    if world.options.randomize_jinjos:
        bad_location_names.extend([
            locationName.JIGGYIH5,
            locationName.JIGGYIH6,

            locationName.JINJOGM1,
            locationName.JINJOCC1,
        ])

    if world.options.randomize_cheato:
        bad_location_names.extend([
            locationName.CHEATOCC2,
            locationName.CHEATOTL1,
            locationName.CHEATOGM1,
        ])

    # The next 5 most expensive silos
    if world.options.randomize_moves:
        sorted_silos = [k for k, v in sorted(world.jamjars_siloname_costs.items(), key=lambda item: item[1])]
        for _ in range(6, 10):
            bad_location_names.append(sorted_silos.pop())

    if world.options.cheato_rewards:
        bad_location_names.extend([
            locationName.CHEATOR3,
        ])

    if world.options.honeyb_rewards:
        bad_location_names.extend([
            locationName.HONEYBR4,
        ])
    return bad_location_names

def generate_move_hints(world: World, hints: List[Hint]):
    move_locations = get_move_locations(world)
    for location in move_locations:
        hints.append(Hint(world, location))

def get_move_locations(world: World) -> List[Location]:
    all_moves_names = []
    if world.options.randomize_moves:
        all_moves_names.extend(moves_table.keys()) # We don't want BT moves to be hinted when they're in the vanilla location.
    all_moves_names.extend(bk_moves_table.keys())
    all_moves_names.extend(progressive_ability_table.keys())

    all_move_locations = [location for location in get_all_hintable_locations(world)\
            if location.item.name in all_moves_names and location.item.player == world.player]
    world.random.shuffle(all_move_locations)
    selected_move_locations = []

    for location in all_move_locations:
        if len(selected_move_locations) >= min(world.options.signpost_move_hints, world.options.signpost_hints):
            return selected_move_locations
        selected_move_locations.append(location)
    return selected_move_locations

def get_location_by_name(world: World, name: str) -> Location:
    potential_match = list(filter(lambda location: location.name == name, get_player_hintable_locations(world)))
    if potential_match:
        return potential_match[0]
    return None

def get_all_hintable_locations(world: World) -> List[Location]:
    return [location for location in world.multiworld.get_locations() if should_consider_location(location)]

def get_player_hintable_locations(world: World) -> List[Location]:
    return [location for location in world.multiworld.get_locations(world.player) if should_consider_location(location)]

def should_consider_location(location: Location) -> bool:
    if not location.item or not location.address:
        return False
    if location.progress_type == LocationProgressType.EXCLUDED:
        return False

    location_hint_blacklist = [
        *WorldUnlocks_table.keys(),
        *MumboTokenBoss_table.keys(),
        *MumboTokenGames_table.keys(),
        *MumboTokenJinjo_table.keys(),
    ]
    if location.name in location_hint_blacklist:
        return False
    return True

def get_signpost_location_ids() -> List[int]:
    location_datas = list(filter(lambda location_data: location_data.group == "Signpost", all_location_table.values()))
    return [location_data.btid for location_data in location_datas]
