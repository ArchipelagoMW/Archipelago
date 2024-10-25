# Credit to sg4e and the YuGiOh Forbidden Memories apworld for being the basis of this project

import typing
import warnings

from worlds.AutoWorld import World, WebWorld
from BaseClasses import CollectionState, Region, Tutorial, LocationProgressType
from worlds.generic.Rules import set_rule

from .client import YGODDMClient
from .utils import Constants
from .items import YGODDMItem, item_name_to_item_id, create_item as fabricate_item, create_victory_event
from .locations import YGODDMLocation, DuelistLocation, location_name_to_id as location_map
from .dice import Dice, all_dice
from .options import YGODDMOptions#, DuelistRematches
from .duelists import Duelist, all_duelists, map_duelists_to_ids
from .version import __version__

class YGODDMWeb(WebWorld):
    theme = "dirt"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        f"A guide to playing {Constants.GAME_NAME} with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Jumza"]
    )

    tutorials = [setup_en]

class YGODDMWorld(World):
    """Yu-Gi-Oh! Dungeon Dice Monsters is a Game Boy Advance dice-based tactics game based on an original board game
    featured in the Yu-Gi-Oh! storyline."""
    game: str = Constants.GAME_NAME
    options_dataclass = YGODDMOptions
    options: YGODDMOptions
    required_client_version = (0, 5, 0)
    web = YGODDMWeb()

    duelist_unlock_order: typing.List[Duelist]

    location_name_to_id = location_map
    item_name_to_id = item_name_to_item_id
    
    def get_available_duelists(self, state: CollectionState) -> typing.List[Duelist]:
        available_duelists: typing.List[Duelist] = [Duelist.YUGI_MOTO]
        for d in self.duelist_unlock_order:
            if (d is not Duelist.YUGI_MOTO):
                if state.has(d.name, self.player):
                    available_duelists.append(d)
        return available_duelists

    def generate_early(self) -> None:
        self.duelist_unlock_order = all_duelists

    def create_item(self, name: str) -> YGODDMItem:
        return fabricate_item(name, self.player)

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        # All duelists are accessible from Free Duel, so it is the only region
        free_duel_region = Region("Free Duel", self.player, self.multiworld)

        # Add duelist locations
        # Hold a reference to these to set locked items and victory event

        for duelist in self.duelist_unlock_order:
            if duelist is not Duelist.YAMI_YUGI:
                duelist_location: DuelistLocation = DuelistLocation(free_duel_region, self.player, duelist)
                set_rule(duelist_location, (lambda state, d=duelist_location:
                                            d.duelist in self.get_available_duelists(state)))
                free_duel_region.locations.append(duelist_location)
            
        
        self.multiworld.completion_condition[self.player] = lambda state: state.has(
            Constants.VICTORY_ITEM_NAME, self.player
        )

        itempool: typing.List[YGODDMItem] = []
        for duelist in self.duelist_unlock_order:
            if duelist is not Duelist.YUGI_MOTO and duelist is not Duelist.YAMI_YUGI:
                itempool.append(self.create_item(duelist.name))

        # Add random Dice items from the pool to fill in empty locations
        filler_slots: int = len(free_duel_region.locations) - len(itempool)
        reward_dice: typing.List[Dice] = [dice for dice in all_dice]
        while len(reward_dice) < filler_slots:
            reward_dice += reward_dice
        self.random.shuffle(reward_dice)

        itempool += [self.create_item(dice.name) for dice in reward_dice][:filler_slots]

        # Set Yami Yugi's item to game victory
        yami_yugi_location: DuelistLocation = DuelistLocation(free_duel_region, self.player, Duelist.YAMI_YUGI)
        yami_yugi_location.place_locked_item(create_victory_event(self.player))
        free_duel_region.locations.append(yami_yugi_location)
        

        self.multiworld.itempool.extend(itempool)

        menu_region.connect(free_duel_region)
        self.multiworld.regions.append(free_duel_region)
        self.multiworld.regions.append(menu_region)

    def fill_slot_data(self) -> typing.Dict[str, typing.Any]:
        return {
            Constants.GENERATED_WITH_KEY: __version__,
            Constants.DUELIST_UNLOCK_ORDER_KEY: map_duelists_to_ids(self.duelist_unlock_order),
            Constants.GAME_OPTIONS_KEY: self.options.serialize()
        }
