import yaml
import os
import zipfile
from copy import deepcopy
from .Regions import object_id_table
from Main import __version__
from worlds.Files import APContainer
import pkgutil

settings_template = yaml.load(pkgutil.get_data(__name__, "data/settings.yaml"), yaml.Loader)


def generate_output(self, output_directory):
    def output_item_name(item):
        if item.player == self.player:
            if item.code > 0x420000 + 256:
                item_name = self.item_id_to_name[item.code - 256]
            else:
                item_name = item.name
            item_name = "".join(item_name.split("'"))
            item_name = "".join(item_name.split(" "))
        else:
            if item.advancement or item.useful or (item.trap and
                                                   self.multiworld.per_slot_randoms[self.player].randint(0, 1)):
                item_name = "APItem"
            else:
                item_name = "APItemFiller"
        return item_name

    item_placement = []
    for location in self.multiworld.get_locations(self.player):
        if location.type != "Trigger":
            item_placement.append({"object_id": object_id_table[location.name], "type": location.type, "content":
                output_item_name(location.item), "player": self.multiworld.player_name[location.item.player],
                                   "item_name": location.item.name})

    def cc(option):
        return option.current_key.title().replace("_", "").replace("OverworldAndDungeons",
            "OverworldDungeons").replace("MobsAndBosses", "MobsBosses").replace("MobsBossesAndDarkKing",
            "MobsBossesDK").replace("BenjaminLevelPlus", "BenPlus").replace("BenjaminLevel", "BenPlus0").replace(
            "RandomCompanion", "Random")

    def tf(option):
        return True if option else False

    options = deepcopy(settings_template)
    options["name"] = self.multiworld.player_name[self.player]
    option_writes = {
        "enemies_density": cc(self.multiworld.enemies_density[self.player]),
        "chests_shuffle": "Include",
        "shuffle_boxes_content": self.multiworld.brown_boxes[self.player] == "shuffle",
        "npcs_shuffle": "Include",
        "battlefields_shuffle": "Include",
        "logic_options": cc(self.multiworld.logic[self.player]),
        "shuffle_enemies_position": tf(self.multiworld.shuffle_enemies_position[self.player]),
        "enemies_scaling_lower": cc(self.multiworld.enemies_scaling_lower[self.player]),
        "enemies_scaling_upper": cc(self.multiworld.enemies_scaling_upper[self.player]),
        "bosses_scaling_lower": cc(self.multiworld.bosses_scaling_lower[self.player]),
        "bosses_scaling_upper": cc(self.multiworld.bosses_scaling_upper[self.player]),
        "enemizer_attacks": cc(self.multiworld.enemizer_attacks[self.player]),
        "leveling_curve": cc(self.multiworld.leveling_curve[self.player]),
        "battles_quantity": cc(self.multiworld.battlefields_battles_quantities[self.player]) if
                               self.multiworld.battlefields_battles_quantities[self.player].value < 5 else
                               "RandomLow" if
                               self.multiworld.battlefields_battles_quantities[self.player].value == 5 else
                               "RandomHigh",
        "shuffle_battlefield_rewards": tf(self.multiworld.shuffle_battlefield_rewards[self.player]),
        "random_starting_weapon": True,
        "progressive_gear": tf(self.multiworld.progressive_gear[self.player]),
        "tweaked_dungeons": tf(self.multiworld.tweak_frustrating_dungeons[self.player]),
        "doom_castle_mode": cc(self.multiworld.doom_castle_mode[self.player]),
        "doom_castle_shortcut": tf(self.multiworld.doom_castle_shortcut[self.player]),
        "sky_coin_mode": cc(self.multiworld.sky_coin_mode[self.player]),
        "sky_coin_fragments_qty": cc(self.multiworld.shattered_sky_coin_quantity[self.player]),
        "enable_spoilers": False,
        "progressive_formations": cc(self.multiworld.progressive_formations[self.player]),
        "map_shuffling": cc(self.multiworld.map_shuffle[self.player]),
        "crest_shuffle": tf(self.multiworld.crest_shuffle[self.player]),
        "enemizer_groups": cc(self.multiworld.enemizer_groups[self.player]),
        "shuffle_res_weak_type": tf(self.multiworld.shuffle_res_weak_types[self.player]),
        "companion_leveling_type": cc(self.multiworld.companion_leveling_type[self.player]),
        "companion_spellbook_type": cc(self.multiworld.companion_spellbook_type[self.player]),
        "starting_companion": cc(self.multiworld.starting_companion[self.player]),
        "available_companions": ["Zero", "One", "Two",
                                 "Three", "Four"][self.multiworld.available_companions[self.player].value],
        "companions_locations": cc(self.multiworld.companions_locations[self.player]),
        "kaelis_mom_fight_minotaur": tf(self.multiworld.kaelis_mom_fight_minotaur[self.player]),
    }

    for option, data in option_writes.items():
        options["Final Fantasy Mystic Quest"][option][data] = 1

    rom_name = f'MQ{__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed_name:11}'[:21]
    self.rom_name = bytearray(rom_name,
                              'utf8')
    self.rom_name_available_event.set()

    setup = {"version": "1.5", "name": self.multiworld.player_name[self.player], "romname": rom_name, "seed":
             hex(self.multiworld.per_slot_randoms[self.player].randint(0, 0xFFFFFFFF)).split("0x")[1].upper()}

    starting_items = [output_item_name(item) for item in self.multiworld.precollected_items[self.player]]
    if self.multiworld.sky_coin_mode[self.player] == "shattered_sky_coin":
        starting_items.append("SkyCoin")

    file_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.apmq")

    APMQ = APMQFile(file_path, player=self.player, player_name=self.multiworld.player_name[self.player])
    with zipfile.ZipFile(file_path, mode="w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9) as zf:
        zf.writestr("itemplacement.yaml", yaml.dump(item_placement))
        zf.writestr("flagset.yaml", yaml.dump(options))
        zf.writestr("startingitems.yaml", yaml.dump(starting_items))
        zf.writestr("setup.yaml", yaml.dump(setup))
        zf.writestr("rooms.yaml", yaml.dump(self.rooms))

        APMQ.write_contents(zf)


class APMQFile(APContainer):
    game = "Final Fantasy Mystic Quest"

    def get_manifest(self):
        manifest = super().get_manifest()
        manifest["patch_file_ending"] = ".apmq"
        return manifest