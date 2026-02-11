from dataclasses import dataclass
from typing import Any, Dict
from BaseClasses import CollectionState, Item, ItemClassification, Location, MultiWorld, Region, Tutorial
from Options import OptionSet, PerGameCommonOptions, Range, StartInventoryPool, Toggle, Choice, OptionDict
import worlds
from worlds import AutoWorld
from worlds.AutoWorld import WebWorld
from worlds.generic import GenericWorld
from worlds.LauncherComponents import Component, components, icon_paths, launch_subprocess, Type
from NetUtils import Hint, SlotType
from settings import Group

def launch_client(*args):
    from .Client import launch
    from CommonClient import gui_enabled
    if not gui_enabled:
        print(args)
        launch(args)
    launch_subprocess(launch, name="SlotLockClient", args=args)
components.append(Component("Slot Lock Client", "SlotLockClient", func=launch_client,
                            component_type=Type.CLIENT, supports_uri=True, game_name="SlotLock"))

class LockItem(Item):
    coin_suffix = ""
    def __init__(self, world: "SlotLockWorld", player: int):
        Item.__init__(self,f"Unlock {world.multiworld.worlds[player].player_name}",ItemClassification.progression,player+1001,world.player)
class LockLocation(Location):
    pass

class SlotsToLock(OptionSet):
    """A list of slot player names to add a lock item to"""
    pass
class NumberOfUnlocks(Range):
    """Number of copies of each unlock item to include."""
    default = 1
    range_start = 1
    range_end = 10
class UnlockItemFiller(Range):
    """Number of additional locations for the world unlock slots. This amount is capped to 10, and automatically includes any copies of the bonus item key plus the additional locations here. The additional locations each add a Nothing item to the pool."""
    default = 0
    range_start = 0
    range_end = 9
class SlotsToLockWhitelistOption(Toggle):
    """If the list of slots to lock should be treated as a blacklist rather than a whitelist. If true, will lock every slot listed. If false, will lock every slot except this one and any slot listed."""
    default = 1
    pass
class FreeSlotItems(Toggle):
    """If true, the free items should be sent out immediately for locked worlds, or if false the 'Unlock {slot_name}' item will be required. If false, it will require other worlds to be open in sphere 1 instead else there will be no worlds available."""
    default = 1
    pass
class FreeUnlockedWorldItems(Range):
    """Adds filler and locations equal to this number, per starting slot of the world."""
    default = 0
    range_start = 0
    range_end = 10
class BonusItemSlots(Range):
    """Number of bonus item slots to include. These will be automatically unlocked when sent their individual keys."""
    default = 0
    range_start = 0
    range_end = 1000
class BonusItemDupes(Range):
    """Number of copies of bonus slot unlocks."""
    default = 1
    range_start = 1
    range_end = 10
class BonusItemFiller(Range):
    """Number of additional locations for the bonus item slots. This amount is capped to 10, and automatically includes any copies of the bonus item key plus the additional locations here."""
    default = 0
    range_start = 0
    range_end = 9
class RandomUnlockedSlots(Range):
    """Number of slots to randomly start with, from the slots that are locked."""
    default = 0
    range_start = 0
    range_end = 100
class AutoHintLockedItems(Toggle):
    """Whether the slotlock client should automatically scout locations in other worlds where its items are if one of its items are hinted."""
    default = 0
    option_no = 0
    option_yes = 1
    alias_true = 1
    alias_false = 0
class AssociatedWorlds(OptionDict):
    """Allows you to associate a list of worlds with another world. These worlds slot unlocks will then be unlocked at the same time as the primary world. Format `WorldName: [AssociatedWorld1,AssociatedWorld2]`. The maximum number of associated worlds per world is 10, and will cause the associated world to only have 1 copy of its world."""
    pass

@dataclass
class SlotLockOptions(PerGameCommonOptions):
    slots_to_lock: SlotsToLock
    slots_whitelist: SlotsToLockWhitelistOption
    unlock_item_copies: NumberOfUnlocks
    unlock_item_filler: UnlockItemFiller
    bonus_item_slots: BonusItemSlots
    bonus_item_copies: BonusItemDupes
    bonus_item_filler: BonusItemFiller
    free_starting_items: FreeSlotItems
    free_unlocked_world_items: FreeUnlockedWorldItems
    random_unlocked_slots: RandomUnlockedSlots
    auto_hint_locked_items: AutoHintLockedItems
    associated_worlds: AssociatedWorlds

class SlotLockWebWorld(WebWorld):
    theme = "partyTime"

    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing SlotLock.",
        language="English",
        file_name="setup_en.md",
        link="setup/en",
        authors=[""]
    )

    tutorials = [setup_en]

class SlotLockWorld(AutoWorld.World):
    """Locks other player slots."""

    game = "SlotLock"
    web = SlotLockWebWorld()
    options: SlotLockOptions
    options_dataclass = SlotLockOptions
    location_name_to_id = {f"Lock_{num+1}": num+10010 for num in range(50000)}
    item_name_to_id = {f"Unlock_{num+1}": num+1001 for num in range(5000)}
    item_name_to_id["Nothing"] = 6999
    multiworld : MultiWorld
    for i in range(1000):
        item_name_to_id[f"Unlock Bonus Slot {i+1}"] = i + 1
        for j in range(10):
            location_name_to_id[f"Bonus Slot {i+1}{" " + str(j+1) if j > 0 else ""}"] = i*10 + j + 10
    item_name_groups = {"Slot Unlocks": set(f"Unlock_{num+1}" for num in range(5000)), "Bonus Slot Unlocks": set(f"Unlock Bonus Slot {num+1}" for num in range(1000))}
    location_name_groups = {"Slot Rewards": set(f"Lock_{num+1}" for num in range(50000)), "Bonus Slot Rewards": set([f"Bonus Slot {(num+10)//10}{" " + str((num % 10)+1) if (num % 10) > 0 else ""}" for num in range(1000)])}
    slots_to_lock = []
    recursive_locks = []
    associated_worlds = set()
    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
    def create_item(self, name: str):
        if "Unlock_" in name:
            return self.create_slotlock_item(self.multiworld.player_name[int(name.split("_")[1])])
        elif "Unlock Bonus Slot" in name:
            return self.create_bonus_key(int(name.split("Slot ")[1]))
        elif "Unlock " in name:
            return self.create_slotlock_item(name.split("lock ")[1])
        elif name == "Nothing":
            return Item(name,ItemClassification.filler,6999, self.player)
        raise Exception("Invalid item name")
    @classmethod
    def stage_generate_early(cls, multiworld: "MultiWorld"):
        item_name_to_id = {}
        location_name_to_id = {}
        world_unlock_items = set()
        world_unlock_locations = set()
        bonus_locations = set()
        bonus_items = set()
        for id, world in multiworld.worlds.items():
            if multiworld.player_types[id] == SlotType.player:
                item_name_to_id[f"Unlock {world.player_name}"] = id + 1001
                world_unlock_items.add(f"Unlock {world.player_name}")
                for i in range(10):
                    location_name_to_id[f"Free Item {world.player_name} {i+1}"] = id*10 + i + 10010
                    world_unlock_locations.add(f"Free Item {world.player_name} {i+1}")
        item_name_to_id["Nothing"] = 6999
        for i in range(1000):
            item_name_to_id[f"Unlock Bonus Slot {i+1}"] = i + 1
            bonus_items.add(f"Unlock Bonus Slot {i+1}")
            for j in range(10):
                location_name_to_id[f"Bonus Slot {i+1}{" " + str(j+1) if j > 0 else ""}"] = i*10 + j + 10
                bonus_locations.add(f"Bonus Slot {i+1}{" " + str(j+1) if j > 0 else ""}")
        cls.item_name_to_id = item_name_to_id
        cls.location_name_to_id = location_name_to_id
        cls.item_name_groups = {"Everything": set(world_unlock_items.union(bonus_items).union(set("Nothing"))), "Slot Unlocks": world_unlock_items, "Bonus Slot Unlocks": bonus_items}
        cls.location_name_groups = {"Everywhere": set(world_unlock_locations.union(bonus_locations)), "Slot Rewards": world_unlock_locations, "Bonus Slot Rewards": bonus_locations}

        # update datapackage checksum
        worlds.network_data_package["games"][cls.game] = cls.get_data_package_data()
    def create_slotlock_item(self, slotName: str) -> LockItem:
        try:
            return LockItem(self,self.multiworld.world_name_lookup[slotName])
        except KeyError:
            return None
    def create_bonus_key(self, bonusSlot: int) -> Item:
        return Item(f"Unlock Bonus Slot {bonusSlot+1}", ItemClassification.progression,bonusSlot+1,self.player)
    def create_items(self) -> None:
        if hasattr(self.multiworld, "generation_is_fake"):
            # UT has no way to get the unlock items so just skip locking altogether
            return

        #print(self.location_name_to_id)
        if self.options.slots_whitelist.value:
            slots_to_lock = [slot for slot in self.options.slots_to_lock.value if any(slot == world.player_name for world in self.multiworld.worlds.values())]
        else:
            slots_to_lock = [slot.player_name for slot in self.multiworld.worlds.values() if slot.player_name not in self.options.slots_to_lock.value and slot.player_name != self.player_name]
        slots_to_lock = [slot for slot in slots_to_lock if slot in self.multiworld.world_name_lookup and self.multiworld.player_types[self.multiworld.world_name_lookup[slot]] == SlotType.player]
        if self.options.random_unlocked_slots.value > len(slots_to_lock):
            raise RuntimeError("Too many random unlocked slots.")
        for i in range(self.options.random_unlocked_slots.value):
            slots_to_lock.remove(self.random.choice(slots_to_lock))
        print(f"{self.player_name}: Locking {slots_to_lock}")
        self.slots_to_lock = slots_to_lock
        for world in self.options.associated_worlds:
            for associated_world in self.options.associated_worlds[world]:
                if world in slots_to_lock and associated_world in slots_to_lock:
                    self.associated_worlds.add(associated_world)
        #(creating regions in create_items to run always after create_regions for everything else.)
        self.region = Region("Menu",self.player,self.multiworld)
        def add_slot_item_to_option(option, world):
            slot = world.player_name
            if isinstance(option.value,dict) and (f"Unlock_{world.player}" in option.value.keys()):
                option.value[f"Unlock {slot}"] = option.value[f"Unlock_{world.player}"]
                del option.value[f"Unlock_{world.player}"]
            elif (isinstance(option.value,list) or isinstance(option.value,set)) and (f"Unlock_{world.player}" in option.value):
                option.value.add(f"Unlock {slot}")
                option.value.remove(f"Unlock_{world.player}")
        def remove_slot_item_from_option(option, world):
            if isinstance(option.value,dict) and (f"Unlock_{world}" in option.value.keys()):
                del option.value[f"Unlock_{world}"]
            elif (isinstance(option.value,list) or isinstance(option.value,set)) and (f"Unlock_{world}" in option.value):
                option.value.remove(f"Unlock_{world}")
        def add_slot_location_to_option(option, world):
            slot = world.player_name
            for i in range(10):
                if isinstance(option.value,dict) and (f"Lock_{world.player*10 + i}" in option.value.keys()):
                    option.value[f"Free Item {slot} {i+1}"] = option.value[f"Lock_{world.player*10 + i}"]
                    del option.value[f"Lock_{world.player*10 + i}"]
                elif (isinstance(option.value,list) or isinstance(option.value, set)) and (f"Lock_{world.player*10 + i}" in option.value):
                    option.value.add(f"Free Item {slot} {i+1}")
                    option.value.remove(f"Lock_{world.player*10 + i}")
        def remove_slot_location_from_option(option, world):
            for i in range(10):
                if isinstance(option.value,dict) and (f"Lock_{world*10 + i}" in option.value.keys()):
                    del option.value[f"Lock_{world*10 + i}"]
                elif (isinstance(option.value,list) or isinstance(option.value, set)) and (f"Lock_{world*10 + i}" in option.value):
                    option.value.remove(f"Lock_{world*10 + i}")
        for world in self.multiworld.worlds.values():
            if world.player_name in slots_to_lock:
                if isinstance(world, SlotLockWorld) and len(world.slots_to_lock) > 0:
                    raise Exception(f"Recursive slot lock: {self.player_name} locking {world.player_name} which locks other worlds, this is not allowed.")
                for i in range(min(10, self.options.unlock_item_copies.value + self.options.unlock_item_filler.value)):
                    self.region.add_locations({f"Free Item {world.player_name} {i+1}": self.location_name_to_id[f"Free Item {world.player_name} {i+1}"]}, LockLocation)
                    if i < self.options.unlock_item_copies.value and world.player_name not in self.associated_worlds:
                        self.multiworld.itempool.append(self.create_slotlock_item(world.player_name))
                    else:
                        self.multiworld.itempool.append(self.create_item("Nothing"))
                fixedLocations = []
                if world.player_name in self.options.associated_worlds.keys():
                    for associated_world in self.options.associated_worlds[world.player_name]:
                        if associated_world in self.associated_worlds:
                            location: Location = self.region.get_locations().pop()
                            location.place_locked_item(self.create_slotlock_item(associated_world))
                            index = -1
                            while self.multiworld.itempool[index].name != "Nothing":
                                index -= 1
                            self.multiworld.itempool.pop(index)
                            fixedLocations.append(location)
                        else:
                            print(f"{self.player_name} Warning: associated world {associated_world} not real world.")
                self.region.get_locations().extend(fixedLocations)

            else:
                try:
                    self.multiworld.push_precollected(self.create_slotlock_item(world.player_name))
                    for i in range(min(10, self.options.free_unlocked_world_items.value)):
                        self.multiworld.itempool.append(self.create_item("Nothing"))
                        self.region.add_locations({f"Free Item {world.player_name} {i+1}": self.location_name_to_id[f"Free Item {world.player_name} {i+1}"]}, LockLocation)
                except AttributeError:
                    pass
            if self.multiworld.player_types[world.player] == SlotType.player:
                add_slot_location_to_option(self.options.exclude_locations, world)
                add_slot_location_to_option(self.options.priority_locations, world)
                add_slot_location_to_option(self.options.start_location_hints, world)
                add_slot_item_to_option(self.options.local_items, world)
                add_slot_item_to_option(self.options.non_local_items, world)
                add_slot_item_to_option(self.options.start_hints, world)
                add_slot_item_to_option(self.options.start_inventory, world)
        for world in range(5001):
            remove_slot_location_from_option(self.options.exclude_locations, world)
            remove_slot_location_from_option(self.options.priority_locations, world)
            remove_slot_location_from_option(self.options.start_location_hints, world)
            remove_slot_item_from_option(self.options.local_items, world)
            remove_slot_item_from_option(self.options.non_local_items, world)
            remove_slot_item_from_option(self.options.start_hints, world)
            remove_slot_item_from_option(self.options.start_inventory, world)
        self.multiworld.regions.append(self.region)
        for bonusSlot in range(self.options.bonus_item_slots.value):
            bonusSlotRegion = Region(f"Bonus Slot {bonusSlot+1}", self.player, self.multiworld)
            for bonusDupes in range(min(self.options.bonus_item_copies.value + self.options.bonus_item_filler.value, 10)):
                if bonusDupes < self.options.bonus_item_copies.value:
                    self.multiworld.itempool.append(self.create_bonus_key(bonusSlot))
                else:
                    self.multiworld.itempool.append(self.create_item("Nothing"))
                locName = f"Bonus Slot {bonusSlot+1}{" " + str(bonusDupes+1) if bonusDupes > 0 else ""}"
                bonusSlotRegion.add_locations({locName: self.location_name_to_id[locName]})
            self.multiworld.regions.append(bonusSlotRegion)
            def rule(state: CollectionState, bonusSlot=bonusSlot):
                return state.has(f"Unlock Bonus Slot {bonusSlot+1}", self.player)
            self.region.connect(bonusSlotRegion,None, rule)

    def create_regions(self) -> None:
        pass
    def get_filler_item_name(self) -> str:
        return "Nothing"
    @classmethod
    def stage_pre_fill(cls, multiworld):
        for self in multiworld.get_game_worlds(cls.game): #workaround this being a classmethod lol
            for world in multiworld.worlds.values():
                if world.player_name in self.slots_to_lock:
                    currentOriginName = world.origin_region_name
                    currentOrigin: Region
                    currentOrigin = world.get_region(currentOriginName)
                    #region = Region(f"Lock {self.player}", world.player, self.multiworld)
                    #region.connect(currentOrigin,None,rule)
                    #self.multiworld.regions.append(region)
                    for exit in currentOrigin.get_exits():
                        old_rule = exit.access_rule
                        def rule(state: CollectionState, self=self, world=world, old_rule=old_rule):
                            #print(f"Lock Rule Called for {world.player}, value {state.has(f"Unlock_{world.player}",self.player)}")
                            return state.has(f"Unlock {world.player_name}",self.player) and old_rule(state)
                        exit.access_rule = rule
                    for location in currentOrigin.get_locations():
                        old_rule = location.access_rule
                        def rule(state: CollectionState, self=self, world=world, old_rule=old_rule):
                            #print(f"Lock Rule Called for {world.player}, value {state.has(f"Unlock_{world.player}",self.player)}")
                            return state.has(f"Unlock {world.player_name}",self.player) and old_rule(state)
                        location.access_rule = rule
                    multiworld.early_items[world.player] = {}
                    multiworld.local_early_items[world.player] = {}
                    world.options.progression_balancing.value = 0

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has_all([f"Unlock {i}" for i in self.slots_to_lock] + [f"Unlock Bonus Slot {i+1}" for i in range(self.options.bonus_item_slots.value)], self.player)
        if not self.options.free_starting_items.value:
            for slot in self.slots_to_lock:
                for i in range(min(self.options.unlock_item_copies+self.options.unlock_item_filler,10)):
                    def rule(state: CollectionState, slot=slot):
                        return state.has(f"Unlock {slot}", self.player)
                    self.get_location(f"Free Item {slot} {i+1}").access_rule = rule
    def fill_slot_data(self):
        item_locations : Dict[str, list[tuple[int, int]]] = {}
        for item in self.multiworld.get_items():
            if item.player == self.player:
                item_locations[item.name] = list(map(lambda loc: (loc.player, loc.address),self.multiworld.find_item_locations(item.name, self.player, True)))
        return {
            "free_starting_items": self.options.free_starting_items.value,
            "auto_hint_locked_items": self.options.auto_hint_locked_items.value,
            "locked_slots": self.slots_to_lock,
            "unlock_item_copies": self.options.unlock_item_copies.value,
            "unlock_item_filler": min(10- self.options.unlock_item_copies.value, self.options.unlock_item_filler.value),
            "bonus_item_copies": self.options.bonus_item_copies.value,
            "bonus_item_filler": min(10- self.options.bonus_item_copies.value, self.options.bonus_item_filler.value),
            "bonus_item_slots": self.options.bonus_item_slots.value,
            "item_locations": item_locations
        }
    def post_fill(self) -> None:
        pass
    def collect(self,state: CollectionState, item: Item):
        res = super().collect(state,item)
        if res and "Unlock " in item.name and item.name.split("Unlock ")[1] in self.slots_to_lock:
            player_name = item.name.split("Unlock ")[1]
            for world in self.multiworld.worlds:
                if self.multiworld.worlds[world].player_name == player_name:
                    state.update_reachable_regions(world)
                    # print(f"Marking {player_name} as stale due to collection of {item.name}")
        return res
    def remove(self,state: CollectionState, item: Item):
        res = super().remove(state,item)
        if res and "Unlock " in item.name and item.name.split("Unlock ")[1] in self.slots_to_lock:
            player_name = item.name.split("Unlock ")[1]
            for world in self.multiworld.worlds:
                if world.player_name == player_name:
                    state.update_reachable_regions(world)
                    # print(f"Marking {player_name} as stale due to removal of {item.name}")
        return res
    def modify_multidata(self, multidata: Dict[str, Any]):
        if len(self.slots_to_lock) == 0:
            return
        def hintfn(hint: Hint) -> Hint:
            if hasattr(hint, "status") and self.multiworld.player_name[hint.receiving_player] in self.slots_to_lock:
                from NetUtils import HintStatus
                hint = hint.re_prioritize(None, HintStatus.HINT_UNSPECIFIED)
            return hint
        for player in self.multiworld.player_ids:
            multidata["precollected_hints"][player] = set(map(hintfn, multidata["precollected_hints"][player]))

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        """
        Fill in additional entrance information text into locations, which is displayed when hinted.
        structure is {player_id: {location_id: text}} You will need to insert your own player_id.
        """
        data = {}
        if self.options.auto_hint_locked_items.value > 0:
            for location in self.get_locations():
                data[location.address] = str(self.multiworld.find_item_locations(self.item_id_to_name[location.address // 10],self.player, True)).removeprefix("[").removesuffix("]")
        hint_data[self.player] = data

