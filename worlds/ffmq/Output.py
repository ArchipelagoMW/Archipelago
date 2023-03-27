import yaml
import os
import zipfile
from pathlib import Path
from copy import deepcopy


base_path = Path(__file__).parent
file_path = (base_path / "data/settings.yaml").resolve()
with open(file_path) as file:
    settings_template = yaml.load(file, yaml.Loader)

def generate_output(self, output_directory):
    item_placement = []
    for location in self.multiworld.get_locations(self.player):
        if location.type != "Trigger":
            if location.item.code > 0x420000 + 256: #"Progressive" in item_name:
                item_name = self.item_id_to_name[location.item.code - 256]
            else:
                item_name = location.item.name
            item_placement.append({"object_id": location.address, "type": location.type, "content":
                "".join(item_name.split(" ")) if location.item.player == self.player else "APItem"})


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
                   "doom_castle_mode": cc(mw.doom_castle[p]),
                   "doom_castle_shortcut": False,
                   "sky_coin_mode": cc(mw.sky_coin_mode[p]),
                   "sky_coin_fragments_qty": cc(mw.shattered_sky_coin_quantity[p]),
                   "enable_spoilers": False,
                   "progressive_formations": cc(mw.progressive_formations[p]),
                   "map_shuffling": "None",
                   "crest_shuffle": tf(mw.crest_shuffle[p]),
                   # "seed": mw.per_slot_randoms[p].randint(0, int("FFFFFFFF", 16)),
                   # "starting_items": [self.multiworld.starting_weapon[self.player].current_key.title().replace("_", ""),
                   #                    "SteelArmor"]
                   #item.name.replace(" ", "") for item in
                   # self.multiworld.precollected_items[self.player]]
               }
    for option, data in option_writes.items():
        options["Final Fantasy Mystic Quest"][option][data] = 1
    options["Final Fantasy Mystic Quest"]["seed"] = mw.per_slot_randoms[p].randint(0, int("FFFFFFFF", 16))
    options["Final Fantasy Mystic Quest"]["starting_items"] = [item.name.title().replace(" ", "") for item in
                                                               self.multiworld.precollected_items[self.player]]
        #
        # [
        # self.multiworld.starting_weapon[self.player].current_key.title().replace("_", ""), "SteelArmor"]

    file_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.zip")
    with zipfile.ZipFile(file_path, mode="w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9) as zf:
        zf.writestr("itemplacement.yaml", yaml.dump(item_placement))
        zf.writestr("settings.yaml", yaml.dump(options))
