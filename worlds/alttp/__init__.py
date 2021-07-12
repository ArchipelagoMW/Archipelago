from BaseClasses import Item, CollectionState
from .SubClasses import ALttPItem
from ..AutoWorld import World
from .Options import alttp_options
from .Items import as_dict_item_table, item_name_groups, item_table
from .Regions import lookup_name_to_id


class ALTTPWorld(World):
    game: str = "A Link to the Past"
    options = alttp_options
    topology_present = True
    item_name_groups = item_name_groups
    item_names = frozenset(item_table)
    location_names = frozenset(lookup_name_to_id)
    hint_blacklist = {"Triforce"}

    item_name_to_id = {name: data.item_code for name, data in item_table.items() if type(data.item_code) == int}
    location_name_to_id = lookup_name_to_id

    def collect(self, state: CollectionState, item: Item) -> bool:
        if item.name.startswith('Progressive '):
            if 'Sword' in item.name:
                if state.has('Golden Sword', item.player):
                    pass
                elif state.has('Tempered Sword', item.player) and self.world.difficulty_requirements[
                    item.player].progressive_sword_limit >= 4:
                    state.prog_items['Golden Sword', item.player] += 1
                    return True
                elif state.has('Master Sword', item.player) and self.world.difficulty_requirements[
                    item.player].progressive_sword_limit >= 3:
                    state.prog_items['Tempered Sword', item.player] += 1
                    return True
                elif state.has('Fighter Sword', item.player) and self.world.difficulty_requirements[item.player].progressive_sword_limit >= 2:
                    state.prog_items['Master Sword', item.player] += 1
                    return True
                elif self.world.difficulty_requirements[item.player].progressive_sword_limit >= 1:
                    state.prog_items['Fighter Sword', item.player] += 1
                    return True
            elif 'Glove' in item.name:
                if state.has('Titans Mitts', item.player):
                    pass
                elif state.has('Power Glove', item.player):
                    state.prog_items['Titans Mitts', item.player] += 1
                    return True
                else:
                    state.prog_items['Power Glove', item.player] += 1
                    return True
            elif 'Shield' in item.name:
                if state.has('Mirror Shield', item.player):
                    pass
                elif state.has('Red Shield', item.player) and self.world.difficulty_requirements[item.player].progressive_shield_limit >= 3:
                    state.prog_items['Mirror Shield', item.player] += 1
                    return True
                elif state.has('Blue Shield', item.player)  and self.world.difficulty_requirements[item.player].progressive_shield_limit >= 2:
                    state.prog_items['Red Shield', item.player] += 1
                    return True
                elif self.world.difficulty_requirements[item.player].progressive_shield_limit >= 1:
                    state.prog_items['Blue Shield', item.player] += 1
                    return True
            elif 'Bow' in item.name:
                if state.has('Silver', item.player):
                    pass
                elif state.has('Bow', item.player) and self.world.difficulty_requirements[item.player].progressive_bow_limit >= 2:
                    state.prog_items['Silver Bow', item.player] += 1
                    return True
                elif self.world.difficulty_requirements[item.player].progressive_bow_limit >= 1:
                    state.prog_items['Bow', item.player] += 1
                    return True
        elif item.advancement or item.smallkey or item.bigkey:
            state.prog_items[item.name, item.player] += 1
            return True
        return False

    def get_required_client_version(self) -> tuple:
        return max((0, 1, 4), super(ALTTPWorld, self).get_required_client_version())

    def create_item(self, name: str) -> Item:
        return ALttPItem(name, self.player, **as_dict_item_table[name])


