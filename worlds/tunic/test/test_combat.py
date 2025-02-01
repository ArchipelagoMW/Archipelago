from BaseClasses import ItemClassification
from random import Random

from . import TunicTestBase
from .. import options
from ..combat_logic import check_combat_reqs, area_data
from ..items import item_table
from .. import TunicWorld


class TestCombat(TunicTestBase):
    options = {options.CombatLogic.internal_name: options.CombatLogic.option_on}
    player = 1
    world: TunicWorld
    combat_items = []
    skipped_items = {"Fairy", "Stick", "Sword", "Magic Dagger", "Magic Orb", "Lantern", "Old House Key", "Key",
                     "Fortress Vault Key", "Golden Coin", "Red Questagon", "Green Questagon", "Blue Questagon",
                     "Scavenger Mask", "Pages 24-25 (Prayer)", "Pages 42-43 (Holy Cross)", "Pages 52-53 (Icebolt)"}
    skipped_items.update({item for item in item_table.keys() if item.startswith("Ladder")})
    for item, data in item_table.items():
        if item in skipped_items:
            continue
        ic = data.combat_ic or data.classification
        if ItemClassification.progression in ic:
            for _ in range(data.quantity_in_item_pool):
                combat_items.append(item)

    # we had an issue where collecting certain items brought certain areas out of logic
    # due to the weirdness of swapping between "you have enough attack that you don't need magic"
    # so this will make sure collecting an item doesn't bring something out of logic
    def test_combat_doesnt_fail_backwards(self):
        random_obj = Random()
        combat_items = self.combat_items.copy()
        random_obj.shuffle(combat_items)
        curr_statuses = {name: False for name in area_data.keys()}
        prev_statuses = curr_statuses.copy()
        area_names = [name for name in area_data.keys()]

        while len(combat_items):
            current_item_name = combat_items.pop()
            current_item = TunicWorld.create_item(self.world, current_item_name)
            self.collect(current_item)
            random_obj.shuffle(area_names)
            for area in area_names:
                curr_statuses[area] = check_combat_reqs(area, self.multiworld.state, self.player)
            can_stop = True
            for area, status in curr_statuses.items():
                if status < prev_statuses[area]:
                    raise Exception(f"Status for {area} decreased after collecting {current_item_name}.")
                if not status:
                    can_stop = False
                prev_statuses[area] = status
            # if they're all True, we're probably not regressing anymore so let's save some time and stop now
            if can_stop:
                break
