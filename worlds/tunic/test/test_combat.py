from BaseClasses import ItemClassification
from collections import Counter

from . import TunicTestBase
from .. import options
from ..combat_logic import (check_combat_reqs, area_data, get_money_count, calc_effective_hp, get_potion_level,
                            get_hp_level, get_def_level, get_sp_level, has_combat_reqs)
from ..items import item_table
from .. import TunicWorld


class TestCombat(TunicTestBase):
    options = {options.CombatLogic.internal_name: options.CombatLogic.option_on}
    player = 1
    world: TunicWorld
    combat_items = []
    # these are items that are progression that do not contribute to combat logic
    # it's listed as using skipped items instead of a list of viable items so that if we add/remove some later,
    # that this won't require updates most likely
    # Stick and Sword are in here because sword progression is the clear determining case here
    skipped_items = {"Fairy", "Stick", "Sword", "Magic Dagger", "Magic Orb", "Lantern", "Old House Key", "Key",
                     "Fortress Vault Key", "Golden Coin", "Red Questagon", "Green Questagon", "Blue Questagon",
                     "Scavenger Mask", "Pages 24-25 (Prayer)", "Pages 42-43 (Holy Cross)", "Pages 52-53 (Icebolt)"}
    # converts golden trophies to their hero relic stat equivalent, for easier parsing
    converter = {
        "Secret Legend": "Hero Relic - DEF",
        "Phonomath": "Hero Relic - DEF",
        "Just Some Pals": "Hero Relic - POTION",
        "Spring Falls": "Hero Relic - POTION",
        "Back To Work": "Hero Relic - POTION",
        "Mr Mayor": "Hero Relic - SP",
        "Power Up": "Hero Relic - SP",
        "Regal Weasel": "Hero Relic - SP",
        "Forever Friend": "Hero Relic - SP",
        "Sacred Geometry": "Hero Relic - MP",
        "Vintage": "Hero Relic - MP",
        "Dusty": "Hero Relic - MP",
    }
    skipped_items.update({item for item in item_table.keys() if item.startswith("Ladder")})
    for item, data in item_table.items():
        if item in skipped_items:
            continue
        ic = data.combat_ic or data.classification
        if item in converter:
            item = converter[item]
        if ItemClassification.progression in ic:
            combat_items += [item] * data.quantity_in_item_pool

    # we had an issue where collecting certain items brought certain areas out of logic
    # due to the weirdness of swapping between "you have enough attack that you don't need magic"
    # so this will make sure collecting an item doesn't bring something out of logic
    def test_combat_doesnt_fail_backwards(self):
        combat_items = self.combat_items.copy()
        self.multiworld.worlds[1].random.shuffle(combat_items)
        curr_statuses = {name: False for name in area_data.keys()}
        prev_statuses = curr_statuses.copy()
        area_names = list(area_data.keys())
        current_items = Counter()
        for current_item_name in combat_items:
            current_items[current_item_name] += 1
            current_item = TunicWorld.create_item(self.world, current_item_name)
            self.collect(current_item)
            self.multiworld.worlds[1].random.shuffle(area_names)
            for area in area_names:
                curr_statuses[area] = check_combat_reqs(area, self.multiworld.state, self.player)
                if curr_statuses[area] < prev_statuses[area]:
                    data = area_data[area]
                    state = self.multiworld.state
                    player = self.player
                    req_effective_hp = calc_effective_hp(data.hp_level, data.potion_level, data.potion_count)
                    player_potion, potion_offerings = get_potion_level(state, player)
                    player_hp, hp_offerings = get_hp_level(state, player)
                    player_def, def_offerings = get_def_level(state, player)
                    player_sp, sp_offerings = get_sp_level(state, player)
                    raise Exception(f"Status for {area} decreased after collecting {current_item_name}.\n"
                                    f"Current items: {current_items}.\n"
                                    f"Total money: {get_money_count(self.multiworld.state, self.player)}.\n"
                                    f"Required Effective HP: {req_effective_hp}.\n"
                                    f"Free HP and Offerings: {player_hp - hp_offerings}, {hp_offerings}\n"
                                    f"Free Potion and Offerings: {player_potion - potion_offerings}, {potion_offerings}\n"
                                    f"Free Def and Offerings: {player_def - def_offerings}, {def_offerings}\n"
                                    f"Free SP and Offerings: {player_sp - sp_offerings}, {sp_offerings}")
                prev_statuses[area] = curr_statuses[area]

    # the issue was that a direct check of the logic and the cache had different results
    # it was actually due to the combat_items in items.py not having the Gun in it
    # but this test is still helpful for verifying the cache
    def test_combat_magic_weapons(self):
        combat_items = self.combat_items.copy()
        combat_items.remove("Magic Wand")
        combat_items.remove("Gun")
        area_names = list(area_data.keys())
        self.multiworld.worlds[1].random.shuffle(combat_items)
        self.multiworld.worlds[1].random.shuffle(area_names)
        current_items = Counter()
        state = self.multiworld.state.copy()
        player = self.player
        gun = TunicWorld.create_item(self.world, "Gun")

        for current_item_name in combat_items:
            current_item = TunicWorld.create_item(self.world, current_item_name)
            state.collect(current_item)
            current_items[current_item_name] += 1
            for area in area_names:
                if check_combat_reqs(area, state, player) != has_combat_reqs(area, state, player):
                    raise Exception(f"Cache for {area} does not match a direct check "
                                    f"after collecting {current_item_name}.\n"
                                    f"Current items: {current_items}.\n"
                                    f"Cache {'succeeded' if has_combat_reqs(area, state, player) else 'failed'}\n"
                                    f"Direct {'succeeded' if check_combat_reqs(area, state, player) else 'failed'}")
            state.collect(gun)
            for area in area_names:
                if check_combat_reqs(area, state, player) != has_combat_reqs(area, state, player):
                    raise Exception(f"Cache for {area} does not match a direct check "
                                    f"after collecting the Gun.\n"
                                    f"Current items: {current_items}.\n"
                                    f"Cache {'succeeded' if has_combat_reqs(area, state, player) else 'failed'}\n"
                                    f"Direct {'succeeded' if check_combat_reqs(area, state, player) else 'failed'}")
            state.remove(gun)
