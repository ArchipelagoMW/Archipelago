from typing import Dict, NamedTuple


class FF12OpenWorldEventData(NamedTuple):
    region: str
    item: str
    difficulty: int = 0


event_data_table: Dict[str, FF12OpenWorldEventData] = {
    "Vaan Event (1)": FF12OpenWorldEventData(
        region="Rabanastre",
        item="Vaan",
        difficulty=0
    ),
    "Penelo Event (1)": FF12OpenWorldEventData(
        region="Giza Plains Dry",
        item="Penelo",
        difficulty=0
    ),
    "Dreadnought Leviathan Guest Event (1)": FF12OpenWorldEventData(
        region="Dreadnought Leviathan",
        item="Guest",
        difficulty=1
    ),
    "Ashe Event (1)": FF12OpenWorldEventData(
        region="Dreadnought Leviathan",
        item="Ashe",
        difficulty=1
    ),
    "Defeat Judge Ghis Event (1)": FF12OpenWorldEventData(
        region="Dreadnought Leviathan",
        item="Defeat Ghis",
        difficulty=1
    ),
    "Escape Characters Event (1)": FF12OpenWorldEventData(
        region="Royal Palace",
        item="Balthier",
        difficulty=1
    ),
    "Escape Characters Event (2)": FF12OpenWorldEventData(
        region="Royal Palace",
        item="Fran",
        difficulty=1
    ),
    "Escape Characters Event (3)": FF12OpenWorldEventData(
        region="Royal Palace",
        item="Guest",
        difficulty=1
    ),
    "Barheim Guest Event (1)": FF12OpenWorldEventData(
        region="Barheim Passage Story",
        item="Guest",
        difficulty=1
    ),
    "Defeat Vossler Event (1)": FF12OpenWorldEventData(
        region="Tomb of Raithwall",
        item="Defeat Vossler",
        difficulty=3
    ),
    "Defeat Bergan Event (1)": FF12OpenWorldEventData(
        region="Mt. Bur-Omisace",
        item="Defeat Bergan",
        difficulty=3
    ),
    "Defeat Earth Tyrant Event (1)": FF12OpenWorldEventData(
        region="Dalmasca Westersand",
        item="Defeat Earth Tyrant",
        difficulty=4
    ),
    "Defeat Cid Event (1)": FF12OpenWorldEventData(
        region="Draklor Laboratory",
        item="Defeat Cid",
        difficulty=5
    ),
    "Hunt 1: Rogue Tomato Event (1)": FF12OpenWorldEventData(
        region="Rabanastre",
        item="Hunt",
        difficulty=1
    ),
    "Hunt 2: Thextera Event (1)": FF12OpenWorldEventData(
        region="Rabanastre",
        item="Hunt",
        difficulty=1
    ),
    "Hunt 3: Flowering Cactoid Event (1)": FF12OpenWorldEventData(
        region="Dalmasca Estersand",
        item="Hunt",
        difficulty=1
    ),
    "Hunt 4: Wraith Event (1)": FF12OpenWorldEventData(
        region="Lowtown",
        item="Hunt",
        difficulty=1
    ),
    "Hunt 5: Nidhogg Event (1)": FF12OpenWorldEventData(
        region="Bhujerba",
        item="Hunt",
        difficulty=1
    ),
    "Hunt 6: White Mousse Event (1)": FF12OpenWorldEventData(
        region="Rabanastre",
        item="Hunt",
        difficulty=5
    ),
    "Hunt 7: Ring Wyrm Event (1)": FF12OpenWorldEventData(
        region="Lowtown",
        item="Hunt",
        difficulty=5
    ),
    "Hunt 8: Wyvern Lord Event (1)": FF12OpenWorldEventData(
        region="Rabanastre",
        item="Hunt",
        difficulty=2
    ),
    "Hunt 9: Marilith Event (1)": FF12OpenWorldEventData(
        region="Rabanastre",
        item="Hunt",
        difficulty=5
    ),
    "Hunt 10: Enkelados Event (1)": FF12OpenWorldEventData(
        region="Jahara",
        item="Hunt",
        difficulty=2
    ),
    "Hunt 11: Croakadile Event (1)": FF12OpenWorldEventData(
        region="Giza Plains Rains",
        item="Hunt",
        difficulty=2
    ),
    "Hunt 12: Ixtab Event (1)": FF12OpenWorldEventData(
        region="Jahara",
        item="Hunt",
        difficulty=2
    ),
    "Hunt 13: Feral Retriever Event (1)": FF12OpenWorldEventData(
        region="Mt. Bur-Omisace",
        item="Hunt",
        difficulty=3
    ),
    "Hunt 14: Vorpal Bunny Event (1)": FF12OpenWorldEventData(
        region="Eruyt Village",
        item="Hunt",
        difficulty=3
    ),
    "Hunt 15: Mindflayer Event (1)": FF12OpenWorldEventData(
        region="Jahara",
        item="Hunt",
        difficulty=4
    ),
    "Hunt 16: Bloodwing Event (1)": FF12OpenWorldEventData(
        region="Dalmasca Estersand",
        item="Hunt",
        difficulty=5
    ),
    "Hunt 17: Atomos Event (1)": FF12OpenWorldEventData(
        region="Nalbina Fortress",
        item="Hunt",
        difficulty=3
    ),
    "Hunt 17: Atomos Event (2)": FF12OpenWorldEventData(
        region="Nalbina Fortress",
        item="Jovy",
        difficulty=3
    ),
    "Hunt 18: Roblon Event (1)": FF12OpenWorldEventData(
        region="Nalbina Fortress",
        item="Hunt",
        difficulty=6
    ),
    "Hunt 18: Roblon Event (2)": FF12OpenWorldEventData(
        region="Nalbina Fortress",
        item="Jovy",
        difficulty=6
    ),
    "Hunt 19: Braegh Event (1)": FF12OpenWorldEventData(
        region="Mosphoran Highwaste",
        item="Hunt",
        difficulty=4
    ),
    "Hunt 20: Darksteel Event (1)": FF12OpenWorldEventData(
        region="Archades",
        item="Hunt",
        difficulty=4
    ),
    "Hunt 21: Vyraal Event (1)": FF12OpenWorldEventData(
        region="Balfonheim",
        item="Hunt",
        difficulty=5
    ),
    "Hunt 22: Lindwyrm Event (1)": FF12OpenWorldEventData(
        region="Old Archades",
        item="Hunt",
        difficulty=5
    ),
    "Hunt 23: Overlord Event (1)": FF12OpenWorldEventData(
        region="Archades",
        item="Hunt",
        difficulty=6
    ),
    "Hunt 24: Goliath Event (1)": FF12OpenWorldEventData(
        region="Nalbina Fortress",
        item="Hunt",
        difficulty=6
    ),
    "Hunt 24: Goliath Event (2)": FF12OpenWorldEventData(
        region="Nalbina Fortress",
        item="Jovy",
        difficulty=6
    ),
    "Hunt 25: Deathscythe Event (1)": FF12OpenWorldEventData(
        region="Nalbina Fortress",
        item="Hunt",
        difficulty=6
    ),
    "Hunt 25: Deathscythe Event (2)": FF12OpenWorldEventData(
        region="Nalbina Fortress",
        item="Jovy",
        difficulty=6
    ),
    "Hunt 26: Deathgaze Event (1)": FF12OpenWorldEventData(
        region="Skyferry",
        item="Hunt",
        difficulty=7
    ),
    "Hunt 27: Diabolos Event (1)": FF12OpenWorldEventData(
        region="Bhujerba",
        item="Hunt",
        difficulty=7
    ),
    "Hunt 28: Piscodaemon Event (1)": FF12OpenWorldEventData(
        region="Mt. Bur-Omisace",
        item="Hunt",
        difficulty=5
    ),
    "Hunt 29: Wild Malboro Event (1)": FF12OpenWorldEventData(
        region="Eruyt Village",
        item="Hunt",
        difficulty=6
    ),
    "Hunt 30: Catoblepas Event (1)": FF12OpenWorldEventData(
        region="Jahara",
        item="Hunt",
        difficulty=6
    ),
    "Hunt 31: Fafnir Event (1)": FF12OpenWorldEventData(
        region="Mt. Bur-Omisace",
        item="Hunt",
        difficulty=7
    ),
    "Hunt 32: Pylraster Event (1)": FF12OpenWorldEventData(
        region="Balfonheim",
        item="Hunt",
        difficulty=7
    ),
    "Hunt 33: Cluckatrice Event (1)": FF12OpenWorldEventData(
        region="Giza Plains Dry",
        item="Hunt",
        difficulty=1
    ),
    "Hunt 34: Rocktoise Event (1)": FF12OpenWorldEventData(
        region="Bhujerba",
        item="Hunt",
        difficulty=1
    ),
    "Hunt 35: Orthros Event (1)": FF12OpenWorldEventData(
        region="Lowtown",
        item="Hunt",
        difficulty=5
    ),
    "Hunt 36: Gil Snapper Event (1)": FF12OpenWorldEventData(
        region="Giza Plains Dry",
        item="Hunt",
        difficulty=3
    ),
    "Hunt 37: Trickster Event (1)": FF12OpenWorldEventData(
        region="Mt. Bur-Omisace",
        item="Hunt",
        difficulty=5
    ),
    "Hunt 38: Antlion Event (1)": FF12OpenWorldEventData(
        region="Bhujerba",
        item="Hunt",
        difficulty=5
    ),
    "Hunt 39: Carrot Event (1)": FF12OpenWorldEventData(
        region="Aerodrome",
        item="Hunt",
        difficulty=7
    ),
    "Hunt 39: Carrot Event (2)": FF12OpenWorldEventData(
        region="Aerodrome",
        item="Jovy",
        difficulty=7
    ),
    "Hunt 40: Gilgamesh Event (1)": FF12OpenWorldEventData(
        region="Clan Hall",
        item="Hunt",
        difficulty=7
    ),
    "Hunt 41: Belito Event (1)": FF12OpenWorldEventData(
        region="Clan Hall",
        item="Hunt",
        difficulty=5
    ),
    "Hunt 42: Behemoth King Event (1)": FF12OpenWorldEventData(
        region="Lowtown",
        item="Hunt",
        difficulty=7
    ),
    "Hunt 43: Ixion Event (1)": FF12OpenWorldEventData(
        region="Balfonheim",
        item="Hunt",
        difficulty=6
    ),
    "Hunt 44: Shadowseer Event (1)": FF12OpenWorldEventData(
        region="Clan Hall",
        item="Hunt",
        difficulty=6
    ),
    "Hunt 45: Yiazmat Event (1)": FF12OpenWorldEventData(
        region="Clan Hall",
        item="Hunt",
        difficulty=8
    ),
    "Reddas Event (1)": FF12OpenWorldEventData(
        region="Balfonheim",
        item="Guest",
        difficulty=0
    ),
    "Basch Event (1)": FF12OpenWorldEventData(
        region="Lowtown",
        item="Basch",
        difficulty=0
    ),
    "Thalassinon - Shelled Trophy Event (1)": FF12OpenWorldEventData(
        region="Phon Coast",
        item="HuntClubStart",
        difficulty=6
    ),
    "Gavial - Fur-scaled Trophy Event (1)": FF12OpenWorldEventData(
        region="Garamsythe Waterway",
        item="HuntClubKill",
        difficulty=6
    ),
    "Ishteen - Bony Trophy Event (1)": FF12OpenWorldEventData(
        region="Barheim Passage",
        item="HuntClubKill",
        difficulty=7
    ),
    "Kaiser Wolf - Fanged Trophy Event (1)": FF12OpenWorldEventData(
        region="Dalmasca Westersand",
        item="HuntClubKill",
        difficulty=5
    ),
    "Terror Tyrant - Hide-covered Trophy Event (1)": FF12OpenWorldEventData(
        region="Dalmasca Estersand",
        item="HuntClubKill",
        difficulty=7
    ),
    "Nazarnir - Maned Trophy Event (1)": FF12OpenWorldEventData(
        region="Giza Plains Dry",
        item="HuntClubKill",
        difficulty=7
    ),
    "Alteci - Fell Trophy Event (1)": FF12OpenWorldEventData(
        region="Zertinan Caverns Center",
        item="HuntClubKill",
        difficulty=5
    ),
    "Disma - Accursed Trophy Event (1)": FF12OpenWorldEventData(
        region="Lhusu Mines",
        item="HuntClubKill",
        difficulty=7
    ),
    "Bull Chocobo - Beaked Trophy Event (1)": FF12OpenWorldEventData(
        region="Ogir-Yensa Sandsea",
        item="HuntClubKill",
        difficulty=7
    ),
    "Victanir - Maverick Trophy Event (1)": FF12OpenWorldEventData(
        region="Nam-Yensa Sandsea",
        item="HuntClubKill",
        difficulty=7
    ),
    "Zombie Lord - Soulless Trophy Event (1)": FF12OpenWorldEventData(
        region="Tomb of Raithwall",
        item="HuntClubKill",
        difficulty=6
    ),
    "Dheed - Leathern Trophy Event (1)": FF12OpenWorldEventData(
        region="Mosphoran Highwaste Upper",
        item="HuntClubKill",
        difficulty=7
    ),
    "Rageclaw - Sickle Trophy Event (1)": FF12OpenWorldEventData(
        region="Salikawood NW",
        item="HuntClubKill",
        difficulty=5
    ),
    "Arioch - Vengeful Trophy Event (1)": FF12OpenWorldEventData(
        region="Nabreus Deadlands",
        item="HuntClubKill",
        difficulty=7
    ),
    "Vorres - Gravesoil Trophy Event (1)": FF12OpenWorldEventData(
        region="Necrohol of Nabudis",
        item="HuntClubKill",
        difficulty=7
    ),
    "Killbug - Metallic Trophy Event (1)": FF12OpenWorldEventData(
        region="Ozmone Plain",
        item="HuntClubKill",
        difficulty=6
    ),
    "Melt - Slimy Trophy Event (1)": FF12OpenWorldEventData(
        region="Henne Mines",
        item="HuntClubKill",
        difficulty=7
    ),
    "Biding Mantis - Scythe Trophy Event (1)": FF12OpenWorldEventData(
        region="Golmore Jungle S",
        item="HuntClubKill",
        difficulty=6
    ),
    "Dreadguard - Feathered Trophy Event (1)": FF12OpenWorldEventData(
        region="Feywood",
        item="HuntClubKill",
        difficulty=7
    ),
    "Crystal Knight - Skull Trophy Event (1)": FF12OpenWorldEventData(
        region="Great Crystal",
        item="HuntClubKill",
        difficulty=5
    ),
    "Ancbolder - Mind Trophy Event (1)": FF12OpenWorldEventData(
        region="Paramina Rift",
        item="HuntClubKill",
        difficulty=5
    ),
    "Myath - Eternal Trophy Event (1)": FF12OpenWorldEventData(
        region="Stilshrine of Miriam",
        item="HuntClubKill",
        difficulty=5
    ),
    "Skullash - Clawed Trophy Event (1)": FF12OpenWorldEventData(
        region="Phon Coast",
        item="HuntClubKill",
        difficulty=7
    ),
    "Kris - Odiferous Trophy Event (1)": FF12OpenWorldEventData(
        region="Tchita Uplands",
        item="HuntClubKill",
        difficulty=7
    ),
    "Grimalkin - Whiskered Trophy Event (1)": FF12OpenWorldEventData(
        region="Tchita Uplands",
        item="HuntClubKill",
        difficulty=7
    ),
    "Wendice - Frigid Trophy Event (1)": FF12OpenWorldEventData(
        region="Sochen Cave Palace Middle",
        item="HuntClubKill",
        difficulty=5
    ),
    "Anubys - Ensanguined Trophy Event (1)": FF12OpenWorldEventData(
        region="Sochen Cave Palace Middle",
        item="HuntClubKill",
        difficulty=7
    ),
    "Bluesang - Cruel Trophy Event (1)": FF12OpenWorldEventData(
        region="Cerobi Steppe",
        item="HuntClubKill",
        difficulty=7
    ),
    "Aspidochelon - Adamantine Trophy Event (1)": FF12OpenWorldEventData(
        region="Cerobi Steppe",
        item="HuntClubKill",
        difficulty=7
    ),
    "Abelisk - Reptilian Trophy Event (1)": FF12OpenWorldEventData(
        region="Ridorana Cataract",
        item="HuntClubKill",
        difficulty=7
    ),
    "Avenger - Vile Trophy Event (1)": FF12OpenWorldEventData(
        region="Pharos of Ridorana",
        item="HuntClubKill",
        difficulty=7
    ),
    "Final Boss Victory Event (1)": FF12OpenWorldEventData(
        region="Bahamut",
        item="Victory",
        difficulty=8
    ),
    "Great-chief Elder After Defeating Vossler Event (1)": FF12OpenWorldEventData(
        region="Jahara",
        item="Guest",
        difficulty=2
    ),
    "Amal's Weaponry Shop Event (1)": FF12OpenWorldEventData(
        region="Rabanastre",
        item="Amal's Weaponry Shop",
        difficulty=0
    ),
    "Panamis's Protectives Shop Event (1)": FF12OpenWorldEventData(
        region="Rabanastre",
        item="Panamis's Protectives Shop",
        difficulty=0
    ),
    "Yugri's Magicks Shop Event (1)": FF12OpenWorldEventData(
        region="Rabanastre",
        item="Yugri's Magicks Shop",
        difficulty=0
    ),
    "Batahn's Technicks Shop Event (1)": FF12OpenWorldEventData(
        region="Rabanastre",
        item="Batahn's Technicks Shop",
        difficulty=0
    ),
    "Migelo's Sundries Shop Event (1)": FF12OpenWorldEventData(
        region="Rabanastre",
        item="Migelo's Sundries Shop",
        difficulty=0
    ),
    "Yamoora's Gambits Shop Event (1)": FF12OpenWorldEventData(
        region="Rabanastre",
        item="Yamoora's Gambits Shop",
        difficulty=0
    ),
    "Clan Provisioner 1 Shop Event (1)": FF12OpenWorldEventData(
        region="Rabanastre",
        item="Clan Provisioner 1 Shop",
        difficulty=0
    ),
    "Clan Provisioner 2 Shop Event (1)": FF12OpenWorldEventData(
        region="Rabanastre",
        item="Clan Provisioner 2 Shop",
        difficulty=0
    ),
    "Clan Provisioner 3 Shop Event (1)": FF12OpenWorldEventData(
        region="Rabanastre",
        item="Clan Provisioner 3 Shop",
        difficulty=0
    ),
    "Clan Provisioner 4 Shop Event (1)": FF12OpenWorldEventData(
        region="Rabanastre",
        item="Clan Provisioner 4 Shop",
        difficulty=0
    ),
    "Clan Provisioner 5 Shop Event (1)": FF12OpenWorldEventData(
        region="Rabanastre",
        item="Clan Provisioner 5 Shop",
        difficulty=0
    ),
    "Clan Provisioner 6 Shop Event (1)": FF12OpenWorldEventData(
        region="Rabanastre",
        item="Clan Provisioner 6 Shop",
        difficulty=0
    ),
    "Clan Provisioner 7 Shop Event (1)": FF12OpenWorldEventData(
        region="Rabanastre",
        item="Clan Provisioner 7 Shop",
        difficulty=0
    ),
    "Clan Provisioner 8 Shop Event (1)": FF12OpenWorldEventData(
        region="Rabanastre",
        item="Clan Provisioner 8 Shop",
        difficulty=0
    ),
    "Clan Provisioner 9 Shop Event (1)": FF12OpenWorldEventData(
        region="Rabanastre",
        item="Clan Provisioner 9 Shop",
        difficulty=0
    ),
    "Clan Provisioner 10 Shop Event (1)": FF12OpenWorldEventData(
        region="Rabanastre",
        item="Clan Provisioner 10 Shop",
        difficulty=0
    ),
    "Clan Provisioner 11 Shop Event (1)": FF12OpenWorldEventData(
        region="Rabanastre",
        item="Clan Provisioner 11 Shop",
        difficulty=0
    ),
    "Clan Provisioner 12 Shop Event (1)": FF12OpenWorldEventData(
        region="Rabanastre",
        item="Clan Provisioner 12 Shop",
        difficulty=0
    ),
    "Travelling Merchant North Shop Event (1)": FF12OpenWorldEventData(
        region="Lowtown",
        item="Travelling Merchant North Shop",
        difficulty=0
    ),
    "Travelling Merchant South Shop Event (1)": FF12OpenWorldEventData(
        region="Lowtown",
        item="Travelling Merchant South Shop",
        difficulty=0
    ),
    "Weapons of War Shop Event (1)": FF12OpenWorldEventData(
        region="Nalbina Fortress",
        item="Weapons of War Shop",
        difficulty=0
    ),
    "Antiqued Armors Shop Event (1)": FF12OpenWorldEventData(
        region="Nalbina Fortress",
        item="Antiqued Armors Shop",
        difficulty=0
    ),
    "Mysterious Magicks Shop Event (1)": FF12OpenWorldEventData(
        region="Nalbina Fortress",
        item="Mysterious Magicks Shop",
        difficulty=0
    ),
    "Troublesome Technicks Shop Event (1)": FF12OpenWorldEventData(
        region="Nalbina Fortress",
        item="Troublesome Technicks Shop",
        difficulty=0
    ),
    "Portentous Provisions Shop Event (1)": FF12OpenWorldEventData(
        region="Nalbina Fortress",
        item="Portentous Provisions Shop",
        difficulty=0
    ),
    "Morning Star Gambits Shop Event (1)": FF12OpenWorldEventData(
        region="Nalbina Fortress",
        item="Morning Star Gambits Shop",
        difficulty=0
    ),
    "Targe's Arms Shop Event (1)": FF12OpenWorldEventData(
        region="Bhujerba",
        item="Targe's Arms Shop",
        difficulty=0
    ),
    "Rithil's Protectives Shop Event (1)": FF12OpenWorldEventData(
        region="Bhujerba",
        item="Rithil's Protectives Shop",
        difficulty=0
    ),
    "Mait's Magicks Shop Event (1)": FF12OpenWorldEventData(
        region="Bhujerba",
        item="Mait's Magicks Shop",
        difficulty=0
    ),
    "Clio's Technicks Shop Event (1)": FF12OpenWorldEventData(
        region="Bhujerba",
        item="Clio's Technicks Shop",
        difficulty=0
    ),
    "Street Vendor Shop Event (1)": FF12OpenWorldEventData(
        region="Bhujerba",
        item="Street Vendor Shop",
        difficulty=0
    ),
    "Bashketi's Gambits Shop Event (1)": FF12OpenWorldEventData(
        region="Bhujerba",
        item="Bashketi's Gambits Shop",
        difficulty=0
    ),
    "Vint's Armaments Weapons Shop Event (1)": FF12OpenWorldEventData(
        region="Archades",
        item="Vint's Armaments Weapons Shop",
        difficulty=0
    ),
    "Vint's Armaments Armors Shop Event (1)": FF12OpenWorldEventData(
        region="Archades",
        item="Vint's Armaments Armors Shop",
        difficulty=0
    ),
    "Charlotte's Magickery Shop Event (1)": FF12OpenWorldEventData(
        region="Archades",
        item="Charlotte's Magickery Shop",
        difficulty=0
    ),
    "Bulward's Technicks Shop Event (1)": FF12OpenWorldEventData(
        region="Archades",
        item="Bulward's Technicks Shop",
        difficulty=0
    ),
    "Granch's Requisites Shop Event (1)": FF12OpenWorldEventData(
        region="Archades",
        item="Granch's Requisites Shop",
        difficulty=0
    ),
    "Lebleu's Gambits Shop Event (1)": FF12OpenWorldEventData(
        region="Archades",
        item="Lebleu's Gambits Shop",
        difficulty=0
    ),
    "Beruny's Armaments Weapons Shop Event (1)": FF12OpenWorldEventData(
        region="Balfonheim",
        item="Beruny's Armaments Weapons Shop",
        difficulty=0
    ),
    "Beruny's Armaments Armors Shop Event (1)": FF12OpenWorldEventData(
        region="Balfonheim",
        item="Beruny's Armaments Armors Shop",
        difficulty=0
    ),
    "Quayside Magickery Shop Event (1)": FF12OpenWorldEventData(
        region="Balfonheim",
        item="Quayside Magickery Shop",
        difficulty=0
    ),
    "Odo's Technicks Shop Event (1)": FF12OpenWorldEventData(
        region="Balfonheim",
        item="Odo's Technicks Shop",
        difficulty=0
    ),
    "The Leapin' Bangaa Shop Event (1)": FF12OpenWorldEventData(
        region="Balfonheim",
        item="The Leapin' Bangaa Shop",
        difficulty=0
    ),
    "Waterfront Gambits Shop Event (1)": FF12OpenWorldEventData(
        region="Balfonheim",
        item="Waterfront Gambits Shop",
        difficulty=0
    ),
    "Dyce Shop Event (1)": FF12OpenWorldEventData(
        region="Balfonheim",
        item="Dyce Shop",
        difficulty=0
    ),
    "Unlucky Merchant Shop Event (1)": FF12OpenWorldEventData(
        region="Dalmasca Estersand",
        item="Unlucky Merchant Shop",
        difficulty=0
    ),
    "Lohen Shop Event (1)": FF12OpenWorldEventData(
        region="Dalmasca Westersand",
        item="Lohen Shop",
        difficulty=0
    ),
    "Arjie Shop Event (1)": FF12OpenWorldEventData(
        region="Giza Plains Dry",
        item="Arjie Shop",
        difficulty=0
    ),
    "Burrough Shop Event (1)": FF12OpenWorldEventData(
        region="Barheim Passage Shop",
        item="Burrough Shop",
        difficulty=0
    ),
    "Tetran Shop Event (1)": FF12OpenWorldEventData(
        region="Dreadnought Leviathan",
        item="Tetran Shop",
        difficulty=0
    ),
    "Garif Trader Shop Event (1)": FF12OpenWorldEventData(
        region="Jahara",
        item="Garif Trader Shop",
        difficulty=0
    ),
    "Tetran Shop Event (2)": FF12OpenWorldEventData(
        region="Eruyt Village",
        item="Tetran Shop",
        difficulty=0
    ),
    "Hume Shop Event (1)": FF12OpenWorldEventData(
        region="Mt. Bur-Omisace",
        item="Hume Shop",
        difficulty=0
    ),
    "Seeq Shop Event (1)": FF12OpenWorldEventData(
        region="Mt. Bur-Omisace",
        item="Seeq Shop",
        difficulty=0
    ),
    "Luccio Shop Event (1)": FF12OpenWorldEventData(
        region="Mosphoran Highwaste",
        item="Luccio Shop",
        difficulty=0
    ),
    "Vendor of Goods Shop Event (1)": FF12OpenWorldEventData(
        region="Phon Coast",
        item="Vendor of Goods Shop",
        difficulty=0
    ),
    "Stranded Merchant Shop Event (1)": FF12OpenWorldEventData(
        region="Old Archades",
        item="Stranded Merchant Shop",
        difficulty=0
    ),
    "Baknamy Shop Event (1)": FF12OpenWorldEventData(
        region="Necrohol of Nabudis",
        item="Baknamy Shop",
        difficulty=0
    ),
    "Storekeeper (Rabanastre <-> Bhujerba) Shop Event (1)": FF12OpenWorldEventData(
        region="Skyferry",
        item="Storekeeper (Rabanastre <-> Bhujerba) Shop",
        difficulty=0
    ),
    "Storekeeper (Rabanastre <-> Nalbina) Shop Event (1)": FF12OpenWorldEventData(
        region="Skyferry",
        item="Storekeeper (Rabanastre <-> Nalbina) Shop",
        difficulty=0
    ),
    "Storekeeper (Rabanastre <-> Archades) Shop Event (1)": FF12OpenWorldEventData(
        region="Skyferry",
        item="Storekeeper (Rabanastre <-> Archades) Shop",
        difficulty=0
    ),
    "Storekeeper (Nalbina <-> Archades) Shop Event (1)": FF12OpenWorldEventData(
        region="Skyferry",
        item="Storekeeper (Nalbina <-> Archades) Shop",
        difficulty=0
    ),
    "Storekeeper (Nalbina <-> Balfonheim) Shop Event (1)": FF12OpenWorldEventData(
        region="Skyferry",
        item="Storekeeper (Nalbina <-> Balfonheim) Shop",
        difficulty=0
    ),
    "Storekeeper (Bhujerba <-> Balfonheim) Shop Event (1)": FF12OpenWorldEventData(
        region="Skyferry",
        item="Storekeeper (Bhujerba <-> Balfonheim) Shop",
        difficulty=0
    ),
    "Storekeeper (Archades <-> Balfonheim) Shop Event (1)": FF12OpenWorldEventData(
        region="Skyferry",
        item="Storekeeper (Archades <-> Balfonheim) Shop",
        difficulty=0
    ),
    "Storekeeper (All) Shop Event (1)": FF12OpenWorldEventData(
        region="Skyferry",
        item="Storekeeper (All) Shop",
        difficulty=0
    ),
}
