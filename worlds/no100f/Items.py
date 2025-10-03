import typing
from BaseClasses import Item, ItemClassification
from .names import ItemNames


class ItemData(typing.NamedTuple):
    id: typing.Optional[int]
    classification: ItemClassification

    def is_progression(self):
        return self.classification & ItemClassification.progression == ItemClassification.progression

    def is_trap(self):
        return self.classification & ItemClassification.trap == ItemClassification.trap

    def is_filler(self):
        return self.classification & ItemClassification.filler == ItemClassification.filler


class NO100FItem(Item):
    game: str = "Night of 100 Frights"


base_id = 1495000

item_table = {
    # Upgrades
    ItemNames.GumPower: ItemData(base_id + 0, ItemClassification.progression),
    ItemNames.SoapPower: ItemData(base_id + 1, ItemClassification.progression),
    ItemNames.BootsPower: ItemData(base_id + 2, ItemClassification.progression),
    ItemNames.PlungerPower: ItemData(base_id + 3, ItemClassification.progression),
    ItemNames.ProgressiveSneak: ItemData(base_id + 4, ItemClassification.useful),
    ItemNames.ProgressiveJump: ItemData(base_id + 7, ItemClassification.progression),
    ItemNames.PoundPower: ItemData(base_id + 8, ItemClassification.progression),
    ItemNames.HelmetPower: ItemData(base_id + 9, ItemClassification.progression),
    ItemNames.ShovelPower: ItemData(base_id + 11, ItemClassification.progression),
    ItemNames.ShockwavePower: ItemData(base_id + 12, ItemClassification.useful),

    # Ammo Upgrades
    ItemNames.GumAmmoUpgrade: ItemData(base_id + 13, ItemClassification.useful),
    ItemNames.SoapAmmoUpgrade: ItemData(base_id + 14, ItemClassification.useful),

    # Monster Tokens
    ItemNames.MT_PROGRESSIVE: ItemData(base_id + 35, ItemClassification.progression),

    # Keys
    ItemNames.Clamor1_Key: ItemData(base_id + 36, ItemClassification.progression),
    ItemNames.Hedge_Key: ItemData(base_id + 37, ItemClassification.progression),
    ItemNames.Fishing_Key: ItemData(base_id + 38, ItemClassification.progression),
    ItemNames.Cellar2_Key: ItemData(base_id + 39, ItemClassification.progression),
    ItemNames.Cellar3_Key: ItemData(base_id + 40, ItemClassification.progression),
    ItemNames.Cavein_Key: ItemData(base_id + 41, ItemClassification.progression),
    ItemNames.FishyClues_Key: ItemData(base_id + 42, ItemClassification.progression),
    ItemNames.Graveplot_Key: ItemData(base_id + 43, ItemClassification.progression),
    ItemNames.Tomb1_Key: ItemData(base_id + 44, ItemClassification.progression),
    ItemNames.Tomb3_Key: ItemData(base_id + 45, ItemClassification.progression),
    ItemNames.Clamor4_Key: ItemData(base_id + 46, ItemClassification.progression),
    ItemNames.MYM_Key: ItemData(base_id + 47, ItemClassification.progression),
    ItemNames.Coast_Key: ItemData(base_id + 48, ItemClassification.progression),
    ItemNames.Attic_Key: ItemData(base_id + 49, ItemClassification.progression),
    ItemNames.Knight_Key: ItemData(base_id + 50, ItemClassification.progression),
    ItemNames.Creepy2_Key: ItemData(base_id + 51, ItemClassification.progression),
    ItemNames.Creepy3_Key: ItemData(base_id + 52, ItemClassification.progression),
    ItemNames.Gusts1_Key: ItemData(base_id + 53, ItemClassification.progression),
    ItemNames.Gusts2_Key: ItemData(base_id + 54, ItemClassification.progression),
    ItemNames.DLD_Key: ItemData(base_id + 55, ItemClassification.progression),
    ItemNames.Shiver_Key: ItemData(base_id + 56, ItemClassification.progression),

    # Warp Gates
    ItemNames.Cellar4_Warp: ItemData(base_id + 57, ItemClassification.progression),
    ItemNames.Cliff4_Warp: ItemData(base_id + 58, ItemClassification.progression),
    ItemNames.Hedge4_Warp: ItemData(base_id + 59, ItemClassification.progression),
    ItemNames.Hedge6_Warp: ItemData(base_id + 60, ItemClassification.progression),
    ItemNames.Hedge9_Warp: ItemData(base_id + 61, ItemClassification.progression),
    ItemNames.Fish3_Warp: ItemData(base_id + 62, ItemClassification.progression),
    ItemNames.Fish7_Warp: ItemData(base_id + 63, ItemClassification.progression),
    ItemNames.Balc1_Warp: ItemData(base_id + 64, ItemClassification.progression),
    ItemNames.Grave5_Warp: ItemData(base_id + 65, ItemClassification.progression),
    ItemNames.Grave8_Warp: ItemData(base_id + 66, ItemClassification.progression),

    ItemNames.Manor3_Warp: ItemData(base_id + 68, ItemClassification.progression),
    ItemNames.Manor6_Warp: ItemData(base_id + 69, ItemClassification.progression),
    ItemNames.LH14_Warp: ItemData(base_id + 70, ItemClassification.progression),
    ItemNames.LH18_Warp: ItemData(base_id + 71, ItemClassification.progression),
    ItemNames.Balc4_Warp: ItemData(base_id + 72, ItemClassification.progression),
    ItemNames.Balc6_Warp: ItemData(base_id + 73, ItemClassification.progression),
    ItemNames.SP3_Warp: ItemData(base_id + 74, ItemClassification.progression),
    ItemNames.SP5_Warp: ItemData(base_id + 75, ItemClassification.progression),
    ItemNames.Roof3_Warp: ItemData(base_id + 76, ItemClassification.progression),
    ItemNames.SL2_Warp: ItemData(base_id + 77, ItemClassification.progression),
    ItemNames.Wreck22_Warp: ItemData(base_id + 78, ItemClassification.progression),
    ItemNames.Wreck26_Warp: ItemData(base_id + 79, ItemClassification.progression),
    ItemNames.LH15_Warp: ItemData(base_id + 80, ItemClassification.progression),
    ItemNames.Grave1_Warp: ItemData(base_id + 81, ItemClassification.progression),
    ItemNames.MG_Warp: ItemData(base_id + 82, ItemClassification.progression),

    # Keyrings
    ItemNames.Clamor1_KeyRing: ItemData(base_id + 83, ItemClassification.progression),
    ItemNames.Hedge_KeyRing: ItemData(base_id + 84, ItemClassification.progression),
    ItemNames.Fishing_KeyRing: ItemData(base_id + 85, ItemClassification.progression),
    ItemNames.Cellar2_KeyRing: ItemData(base_id + 86, ItemClassification.progression),
    ItemNames.Cellar3_KeyRing: ItemData(base_id + 87, ItemClassification.progression),
    ItemNames.Cavein_KeyRing: ItemData(base_id + 88, ItemClassification.progression),
    ItemNames.FishyClues_KeyRing: ItemData(base_id + 89, ItemClassification.progression),
    ItemNames.Graveplot_KeyRing: ItemData(base_id + 90, ItemClassification.progression),
    ItemNames.Tomb1_KeyRing: ItemData(base_id + 91, ItemClassification.progression),
    ItemNames.Tomb3_KeyRing: ItemData(base_id + 92, ItemClassification.progression),
    ItemNames.Clamor4_KeyRing: ItemData(base_id + 93, ItemClassification.progression),
    ItemNames.MYM_KeyRing: ItemData(base_id + 94, ItemClassification.progression),
    ItemNames.Coast_KeyRing: ItemData(base_id + 95, ItemClassification.progression),
    ItemNames.Attic_KeyRing: ItemData(base_id + 96, ItemClassification.progression),
    ItemNames.Knight_KeyRing: ItemData(base_id + 97, ItemClassification.progression),
    ItemNames.Creepy2_KeyRing: ItemData(base_id + 98, ItemClassification.progression),
    ItemNames.Creepy3_KeyRing: ItemData(base_id + 99, ItemClassification.progression),
    ItemNames.Gusts1_KeyRing: ItemData(base_id + 100, ItemClassification.progression),
    ItemNames.Gusts2_KeyRing: ItemData(base_id + 101, ItemClassification.progression),
    ItemNames.DLD_KeyRing: ItemData(base_id + 102, ItemClassification.progression),
    ItemNames.Shiver_KeyRing: ItemData(base_id + 103, ItemClassification.progression),

    ItemNames.FillerSnack: ItemData(base_id + 104, ItemClassification.filler),

    ItemNames.Snack: ItemData(base_id + 105, ItemClassification.progression_skip_balancing),
    ItemNames.SnackBox: ItemData(base_id + 106, ItemClassification.progression),

    # events
    ItemNames.victory: ItemData(None, ItemClassification.progression)
}

lookup_id_to_name: typing.Dict[int, str] = {data.id: name for name, data in item_table.items() if data.id}
