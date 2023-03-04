from typing import List

from BaseClasses import MultiWorld, Region, Location
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule


class WargrooveLogic(LogicMixin):
    def _wargroove_has_item(self, player: int, item: str) -> bool:
        return self.has(item, player)

    def _wargroove_has_region(self, player: int, region: str) -> bool:
        return self.can_reach(region, 'Region', player)

    def _wargroove_has_item_and_region(self, player: int, item: str, region: str) -> bool:
        return self.can_reach(region, 'Region', player) and self.has(item, player)


def set_rules(world: MultiWorld, player: int):
    # Final Level
    set_rule(world.get_location('Wargroove Finale: Victory', player),
             lambda state: state._wargroove_has_item(player, "Final Bridges") and
                           state._wargroove_has_item(player, "Final Walls") and
                           state._wargroove_has_item(player, "Final Sickle"))
    # Level 1
    set_rule(world.get_location('Humble Beginnings: Caesar', player), lambda state: True)
    set_rule(world.get_location('Humble Beginnings: Chest 1', player), lambda state: True)
    set_rule(world.get_location('Humble Beginnings: Chest 2', player), lambda state: True)
    set_rule(world.get_location('Humble Beginnings: Victory', player), lambda state: True)
    set_region_exit_rules(world.get_region('Humble Beginnings', player),
                          [world.get_location('Humble Beginnings: Victory', player)])

    # Levels 2A-2C
    set_rule(world.get_location('Best Friendssss: Find Sedge', player), lambda state: True)
    set_rule(world.get_location('Best Friendssss: Victory', player), lambda state: True)
    set_region_exit_rules(world.get_region('Best Friendssss', player),
                          [world.get_location('Best Friendssss: Victory', player)])

    set_rule(world.get_location('A Knight\'s Folly: Caesar', player), lambda state: True)
    set_rule(world.get_location('A Knight\'s Folly: Victory', player), lambda state: True)
    set_region_exit_rules(world.get_region('A Knight\'s Folly', player),
                          [world.get_location('A Knight\'s Folly: Victory', player)])

    set_rule(world.get_location('Denrunaway: Chest', player), lambda state: True)
    set_rule(world.get_location('Denrunaway: Victory', player), lambda state: True)
    set_region_exit_rules(world.get_region('Denrunaway', player), [world.get_location('Denrunaway: Victory', player)])

    # Levels 3AA-3AC
    set_rule(world.get_location('Dragon Freeway: Victory', player),
             lambda state: state._wargroove_has_item(player, 'Mage'))
    set_region_exit_rules(world.get_region('Dragon Freeway', player),
                          [world.get_location('Dragon Freeway: Victory', player)])

    set_rule(world.get_location('Deep Thicket: Find Sedge', player),
             lambda state: state._wargroove_has_item(player, 'Mage'))
    set_rule(world.get_location('Deep Thicket: Victory', player),
             lambda state: state._wargroove_has_item(player, 'Mage'))
    set_region_exit_rules(world.get_region('Deep Thicket', player),
                          [world.get_location('Deep Thicket: Victory', player)])

    set_rule(world.get_location('Corrupted Inlet: Victory', player),
             lambda state: state._wargroove_has_item(player, 'Barge') or
                           state._wargroove_has_item(player, 'Merfolk') or
                           state._wargroove_has_item(player, 'Warship'))
    set_region_exit_rules(world.get_region('Corrupted Inlet', player),
                          [world.get_location('Corrupted Inlet: Victory', player)])

    # Levels 3BA-3BC
    set_rule(world.get_location('Mage Mayhem: Caesar', player),
             lambda state: state._wargroove_has_item(player, 'Harpy') or state._wargroove_has_item(player, 'Dragon'))
    set_rule(world.get_location('Mage Mayhem: Victory', player),
             lambda state: state._wargroove_has_item(player, 'Harpy') or state._wargroove_has_item(player, 'Dragon'))
    set_region_exit_rules(world.get_region('Mage Mayhem', player), [world.get_location('Mage Mayhem: Victory', player)])

    set_rule(world.get_location('Endless Knight: Victory', player),
             lambda state: state._wargroove_has_item(player, 'Eastern Bridges') and (
                           state._wargroove_has_item(player, 'Spearman') or
                           state._wargroove_has_item(player, 'Harpy') or
                           state._wargroove_has_item(player, 'Dragon')))
    set_region_exit_rules(world.get_region('Endless Knight', player),
                          [world.get_location('Endless Knight: Victory', player)])

    set_rule(world.get_location('Ambushed in the Middle: Victory (Blue)', player),
             lambda state: state._wargroove_has_item(player, 'Spearman'))
    set_rule(world.get_location('Ambushed in the Middle: Victory (Green)', player),
             lambda state: state._wargroove_has_item(player, 'Spearman'))
    set_region_exit_rules(world.get_region('Ambushed in the Middle', player),
                          [world.get_location('Ambushed in the Middle: Victory (Blue)', player),
                           world.get_location('Ambushed in the Middle: Victory (Green)', player)])

    # Levels 3CA-3CC
    set_rule(world.get_location('The Churning Sea: Victory', player),
             lambda state: (state._wargroove_has_item(player, 'Merfolk') or state._wargroove_has_item(player, 'Turtle'))
                           and state._wargroove_has_item(player, 'Harpoon Ship'))
    set_region_exit_rules(world.get_region('The Churning Sea', player),
                          [world.get_location('The Churning Sea: Victory', player)])

    set_rule(world.get_location('Frigid Archery: Light the Torch', player),
             lambda state: state._wargroove_has_item(player, 'Archer') and
                           state._wargroove_has_item(player, 'Southern Walls'))
    set_rule(world.get_location('Frigid Archery: Victory', player),
             lambda state: state._wargroove_has_item(player, 'Archer'))
    set_region_exit_rules(world.get_region('Frigid Archery', player),
                          [world.get_location('Frigid Archery: Victory', player)])

    set_rule(world.get_location('Archery Lessons: Chest', player),
             lambda state: state._wargroove_has_item(player, 'Knight') and
                           state._wargroove_has_item(player, 'Southern Walls'))
    set_rule(world.get_location('Archery Lessons: Victory', player),
             lambda state: state._wargroove_has_item(player, 'Knight') and
                           state._wargroove_has_item(player, 'Southern Walls'))
    set_region_exit_rules(world.get_region('Archery Lessons', player),
                          [world.get_location('Archery Lessons: Victory', player)])

    # Levels 4AA-4AC
    set_rule(world.get_location('Surrounded: Caesar', player),
             lambda state: state._wargroove_has_item_and_region(player, 'Knight', 'Surrounded'))
    set_rule(world.get_location('Surrounded: Victory', player),
             lambda state: state._wargroove_has_item_and_region(player, 'Knight', 'Surrounded'))
    set_rule(world.get_location('Darkest Knight: Victory', player),
             lambda state: state._wargroove_has_item_and_region(player, 'Spearman', 'Darkest Knight'))
    set_rule(world.get_location('Robbed: Victory', player),
             lambda state: state._wargroove_has_item_and_region(player, 'Thief', 'Robbed') and
                           state._wargroove_has_item(player, 'Rifleman'))

    # Levels 4BA-4BC
    set_rule(world.get_location('Open Season: Caesar', player),
             lambda state: state._wargroove_has_item_and_region(player, 'Mage', 'Open Season') and
                           state._wargroove_has_item(player, 'Knight'))
    set_rule(world.get_location('Open Season: Victory', player),
             lambda state: state._wargroove_has_item_and_region(player, 'Mage', 'Open Season') and
                           state._wargroove_has_item(player, 'Knight'))
    set_rule(world.get_location('Doggo Mountain: Find all the Dogs', player),
             lambda state: state._wargroove_has_item_and_region(player, 'Knight', 'Doggo Mountain'))
    set_rule(world.get_location('Doggo Mountain: Victory', player),
             lambda state: state._wargroove_has_item_and_region(player, 'Knight', 'Doggo Mountain'))
    set_rule(world.get_location('Tenri\'s Fall: Victory', player),
             lambda state: state._wargroove_has_item_and_region(player, 'Mage', 'Tenri\'s Fall') and
                           state._wargroove_has_item(player, 'Thief'))
    set_rule(world.get_location('Foolish Canal: Victory', player),
             lambda state: state._wargroove_has_item_and_region(player, 'Mage', 'Foolish Canal') and
                           state._wargroove_has_item(player, 'Spearman'))

    # Levels 4CA-4CC
    set_rule(world.get_location('Master of the Lake: Victory', player),
             lambda state: state._wargroove_has_item_and_region(player, 'Warship', 'Master of the Lake'))
    set_rule(world.get_location('A Ballista\'s Revenge: Victory', player),
             lambda state: state._wargroove_has_item_and_region(player, 'Ballista', 'A Ballista\'s Revenge'))
    set_rule(world.get_location('Rebel Village: Victory (Pink)', player),
             lambda state: state._wargroove_has_item_and_region(player, 'Spearman', 'Rebel Village'))
    set_rule(world.get_location('Rebel Village: Victory (Red)', player),
             lambda state: state._wargroove_has_item_and_region(player, 'Spearman', 'Rebel Village'))


def set_region_exit_rules(region: Region, locations: List[Location], operator: str = "or"):
    if operator == "or":
        exit_rule = lambda state: any(location.access_rule(state) for location in locations)
    else:
        exit_rule = lambda state: all(location.access_rule(state) for location in locations)
    for region_exit in region.exits:
        region_exit.access_rule = exit_rule
