import yaml
import os
import zipfile
import Utils
from copy import deepcopy
from .Regions import object_id_table
from worlds.Files import APPatch
import pkgutil

settings_template = Utils.parse_yaml(pkgutil.get_data(__name__, "data/settings.yaml"))


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
                                                   self.random.randint(0, 1)):
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
        "enemies_density": cc(self.options.enemies_density),
        "chests_shuffle": "Include",
        "shuffle_boxes_content": self.options.brown_boxes == "shuffle",
        "npcs_shuffle": "Include",
        "battlefields_shuffle": "Include",
        "logic_options": cc(self.options.logic),
        "shuffle_enemies_position": tf(self.options.shuffle_enemies_position),
        "enemies_scaling_lower": cc(self.options.enemies_scaling_lower),
        "enemies_scaling_upper": cc(self.options.enemies_scaling_upper),
        "bosses_scaling_lower": cc(self.options.bosses_scaling_lower),
        "bosses_scaling_upper": cc(self.options.bosses_scaling_upper),
        "enemizer_attacks": cc(self.options.enemizer_attacks),
        "leveling_curve": cc(self.options.leveling_curve),
        "battles_quantity": cc(self.options.battlefields_battles_quantities) if
                               self.options.battlefields_battles_quantities.value < 5 else
                               "RandomLow" if
                               self.options.battlefields_battles_quantities.value == 5 else
                               "RandomHigh",
        "shuffle_battlefield_rewards": tf(self.options.shuffle_battlefield_rewards),
        "random_starting_weapon": True,
        "progressive_gear": tf(self.options.progressive_gear),
        "tweaked_dungeons": tf(self.options.tweak_frustrating_dungeons),
        "doom_castle_mode": cc(self.options.doom_castle_mode),
        "doom_castle_shortcut": tf(self.options.doom_castle_shortcut),
        "sky_coin_mode": cc(self.options.sky_coin_mode),
        "sky_coin_fragments_qty": cc(self.options.shattered_sky_coin_quantity),
        "enable_spoilers": False,
        "progressive_formations": cc(self.options.progressive_formations),
        "map_shuffling": cc(self.options.map_shuffle),
        "crest_shuffle": tf(self.options.crest_shuffle),
        "enemizer_groups": cc(self.options.enemizer_groups),
        "shuffle_res_weak_type": tf(self.options.shuffle_res_weak_types),
        "companion_leveling_type": cc(self.options.companion_leveling_type),
        "companion_spellbook_type": cc(self.options.companion_spellbook_type),
        "starting_companion": cc(self.options.starting_companion),
        "available_companions": ["Zero", "One", "Two",
                                 "Three", "Four"][self.options.available_companions.value],
        "companions_locations": cc(self.options.companions_locations),
        "kaelis_mom_fight_minotaur": tf(self.options.kaelis_mom_fight_minotaur),
    }

    for option, data in option_writes.items():
        options["Final Fantasy Mystic Quest"][option][data] = 1

    rom_name = f'MQ{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed_name:11}'[:21]
    self.rom_name = bytearray(rom_name,
                              'utf8')
    self.rom_name_available_event.set()

    setup = {"version": "1.5", "name": self.multiworld.player_name[self.player], "romname": rom_name, "seed":
             hex(self.random.randint(0, 0xFFFFFFFF)).split("0x")[1].upper()}

    starting_items = [output_item_name(item) for item in self.multiworld.precollected_items[self.player]]
    if self.options.sky_coin_mode == "shattered_sky_coin":
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


class APMQFile(APPatch):
    game = "Final Fantasy Mystic Quest"

    def get_manifest(self):
        manifest = super().get_manifest()
        manifest["patch_file_ending"] = ".apmq"
        return manifest
