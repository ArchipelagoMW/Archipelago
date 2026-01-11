from typing import TYPE_CHECKING

from BaseClasses import ItemClassification as IC

from ..Hints import *
from ..Items import ITEM_TABLE
from ..Locations import SSLocType, LOCATION_TABLE, SSLocation
from ..Constants import GONDO_UPGRADES

from .ItemPlacement import item_classification

if TYPE_CHECKING:
    from .. import SSWorld


class Hints:
    """
    Class handles in-game fi and gossip stone hints, as well as song and impa hints.
    """

    def __init__(self, world: "SSWorld"):
        self.world = world
        self.multiworld = world.multiworld

        self.placed_hints: dict[str, list] = {}
        self.placed_hints_log: dict[str, list] = {}
        self.locations_for_hint: dict[str, list] = {}
        self.hinted_locations: list[str] = []
        self.hinted_item_locations: list = []
        self.distribution_option = self.world.options.hint_distribution
        if self.distribution_option == "standard":
            self.distribution: dict[str, any] = HINT_DISTRIBUTIONS["Standard"]
        if self.distribution_option == "junk":
            self.distribution: dict[str, any] = HINT_DISTRIBUTIONS["Junk"]

        self.always_locations = [
            loc
            for loc in self.world.progress_locations
            if self.world.get_location(loc).hint == SSHintType.ALWAYS
        ]
        self.sometimes_locations = [
            loc
            for loc in self.world.progress_locations
            if self.world.get_location(loc).hint == SSHintType.SOMETIMES
        ]
        self.hintable_items = []
        for itm, data in ITEM_TABLE.items():
            classification = (
                data.classification
                if item_classification(self.world, itm) is None
                else item_classification(self.world, itm)
            )
            if classification == IC.progression or classification == IC.progression_skip_balancing:
                if data.code is None:
                    continue
                self.hintable_items.extend([itm] * data.quantity)

        # Remove starting items and gondo items (if shuffle off) from hintable pool
        for itm in self.world.starting_items:
            if itm in self.hintable_items:
                self.hintable_items.remove(itm)
        if not self.world.options.gondo_upgrades:
            for itm in GONDO_UPGRADES:
                if itm in self.hintable_items:
                    self.hintable_items.remove(itm)
        self.all_hints = []

    def handle_hints(self) -> tuple[dict[str, list], dict[str, list]]:
        """
        Handles hints for Skyward Sword during the APSSR file output.

        :param world: The SS game world.
        :return: A tuple of a dict containing in-game hints for Fi, each Gossip Stone, and songs; and a dict of log hints.
        """
        if self.world.options.song_hints == "direct":
            self.sometimes_locations = [
                loc
                for loc in self.sometimes_locations
                if self.world.get_location(loc).type != SSLocType.WPOBJ
            ]

        # Create and fill hint classes
        location_hints, item_hints, junk_hints = self._create_hints()
        for hint in location_hints:
            loc = hint.location
            itm = self.world.get_location(loc).item
            hint.region = self.world.get_location(loc).region
            hint.player_to_receive = self.multiworld.get_player_name(itm.player)
            hint.item = itm.name
        for hint in item_hints:
            itm = hint.item
            locs = [
                loc
                for loc in self.multiworld.get_locations()
                if loc.item.name == itm and loc.item.player == self.world.player
            ]
            for loc in self.hinted_item_locations:
                if loc in locs:
                    locs.remove(loc)
            if len(locs) == 0:
                raise Exception(
                    f"Tried to hint item {itm} but couldn't find any locations with that item!"
                )
            loc = self.world.random.choice(locs)
            hint.location = loc.name
            hint.region = loc.parent_region
            hint.player_to_find = self.multiworld.get_player_name(loc.player)
        for hint in junk_hints:
            pass  # We don't need to do anything with these right now

        self.all_hints.extend(location_hints)
        self.all_hints.extend(item_hints)
        self.all_hints.extend(junk_hints)
        self.world.random.shuffle(self.all_hints)

        for hint, data in HINT_TABLE.items():
            if data.type == SSHintType.FI:
                fi_hints = []
                for _ in range(self.distribution["fi"]):
                    fi_hints.append(self.all_hints.pop())
                self.placed_hints["Fi"] = [fh.to_fi_text() for fh in fi_hints]
                self.placed_hints_log["Fi"] = [fh.to_log_text() for fh in fi_hints]
                self.locations_for_hint["Fi"] = [fh.aplocation for fh in fi_hints if isinstance(fh, SSLocationHint)]
            elif data.type == SSHintType.STONE:
                stone_hints = []
                for _ in range(self.distribution["hints_per_stone"]):
                    stone_hints.append(self.all_hints.pop())
                self.placed_hints[hint] = [sh.to_stone_text() for sh in stone_hints]
                self.placed_hints_log[hint] = [sh.to_log_text() for sh in stone_hints]
                self.locations_for_hint[hint] = [sh.aplocation for sh in stone_hints if isinstance(sh, SSLocationHint)]
            elif data.type == SSHintType.SONG:
                song_hints = self._handle_song_hints(hint)
                self.placed_hints[hint] = song_hints
                self.placed_hints_log[hint] = song_hints

        return self.placed_hints, self.placed_hints_log

    def handle_impa_sot_hint(self) -> tuple[str, str] | None:
        """
        Handles Impa's Stone of Trials hint.
        """
        sot_locations = [
            loc
            for loc in self.multiworld.get_locations()
            if loc.item.player == self.world.player
            and loc.item.name == "Stone of Trials"
        ]
        if len(sot_locations) == 1:
            sot_location = sot_locations.pop()
            return (
                sot_location.parent_region.name,
                self.multiworld.get_player_name(sot_location.player),
            )
        else:
            return None

    def _create_hints(self) -> tuple[list, list, list]:
        fi_hints = self.distribution["fi"]
        hints_per_stone = self.distribution["hints_per_stone"]
        num_hints_to_place = fi_hints + (18 * hints_per_stone)
        location_hints: list[SSLocationHint] = []
        item_hints: list[SSItemHint] = []
        junk_hints: list[SSJunkHint] = []

        if num_hints_to_place == 0:
            return location_hints, item_hints, junk_hints

        # Place always hints first
        if "always" in self.distribution["distribution"]:
            for loc in self.always_locations:
                location_hints.append(SSLocationHint(loc, self.world))
                self.hinted_locations.append(loc)

        if len(location_hints) >= num_hints_to_place:
            return location_hints, item_hints, junk_hints

        # Place fixed hints next, in order
        current_order = 0
        max_order = self.distribution["max_order"]
        while (
            len(location_hints) + len(item_hints) + len(junk_hints)
        ) < num_hints_to_place:
            for h_type, h_data in self.distribution["distribution"].items():
                if h_type != "always":
                    if h_data["order"] == current_order:
                        fixed_hints_to_place = h_data["fixed"]
                        if h_type == "sometimes":
                            location_hints.extend(
                                self._create_sometimes_hints(fixed_hints_to_place)
                                * h_data["copies"]
                            )
                        elif h_type == "item":
                            item_hints.extend(
                                self._create_item_hints(fixed_hints_to_place)
                                * h_data["copies"]
                            )
                        elif h_type == "junk":
                            junk_hints.extend(
                                self._create_junk_hints(fixed_hints_to_place)
                                * h_data["copies"]
                            )
            if current_order >= max_order:
                break
            current_order += 1

        # Fill the remaining hints based on weights
        while (
            len(location_hints) + len(item_hints) + len(junk_hints)
        ) < num_hints_to_place:
            placeable_hint_types = ["junk"]
            if (
                len(self.sometimes_locations) > 0
                and "sometimes" in self.distribution["distribution"]
            ):
                placeable_hint_types.append("sometimes")
            if (
                len(self.hintable_items) > 0
                and "item" in self.distribution["distribution"]
            ):
                placeable_hint_types.append("item")

            hint_type_to_place = self.world.random.choices(
                placeable_hint_types,
                weights=[
                    self.distribution["distribution"][t]["weight"]
                    for t in placeable_hint_types
                ],
                k=1,
            ).pop()

            if hint_type_to_place == "sometimes":
                copies = self.distribution["distribution"]["sometimes"]["copies"]
                location_hints.extend(self._create_sometimes_hints(1) * copies)
            if hint_type_to_place == "item":
                copies = self.distribution["distribution"]["item"]["copies"]
                item_hints.extend(self._create_item_hints(1) * copies)
            if hint_type_to_place == "junk":
                copies = self.distribution["distribution"]["junk"]["copies"]
                junk_hints.extend(self._create_junk_hints(1) * copies)

        return location_hints, item_hints, junk_hints

    def _create_sometimes_hints(self, q) -> list[SSLocationHint]:
        hints = []

        for _ in range(q):
            self.world.random.shuffle(self.sometimes_locations)
            loc_to_hint = self.sometimes_locations.pop()
            if loc_to_hint in self.hinted_locations:
                raise Exception(
                    f"Tried to hint location {loc_to_hint} but location was already hinted!"
                )
            hints.append(loc_to_hint)
            self.hinted_locations.append(loc_to_hint)

        return [SSLocationHint(loc, self.world) for loc in hints]

    def _create_item_hints(self, q) -> list[SSItemHint]:
        hints = []

        for _ in range(q):
            self.world.random.shuffle(self.hintable_items)
            itm_to_hint = self.hintable_items.pop()
            hints.append(itm_to_hint)

        return [SSItemHint(itm) for itm in hints]

    def _create_junk_hints(self, q) -> list[SSJunkHint]:
        hints = self._get_junk_hint_texts(q)
        return [SSJunkHint(text) for text in hints]

    def _handle_song_hints(self, hint) -> list[str]:
        direct_text = "This trial holds {plr}'s {itm}"
        required_text = "Your spirit will grow by completing this trial"
        useful_text = "Someone might need its reward..."
        useless_text = "Its reward is probably not too important..."

        trial_gate = SONG_HINT_TO_TRIAL_GATE[hint]
        trial_connection = [
            trl
            for trl, gate in self.world.entrances.trial_connections.items()
            if gate == trial_gate
        ].pop()
        trial_item = self.world.get_location(f"{trial_connection} - Trial Reward").item
        if self.world.options.song_hints == "none":
            return [""]
        if self.world.options.song_hints == "basic":
            return (
                [useful_text]
                if trial_item.classification == IC.progression
                or trial_item.classification == IC.progression_skip_balancing
                or trial_item.classification == IC.useful
                else [useless_text]
            )
        if self.world.options.song_hints == "advanced":
            if trial_item.classification == IC.progression or trial_item.classification == IC.progression_skip_balancing:
                return [required_text]
            elif trial_item.classification == IC.useful:
                return [useful_text]
            else:
                return [useless_text]
        if self.world.options.song_hints == "direct":
            self.locations_for_hint[hint] = [f"{trial_connection} - Trial Reward"]
            player_name = self.multiworld.get_player_name(trial_item.player)
            item_name = trial_item.name
            return [direct_text.format(plr=player_name, itm=item_name)]

    def _get_junk_hint_texts(self, q: int) -> list[str]:
        """
        Get q number of junk hint texts.

        :param q: Quantity of junk hints to return.
        :return: List of q junk hints.
        """
        return self.world.random.sample(JUNK_HINT_TEXT, k=q)
