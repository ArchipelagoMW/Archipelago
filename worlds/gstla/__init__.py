from __future__ import annotations

from Options import PerGameCommonOptions
from worlds.AutoWorld import WebWorld, World
import os

from typing import List, TextIO, BinaryIO, Dict, ClassVar, Type, cast

from .Options import GSTLAOptions, RandoOptions
from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification,\
    LocationProgressType, Region, Entrance
from .Items import GSTLAItem, item_table, all_items, ItemType, create_events, create_items, create_item, \
    AP_PLACEHOLDER_ITEM, items_by_id
from .Locations import GSTLALocation, all_locations, location_name_to_id, location_type_to_data
from .Rules import set_access_rules, set_item_rules, set_entrance_rules
from .Regions import create_regions
from .Connections import create_connections
from .gen.LocationData import LocationType, location_name_to_data
from .gen.ItemNames import ItemName, item_id_by_name
from .gen.LocationNames import LocationName, ids_by_loc_name, loc_names_by_id
from .Names.RegionName import RegionName
from .Rom import get_base_rom_path, get_base_rom_bytes, LocalRom, GSTLADeltaPatch
from .BizClient import GSTLAClient

import logging

class GSTLAWeb(WebWorld):
    theme = "jungle"

class GSTLAWorld(World):
    game = "Golden Sun The Lost Age"
    options_dataclass: ClassVar[Type[PerGameCommonOptions]] = GSTLAOptions
    options: GSTLAOptions
    data_version = 1
    items_ids_populated = set()
    location_flags_populated = set()

    item_name_to_id = item_id_by_name#{item.itemName: itemfor item in all_items if item.type != ItemType.Event}
    location_name_to_id = ids_by_loc_name#{location: location_name_to_id[location].id for location in location_name_to_id}
    web = GSTLAWeb()

    item_name_groups = {
        ItemType.Djinn.name: {item.name for item in all_items if item.type == ItemType.Djinn},
        ItemType.Character.name: {item.name for item in all_items if item.type == ItemType.Character}
    }

    def generate_early(self) -> None:
        self.options.non_local_items.value -= self.item_name_groups[ItemType.Djinn.name]

        if self.options.character_shuffle > 0:
            self.options.non_local_items.value -= self.item_name_groups[ItemType.Character.name]

        if self.options.starter_ship == 2:
            self.options.start_inventory.value[ ItemName.Ship ] = 1

        #force unsupported options to off
        self.options.gs1_items = 0

    def create_regions(self) -> None:
        create_regions(self)
        create_connections(self.multiworld, self.player)

    def create_items(self) -> None:
        create_events(self)
        create_items(self, self.player)

    def set_rules(self) -> None:
        set_entrance_rules(self)
        set_item_rules(self)
        set_access_rules(self)

        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has(ItemName.Victory, self.player)

    def generate_basic(self):
        pass

    def pre_fill(self) -> None:
        pass

    def generate_output(self, output_directory: str):
        self._generate_rando_file(output_directory)
        rom = LocalRom(get_base_rom_path())
        world = self.multiworld
        player = self.player

        rom.write_story_flags()
        rom.apply_qol_patches()

        for region in self.multiworld.get_regions(self.player):
            for location in region.locations:
                location_data = location_name_to_id.get(location.name, None)

                if location_data is None or location_data.loc_type == LocationType.Event or location_data.loc_type == LocationType.Character:
                    continue
                ap_item = location.item
                # print(ap_item)
                if ap_item is None:
                    # TODO: need to fill with something else
                    continue

                if ap_item.player != self.player:
                    item_data = AP_PLACEHOLDER_ITEM
                else:
                    item_data = item_table[ap_item.name]

                if item_data.type == ItemType.Djinn:
                    rom.write_djinn(location_data, item_data)
                else:
                    rom.write_item(location_data, item_data)

        rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.gba")

        try:
            rom.write_to_file(rompath)
            patch = GSTLADeltaPatch(os.path.splitext(rompath)[0]+GSTLADeltaPatch.patch_file_ending, player=player,
                        player_name=world.player_name[player], patched_path=rompath)

            patch.write()
        except:
            raise()
        finally:
            if os.path.exists(rompath):
                os.unlink(rompath)

    def _generate_rando_data(self, rando_file: BinaryIO, debug_file: TextIO):
        rando_file.write(0x1.to_bytes(length=1, byteorder='little'))
        debug_file.write("Version: 1\n")

        rando_file.write(self.multiworld.seed.to_bytes(length=16, byteorder='little'))
        debug_file.write(f"Seed: {self.multiworld.seed}\n")

        self._write_options_for_rando(rando_file, debug_file)

        # rando_file.write((0).to_bytes(length=16, byteorder='little'))
        # debug_file.write("no settings (TBD)\n")

        rando_file.write(f"{self.player_name}\n".encode('ascii'))
        debug_file.write(f"Slot Name {self.player_name.encode('ascii')}\n")

        # locations = [x for x in all_locations if x.loc_type not in {LocationType.Event, LocationType.Djinn}]

        djinn_locs: List[GSTLALocation] = []
        index = 0
        for region in self.multiworld.get_regions(self.player):
            for location in region.locations:
                location_data = location_name_to_id.get(location.name, None)

                if location_data is None or location_data.loc_type == LocationType.Event:
                    continue
                ap_item = location.item
                # print(ap_item)
                if ap_item is None:
                    # TODO: need to fill with something else
                    continue

                if ap_item.player != self.player:
                    item_data = AP_PLACEHOLDER_ITEM
                else:
                    item_data = item_table[ap_item.name]

                if item_data.type == ItemType.Djinn:
                    djinn_locs.append(location)
                else:
                    # rom.write_item(location_data, item_data)
                    # TODO: cleanup
                    item_id = 0xA00 if item_data.id == 412 else item_data.id
                    rando_file.write(location_data.rando_flag.to_bytes(length=2, byteorder='little'))
                    rando_file.write(item_id.to_bytes(length=2, byteorder='little'))
                    debug_file.write(
                        f"{index} \n\tLocation: {location.name.value} \n\tLocation Flag: {hex(location_data.rando_flag)} \n\tItem: {location.item.name} \n\tItem ID: {item_id}\n\n")
                index += 1
                # debug_file.write()
                # TODO: Questions
                # Rando flags for summon tablets
                # Rando flags for psyenergy items
                # Rando flags for characters
                # Rando flags for djinn

        rando_file.write(0xFFFFFFFF.to_bytes(length=4, byteorder='little'))
        debug_file.write("0xFFFFFFFF\n")

        for loc in djinn_locs:
            item_data = item_table[loc.item.name]
            location_data = location_name_to_id[loc.name]
            rando_file.write(location_data.rando_flag.to_bytes(length=2, byteorder='little'))
            rando_file.write(item_data.get_rando_flag().to_bytes(length=2, byteorder='little'))
            loc_name = loc_names_by_id[location_data.ap_id]
            debug_file.write(
                f"Djinn(Location): {loc_name}\nDjinn(Location) Flag: {hex(location_data.rando_flag)}\nDjinn(Item): {item_data.name}\nDjinn(Item) Flag: {hex(item_data.get_rando_flag())}\n\n")

    def _generate_rando_file(self, output_directory: str):
        with open(os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}_debug.txt"),'w') as debug_file:
            with open(os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.gstlarando"),'wb') as rando_file:
                self._generate_rando_data(rando_file, debug_file)


    #TODO: gs1_items we do shuffle, dummy-items we dont shuffle, adv-equip we dont shuffle
    def _write_options_for_rando(self, rando_file: BinaryIO, debug_file: TextIO):
        #First byte of base rando settings
        write_me = 0
        write_me += self.options.item_shuffle << 6
        debug_file.write('Item Shuffle: ' + self.options.item_shuffle.name_lookup[self.options.item_shuffle] + '\n')
        write_me += self.options.omit_locations << 4
        debug_file.write('Omit Locations: ' + self.options.omit_locations.name_lookup[self.options.omit_locations] + '\n')
        write_me += self.options.gs1_items << 3
        debug_file.write('GS1 Items: ' + self.options.gs1_items.name_lookup[self.options.gs1_items] + '\n')
        write_me += self.options.visible_items << 2
        debug_file.write('Visible Items: ' + self.options.visible_items.name_lookup[self.options.visible_items] + '\n')
        write_me += self.options.no_learning_util << 1
        debug_file.write('No Learning Util: ' + self.options.no_learning_util.name_lookup[self.options.no_learning_util] + '\n')
        write_me += self.options.shuffle_class_stats
        debug_file.write('Class Stats Shuffle: ' + self.options.shuffle_class_stats.name_lookup[self.options.shuffle_class_stats] + '\n')
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))

        write_me = 0

        if False:
            write_me |= RandoOptions.EquipShuffle.bit_flag
            debug_file.write(RandoOptions.EquipShuffle.name + '\n')
        if False:
            write_me |= RandoOptions.EquipCost.bit_flag
            debug_file.write(RandoOptions.EquipCost.name + '\n')
        if False:
            write_me |= RandoOptions.EquipStats.bit_flag
            debug_file.write(RandoOptions.EquipStats.name + '\n')
        if False:
            write_me |= RandoOptions.EquipSort.bit_flag
            debug_file.write(RandoOptions.EquipSort.name + '\n')
        if False:
            write_me |= RandoOptions.EquipUnleash.bit_flag
            debug_file.write(RandoOptions.EquipUnleash.name + '\n')
        if False:
            write_me |= RandoOptions.EquipEffect.bit_flag
            debug_file.write(RandoOptions.EquipEffect.name + '\n')
        if False:
            write_me |= RandoOptions.EquipCurse.bit_flag
            debug_file.write(RandoOptions.EquipCurse.name + '\n')
        if False:
            write_me |= RandoOptions.PsyEnergyPower.bit_flag
            debug_file.write(RandoOptions.PsyEnergyPower.name + '\n')

        # Equip not a thing
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))
        write_me = 0

        if True:
            write_me |= RandoOptions.DjinnShuffle.bit_flag
            debug_file.write(RandoOptions.DjinnShuffle.name + '\n')
        if False:
            write_me |= RandoOptions.DjinnStats.bit_flag
            debug_file.write(RandoOptions.DjinnStats.name + '\n')
        if False:
            write_me |= RandoOptions.DjinnPower.bit_flag
            debug_file.write(RandoOptions.DjinnPower.name + '\n')
        if False:
            write_me |= RandoOptions.DjinnAoe.bit_flag
            debug_file.write(RandoOptions.DjinnAoe.name + '\n')
        if False:
            write_me |= RandoOptions.DjinnScale.bit_flag
            debug_file.write(RandoOptions.DjinnScale.name + '\n')
        if False:
            write_me |= RandoOptions.SummonCost.bit_flag
            debug_file.write(RandoOptions.SummonCost.name + '\n')
        if False:
            write_me |= RandoOptions.SummonPower.bit_flag
            debug_file.write(RandoOptions.SummonPower.name + '\n')
        if False:
            write_me |= RandoOptions.SummonSort.bit_flag
            debug_file.write(RandoOptions.SummonSort.name + '\n')


        # Djinn/Summon
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))
        write_me = 0

        if False:
            write_me |= RandoOptions.CharStatsAdj.bit_flag
            debug_file.write(RandoOptions.CharStatsAdj.name + '\n')
        else:
            write_me |= RandoOptions.CharStatsShuf.bit_flag
            debug_file.write(RandoOptions.CharStatsShuf.name + '\n')
        if False:
            write_me |= RandoOptions.CharEleAdj.bit_flag
            debug_file.write(RandoOptions.CharEleAdj.name + '\n')
        else:
            write_me |= RandoOptions.CharEletShuf.bit_flag
            debug_file.write(RandoOptions.CharEletShuf.name + '\n')
        if False:
            write_me |= RandoOptions.PsyEnergyCost.bit_flag
            debug_file.write(RandoOptions.PsyEnergyCost.name + '\n')
        if False:
            write_me |= RandoOptions.PsyEnergyAoe.bit_flag
            debug_file.write(RandoOptions.PsyEnergyAoe.name + '\n')
        if False:
            write_me |= RandoOptions.EnemyPsyPow.bit_flag
            debug_file.write(RandoOptions.EnemyPsyPow.name + '\n')
        if False:
            write_me |= RandoOptions.EnemyPsyAoe.bit_flag
            debug_file.write(RandoOptions.EnemyPsyAoe.name + '\n')

        # Char Stat/Enemy Psy Shuffle
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))
        write_me = 0

        if False:
            write_me |= RandoOptions.ShuffPsyGrp.bit_flag
            debug_file.write(RandoOptions.ShuffPsyGrp.name + '\n')
        elif False:
            write_me |= RandoOptions.ShuffPsy.bit_flag
            debug_file.write(RandoOptions.ShuffPsy.name + '\n')
        elif False:
            write_me |= RandoOptions.ClassPsyEle.bit_flag
            debug_file.write(RandoOptions.ClassPsyEle.name + '\n')
        elif False:
            write_me |= RandoOptions.ClassPsyGrp.bit_flag
            debug_file.write(RandoOptions.ClassPsyGrp.name + '\n')
        else:
            write_me |= RandoOptions.ClassPsyShuf.bit_flag
            debug_file.write(RandoOptions.ClassPsyShuf.name + '\n')
        if False:
            write_me |= RandoOptions.ClassLevelsRand.bit_flag
            debug_file.write(RandoOptions.ClassLevelsRand.name + '\n')
        else:
            write_me |= RandoOptions.ClassLevelsShuf.bit_flag
            debug_file.write(RandoOptions.ClassLevelsShuf.name + '\n')
        if False:
            write_me |= RandoOptions.QolCutscenes.bit_flag
            debug_file.write(RandoOptions.QolCutscenes.name + '\n')
        if False:
            write_me |= RandoOptions.QolTickets.bit_flag
            debug_file.write(RandoOptions.QolTickets.name + '\n')
        if False:
            write_me |= RandoOptions.QolFastShip.bit_flag
            debug_file.write(RandoOptions.QolFastShip.name + '\n')

        # Psy/Qol
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))
        write_me = 0

        #Ship/Skips
        ship = self.options.starter_ship
        if ship == 2:
            write_me |= RandoOptions.ShipFromStart.bit_flag
            debug_file.write(RandoOptions.ShipFromStart.name + '\n')
        elif ship == 1:
            write_me |= RandoOptions.ShipUnlock.bit_flag
            debug_file.write(RandoOptions.ShipUnlock.name + '\n')

        if False:
            write_me |= RandoOptions.SkipsBasic.bit_flag
            debug_file.write(RandoOptions.SkipsBasic.name + '\n')
        if False:
            write_me |= RandoOptions.SkipsOOBEasy.bit_flag
            debug_file.write(RandoOptions.SkipsOOBEasy.name + '\n')
        if False:
            write_me |= RandoOptions.SkipsMaze.bit_flag
            debug_file.write(RandoOptions.SkipsMaze.name + '\n')
        if False:
            write_me |= RandoOptions.BossLogic.bit_flag
            debug_file.write(RandoOptions.BossLogic.name + '\n')
        if True:
            write_me |= RandoOptions.FreeAvoid.bit_flag
            debug_file.write(RandoOptions.FreeAvoid.name + '\n')
        if True:
            write_me |= RandoOptions.FreeRetreat.bit_flag
            debug_file.write(RandoOptions.FreeRetreat.name + '\n')

        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))
        write_me = 0

        if False:
            write_me |= RandoOptions.AdvEquip.bit_flag
            debug_file.write(RandoOptions.AdvEquip.name + '\n')
        if False:
            write_me |= RandoOptions.DummyItems.bit_flag
            debug_file.write(RandoOptions.DummyItems.name + '\n')
        if False:
            write_me |= RandoOptions.SkipsOOBHard.bit_flag
            debug_file.write(RandoOptions.SkipsOOBHard.name + '\n')
        if False:
            write_me |= RandoOptions.EquipAttack.bit_flag
            debug_file.write(RandoOptions.EquipAttack.name + '\n')
        if False:
            write_me |= RandoOptions.QoLHints.bit_flag
            debug_file.write(RandoOptions.QoLHints.name + '\n')
        if False:
            write_me |= RandoOptions.StartHeal.bit_flag
            debug_file.write(RandoOptions.StartHeal.name + '\n')
        if False:
            write_me |= RandoOptions.StartRevive.bit_flag
            debug_file.write(RandoOptions.StartRevive.name + '\n')
        if False:
            write_me |= RandoOptions.StartReveal.bit_flag
            debug_file.write(RandoOptions.StartReveal.name + '\n')

        # More QoL
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))
        write_me = 0

        # Scale Exp/Coins      
        if True:
            write_me |= 0b00010000
            debug_file.write(RandoOptions.ScaleExp.name + '\n')
        if True:
            write_me |= 0b00000001
            debug_file.write(RandoOptions.ScaleCoins.name + '\n')

        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))
        write_me = 0

        if False:
            write_me |= RandoOptions.EquipDefense.bit_flag
            debug_file.write(RandoOptions.EquipDefense.name + '\n')
            
        if True:
            write_me |= 0b00000101
            debug_file.write(RandoOptions.StartLevels.name + '\n')

        # Equip Defense/start levels
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))
        write_me = 0

        if False:
            write_me |= RandoOptions.EnemyeResRand.bit_flag
            debug_file.write(RandoOptions.EnemyeResRand.name + '\n')
        elif False:
            write_me |= RandoOptions.EnemyeResShuf.bit_flag
            debug_file.write(RandoOptions.EnemyeResShuf.name + '\n')
        
        if False:
            write_me |= RandoOptions.SancRevFixed.bit_flag
            debug_file.write(RandoOptions.SancRevFixed.name + '\n')
        elif True:
            write_me |= RandoOptions.SancRevCheap.bit_flag
            debug_file.write(RandoOptions.SancRevCheap.name + '\n')

        if False:
            write_me |= RandoOptions.CurseDisable.bit_flag
            debug_file.write(RandoOptions.CurseDisable.name + '\n')
        if True:
            write_me |= RandoOptions.AvoidPatch.bit_flag
            debug_file.write(RandoOptions.AvoidPatch.name + '\n')
        if False:
            write_me |= RandoOptions.RetreatPatch.bit_flag
            debug_file.write(RandoOptions.RetreatPatch.name + '\n')
        if True:
            write_me |= RandoOptions.TeleportPatch.bit_flag
            debug_file.write(RandoOptions.TeleportPatch.name + '\n')

        # More QoL
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))
        write_me = 0

        if False:
            write_me |= RandoOptions.HardMode.bit_flag
            debug_file.write(RandoOptions.HardMode.name + '\n')
        if False:
            write_me |= RandoOptions.HalveEnc.bit_flag
            debug_file.write(RandoOptions.HalveEnc.name + '\n')
        if False:
            write_me |= RandoOptions.MajorShuffle.bit_flag
            debug_file.write(RandoOptions.MajorShuffle.name + '\n')
        if False:
            write_me |= RandoOptions.EasierBosses.bit_flag
            debug_file.write(RandoOptions.EasierBosses.name + '\n')
        if False:
            write_me |= RandoOptions.RandomPuzzles.bit_flag
            debug_file.write(RandoOptions.RandomPuzzles.name + '\n')
        if False:
            write_me |= RandoOptions.FixedPuzzles.bit_flag
            debug_file.write(RandoOptions.FixedPuzzles.name + '\n')
        if False:
            write_me |= RandoOptions.ManualRG.bit_flag
            debug_file.write(RandoOptions.ManualRG.name + '\n')
        if False:
            write_me |= RandoOptions.ShipWings.bit_flag
            debug_file.write(RandoOptions.ShipWings.name + '\n')

        # Speedstuffs
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))
        write_me = 0

        if False:
            write_me |= RandoOptions.MusicShuffle.bit_flag
            debug_file.write(RandoOptions.MusicShuffle.name + '\n')
        if False:
            write_me |= RandoOptions.TeleportAny.bit_flag
            debug_file.write(RandoOptions.TeleportAny.name + '\n')
        if False:
            write_me |= RandoOptions.ForceBossDrop.bit_flag
            debug_file.write(RandoOptions.ForceBossDrop.name + '\n')
        if False:
            write_me |= RandoOptions.ForceSuperMin.bit_flag
            debug_file.write(RandoOptions.ForceSuperMin.name + '\n')
        if False:
            write_me |= RandoOptions.AnemosOpen.bit_flag
            debug_file.write(RandoOptions.AnemosOpen.name + '\n')
        elif False:
            write_me |= RandoOptions.AnemosRand.bit_flag
            debug_file.write(RandoOptions.AnemosRand.name + '\n')

        # Misc
        if self.options.character_shuffle < 2:
            write_me |= RandoOptions.ShufflePCs
        rando_file.write(write_me.to_bytes(length=1, byteorder='big'))
        write_me = 0

        # Placeholder in case we need more flags
        rando_file.write(write_me.to_bytes(length=4, byteorder='big'))

    def create_item(self, name: str) -> "Item":
        return create_item(name, self.player)

    def get_location(self, location_name: str) -> GSTLALocation:
        return cast(GSTLALocation, super().get_location(location_name))