import enum
import logging
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

    submitted_cryptic_hinted_locations: Set[Location] = set()

    # For each locations tested, lists who CANNOT beat their seed without collecting the location.
    item_requirement_cache: dict[Location, List[int]] = {}

    final_state: CollectionState | None = None

    def __init__(self, world: "BanjoTooieWorld", location: Location):
        self.world = world
        self.location = location

    @staticmethod
    def submit_hinted_locations(hinted_locations: Set[Location]):
        Hint.submitted_cryptic_hinted_locations.update(hinted_locations)

    @staticmethod
    def compute_item_requirement_cache(world: "BanjoTooieWorld") -> None:
        # Since this function is complicated, and I think that some people would want this, let me explain it in plain English.

        # Core concept: calling CollectionState.sweep_for_advancements by passing locations that haven't been checked by the state in the
        # locations_checked parameter allows you to compute everything that is reachable without collecting those locations, effectively excluding them from the computation.

        # First, we apply the status of not required to any location that has an item that's not progression.
        # Then, while there's still locations that haven't been computed:
        #   Update a base state to the point where it reaches everything except everything that is locked behind the locations that haven't computed.
        #   Get the remaining locations that are currently reachable by the base state.
        #       Nothing reachable? The remaining locations are marked as not required, since they're unreachable locations.
        #   Split the reachable locations in batches of BATCH_SIZE locations. (Value gotten experimentally with seeds of 64 Tooies with max options, about 69k total locations.)
        #   For each batch:
        #       Create a copy of base state, and advance it, excluding only the locations from the current batch.
        #       For each location in current batch:
        #           Create a test state for that one location.
        #           Advance the test state, excluding only that one location.
        #           Note down every world id whose completion is locked by that location.
        #               Nobody's goal is locked by that location? The other hinted locations that are locked by that location are also not required.
        #       Update base state, allowing it to collect the locations in the batch.
        # At the very end, we have the base state has done sweep_for_advancements with no excluded locations. We save that state, so that we can determine
        #   which of the hinted locations are not reachable, so that we can say "lost" in the cryptic hint.

        BATCH_SIZE = 25

        # In case of when everybody with cryptic hints has signpost_hints = 0
        if not Hint.submitted_cryptic_hinted_locations:
            return

        # Already computed by a previous world.
        if Hint.item_requirement_cache:
            return

        for location in {loc for loc in Hint.submitted_cryptic_hinted_locations if not loc.advancement}:
            Hint.item_requirement_cache[location] = []

        worthwhile_locations = {loc for loc in Hint.submitted_cryptic_hinted_locations if loc.advancement and loc not in Hint.item_requirement_cache}

        base_state = CollectionState(world.multiworld)

        while worthwhile_locations:
            base_state.sweep_for_advancements(checked_locations=base_state.locations_checked | worthwhile_locations)
            current_sphere_locations = {loc for loc in worthwhile_locations if base_state.can_reach(loc)}
            if not current_sphere_locations:
                # Remaining locations are unreachable, so not required.
                for location in worthwhile_locations:
                    Hint.item_requirement_cache[location] = []
                break
            for location in current_sphere_locations:
                worthwhile_locations.remove(location)
            while current_sphere_locations:
                # Doing things in batches saves a lot of time, since some locations can slow things down significantly.
                location_batch = [current_sphere_locations.pop() for _ in range(min(len(current_sphere_locations), BATCH_SIZE))]

                batch_state = base_state.copy()
                batch_state.sweep_for_advancements(checked_locations=base_state.locations_checked | set(location_batch))
                while location_batch:
                    loc = world.random.choice(location_batch)
                    location_batch.remove(loc)

                    test_state = batch_state.copy()
                    test_state.sweep_for_advancements(checked_locations=test_state.locations_checked | {loc})

                    Hint.item_requirement_cache[loc] = [player for player in world.multiworld.player_ids if not world.multiworld.has_beaten_game(test_state, player)]

                    # If collecting one location is not required, then everything that remains unreachable without collecting that location is also not required.
                    if not Hint.item_requirement_cache[loc]:
                        for new_reachable in {location for location in worthwhile_locations if not test_state.can_reach(location)}:
                            worthwhile_locations.remove(new_reachable)
                            Hint.item_requirement_cache[new_reachable] = []

                # We no longer need to test that location, so advance the base state with that location not excluded to save time on the next iterations.
                base_state.sweep_for_advancements(checked_locations=base_state.locations_checked | worthwhile_locations | current_sphere_locations)
        # Save final state for lost hints
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
            if self.world.player in Hint.item_requirement_cache[self.location]:
                return f"{formatted_location} is on the Wahay of the Duo."
            if Hint.item_requirement_cache[self.location]:
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

def generate_hint_data(world: "BanjoTooieWorld"):

    if world.options.hint_clarity.value == HintClarity.option_cryptic:
        Hint.compute_item_requirement_cache(world)

    hint_data = [Hint(world, location).hint_data for location in world.hinted_locations]

    generate_joke_hints(world, hint_data)

    # Since these are static variables, we have to manually empty them.
    # Using del messes up with tests, so we're simply deleting the reference.
    if world.options.hint_clarity.value == HintClarity.option_cryptic:
        if Hint.is_last_cryptic_hint_world(world):
            Hint.item_requirement_cache = dict()
            Hint.submitted_cryptic_hinted_locations = set()
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

SLOW_LOCATION_NAMES = [
    locationName.JINJOGM1,
    locationName.JINJOGI3,
    locationName.JINJOGI5,
    locationName.JIGGYMT1,
    locationName.JIGGYMT5,
    locationName.JIGGYGM5,
    locationName.JIGGYMT3,
    locationName.JIGGYWW1,
    locationName.JIGGYWW2,
    locationName.JIGGYWW3,
    locationName.JIGGYWW4,
    locationName.JIGGYWW5,
    locationName.JIGGYWW7,
    locationName.JIGGYWW8,
    locationName.JIGGYJR3,
    locationName.JIGGYJR4,
    locationName.JIGGYJR9,
    locationName.JIGGYTD3,
    locationName.JIGGYTD5,
    locationName.JIGGYTD6,
    locationName.JIGGYTD7,
    locationName.JIGGYGI1,
    locationName.JIGGYGI2,
    locationName.JIGGYGI3,
    locationName.JIGGYGI4,
    locationName.JIGGYGI6,
    locationName.JIGGYGI9,
    locationName.JIGGYHP1,
    locationName.JIGGYHP3,
    locationName.JIGGYHP5,
    locationName.JIGGYHP6,
    locationName.JIGGYHP7,
    locationName.JIGGYHP8,
    locationName.JIGGYHP9,
    locationName.JIGGYHP10,
    locationName.JIGGYCC2,
    locationName.JIGGYCC3,
    locationName.JIGGYCC4,
    locationName.JIGGYCC7,
    locationName.JIGGYIH5,
    locationName.JIGGYIH6,
    locationName.JIGGYIH7,
    locationName.JIGGYIH8,
    locationName.JIGGYIH9,
    locationName.GLOWBOMEG,
    locationName.HONEYCJR3,
    locationName.CHEATOGM1,
    locationName.CHEATOWW3,
    locationName.CHEATOJR1,
    locationName.CHEATOTL1,
    locationName.CHEATOGI3,
    locationName.CHEATOCC1,
    locationName.CHEATOCC2,
    locationName.CHEATOR3,
    locationName.CHEATOR4,
    locationName.CHEATOR5,
    locationName.HONEYBR4,
    locationName.HONEYBR5,
    locationName.SCRUT,
    locationName.SCRAT,
    locationName.GROGGY,
    locationName.GAMETTE,
    locationName.BETETTE,
    locationName.ALPHETTE,
    locationName.SKIVF1,
    locationName.SKIVF2,
    locationName.NESTGM15,
    locationName.NESTTL35,
    locationName.NESTGI50,
    locationName.NESTGI51,
    locationName.NESTGI52,
    locationName.NESTHP21,
    locationName.NESTHP22,
    locationName.SIGNCC2,
    locationName.WARPCK2,
]

def compute_item_requirement(world: "BanjoTooieWorld"):
    if not Hint.item_requirement_cache:
        Hint.compute_item_requirement_cache(world)

def choose_hinted_locations(world: "BanjoTooieWorld"):
    choose_move_locations(world)
    choose_slow_locations(world)
    choose_random_locations(world)

    if world.options.hint_clarity == HintClarity.option_cryptic:
        Hint.submit_hinted_locations(world.hinted_locations)

def choose_random_locations(world: "BanjoTooieWorld"):
    if len(world.hinted_locations) >= world.options.signpost_hints:
        return
    remaining_locations = [location for location in world.get_locations() if location not in world.hinted_locations and should_consider_location(location)]
    world.random.shuffle(remaining_locations)
    while len(world.hinted_locations) < world.options.signpost_hints:
        world.hinted_locations.add(remaining_locations.pop())

def get_slow_location_weight(location: Location) -> int:
    if location.item.classification == ItemClassification.progression:
        return 20
    elif location.item.classification & ItemClassification.progression_skip_balancing\
            == ItemClassification.progression_skip_balancing\
        or location.item.classification & ItemClassification.progression_deprioritized\
            == ItemClassification.progression_deprioritized:
        return 5
    elif location.item.classification == ItemClassification.useful:
        return 3
    return 1

def choose_slow_locations(world: "BanjoTooieWorld"):
    if len(world.hinted_locations) >= world.options.signpost_hints:
        return
    slow_locations = [location for location in world.get_locations() if location.name in SLOW_LOCATION_NAMES]

    if world.options.randomize_bt_moves.value:
        sorted_silos = [k for k, v in sorted(world.jamjars_siloname_costs.items(), key=lambda item: item[1])]
        for _ in range(1, 7):
            slow_locations.append(get_location_by_name(world, sorted_silos.pop()))

    unhinted_slow_locations = list(set([location for location in slow_locations if location not in world.hinted_locations]))
    weights = [get_slow_location_weight(hint) for hint in unhinted_slow_locations]
    locations_weights = list(zip(unhinted_slow_locations, weights))
    locations_weights = sorted(locations_weights, key=lambda x: world.random.random() / x[1])
    weighted_locations = list(map(lambda lw: lw[0], locations_weights))
    
    world.hinted_locations.update(weighted_locations[:world.options.signpost_hints.value - len(world.hinted_locations)])

def choose_move_locations(world: "BanjoTooieWorld"):
    all_moves_names = []

    # We don't want BT moves to be hinted when they're in the vanilla location.
    if world.options.randomize_bt_moves.value:
        all_moves_names.extend(moves_table.keys())
    all_moves_names.extend(bk_moves_table.keys())
    all_moves_names.extend(progressive_ability_table.keys())

    all_move_locations = [location for location in get_all_hintable_locations(world)
                          if location.item.name in all_moves_names and location.item.player == world.player]
    world.random.shuffle(all_move_locations)

    for location in all_move_locations:
        if len(world.hinted_locations) < min(
            world.options.signpost_move_hints.value,
            world.options.signpost_hints.value
        ):
            world.hinted_locations.add(location)


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
