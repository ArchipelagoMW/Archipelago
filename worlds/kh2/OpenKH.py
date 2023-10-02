import logging

import yaml
import os
import Utils
import zipfile

from .Items import item_dictionary_table, CheckDupingItems
from .Locations import all_locations, SoraLevels, exclusion_table
from .XPValues import lvlStats, formExp, soraExp
from worlds.Files import APContainer


class KH2Container(APContainer):
    game: str = 'Kingdom Hearts 2'

    def __init__(self, patch_data: dict, base_path: str, output_directory: str,
                 player=None, player_name: str = "", server: str = ""):
        self.patch_data = patch_data
        self.file_path = base_path
        container_path = os.path.join(output_directory, base_path + ".zip")
        super().__init__(container_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        for filename, yml in self.patch_data.items():
            opened_zipfile.writestr(filename, yml)
        for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), "mod_template")):
            for file in files:
                opened_zipfile.write(os.path.join(root, file),
                                     os.path.relpath(os.path.join(root, file),
                                                     os.path.join(os.path.dirname(__file__), "mod_template")))
        # opened_zipfile.writestr(self.zpf_path, self.patch_data)
        super().write_contents(opened_zipfile)


def patch_kh2(self, output_directory):
    def increaseStat(i):
        if lvlStats[i] == "str":
            self.strength += 2
        elif lvlStats[i] == "mag":
            self.magic += 2
        elif lvlStats[i] == "def":
            self.defense += 1
        elif lvlStats[i] == "ap":
            self.ap += 3

    self.formattedTrsr = {}
    self.formattedBons = []
    self.formattedLvup = {"Sora": {}}
    self.formattedBons = {}
    self.formattedFmlv = {}
    self.formattedItem = {"Stats": []}
    self.formattedPlrp = []
    self.strength = 2
    self.magic = 6
    self.defense = 2
    self.ap = 0
    self.dblbonus = 0
    formexp = None
    formName = None
    levelsetting = list()
    slotDataDuping = set()
    for values in CheckDupingItems.values():
        if isinstance(values, set):
            slotDataDuping = slotDataDuping.union(values)
        else:
            for inner_values in values.values():
                slotDataDuping = slotDataDuping.union(inner_values)

    if self.multiworld.Keyblade_Minimum[self.player].value > self.multiworld.Keyblade_Maximum[self.player].value:
        logging.info(
                f"{self.multiworld.get_file_safe_player_name(self.player)} has Keyblade Minimum greater than Keyblade Maximum")
        keyblademin = self.multiworld.Keyblade_Maximum[self.player].value
        keyblademax = self.multiworld.Keyblade_Minimum[self.player].value
    else:
        keyblademin = self.multiworld.Keyblade_Minimum[self.player].value
        keyblademax = self.multiworld.Keyblade_Maximum[self.player].value

    if self.multiworld.LevelDepth[self.player] == "level_50":
        levelsetting.extend(exclusion_table["Level50"])

    elif self.multiworld.LevelDepth[self.player] == "level_99":
        levelsetting.extend(exclusion_table["Level99"])

    elif self.multiworld.LevelDepth[self.player] != "level_1":
        levelsetting.extend(exclusion_table["Level50Sanity"])

        if self.multiworld.LevelDepth[self.player] == "level_99_sanity":
            levelsetting.extend(exclusion_table["Level99Sanity"])

    mod_name = f"AP-{self.multiworld.seed_name}-P{self.player}-{self.multiworld.get_file_safe_player_name(self.player)}"

    for location in self.multiworld.get_filled_locations(self.player):

        data = all_locations[location.name]
        if location.item.player == self.player:
            itemcode = item_dictionary_table[location.item.name].kh2id
        else:
            itemcode = 90  # castle map

        if data.yml == "Chest":
            self.formattedTrsr[data.locid] = {"ItemId": itemcode}

        elif data.yml in ["Get Bonus", "Double Get Bonus", "Second Get Bonus"]:
            if data.yml == "Get Bonus":
                self.dblbonus = 0
            # if double bonus then addresses dbl bonus so the next check gets 2 items on it
            if data.yml == "Double Get Bonus":
                self.dblbonus = itemcode
                continue
            if data.locid not in self.formattedBons.keys():
                self.formattedBons[data.locid] = {}
            self.formattedBons[data.locid][data.charName] = {
                "RewardId":             data.locid,
                "CharacterId":          data.charNumber,
                "HpIncrease":           0,
                "MpIncrease":           0,
                "DriveGaugeUpgrade":    0,
                "ItemSlotUpgrade":      0,
                "AccessorySlotUpgrade": 0,
                "ArmorSlotUpgrade":     0,
                "BonusItem1":           itemcode,
                "BonusItem2":           self.dblbonus,
                "Padding":              0

            }
            # putting dbl bonus at 0 again, so we don't have the same item placed multiple time
            self.dblbonus = 0
        elif data.yml == "Keyblade":
            self.formattedItem["Stats"].append({
                "Id":                  data.locid,
                "Attack":              self.multiworld.per_slot_randoms[self.player].randint(keyblademin, keyblademax),
                "Magic":               self.multiworld.per_slot_randoms[self.player].randint(keyblademin, keyblademax),
                "Defense":             0,
                "Ability":             itemcode,
                "AbilityPoints":       0,
                "Unknown08":           100,
                "FireResistance":      100,
                "IceResistance":       100,
                "LightningResistance": 100,
                "DarkResistance":      100,
                "Unknown0d":           100,
                "GeneralResistance":   100,
                "Unknown":             0
            })

        elif data.yml == "Forms":
            # loc id is form lvl
            # char name is the form name number :)
            if data.locid == 2:
                formDict = {1: "Valor", 2: "Wisdom", 3: "Limit", 4: "Master", 5: "Final"}
                formDictExp = {
                    1: self.multiworld.Valor_Form_EXP[self.player].value,
                    2: self.multiworld.Wisdom_Form_EXP[self.player].value,
                    3: self.multiworld.Limit_Form_EXP[self.player].value,
                    4: self.multiworld.Master_Form_EXP[self.player].value,
                    5: self.multiworld.Final_Form_EXP[self.player].value}
                formexp = formDictExp[data.charName]
                formName = formDict[data.charName]
                self.formattedFmlv[formName] = []
                self.formattedFmlv[formName].append({
                    "Ability":            1,
                    "Experience":         int(formExp[data.charName][data.locid] / formexp),
                    "FormId":             data.charName,
                    "FormLevel":          1,
                    "GrowthAbilityLevel": 0,
                })
            # row is form column is lvl
            self.formattedFmlv[formName].append({
                "Ability":            itemcode,
                "Experience":         int(formExp[data.charName][data.locid] / formexp),
                "FormId":             data.charName,
                "FormLevel":          data.locid,
                "GrowthAbilityLevel": 0,
            })

    # Summons have no checks on them so done fully locally
    self.formattedFmlv["Summon"] = []
    for x in range(1, 7):
        self.formattedFmlv["Summon"].append({
            "Ability":            123,
            "Experience":         int(formExp[0][x] / self.multiworld.Summon_EXP[self.player].value),
            "FormId":             0,
            "FormLevel":          x,
            "GrowthAbilityLevel": 0,
        })
    # levels done down here because of optional settings that can take locations out of the pool.
    self.i = 1
    for location in SoraLevels:
        increaseStat(self.multiworld.per_slot_randoms[self.player].randint(0, 3))
        if location in levelsetting:
            data = self.multiworld.get_location(location, self.player)
            if data.item.player == self.player:
                itemcode = item_dictionary_table[data.item.name].kh2id
            else:
                itemcode = 90  # castle map
        else:
            increaseStat(self.multiworld.per_slot_randoms[self.player].randint(0, 3))
            itemcode = 0
        self.formattedLvup["Sora"][self.i] = {
            "Exp":           int(soraExp[self.i] / self.multiworld.Sora_Level_EXP[self.player].value),
            "Strength":      self.strength,
            "Magic":         self.magic,
            "Defense":       self.defense,
            "Ap":            self.ap,
            "SwordAbility":  itemcode,
            "ShieldAbility": itemcode,
            "StaffAbility":  itemcode,
            "Padding":       0,
            "Character":     "Sora",
            "Level":         self.i
        }
        self.i += 1
    # averaging stats for the struggle bats
    for x in {122, 144, 145}:
        self.formattedItem["Stats"].append({
            "Id":                  x,
            "Attack":              int((keyblademin + keyblademax) / 2),
            "Magic":               int((keyblademin + keyblademax) / 2),
            "Defense":             0,
            "Ability":             405,
            "AbilityPoints":       0,
            "Unknown08":           100,
            "FireResistance":      100,
            "IceResistance":       100,
            "LightningResistance": 100,
            "DarkResistance":      100,
            "Unknown0d":           100,
            "GeneralResistance":   100,
            "Unknown":             0
        })
    mod_dir = os.path.join(output_directory, mod_name + "_" + Utils.__version__)

    openkhmod = {
        "TrsrList.yml": yaml.dump(self.formattedTrsr, line_break="\n"),
        "LvupList.yml": yaml.dump(self.formattedLvup, line_break="\n"),
        "BonsList.yml": yaml.dump(self.formattedBons, line_break="\n"),
        "ItemList.yml": yaml.dump(self.formattedItem, line_break="\n"),
        "FmlvList.yml": yaml.dump(self.formattedFmlv, line_break="\n"),
    }

    mod = KH2Container(openkhmod, mod_dir, output_directory, self.player,
                       self.multiworld.get_file_safe_player_name(self.player))
    mod.write()
