import enum
import re
from typing import Iterable, List, Set, Union, TYPE_CHECKING
from dataclasses import dataclass
from BaseClasses import ItemClassification, Location, LocationProgressType, CollectionState, MultiWorld
from .Options import HintClarity, AddSignpostHintsToArchipelagoHints
from .Items import moves_table, bk_moves_table, progressive_ability_table
from .Locations import (MumboTokenBoss_table, MumboTokenGames_table, MumboTokenJinjo_table, all_location_table,
                        WorldUnlocks_table)
from .Names import locationName
if TYPE_CHECKING:
    from . import BanjoTooieWorld

TOTAL_HINTS = 61

@dataclass
class HintData:
    text: str  # The displayed text in the game.
    location_id: Union[int, None] = None
    location_player_id: Union[int, None] = None
    should_add_hint: bool = False


class Hint:

    class ItemRequirement(enum.Enum):
        REQUIRED_BY_PLAYER = 0,
        REQUIRED_BY_MULTIWORLD = 1,
        NOT_REQUIRED = 2

    item_requirement_cache: dict[Location, ItemRequirement] = {}
    final_state: CollectionState | None = None

    def __init__(self, world: "BanjoTooieWorld", location: Location):
        self.world = world
        self.location = location

    @staticmethod
    def fill_item_requirement_cache(hints: Iterable["Hint"]) -> None:
        if not hints:
            return

        hinted_locations = {hint.location for hint in hints}
        world = hints[0].world
        base_state = CollectionState(world.multiworld)

        for location in {loc for loc in hinted_locations if not loc.advancement}:
            Hint.item_requirement_cache[location] = Hint.ItemRequirement.NOT_REQUIRED

        remaining_locations = {loc for loc in hinted_locations if loc.advancement and loc not in Hint.item_requirement_cache}
        assert base_state.locations_checked.isdisjoint(remaining_locations)

        base_state.sweep_for_advancements(checked_locations=base_state.locations_checked | remaining_locations)

        while remaining_locations:
            reachable = [loc for loc in remaining_locations if base_state.can_reach(loc)]

            if not reachable:
                for loc in remaining_locations:
                    Hint.item_requirement_cache[loc] = Hint.ItemRequirement.NOT_REQUIRED
                break

            loc = world.random.choice(reachable)
            remaining_locations.remove(loc)

            test_state = base_state.copy()
            test_state.sweep_for_advancements(checked_locations=test_state.locations_checked | {loc})

            if not world.multiworld.has_beaten_game(test_state, world.player):
                Hint.item_requirement_cache[loc] = Hint.ItemRequirement.REQUIRED_BY_PLAYER
            elif not world.multiworld.has_beaten_game(test_state):
                Hint.item_requirement_cache[loc] = Hint.ItemRequirement.REQUIRED_BY_MULTIWORLD
            else:
                Hint.item_requirement_cache[loc] = Hint.ItemRequirement.NOT_REQUIRED

            if remaining_locations or not Hint.final_state:
                base_state.sweep_for_advancements(checked_locations=base_state.locations_checked | remaining_locations)

        if not Hint.final_state:
            Hint.final_state = base_state

    @staticmethod
    def is_last_cryptic_hint_world(world: "BanjoTooieWorld"):
        tooie_worlds: List[BanjoTooieWorld] = [
            tooie_world
            for tooie_world in world.multiworld.worlds.values()
            if tooie_world.game == world.game
        ]
        cryptic_hint_worlds = [
            tooie_world
            for tooie_world in tooie_worlds
            if tooie_world.options.hint_clarity.value == HintClarity.option_cryptic
        ]
        return cryptic_hint_worlds[-1] == world

    # TODO: have some fun with Grunty's rhymes here
    @property
    def hint_data(self) -> HintData:
        if self.world.options.hint_clarity.value == HintClarity.option_clear:
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

    @property
    def is_required(self) -> ItemRequirement:
        return self.item_requirement_cache[self.location]

    def __format_accessibility(self) -> str:
        return "" if Hint.final_state.can_reach(self.location) else "lost "

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
        formatted_accessibility = self.__format_accessibility()
        if self.location.item.advancement:
            requirement = self.is_required
            if requirement == Hint.ItemRequirement.REQUIRED_BY_PLAYER:
                return f"{formatted_location} is on the Wahay of the Duo."
            if requirement == Hint.ItemRequirement.REQUIRED_BY_MULTIWORLD:
                return f"{formatted_location} is on the Wahay of the Archipelago."
            if self.one_of_a_kind:
                return f"{formatted_location} has a {formatted_accessibility}legendary one-of-a-kind item."
            if self.location.item.classification == ItemClassification.progression:
                return f"{formatted_location} has a {formatted_accessibility}wonderful item."
            if ItemClassification.skip_balancing in self.location.item.classification \
                or ItemClassification.deprioritized in self.location.item.classification:
                return f"{formatted_location} has a {formatted_accessibility}great item."
        if self.location.item.classification == ItemClassification.useful:
            return f"{formatted_location} has a {formatted_accessibility}good item."
        if self.location.item.classification == ItemClassification.filler:
            return f"{formatted_location} has a {formatted_accessibility}useless item."
        if self.location.item.classification == ItemClassification.trap:
            return f"{formatted_location} has a {formatted_accessibility}bad item."

        # Not sure what actually fits in the remaining multi-flag classifications
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
    def __player_id_to_name(world: "BanjoTooieWorld", player: int) -> str:
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


def generate_hints(world: "BanjoTooieWorld"):
    hints: List[Hint] = []

    generate_move_hints(world, hints)
    generate_slow_locations_hints(world, hints)

    if world.options.hint_clarity.value == HintClarity.option_cryptic:
        Hint.fill_item_requirement_cache(hints)

    hint_data = [hint.hint_data for hint in hints]

    generate_joke_hints(world, hint_data)

    # Since these are static variables, we have to manually empty them.
    # Using del messes up with tests, so we're simply deleting the reference.
    if world.options.hint_clarity.value == HintClarity.option_cryptic:
        if Hint.is_last_cryptic_hint_world(world):
            Hint.item_requirement_cache = dict()
            Hint.final_state = None

    world.random.shuffle(hint_data)
    world.hints = dict(zip(get_signpost_location_ids(), hint_data))


def generate_joke_hints(world: "BanjoTooieWorld", hints: List[HintData]):
    # Fills the rest of the signposts with jokes.
    if len(hints) == TOTAL_HINTS:
        return
    generate_suggestion_hint(world, hints)
    generate_forced_joke_hint(world, hints)
    generate_generic_joke_hint(world, hints)


def generate_forced_joke_hint(world: "BanjoTooieWorld", hint_datas: List[HintData]):
    if len(hint_datas) == TOTAL_HINTS:
        return
    hint_datas.append(HintData(f"Sorry {world.player_name}, but we are not adding that feature in this game."))


def generate_generic_joke_hint(world: "BanjoTooieWorld", hint_datas: List[HintData]):
    selected_jokes = (world.random.choices([
        "A hint is what you want, but instead here's a taunt.",
        "This is an information signpost.",
        "This joke hint features no newline.",
        "Press \x86 to read this signpost.",  # That's the B button
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
    ], k=TOTAL_HINTS - len(hint_datas)))

    for joke in selected_jokes:
        hint_datas.append(HintData(joke))


def generate_suggestion_hint(world: "BanjoTooieWorld", hint_datas: List[HintData]):
    non_tooie_player_names = [
        world.player_name
        for world in world.multiworld.worlds.values()
        if world.game != "Banjo-Tooie"
    ]
    if not non_tooie_player_names:
        return
    hint = "You should suggest {} to try the Banjo-Tooie Randomizer.".format(
                world.random.choice(non_tooie_player_names)
            )
    hint_datas.append(HintData(hint))


def generate_slow_locations_hints(world: "BanjoTooieWorld", hints: List[Hint]):
    already_hinted = [hint.location.name for hint in hints if hint.location.player == world.player]

    worst_locations_names = [location_name for location_name in get_worst_location_names(world)
                             if location_name not in already_hinted]
    bad_location_names = [location_name for location_name in get_bad_location_names(world)
                          if location_name not in already_hinted]

    local_hint_location_names = already_hinted + worst_locations_names + bad_location_names

    def get_weight(hint: Hint) -> int:
        if hint.one_of_a_kind:
            return 20
        elif hint.location.item.classification == ItemClassification.progression:
            return 10
        elif hint.location.item.classification & ItemClassification.progression_skip_balancing\
                == ItemClassification.progression_skip_balancing\
            or hint.location.item.classification & ItemClassification.progression_deprioritized\
                == ItemClassification.progression_deprioritized:
            return 5

        return 1

    worst_hints = [Hint(world, get_location_by_name(world, location_name))
                   for location_name in worst_locations_names if get_location_by_name(world, location_name)]
    worst_weights = [10 + get_weight(hint) for hint in worst_hints]

    bad_hints = [Hint(world, get_location_by_name(world, location_name))
                 for location_name in bad_location_names if get_location_by_name(world, location_name)]
    bad_weights = [get_weight(hint) for hint in worst_hints]

    hint_shuffled = list(zip(bad_hints, bad_weights)) + list(zip(worst_hints, worst_weights))
    hint_shuffled = sorted(hint_shuffled, key=lambda x: world.random.random() / x[1])

    new_hints = [elem for elem, _ in hint_shuffled]
    new_hints = new_hints[:world.options.signpost_hints.value - len(hints)]
    hints.extend(new_hints)

    # At this point, we went through all the bad locations, and we still don't have enough hints.
    # So we just hint random locations in our own world that have not been picked.
    remaining_locations = [location for location in get_player_hintable_locations(world)
                           if location.name not in local_hint_location_names]
    world.random.shuffle(remaining_locations)

    while len(hints) < world.options.signpost_hints.value:
        hints.append(Hint(world, remaining_locations.pop()))


def get_worst_location_names(world: "BanjoTooieWorld"):
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

    if world.options.randomize_jinjos.value:
        worst_location_names.extend([
            locationName.JIGGYIH7,
            locationName.JIGGYIH8,
            locationName.JIGGYIH9,

            locationName.JINJOGI3,
            locationName.JINJOGI5,
        ])

    if world.options.randomize_glowbos.value:
        worst_location_names.extend([
            locationName.GLOWBOMEG,
        ])

    if world.options.randomize_cheato.value:
        worst_location_names.extend([
            locationName.CHEATOWW3,
            locationName.CHEATOJR1,
            locationName.CHEATOGI3,
            locationName.CHEATOCC1,
        ])

    # The 5 most expensive silos
    if world.options.randomize_bt_moves.value:
        sorted_silos = [k for k, v in sorted(world.jamjars_siloname_costs.items(), key=lambda item: item[1])]
        for _ in range(5):
            worst_location_names.append(sorted_silos.pop())

    if world.options.cheato_rewards.value:
        worst_location_names.extend([
            locationName.CHEATOR4,
            locationName.CHEATOR5,
        ])

    if world.options.honeyb_rewards.value:
        worst_location_names.extend([
            locationName.HONEYBR5,
        ])

    return worst_location_names


def get_bad_location_names(world: "BanjoTooieWorld"):
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

    if world.options.randomize_jinjos.value:
        bad_location_names.extend([
            locationName.JIGGYIH5,
            locationName.JIGGYIH6,

            locationName.JINJOGM1,
            locationName.JINJOCC1,
        ])

    if world.options.randomize_cheato.value:
        bad_location_names.extend([
            locationName.CHEATOCC2,
            locationName.CHEATOTL1,
            locationName.CHEATOGM1,
        ])

    # The next 5 most expensive silos
    if world.options.randomize_bt_moves.value:
        sorted_silos = [k for k, v in sorted(world.jamjars_siloname_costs.items(), key=lambda item: item[1])]
        for _ in range(6, 10):
            bad_location_names.append(sorted_silos.pop())

    if world.options.cheato_rewards.value:
        bad_location_names.extend([
            locationName.CHEATOR3,
        ])

    if world.options.honeyb_rewards.value:
        bad_location_names.extend([
            locationName.HONEYBR4,
        ])
    return bad_location_names


def generate_move_hints(world: "BanjoTooieWorld", hints: List[Hint]):
    move_locations = get_move_locations(world)
    for location in move_locations:
        hints.append(Hint(world, location))


def get_move_locations(world: "BanjoTooieWorld") -> List[Location]:
    all_moves_names = []

    # We don't want BT moves to be hinted when they're in the vanilla location.
    if world.options.randomize_bt_moves.value:
        all_moves_names.extend(moves_table.keys())
    all_moves_names.extend(bk_moves_table.keys())
    all_moves_names.extend(progressive_ability_table.keys())

    all_move_locations = [location for location in get_all_hintable_locations(world)
                          if location.item.name in all_moves_names and location.item.player == world.player]
    world.random.shuffle(all_move_locations)
    selected_move_locations = []

    for location in all_move_locations:
        if len(selected_move_locations) >= min(
            world.options.signpost_move_hints.value,
            world.options.signpost_hints.value
        ):
            return selected_move_locations
        selected_move_locations.append(location)
    return selected_move_locations


def get_location_by_name(world: "BanjoTooieWorld", name: str) -> Location | None:
    potential_match = [location for location in get_player_hintable_locations(world) if location.name == name]
    if potential_match:
        return potential_match[0]
    return None


def get_all_hintable_locations(world: "BanjoTooieWorld") -> List[Location]:
    return [location for location in world.multiworld.get_locations() if should_consider_location(location)]


def get_player_hintable_locations(world: "BanjoTooieWorld") -> List[Location]:
    return [location for location in world.get_locations() if should_consider_location(location)]


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
    return location.name not in location_hint_blacklist


def get_signpost_location_ids() -> List[int]:
    return [location_data.btid for location_data in all_location_table.values() if location_data.group == "Signpost"]
