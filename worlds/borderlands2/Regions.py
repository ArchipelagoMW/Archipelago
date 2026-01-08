from typing import Dict, List, NamedTuple, Union


class Borderlands2RegionData(NamedTuple):
    name: str = ""
    travel_item_name: Union[str, List[str]] = ""
    connecting_regions: List[str] = []
    @property
    def primary_travel_item(self):
        if type(self.travel_item_name) is str:
            return self.travel_item_name
        elif len(self.travel_item_name) > 0:
            return self.travel_item_name[0]
        return ""

region_data_table: Dict[str, Borderlands2RegionData] = {
    "Menu": Borderlands2RegionData("Menu", "", [
        "WindshearWaste",
        "DigistructPeak",
        # "FFSIntroSanctuary",
        # "UnassumingDocks",
        # "BadassCrater",
        # "Oasis",
        # "HuntersGrotto",
        # "MarcusMercenaryShop",
        # "GluttonyGulch",
        # "RotgutDistillery",
        # "WamBamIsland",
        # "HallowedHollow",
    ]),

    "WindshearWaste": Borderlands2RegionData("WindshearWaste", "", ["SouthernShelf"]),
    "SouthernShelf": Borderlands2RegionData("SouthernShelf", "Travel: Southern Shelf", ["SouthernShelfBay", "ThreeHornsDivide"]),
    "SouthernShelfBay": Borderlands2RegionData("SouthernShelfBay", "Travel: Southern Shelf Bay", []),
    "ThreeHornsDivide": Borderlands2RegionData("ThreeHornsDivide", "Travel: Three Horns Divide", ["ThreeHornsValley", "Sanctuary"]),
    "ThreeHornsValley": Borderlands2RegionData("ThreeHornsValley", "Travel: Three Horns Valley", ["SouthpawSteam&Power", "Dust"]),
    "Sanctuary": Borderlands2RegionData("Sanctuary", "Travel: Sanctuary", ["FrostburnCanyon"]),
    "FrostburnCanyon": Borderlands2RegionData("FrostburnCanyon", "Travel: Frostburn Canyon", ["BloodshotStronghold", "FriendshipGulag"]),
    "SouthpawSteam&Power": Borderlands2RegionData("SouthpawSteam&Power", "Travel: Southpaw Steam & Power", []),
    "Dust": Borderlands2RegionData("Dust", "Travel: The Dust", ["Lynchwood"]),
    "BloodshotStronghold": Borderlands2RegionData("BloodshotStronghold", ["Travel: Bloodshot Stronghold", "Travel: The Dust", "Travel: Frostburn Canyon", "Travel: Three Horns Valley"], ["BloodshotRamparts"]),
    "BloodshotRamparts": Borderlands2RegionData("BloodshotRamparts", "Travel: Bloodshot Ramparts", [
        "TundraExpress",
        "MarcusMercenaryShop",
        "GluttonyGulch",
        "RotgutDistillery",
        "WamBamIsland",
        "HallowedHollow",
        "BadassCrater",
        "Oasis",
    ]),
    "Fridge": Borderlands2RegionData("Fridge", ["Travel: The Fridge"], ["FinksSlaughterhouse", "HighlandsOutwash"]),
    "HighlandsOutwash": Borderlands2RegionData("HighlandsOutwash", ["Travel: Highlands Outwash"], ["Highlands"]),
    "Highlands": Borderlands2RegionData("Highlands", ["Travel: Highlands"], ["HolySpirits", "WildlifeExploitationPreserve", "ThousandCuts","Opportunity"]),
    "FriendshipGulag": Borderlands2RegionData("FriendshipGulag", ["Travel: Friendship Gulag"], []),
    "Lynchwood": Borderlands2RegionData("Lynchwood", ["Travel: Lynchwood"], []),
    "FinksSlaughterhouse": Borderlands2RegionData("FinksSlaughterhouse", ["Travel: Fink's Slaughterhouse"], []),
    "SanctuaryHole": Borderlands2RegionData("SanctuaryHole", ["Travel: Sanctuary Hole"], ["CausticCaverns"]),
    "TerramorphousPeak": Borderlands2RegionData("TerramorphousPeak", ["Travel: Terramorphous Peak"], []),
    "CausticCaverns": Borderlands2RegionData("CausticCaverns", ["Travel: Caustic Caverns"], []),
    "Opportunity": Borderlands2RegionData("Opportunity", ["Travel: Opportunity"], ["Bunker"]),
    "HolySpirits": Borderlands2RegionData("HolySpirits", ["Travel: The Holy Spirits"], []),
    "WildlifeExploitationPreserve": Borderlands2RegionData("WildlifeExploitationPreserve", ["Travel: Wildlife Exploitation Preserve"], ["NaturalSelectionAnnex", "Bunker"]),
    "NaturalSelectionAnnex": Borderlands2RegionData("NaturalSelectionAnnex", ["Travel: Natural Selection Annex"], []),
    "TundraExpress": Borderlands2RegionData("TundraExpress", ["Travel: Tundra Express"], ["EndOfTheLine"]),
    "EndOfTheLine": Borderlands2RegionData("EndOfTheLine", ["Travel: End of the Line"], ["SanctuaryHole", "Fridge"]),
    "Bunker": Borderlands2RegionData("Bunker", ["Travel: The Bunker",
                                                "Travel: Wildlife Exploitation Preserve",
                                                "Travel: Thousand Cuts",
                                                "Travel: Opportunity"], ["ControlCoreAngel"]),
    "ThousandCuts": Borderlands2RegionData("ThousandCuts", ["Travel: Thousand Cuts"], ["Bunker"]),
    "EridiumBlight": Borderlands2RegionData("EridiumBlight", ["Travel: Eridium Blight"], ["OreChasm", "SawtoothCauldron"]),
    "SawtoothCauldron": Borderlands2RegionData("SawtoothCauldron", ["Travel: Sawtooth Cauldron"], ["AridNexusBoneyard"]),
    "OreChasm": Borderlands2RegionData("OreChasm", ["Travel: Ore Chasm"], []),
    "ControlCoreAngel": Borderlands2RegionData("ControlCoreAngel", ["Travel: Control Core Angel"], ["EridiumBlight"]),
    "AridNexusBoneyard": Borderlands2RegionData("AridNexusBoneyard", ["Travel: Arid Nexus Boneyard"], ["AridNexusBadlands"]),
    "AridNexusBadlands": Borderlands2RegionData("AridNexusBadlands", ["Travel: Arid Nexus Badlands"], ["HerosPass"]),
    "HerosPass": Borderlands2RegionData("HerosPass", ["Travel: Hero's Pass"], ["VaultOfTheWarrior"]),
    "VaultOfTheWarrior": Borderlands2RegionData("VaultOfTheWarrior", ["Travel: Vault of the Warrior"], ["TerramorphousPeak",
        "FFSIntroSanctuary",
        "UnassumingDocks",
        "HuntersGrotto",
        "DigistructPeakInner",
    ]),

    "FFSIntroSanctuary": Borderlands2RegionData("FFSIntroSanctuary", ["Travel: FFS Intro Sanctuary"], ["Backburner"]),
    "Burrows": Borderlands2RegionData("Burrows", ["Travel: The Burrows"], ["HeliosFallen"]),
    "Backburner": Borderlands2RegionData("Backburner", ["Travel: The Backburner", "Travel: FFS Intro Sanctuary"], ["DahlAbandon"]),
    "DahlAbandon": Borderlands2RegionData("DahlAbandon", ["Travel: Dahl Abandon"], ["Burrows"]),
    "HeliosFallen": Borderlands2RegionData("HeliosFallen", ["Travel: Helios Fallen"], ["Mt.ScarabResearchCenter"]),
    "WrithingDeep": Borderlands2RegionData("WrithingDeep", ["Travel: Writhing Deep"], []),
    "Mt.ScarabResearchCenter": Borderlands2RegionData("Mt.ScarabResearchCenter", ["Travel: Mt. Scarab Research Center"], ["FFSBossFight"]),
    "FFSBossFight": Borderlands2RegionData("FFSBossFight", ["Travel: FFS Boss Fight"], ["WrithingDeep"]),

    "UnassumingDocks": Borderlands2RegionData("UnassumingDocks", ["Travel: Unassuming Docks"], ["FlamerockRefuge"]),
    "FlamerockRefuge": Borderlands2RegionData("FlamerockRefuge", ["Travel: Flamerock Refuge"], ["Forest"]),
    "HatredsShadow": Borderlands2RegionData("HatredsShadow", ["Travel: Hatred's Shadow"], ["LairOfInfiniteAgony"]),
    "LairOfInfiniteAgony": Borderlands2RegionData("LairOfInfiniteAgony",["Travel: Lair of Infinite Agony"], ["DragonKeep"]),
    "ImmortalWoods": Borderlands2RegionData("ImmortalWoods", ["Travel: Immortal Woods"], ["MinesOfAvarice"]),
    "Forest": Borderlands2RegionData("Forest", ["Travel: The Forest"], ["ImmortalWoods"]),
    "MinesOfAvarice": Borderlands2RegionData("MinesOfAvarice", ["Travel: Mines of Avarice"], ["HatredsShadow"]),
    "MurderlinsTemple": Borderlands2RegionData("MurderlinsTemple", ["Travel: Murderlin's Temple"], []),
    "WingedStorm": Borderlands2RegionData("WingedStorm", ["Travel: The Winged Storm"], []),
    "DragonKeep": Borderlands2RegionData("DragonKeep", ["Travel: Dragon Keep"], ["WingedStorm", "MurderlinsTemple"]),

    "BadassCrater": Borderlands2RegionData("BadassCrater", ["Travel: Badass Crater"], ["TorgueArena"]),
    "Beatdown": Borderlands2RegionData("Beatdown", ["Travel: The Beatdown"], ["PyroPetesBar"]),
    "TorgueArena": Borderlands2RegionData("TorgueArena", ["Travel: Torgue Arena"], ["TorgueArenaRing","Beatdown"]),
    "TorgueArenaRing": Borderlands2RegionData("TorgueArenaRing", ["Travel: Torgue Arena Ring"], ["SouthernRaceway"]),
    "BadassCraterBar": Borderlands2RegionData("BadassCraterBar", ["Travel: Badass Crater Bar"], ["SouthernRaceway"]),
    "Forge": Borderlands2RegionData("Forge", ["Travel: The Forge"], []),
    "SouthernRaceway": Borderlands2RegionData("SouthernRaceway", ["Travel: Southern Raceway", "Travel: Torgue Arena Ring"], ["Forge"]),
    "PyroPetesBar": Borderlands2RegionData("PyroPetesBar", ["Travel: Pyro Pete's Bar"], ["BadassCraterBar"]),

    "Oasis": Borderlands2RegionData("Oasis", ["Travel: Oasis"], ["Wurmwater"]),
    "HaytersFolly": Borderlands2RegionData("HaytersFolly", ["Travel: Hayter's Folly"], ["Rustyards"]),
    "Wurmwater": Borderlands2RegionData("Wurmwater", ["Travel: Wurmwater"], ["HaytersFolly"]),
    "WashburneRefinery": Borderlands2RegionData("WashburneRefinery", ["Travel: Washburne Refinery"], ["MagnysLighthouse"]),
    "Rustyards": Borderlands2RegionData("Rustyards", ["Travel: The Rustyards"], ["WashburneRefinery"]),
    "MagnysLighthouse": Borderlands2RegionData("MagnysLighthouse", ["Travel: Magnys Lighthouse"], ["LeviathansLair"]),
    "LeviathansLair": Borderlands2RegionData("LeviathansLair", ["Travel: The Leviathan's Lair"], []),

    "HuntersGrotto": Borderlands2RegionData("HuntersGrotto", ["Travel: Hunter's Grotto"], ["ScyllasGrove"]),
    "CandlerakksCrag": Borderlands2RegionData("CandlerakksCrag", ["Travel: Candlerakk's Cragg"], ["Terminus"]),
    "ArdortonStation": Borderlands2RegionData("ArdortonStation", ["Travel: Ardorton Station"], ["CandlerakksCrag"]),
    "ScyllasGrove": Borderlands2RegionData("ScyllasGrove", ["Travel: Scylla's Grove"], ["ArdortonStation"]),
    "Terminus": Borderlands2RegionData("Terminus", ["Travel: Terminus"], []),

    "DigistructPeak": Borderlands2RegionData("DigistructPeak", ["Travel: Digistruct Peak"], []),
    "DigistructPeakInner": Borderlands2RegionData("DigistructPeakInner", ["Travel: Digistruct Peak"], []),
    # "DigistructPeakOP5": Borderlands2RegionData("DigistructPeakOP5", "", []),

    "MarcusMercenaryShop": Borderlands2RegionData("MarcusMercenaryShop", ["Travel: Marcus's Mercenary Shop"], []),
    "GluttonyGulch": Borderlands2RegionData("GluttonyGulch", ["Travel: Gluttony Gulch"], []),
    "RotgutDistillery": Borderlands2RegionData("RotgutDistillery", ["Travel: Rotgut Distillery"], []),
    "WamBamIsland": Borderlands2RegionData("WamBamIsland", ["Travel: Wam Bam Island"], []),
    "HallowedHollow": Borderlands2RegionData("HallowedHollow", ["Travel: Hallowed Hollow"], []),
}
