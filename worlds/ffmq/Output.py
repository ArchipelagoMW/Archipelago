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
        return option.current_key.title().replace("_", "")

    def tf(option):
        return True if option else False

    # breaking the rules here but this should cut this block of code down to be more readable
    mw = self.multiworld
    p = self.player

    options = deepcopy(settings_template)
    options["name"] = mw.player_name[p]

    option_writes = {
                   "enemies_density": cc(mw.enemies_density[p]),
                   "chests_shuffle": "Include",
                   "shuffle_boxes_content": True if mw.brown_boxes[p] == "shuffle" else False,
                   "npcs_shuffle": "Include",
                   "battlefields_shuffle": "Include",
                   "logic_options": cc(mw.logic[p]),
                   "shuffle_enemies_position": tf(mw.shuffle_enemies_position[p]),
                   "enemies_scaling_lower": cc(mw.enemies_scaling_lower[p]),
                   "enemies_scaling_upper": cc(mw.enemies_scaling_upper[p]),
                   "bosses_scaling_lower": cc(mw.bosses_scaling_lower[p]),
                   "bosses_scaling_upper": cc(mw.bosses_scaling_upper[p]),
                   "enemizer_attacks": cc(mw.enemizer_attacks[p]),
                   "leveling_curve": cc(mw.leveling_curve[p]),
                   "battles_quantity": cc(mw.battlefields_battles_quantities[p]) if
                                        mw.battlefields_battles_quantities[p].value < 5 else "RandomLow" if
                                        mw.battlefields_battles_quantities[p].value == 5 else "RandomHigh",
                   "shuffle_battlefield_rewards": tf(mw.shuffle_battlefield_rewards[p]),
                   "random_starting_weapon": True,
                   "progressive_gear": tf(mw.progressive_gear[p]),
                   "tweaked_dungeons": tf(mw.tweak_frustrating_dungeons[p]),
                   "doom_castle_mode": cc(mw.doom_castle_mode[p]),
                   "doom_castle_shortcut": tf(mw.doom_castle_shortcut[p]),
                   "sky_coin_mode": cc(mw.sky_coin_mode[p]),
                   "sky_coin_fragments_qty": cc(mw.shattered_sky_coin_quantity[p]),
                   "enable_spoilers": False,
                   "progressive_formations": cc(mw.progressive_formations[p]),
                   "map_shuffling": "None",
                   "crest_shuffle": tf(mw.crest_shuffle[p]),
               }
    for option, data in option_writes.items():
        options["Final Fantasy Mystic Quest"][option][data] = 1

    rom_name = f'MQ{__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}'[:21]
    #rom_name.extend([0] * (21 - len(self.rom_name)))
    self.rom_name = bytearray(rom_name,
                              'utf8')
    self.rom_name_available_event.set()

    setup = {"version": "1.4", "name": mw.player_name[p], "romname": rom_name, "seed":
        hex(mw.per_slot_randoms[p].randint(0, int("FFFFFFFF", 16))).split("0x")[1].upper()}

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