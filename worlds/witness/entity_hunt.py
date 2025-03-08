from collections import defaultdict
from logging import debug, warning
from pprint import pformat
from typing import TYPE_CHECKING, Dict, List, Set, Tuple

from .data import static_logic as static_witness_logic

if TYPE_CHECKING:
    from . import WitnessWorld
    from .player_logic import WitnessPlayerLogic

DISALLOWED_ENTITIES_FOR_PANEL_HUNT = {
    "0x03629",  # Tutorial Gate Open, which is the panel that is locked by panel hunt
    "0x03505",  # Tutorial Gate Close (same thing)
    "0x3352F",  # Gate EP (same thing)
    "0x09F7F",  # Mountaintop Box Short. This is reserved for panel_hunt_postgame.
    "0x00CDB",  # Challenge Reallocating
    "0x0051F",  # Challenge Reallocating
    "0x00524",  # Challenge Reallocating
    "0x00CD4",  # Challenge Reallocating
    "0x00CB9",  # Challenge May Be Unsolvable
    "0x00CA1",  # Challenge May Be Unsolvable
    "0x00C80",  # Challenge May Be Unsolvable
    "0x00C68",  # Challenge May Be Unsolvable
    "0x00C59",  # Challenge May Be Unsolvable
    "0x00C22",  # Challenge May Be Unsolvable
    "0x0A3A8",  # Reset PP
    "0x0A3B9",  # Reset PP
    "0x0A3BB",  # Reset PP
    "0x0A3AD",  # Reset PP
}

ALL_HUNTABLE_PANELS = [
    entity_hex
    for entity_hex, entity_obj in static_witness_logic.ENTITIES_BY_HEX.items()
    if entity_obj["entityType"] == "Panel" and entity_hex not in DISALLOWED_ENTITIES_FOR_PANEL_HUNT
]


class EntityHuntPicker:
    def __init__(self, player_logic: "WitnessPlayerLogic", world: "WitnessWorld",
                 pre_picked_entities: Set[str]) -> None:
        self.player_logic = player_logic
        self.player_options = world.options
        self.player_name = world.player_name
        self.random = world.random

        self.PRE_PICKED_HUNT_ENTITIES = pre_picked_entities.copy()
        self.HUNT_ENTITIES: Set[str] = set()

        self._add_plandoed_hunt_panels_to_pre_picked()

        self.ALL_ELIGIBLE_ENTITIES, self.ELIGIBLE_ENTITIES_PER_AREA = self._get_eligible_panels()

    def pick_panel_hunt_panels(self, total_amount: int) -> Set[str]:
        """
        The process of picking all hunt entities is:

        1. Add pre-defined hunt entities
        2. Pick random hunt entities to fill out the rest
        3. Replace unfair entities with fair entities

        Each of these is its own function.
        """

        self.HUNT_ENTITIES = self.PRE_PICKED_HUNT_ENTITIES.copy()

        self._pick_all_hunt_entities(total_amount)
        self._replace_unfair_hunt_entities_with_good_hunt_entities()
        self._log_results()

        return self.HUNT_ENTITIES

    def _entity_is_eligible(self, panel_hex: str, plando: bool = False) -> bool:
        """
        Determine whether an entity is eligible for entity hunt based on player options.
        """
        panel_obj = static_witness_logic.ENTITIES_BY_HEX[panel_hex]

        if not self.player_logic.solvability_guaranteed(panel_hex) or panel_hex in self.player_logic.EXCLUDED_ENTITIES:
            if plando:
                warning(f"Panel {panel_obj['checkName']} is disabled / excluded and thus not eligible for panel hunt.")
            return False

        return plando or not (
            # Due to an edge case, Discards have to be on in disable_non_randomized even if Discard Shuffle is off.
            # However, I don't think they should be hunt panels in this case.
            self.player_options.disable_non_randomized_puzzles
            and not self.player_options.shuffle_discarded_panels
            and panel_obj["locationType"] == "Discard"
        )

    def _add_plandoed_hunt_panels_to_pre_picked(self) -> None:
        """
        Add panels the player explicitly specified to be included in panel hunt to the pre picked hunt panels.
        Output a warning if a panel could not be added for some reason.
        """

        # Plandoed hunt panels should be in random order, but deterministic by seed, so we sort, then shuffle
        panels_to_plando = sorted(self.player_options.panel_hunt_plando.value)
        self.random.shuffle(panels_to_plando)

        for location_name in panels_to_plando:
            entity_hex = static_witness_logic.ENTITIES_BY_NAME[location_name]["entity_hex"]

            if entity_hex in self.PRE_PICKED_HUNT_ENTITIES:
                continue

            if self._entity_is_eligible(entity_hex, plando=True):
                if len(self.PRE_PICKED_HUNT_ENTITIES) == self.player_options.panel_hunt_total:
                    warning(
                        f"Panel {location_name} could not be plandoed as a hunt panel for {self.player_name}'s world, "
                        f"because it would exceed their panel hunt total."
                    )
                    continue

                self.PRE_PICKED_HUNT_ENTITIES.add(entity_hex)

    def _get_eligible_panels(self) -> Tuple[List[str], Dict[str, Set[str]]]:
        """
        There are some entities that are not allowed for panel hunt for various technical of gameplay reasons.
        Make a list of all the ones that *are* eligible, plus a lookup of eligible panels per area.
        """

        all_eligible_panels = [
            panel for panel in ALL_HUNTABLE_PANELS
            if self._entity_is_eligible(panel)
        ]

        eligible_panels_by_area = defaultdict(set)
        for eligible_panel in all_eligible_panels:
            associated_area = static_witness_logic.ENTITIES_BY_HEX[eligible_panel]["area"]["name"]
            eligible_panels_by_area[associated_area].add(eligible_panel)

        return all_eligible_panels, eligible_panels_by_area

    def _get_percentage_of_hunt_entities_by_area(self) -> Dict[str, float]:
        hunt_entities_picked_so_far_prevent_div_0 = max(len(self.HUNT_ENTITIES), 1)

        contributing_percentage_per_area = {}
        for area, eligible_entities in self.ELIGIBLE_ENTITIES_PER_AREA.items():
            amount_of_already_chosen_entities = len(self.ELIGIBLE_ENTITIES_PER_AREA[area] & self.HUNT_ENTITIES)
            current_percentage = amount_of_already_chosen_entities / hunt_entities_picked_so_far_prevent_div_0
            contributing_percentage_per_area[area] = current_percentage

        return contributing_percentage_per_area

    def _get_next_random_batch(self, amount: int, same_area_discouragement: float) -> List[str]:
        """
        Pick the next batch of hunt entities.
        Areas that already have a lot of hunt entities in them will be discouraged from getting more.
        The strength of this effect is controlled by the same_area_discouragement factor from the player's options.
        """

        percentage_of_hunt_entities_by_area = self._get_percentage_of_hunt_entities_by_area()

        max_percentage = max(percentage_of_hunt_entities_by_area.values())
        if max_percentage == 0:
            allowance_per_area = {area: 1.0 for area in percentage_of_hunt_entities_by_area}
        else:
            allowance_per_area = {
                area: (max_percentage - current_percentage) / max_percentage
                for area, current_percentage in percentage_of_hunt_entities_by_area.items()
            }
            # use same_area_discouragement as lerp factor
            allowance_per_area = {
                area: (1.0 - same_area_discouragement) + (weight * same_area_discouragement)
                for area, weight in allowance_per_area.items()
            }

        assert min(allowance_per_area.values()) >= 0, (
            f"Somehow, an area had a negative weight when picking hunt entities: {allowance_per_area}"
        )

        remaining_entities, remaining_entity_weights = [], []
        for area, eligible_entities in self.ELIGIBLE_ENTITIES_PER_AREA.items():
            for panel in sorted(eligible_entities - self.HUNT_ENTITIES):
                remaining_entities.append(panel)
                remaining_entity_weights.append(allowance_per_area[area])

        # I don't think this can ever happen, but let's be safe
        if sum(remaining_entity_weights) == 0:
            remaining_entity_weights = [1] * len(remaining_entity_weights)

        return self.random.choices(remaining_entities, weights=remaining_entity_weights, k=amount)

    def _pick_all_hunt_entities(self, total_amount: int) -> None:
        """
        The core function of the EntityHuntPicker in which all Hunt Entities are picked,
        respecting the player's choices for total amount and same area discouragement.
        """
        same_area_discouragement = self.player_options.panel_hunt_discourage_same_area_factor / 100

        # If we're using random picking, just choose all the entities now and return
        if not same_area_discouragement:
            hunt_entities = self.random.sample(
                [entity for entity in self.ALL_ELIGIBLE_ENTITIES if entity not in self.HUNT_ENTITIES],
                k=total_amount - len(self.HUNT_ENTITIES),
            )
            self.HUNT_ENTITIES.update(hunt_entities)
            return

        # If we're discouraging entities from the same area being picked, we have to pick entities one at a time
        # For higher total counts, we do them in small batches for performance
        batch_size = max(1, total_amount // 20)

        while len(self.HUNT_ENTITIES) < total_amount:
            actual_amount_to_pick = min(batch_size, total_amount - len(self.HUNT_ENTITIES))

            self.HUNT_ENTITIES.update(self._get_next_random_batch(actual_amount_to_pick, same_area_discouragement))

    def _replace_unfair_hunt_entities_with_good_hunt_entities(self) -> None:
        """
        For connected entities that "solve together", make sure that the one you're guaranteed
        to be able to see and interact with first is the one that is chosen, so you don't get "surprise entities".
        """

        replacements = {
            "0x18488": "0x00609",  # Replace Swamp Sliding Bridge Underwater -> Swamp Sliding Bridge Above Water
            "0x03676": "0x03678",  # Replace Quarry Upper Ramp Control -> Lower Ramp Control
            "0x03675": "0x03679",  # Replace Quarry Upper Lift Control -> Lower Lift Control

            "0x03702": "0x15ADD",  # Jungle Vault Box -> Jungle Vault Panel
            "0x03542": "0x002A6",  # Mountainside Vault Box -> Mountainside Vault Panel
            "0x03481": "0x033D4",  # Tutorial Vault Box -> Tutorial Vault Panel
            "0x0339E": "0x0CC7B",  # Desert Vault Box -> Desert Vault Panel
            "0x03535": "0x00AFB",  # Shipwreck Vault Box -> Shipwreck Vault Panel
        }

        if self.player_options.shuffle_doors < 2:
            replacements.update(
                {
                    "0x334DC": "0x334DB",  # In door shuffle, the Shadows Timer Panels are disconnected
                    "0x17CBC": "0x2700B",  # In door shuffle, the Laser Timer Panels are disconnected
                }
            )

        for bad_entitiy, good_entity in replacements.items():
            # If the bad entity was picked as a hunt entity ...
            if bad_entitiy not in self.HUNT_ENTITIES:
                continue

            # ... and the good entity was not ...
            if good_entity in self.HUNT_ENTITIES or good_entity not in self.ALL_ELIGIBLE_ENTITIES:
                continue

            # ... and it's not a forced pick that should stay the same ...
            if bad_entitiy in self.PRE_PICKED_HUNT_ENTITIES:
                continue

            # ... replace the bad entity with the good entity.
            self.HUNT_ENTITIES.remove(bad_entitiy)
            self.HUNT_ENTITIES.add(good_entity)

    def _log_results(self) -> None:
        final_percentage_by_area = self._get_percentage_of_hunt_entities_by_area()

        sorted_area_percentages_dict = dict(sorted(final_percentage_by_area.items(), key=lambda x: x[1]))
        sorted_area_percentages_dict_pretty_print = {
            area: str(percentage) + (" (maxed)" if self.ELIGIBLE_ENTITIES_PER_AREA[area] <= self.HUNT_ENTITIES else "")
            for area, percentage in sorted_area_percentages_dict.items()
        }
        player_name = self.player_name
        discouragemenet_factor = self.player_options.panel_hunt_discourage_same_area_factor
        debug(
            f'Final area percentages for player "{player_name}" ({discouragemenet_factor} discouragement):\n'
            f"{pformat(sorted_area_percentages_dict_pretty_print)}"
        )
