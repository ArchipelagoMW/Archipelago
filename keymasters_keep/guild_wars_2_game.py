from __future__ import annotations

from typing import List, Set

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class GuildWars2ArchipelagoOptions:
    guild_wars_2_storylines_owned: GuildWars2StorylinesOwned
    guild_wars_2_game_modes: GuildWars2GameModes


class GuildWars2Game(Game):
    # Initial implementation by @feldaar on Discord
    # Expanded by SerpentAI (Exploration + Gathering & Crafting)

    name = "Guild Wars 2"
    platform = KeymastersKeepGamePlatforms.PC

    is_adult_only_or_unrated = False

    options_cls = GuildWars2ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Create a new RACE PROFESSION character",
                data={
                    "RACE": (self.races, 1),
                    "PROFESSION": (self.professions, 1),
                }
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objective_list = [
            GameObjectiveTemplate(
                label="Craft a Legendary",
                data=dict(),
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Gain AP_AMOUNT AP",
                data={
                    "AP_AMOUNT": (self.ap_amounts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=15,
            ),
            GameObjectiveTemplate(
                label="Do DAILY_CATEGORY Dailies",
                data={
                    "DAILY_CATEGORY": (self.daily_categories, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=len(self.daily_categories()) * 5,
            ),
            GameObjectiveTemplate(
                label="Do a WEEKLY_CATEGORY Weekly",
                data={
                    "WEEKLY_CATEGORY": (self.weekly_categories, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=len(self.weekly_categories()) * 5,
            ),
            GameObjectiveTemplate(
                label="Do a Wizard's Vault Special",
                data=dict(),
                is_time_consuming=True,
                is_difficult=False,
                weight=10,
            ),
        ]

        if "Exploration" in self.game_modes_played:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete PERCENTAGE% of ZONE",
                    data={
                        "PERCENTAGE": (self.zone_percentage_range, 1),
                        "ZONE": (self.zones, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Visit the following vistas: VISTAS",
                    data={
                        "VISTAS": (self.vistas, 3),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Visit all points of interest in ZONE",
                    data={
                        "ZONE": (self.zones, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Unlock all waypoints in ZONE",
                    data={
                        "ZONE": (self.zones, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=5,
                ),
            ]

        if "Jumping Puzzle" in self.game_modes_played:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete the JUMPING_PUZZLE jumping puzzle",
                    data={
                        "JUMPING_PUZZLE": (self.jumping_puzzles, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=5,
                ),
            ]

        if "End of Dragons" in self.storylines_owned and "Fishing" in self.game_modes_played:
            objective_list.append(GameObjectiveTemplate(
                label="Catch COUNTx FISHABLE",
                data={
                    "COUNT": (self.fishing_count_range, 1),
                    "FISHABLE": (self.fishables, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ))

        if "Gathering" in self.game_modes_played:
            objective_list += [
                GameObjectiveTemplate(
                    label="Harvest COUNTx HARVESTABLE",
                    data={
                        "COUNT": (self.harvest_count_range, 1),
                        "HARVESTABLE": (self.harvestables, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
                GameObjectiveTemplate(
                    label="Log COUNTx LOGGABLE",
                    data={
                        "COUNT": (self.logging_count_range_high, 1),
                        "LOGGABLE": (self.loggables, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Log COUNTx LOGGABLE",
                    data={
                        "COUNT": (self.logging_count_range_low, 1),
                        "LOGGABLE": (self.loggables_extra, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Mine COUNTx MINEABLE",
                    data={
                        "COUNT": (self.mining_count_range_high, 1),
                        "MINEABLE": (self.mineables, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Mine COUNTx MINEABLE",
                    data={
                        "COUNT": (self.mining_count_range_low, 1),
                        "MINEABLE": (self.mineables_gemstones, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
            ]

        if "Crafting" in self.game_modes_played:
            objective_list.append(
                GameObjectiveTemplate(
                    label="Reach level LEVEL in DISCIPLINE",
                    data={
                        "LEVEL": (self.crafting_discipline_level_range, 1),
                        "DISCIPLINE": (self.crafting_disciplines, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                )
            )

        if "Open World" in self.game_modes_played:
            objective_list.append(GameObjectiveTemplate(
                label="Participate in META_EVENT event",
                data={
                    "META_EVENT": (self.meta_events, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=25,
            ))

        if "Story" in self.game_modes_played:
            objective_list.append(GameObjectiveTemplate(
                label="Complete a story mission from STORYLINE",
                data={
                    "STORYLINE": (self.storylines, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=15,
            ))

        if "WvW" in self.game_modes_played:
            objective_list += [
                GameObjectiveTemplate(
                    label="Capture WVW_OBJECTIVE in WvW",
                    data={
                        "WVW_OBJECTIVE": (self.wvw_objectives, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=25,
                ),
                GameObjectiveTemplate(
                    label="Earn a large skirmish chest",
                    data=dict(),
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10,
                ),
            ]

        if "PvP" in self.game_modes_played:
            objective_list.append(GameObjectiveTemplate(
                label="Play PVP_MATCH_COUNT PvP Matches",
                data={
                    "PVP_MATCH_COUNT": (self.pvp_match_counts, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=15,
            ))

        if "Fractals" in self.game_modes_played:
            objective_list.append(GameObjectiveTemplate(
                label="Run Tier TIER FRACTAL Fractal",
                data={
                    "TIER": (self.fractal_tiers, 1),
                    "FRACTAL": (self.fractals, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=15,
            ))

        if "Dungeons" in self.game_modes_played:
            objective_list.append(GameObjectiveTemplate(
                label="Run DUNGEON",
                data={
                    "DUNGEON": (self.dungeons, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=15,
            ))

        if "Raids" in self.game_modes_played and len(self.raids()) > 0:
            objective_list.append(GameObjectiveTemplate(
                label="Run RAID",
                data={
                    "RAID": (self.raids, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=10,
            ))

        if "Strikes" in self.game_modes_played:
            objective_list.append(GameObjectiveTemplate(
                label="Run STRIKE",
                data={
                    "STRIKE": (self.strikes, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=15,
            ))

        if "Convergences" in self.game_modes_played:
            objective_list.append(GameObjectiveTemplate(
                label="Participate in CONVERGENCE",
                data={
                    "CONVERGENCE": (self.convergences, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=15,
            ))

        return objective_list

    @property
    def storylines_owned(self) -> Set[str]:
        return self.archipelago_options.guild_wars_2_storylines_owned.value

    def storylines(self) -> List[str]:
        return sorted(self.storylines_owned)

    @property
    def game_modes_played(self) -> Set[str]:
        return self.archipelago_options.guild_wars_2_game_modes.value

    @staticmethod
    def races() -> List[str]:
        return [
            "Asura",
            "Charr",
            "Human",
            "Norn",
            "Sylvari",
        ]

    def professions(self) -> List[str]:
        professions = [
            "Guardian",
            "Warrior",
            "Engineer",
            "Ranger",
            "Thief",
            "Elementalist",
            "Mesmer",
            "Necromancer",
        ]

        if "Heart of Thorns" in self.storylines_owned:
            professions.append("Revenant")

        return sorted(professions)

    def daily_categories(self) -> List[str]:
        categories = ["Wizard's Vault"]

        if "Open World" in self.game_modes_played:
            categories += [
                "Blood in the Water",
                "Daily Portal Closer",
            ]
        if "PvP" in self.game_modes_played:
            categories += ["League Participator"]
        if "Strikes" in self.game_modes_played:
            categories += ["Strikes"]
        if "Fractals" in self.game_modes_played:
            categories += ["Fractals"]
        if "End of Dragons" in self.storylines_owned:
            categories += ["End of Dragons"]
        if "Icebrood Saga" in self.storylines_owned:
            categories += ["Icebrood Saga"]
        if "Season 4" in self.storylines_owned:
            categories += ["Living World Season 4"]
        if "Season 3" in self.storylines_owned:
            categories += ["Living World Season 3"]
        if "Janthir Wilds" in self.storylines_owned and "Jumping Puzzles" in self.game_modes_played:
            categories += ["Buzzy Treetops"]

        return categories

    def weekly_categories(self) -> List[str]:
        categories = ["Wizard's Vault"]

        if "WvW" in self.game_modes_played:
            categories += ["WvW"]

        if "Secrets of the Obscure" in self.storylines_owned:
            categories += ["Krytpis Rift Hunting"]

        if "Janthir Wilds" in self.storylines_owned:
            categories += ["Janthir Rift Hunting"]

        return categories

    @staticmethod
    def zone_percentage_range() -> range:
        return range(40, 101, 5)

    def zones(self) -> List[str]:
        zones = [
            "Black Citadel",
            "Blazeridge Steppes",
            "Bloodtide Coast",
            "Brisban Wildlands",
            "Caledon Forest",
            "Cursed Shore",
            "Diessa Plateau",
            "Divinity's Reach",
            "Dredgehaunt Cliffs",
            "Dry Top",
            "Fields of Ruin",
            "Fireheart Rise",
            "Frostgorge Sound",
            "Gendarran Fields",
            "Harathi Hinterlands",
            "Hoelbrak",
            "Iron Marches",
            "Kessex Hills",
            "Lion's Arch",
            "Lornar's Pass",
            "Malchor's Leap",
            "Metrica Province",
            "Mount Maelstrom",
            "Plains of Ashford",
            "Queensdale",
            "Rata Sum",
            "Snowden Drifts",
            "Southsun Cove",
            "Sparkfly Fen",
            "Straits of Devastation",
            "The Grove",
            "The Silverwastes",
            "Timberline Falls",
            "Wayfarer Foothills",
        ]

        if "Heart of Thorns" in self.storylines_owned:
            zones += [
                "Auric Basin",
                "Dragon's Stand",
                "Tangled Depths",
                "Verdant Brink",
            ]

        if "Season 3" in self.storylines_owned:
            zones += [
                "Bitterfrost Frontier",
                "Bloodstone Fen",
                "Draconis Mons",
                "Ember Bay",
                "Lake Doric",
                "Siren's Landing",
            ]

        if "Path of Fire" in self.storylines_owned:
            zones += [
                "Crystal Oasis",
                "Desert Highlands",
                "Domain of Vabbi",
                "Elon Riverlands",
                "The Desolation",
            ]

        if "Season 4" in self.storylines_owned:
            zones += [
                "Domain of Istan",
                "Domain of Kourna",
                "Dragonfall",
                "Jahai Bluffs",
                "Sandswept Isles",
                "Thunderhead Peaks",
            ]

        if "Icebrood Saga" in self.storylines_owned:
            zones += [
                "Bjora Marches",
                "Drizzlewood Coast",
                "Grothmar Valley",
            ]

        if "End of Dragons" in self.storylines_owned:
            zones += [
                "Dragon's End",
                "Gyala Delve",
                "New Kaineng City",
                "Seitung Province",
                "The Echovald Wilds",
            ]

        if "Secrets of the Obscure" in self.storylines_owned:
            zones += [
                "Amnytas",
                "Inner Nayos",
                "Skywatch Archipelago",
            ]

        if "Janthir Wilds" in self.storylines_owned:
            zones += [
                "Janthir Syntri",
                "Lowland Shore",
            ]

        return sorted(zones)

    def vistas(self) -> List[str]:
        vistas = [
            "Aleem's Penance (Sparkfly Fen)",
            "Almuten Mansion (Gendarran Fields)",
            "Altar's Windings (Queensdale)",
            "Amber Sandfall (The Silverwastes)",
            "Applenook Hamlet (Gendarran Fields)",
            "Apprentice Carrels (Rata Sum)",
            "Arterium Haven (Metrica Province)",
            "Ascalon City Ruins (Plains of Ashford)",
            "Ascalon Settlement (Gendarran Fields)",
            "Azabe Qabar (Cursed Shore)",
            "Bandithaunt Caverns (Queensdale)",
            "Barricade Camp (Harathi Hinterlands)",
            "Bay Haven (Caledon Forest)",
            "Bear Lodge (Hoelbrak)",
            "Bear's Jaws Shrine (Dredgehaunt Cliffs)",
            "Benthic Kelp Beds (Mount Maelstrom)",
            "Bilrost Gallery (Hoelbrak)",
            "Black Haven (Kessex Hills)",
            "Bloodcliff Quarry (Diessa Plateau)",
            "Bloodcoast Ward (Lion's Arch)",
            "Blue Ice Shining (Frostgorge Sound)",
            "Bore Lynch (Frostgorge Sound)",
            "Bouldermouth Vale (Lornar's Pass)",
            "Breachwater Lake (Diessa Plateau)",
            "Brill Alliance Labs (Metrica Province)",
            "Butcher's Block (Diessa Plateau)",
            "Cadem Forest (Plains of Ashford)",
            "Caledon Haven (Caledon Forest)",
            "Caledon Path (The Grove)",
            "Camp Resolve (The Silverwastes)",
            "Canton Factorium (Black Citadel)",
            "Cereboth Canyon (Kessex Hills)",
            "Charnel Grounds (The Silverwastes)",
            "Clayent Falls (Queensdale)",
            "Compass Plaza (Cursed Shore)",
            "Concordia (Timberline Falls)",
            "Covington Keep (Bloodtide Coast)",
            "Crash Site (Dry Top)",
            "Crash Site 2 (Dry Top)",
            "Creator's Commons (Rata Sum)",
            "Criterion Canyon (Mount Maelstrom)",
            "Crow's Nest Tavern (Lion's Arch)",
            "Darkriven Bluffs (Wayfarer Foothills)",
            "Deep and Troubled Waters (Frostgorge Sound)",
            "Demon's Maw (Lornar's Pass)",
            "Desider Atum (Metrica Province)",
            "Desperate Passage (The Silverwastes)",
            "Devast District (Plains of Ashford)",
            "Dociu Excavation (Dredgehaunt Cliffs)",
            "Dostoev Sky Peak (Dredgehaunt Cliffs)",
            "Drowned Brine (Malchor's Leap)",
            "Earthshake Basin (Frostgorge Sound)",
            "Earthworks Bluff (Kessex Hills)",
            "Ebbing Heart Run (Iron Marches)",
            "Echoslab Arches (Iron Marches)",
            "False Lake (Lornar's Pass)",
            "False River Valley East (Lornar's Pass)",
            "False River Valley North (Lornar's Pass)",
            "Fields of Gold (Cursed Shore)",
            "Foewatch Encampment (Blazeridge Steppes)",
            "Font of Rhand (Diessa Plateau)",
            "Fort Salma (Kessex Hills)",
            "Fort Trinity (Straits of Devastation)",
            "Garden of Ilya (Malchor's Leap)",
            "Garenhoff (Kessex Hills)",
            "Gates of Flame (Fireheart Rise)",
            "Gauntlet Gulch (Mount Maelstrom)",
            "Gentle River (Timberline Falls)",
            "Giant's Passage (Kessex Hills)",
            "Gladefall Run (Iron Marches)",
            "Gladium Canton (Black Citadel)",
            "Glorious Drill Collective #4 (Bloodtide Coast)",
            "Godslost Swamp (Queensdale)",
            "Gotala Cascade (Brisban Wildlands)",
            "Grand Piazza (Lion's Arch)",
            "Great Helix (The Grove)",
            "Great Imperial Smelter (Black Citadel)",
            "Grey Gritta's (Harathi Hinterlands)",
            "Griffonclaw Peak (Blazeridge Steppes)",
            "Haymal Gore (Fireheart Rise)",
            "Heart of the Bear (Wayfarer Foothills)",
            "Hidden Falls (Harathi Hinterlands)",
            "Hidden Lake (Brisban Wildlands)",
            "Horncall (Wayfarer Foothills)",
            "Human's Lament (Plains of Ashford)",
            "Hunter's Gorge (Fields of Ruin)",
            "Icedevil's Needle (Lornar's Pass)",
            "Incendio Templum (Diessa Plateau)",
            "Incinergen Labs (Metrica Province)",
            "Indigo Cave (The Silverwastes)",
            "Inner Harbor North (Lion's Arch)",
            "Inner Harbor West (Lion's Arch)",
            "Inquest Base (Dry Top)",
            "Inquest Outer Complex (Metrica Province)",
            "Izz-al-Din Sarayi (Straits of Devastation)",
            "Jelako Cliffrise (Bloodtide Coast)",
            "Jormabakke Stead (Snowden Drifts)",
            "Junction Camp (Harathi Hinterlands)",
            "King Jalis's Refuge (Snowden Drifts)",
            "Kiriel Rock (Timberline Falls)",
            "Koga Ruins (Brisban Wildlands)",
            "Kraitbane Haven (Caledon Forest)",
            "Krongar Pass (Timberline Falls)",
            "Krytan Freeholds (Queensdale)",
            "Lair of the Seawitch (Kessex Hills)",
            "Lake Adorea (Plains of Ashford)",
            "Lake Feritas (Plains of Ashford)",
            "Lake Mourn (Hoelbrak)",
            "Leopard's Snarl Shrine (Dredgehaunt Cliffs)",
            "Ley Line Hub (Dry Top)",
            "Ligacus Notus (Black Citadel)",
            "Lightfoot Passage (Straits of Devastation)",
            "Loreclaw Expanse (Plains of Ashford)",
            "Lost Delver's Ridge (Lornar's Pass)",
            "Maelstrom's Bile (Mount Maelstrom)",
            "Malchor's Fingers (Malchor's Leap)",
            "Mantelet Refuge (Dredgehaunt Cliffs)",
            "Martyr's Woods (Plains of Ashford)",
            "Mithric Cliffs (Fields of Ruin)",
            "Molensk (Wayfarer Foothills)",
            "Monument Grounds (Blazeridge Steppes)",
            "Nebo Terrace (Gendarran Fields)",
            "Nemeton Grove (Brisban Wildlands)",
            "Nentor Valley (Lornar's Pass)",
            "Northern Shelf (The Silverwastes)",
            "Northfields (Gendarran Fields)",
            "Ogham Wilds (Caledon Forest)",
            "Old Lion's Arch (Lion's Arch)",
            "Orsippus (Frostgorge Sound)",
            "Orvanic Cliffs (Sparkfly Fen)",
            "Orvanic Shore (Sparkfly Fen)",
            "Ossan Quarter (Divinity's Reach)",
            "Owl Lodge (Snowden Drifts)",
            "Pale Tree's Circle (The Grove)",
            "Phoenix Roost (Lion's Arch)",
            "Pig Iron Mine (Fireheart Rise)",
            "Plaza of Grenth (Divinity's Reach)",
            "Plaza of Lissa (Divinity's Reach)",
            "Plaza of Melandru (Divinity's Reach)",
            "Pockmark Roughs (Blazeridge Steppes)",
            "Podaga Steading (Snowden Drifts)",
            "Portage Hills (Bloodtide Coast)",
            "Postern Ward (Lion's Arch)",
            "Provatum Castrum (Fireheart Rise)",
            "Quarryside (Kessex Hills)",
            "Raptor Prowl (Dry Top)",
            "Rata Sum Port Authority (Rata Sum)",
            "Reaper's Corridor (Diessa Plateau)",
            "Red Rock Bastion (The Silverwastes)",
            "Ronan's Bower (The Grove)",
            "Ruins of Rin (Black Citadel)",
            "Saltflood Mire (Sparkfly Fen)",
            "Scorchlands (Iron Marches)",
            "Sentinel's Perch (Fields of Ruin)",
            "Seraph's Landing (Harathi Hinterlands)",
            "Shadow Cleft (Fireheart Rise)",
            "Shaemoor Fields (Queensdale)",
            "Shaemoor Garrison (Queensdale)",
            "Sharkmaw Caverns (Lion's Arch)",
            "Shire of Beetletun (Queensdale)",
            "Shoadowheart Site (Kessex Hills)",
            "Sipedon Deeps (Timberline Falls)",
            "Skovtrolde Hearthstead (Dredgehaunt Cliffs)",
            "Skrittsburgh Tunnels (Brisban Wildlands)",
            "Slade's Bay (Gendarran Fields)",
            "Sleive's Inlet (Caledon Forest)",
            "Sloven Pitch (Fireheart Rise)",
            "Sniper's Woods (Fields of Ruin)",
            "Snow Leopard (Hoelbrak)",
            "Snowlord's Gate (Wayfarer Foothills)",
            "Sootberme (Mount Maelstrom)",
            "Southshore Wastes (Iron Marches)",
            "Sparring Rock (Dry Top)",
            "Splintered Coast (Sparkfly Fen)",
            "Splorge Metamystics (Metrica Province)",
            "Starbower Nursery (The Grove)",
            "Stonefish Beach (Gendarran Fields)",
            "Stonesheath Overlook (Iron Marches)",
            "Stonesledge Draft (Frostgorge Sound)",
            "Stormbluff Beacon (Bloodtide Coast)",
            "Stronhold of Ebonhawke (Fields of Ruin)",
            "Stygian Deeps (Straits of Devastation)",
            "Sunshade Caves (Metrica Province)",
            "Svanir's Dome (Wayfarer Foothills)",
            "Synergetics Union (Rata Sum)",
            "Terra Combusta (Blazeridge Steppes)",
            "Thaumanova Reactor (Metrica Province)",
            "The Blasted Moors (Diessa Plateau)",
            "The Breached Wall (Diessa Plateau)",
            "The Crown Pavilion (Divinity's Reach)",
            "The Golem Mines (Rata Sum)",
            "The Granite Front (Iron Marches)",
            "The Great Lodge (Hoelbrak)",
            "The Maker's Path (The Grove)",
            "The Mire Sea (Mount Maelstrom)",
            "The Osenfold Shear (Wayfarer Foothills)",
            "The Shadowhorns (Wayfarer Foothills)",
            "The Shattered Henge (Brisban Wildlands)",
            "The Shipyard (Cursed Shore)",
            "The Stychs (Mount Maelstrom)",
            "The Thunderhorns (Lornar's Pass)",
            "The Toppled Wall (Plains of Ashford)",
            "The Undermarket (Lion's Arch)",
            "The Upper City (Divinity's Reach)",
            "The Vizier's Tower (Straits of Devastation)",
            "Theater of Delight (Malchor's Leap)",
            "Thunder Rock (Harathi Hinterlands)",
            "Titan's Staircase (Caledon Forest)",
            "Town of Cowlfang (Iron Marches)",
            "Town of Nageling (Diessa Plateau)",
            "Town of Nolan (Diessa Plateau)",
            "Trapper's Labyrinth (Snowden Drifts)",
            "Trebusha's Overlook (Harathi Hinterlands)",
            "Tribulation Rift (Dredgehaunt Cliffs)",
            "Trionic Lattice (Frostgorge Sound)",
            "Triumph Plaza (Straits of Devastation)",
            "Troll's Teeth (Dredgehaunt Cliffs)",
            "Tuyere Command Post (Fireheart Rise)",
            "Twinspur Haven (Wayfarer Foothills)",
            "Unseen Ruins (Caledon Forest)",
            "Valance Tutory (Timberline Falls)",
            "Venison Pass (Lornar's Pass)",
            "Venlin Vale (Brisban Wildlands)",
            "Ventry Bay (Caledon Forest)",
            "Victor's Presidium (Plains of Ashford)",
            "Vidius Castrum (Fireheart Rise)",
            "Vigil Keep (Gendarran Fields)",
            "Villmark Foothills (Snowden Drifts)",
            "Vindar's Lagoon (Bloodtide Coast)",
            "Warrior's Crown (Fields of Ruin)",
            "Western Divinity Dam (Queensdale)",
            "Western Ward (Lion's Arch)",
            "Whisper Bay (Malchor's Leap)",
            "Whisperwill Bogs (Bloodtide Coast)",
            "Wildflame Caverns (Metrica Province)",
            "Winterknell Shore (Cursed Shore)",
            "Wurmhowl Spikes (Wayfarer Foothills)",
            "Wynchona Rally Point (Harathi Hinterlands)",
            "Yak's Bend (Frostgorge Sound)",
        ]

        if "Heart of Thorns" in self.storylines_owned:
            vistas += [
                "Bristleback Chasm (Auric Basin)",
                "Burnisher Quarry (Auric Basin)",
                "Central Barbed Gate (Dragon's Stand)",
                "Deeproot Sink (Tangled Depths)",
                "Dragon's Domain (Dragon's Stand)",
                "Exhumed Delve (Dragon's Stand)",
                "Inner Chamber (Auric Basin)",
                "Jaka Itzel (Verdant Brink)",
                "Mellaggan's Valor (Verdant Brink)",
                "New Skrittington (Auric Basin)",
                "Northern Barbed Gate (Dragon's Stand)",
                "Rata Novus (Tangled Depths)",
                "Rooted Copse (Dragon's Stand)",
                "SCAR Bivouac (Tangled Depths)",
                "SCAR Lane (Tangled Depths)",
                "Shrouded Ruins (Verdant Brink)",
                "Snarled Frontier (Verdant Brink)",
                "Southern Barbed Gate (Dragon's Stand)",
                "Stonetwist Paths (Verdant Brink)",
                "Tangled Descent (Tangled Depths)",
                "Tarir (Auric Basin)",
                "Teku Nuhoch (Tangled Depths)",
                "The Falls (Auric Basin)",
                "Uprooted Paradise (Verdant Brink)",
                "Wyvern Scar (Dragon's Stand)",
            ]

        if "Season 3" in self.storylines_owned:
            vistas += [
                "Basalt Rise (Ember Bay)",
                "Caliph's Steps (Ember Bay)",
                "Castaway Circus (Ember Bay)",
                "Cavern of Unseen Lights (Bloodstone Fen)",
                "Chokocooka's Throne (Bitterfrost Frontier)",
                "Colosseum of the Faithful (Bloodstone Fen)",
                "Doric Lumberyard (Lake Doric)",
                "Doric's Landing (Lake Doric)",
                "Dragon's Teeth Hot Springs (Bitterfrost Frontier)",
                "Fort Evennia (Lake Doric)",
                "Fractured Caldera (Ember Bay)",
                "Fragmented Wastes (Bloodstone Fen)",
                "Harvest Cascades (Lake Doric)",
                "Heathen's Hold (Draconis Mons)",
                "Infernal Cape (Ember Bay)",
                "Joyless Falls (Bitterfrost Frontier)",
                "Lakeside Bazaar (Lake Doric)",
                "Mariner's Landing (Draconis Mons)",
                "Melandru's Flourish (Lake Doric)",
                "Mosaic Bower (Siren's Landing)",
                "New Loamhurst (Lake Doric)",
                "Osprey Pillars (Ember Bay)",
                "Pedestal of Flames (Ember Bay)",
                "Rata Arcanum (Draconis Mons)",
                "Ruined Panorama (Siren's Landing)",
                "Savage Rise (Draconis Mons)",
                "Scalding Gorge (Draconis Mons)",
                "Sorrow's Eclipse (Bitterfrost Frontier)",
                "The Arm of Abaddon (Siren's Landing)",
                "The Svanir Hive (Bitterfrost Frontier)",
                "Updraft Alley (Siren's Landing)",
                "Watcher's Hollow (Lake Doric)",
                "Watchtower Cliffs (Lake Doric)",
            ]

        if "Path of Fire" in self.storylines_owned:
            vistas += [
                "Acrid Springs (The Desolation)",
                "Amnoon Harbor (Crystal Oasis)",
                "Arid Gladefields (Elon Riverlands)",
                "Augury Rock (Elon Riverlands)",
                "Boundary Preserve (The Desolation)",
                "Brightwater Inlet (Desert Highlands)",
                "Deadlock Sweep (Elon Riverlands)",
                "Destiny's Gorge (Crystal Oasis)",
                "Diviner's Passage (Crystal Oasis)",
                "Elon Riverbank (Elon Riverlands)",
                "Elona Reach (Crystal Oasis)",
                "Enchanted Bluffs (Desert Highlands)",
                "Fortune's Vale (Desert Highlands)",
                "Free City of Amnoon (Crystal Oasis)",
                "Garden of Seborhin (Domain of Vabbi)",
                "Godfall Tower (Desert Highlands)",
                "Grand Court of Sebelkeh (Domain of Vabbi)",
                "Hanging Gardens (Domain of Vabbi)",
                "Hatari Tablelands (Crystal Oasis)",
                "Joko's Domain (The Desolation)",
                "Kodash Bazaar (Domain of Vabbi)",
                "Lair of the Forgotten (The Desolation)",
                "Lifeblood Ravine (Desert Highlands)",
                "Mekele Bluffs (Crystal Oasis)",
                "Northern Way Station (Crystal Oasis)",
                "Omiramba Sand Sea (Crystal Oasis)",
                "Palawa Cut (The Desolation)",
                "Prickpatch Hollow (Desert Highlands)",
                "Prophet's Fall (Desert Highlands)",
                "Prophet's Path (Elon Riverlands)",
                "Salt Flats (Desert Highlands)",
                "Sand Jackal Run (The Desolation)",
                "Shallows of Despair (Elon Riverlands)",
                "Shoals of Sovereignty (Elon Riverlands)",
                "Stampede Uplands (Desert Highlands)",
                "The Foundry (Domain of Vabbi)",
                "The Necropolis (Domain of Vabbi)",
                "The Quickmire (Elon Riverlands)",
                "The Ruination (The Desolation)",
                "The Ruptured Heart (The Desolation)",
                "The Scavengelands (Elon Riverlands)",
                "The Scourgeway (The Desolation)",
                "The Sinking Ruins (Crystal Oasis)",
                "The Spillway (The Desolation)",
                "Tomb of the Primeval Kings (Desert Highlands)",
                "Vehtendi Academy (Domain of Vabbi)",
                "Venjin Palace (Domain of Vabbi)",
                "Whispering Grottos (Elon Riverlands)",
                "Winter's Teeth (Desert Highlands)",
                "Yahnur Plateau (Domain of Vabbi)",
                "Zagonur Cliffs (Domain of Vabbi)",
            ]

        if "Season 4" in self.storylines_owned:
            vistas += [
                "Argon Garrison (Jahai Bluffs)",
                "Astralarium (Domain of Istan)",
                "Atholma (Sandwept Isles)",
                "Champion's Dawn (Domain of Istan)",
                "Churrhir Cliffs (Domain of Istan)",
                "Deldrimor Ruins (Thunderhead Peaks)",
                "Displaced Towers (Jahai Bluffs)",
                "Fortress of Jahai (Jahai Bluffs)",
                "Freetrader Haven (Domain of Istan)",
                "Gnarlgrove (Domain of Kourna)",
                "Grenth's Teeth (Domain of Kourna)",
                "Griffonstone Buttresses (Sandswept Isles)",
                "Heretic's Arena (Domain of Istan)",
                "Hundar Pike (Thunderhead Peaks)",
                "Ice Floe (Thunderhead Peaks)",
                "Jungle Anomaly (Jahai Bluffs)",
                "Melandru's Chalice (Domain of Kourna)",
                "Mosswood (Domain of Kourna)",
                "Necrotic Coast (Domain of Kourna)",
                "Pact Command (Domain of Kourna)",
                "Palawadan (Domain of Istan)",
                "Reclaimed Chantry (Jahai Bluffs)",
                "Reserve Generator Site (Sandswept Isles)",
                "Ruined Procession (Jahai Bluffs)",
                "Scorched Cliffs (Domain of Kourna)",
                "Symphony's Haven (Thunderhead Peaks)",
                "The Forge (Thunderhead Peaks)",
                "The Grotto (Thunderhead Peaks)",
                "The Hunting Grounds (Sandwept Isles)",
                "Thunderhead Keep (Thunderhead Peaks)",
                "Umbral Battlegrounds (Domain of Kourna)",
                "Yatendi Village (Jahai Bluffs)",
            ]

        if "Icebrood Saga" in self.storylines_owned:
            vistas += [
                "Archstone Coast (Drizzlewood Coast)",
                "Asgeir's Legacy (Bjora Marches)",
                "Breakroot Basin (Drizzlewood Coast)",
                "Burning Effigy (Grothmar Valley)",
                "Canopy Crag (Drizzlewood Coast)",
                "Doomlore Ruins (Grothmar Valley)",
                "Drizzlewood Peak (Drizzlewood Coast)",
                "Eaglewatch Rise (Bjora Marches)",
                "Fallen Mountains (Bjora Marches)",
                "Fallen Ruins (Bjora Marches)",
                "Flame Legion Camp (Grothmar Valley)",
                "Fort Defiance (Drizzlewood Coast)",
                "Frostborn Cascades (Bjora Marches)",
                "Ice Spire Peaks (Bjora Marches)",
                "Iron Legion Camp (Grothmar Valley)",
                "Khan-Ur's Gauntlet (Grothmar Valley)",
                "Leadfoot Village Northeast (Drizzlewood Coast)",
                "Leadfoot Village Southwest (Drizzlewood Coast)",
                "Lighthouse Point (Drizzlewood Coast)",
                "Lower Blood Keep (Grothmar Valley)",
                "Petraj Overlook (Drizzlewood Coast)",
                "Port Cascadia (Drizzlewood Coast)",
                "Rusty Meadows (Grothmar Valley)",
                "Sacnoth Stream (Grothmar Valley)",
                "Sentinel Bay (Drizzlewood Coast)",
                "Southern Mountains (Bjora Marches)",
                "Spirits' Refuge (Bjora Marches)",
                "The Bloodfield Northeast (Drizzlewood Coast)",
                "The Bloodfield Northwest (Drizzlewood Coast)",
                "The Ooze Pit (Grothmar Valley)",
                "The Overlook (Grothmar Valley)",
                "Umbral Grotto (Drizzlewood Coast)",
                "Vloxen Mine (Drizzlewood Coast)",
                "Wolf's Crossing (Drizzlewood Coast)",
            ]

        if "End of Dragons" in self.storylines_owned:
            vistas += [
                "Archipelagos Rim (Dragon's End)",
                "Argo Crawler (Dragon's End)",
                "Brotherhood Woodlands (The Echovald Wilds)",
                "Garden Heights (New Kaineng City)",
                "Grub Lane (New Kaineng City)",
                "Haiju Lagoon (Seitung Province)",
                "Howling Caves (Gyala Delve)",
                "Juno Hatchery (Dragon's End)",
                "Kaolai Tower (Dragon's End)",
                "Kurzick Cemetery (The Echovald Wilds)",
                "Lake Lutgardis (The Echovald Wilds)",
                "Lutgardis Plaza (New Kaineng City)",
                "Ministry Ward (New Kaineng City)",
                "North Peninsula (Seitung Province)",
                "Old Kaineng (New Kaineng City)",
                "Qinkaishi Basin (The Echovald Wilds)",
                "Seitung Harbor (Seitung Province)",
                "Shing Jea Monastery (Seitung Province)",
                "Shinota Shore (Seitung Province)",
                "Southern Bluffs (Dragon's End)",
                "The Deep (Gyala Delve)",
                "The Hollow (Gyala Delve)",
                "Warden's Folly (The Echovald Wilds)",
            ]

        if "Secrets of the Obscure" in self.storylines_owned:
            vistas += [
                "Bastion of Balance (Amnytas)",
                "Bastion of Knowledge (Amnytas)",
                "Bastion of Strength (Amnytas)",
                "Botanical Skygarden (Amnytas)",
                "Celestial Control Ring (Amnytas)",
                "Defiled Cradle North (Inner Nayos)",
                "Defiled Cradle South (Inner Nayos)",
                "Devastated Garenhoff (Skywatch Archipelago)",
                "Droknar's Light (Skywatch Archipelago)",
                "Heitor's Dominion (Inner Nayos)",
                "Jade Mech Habitation Zone 03 (Skywatch Archipelago)",
                "Memory's Hollow (Inner Nayos)",
                "Nyedra Dreamer's Sanctum (Inner Nayos)",
                "Primal Maguuma (Skywatch Archipelago)",
                "Rata Novus Promenade (Skywatch Archipelago)",
                "Skyward Marshes (Skywatch Archipelago)",
                "Southern Wizard's Tower (Skywatch Archipelago)",
                "Spellcrafting Workshop (Amnytas)",
                "Spireshadow Lagoon (Amnytas)",
                "Spiritual Center (Amnytas)",
                "The Bleeding Wastes (Inner Nayos)",
                "The Midnight Abyss (Inner Nayos)",
                "Wizard's Ascent (Skywatch Archipelago)",
            ]

        if "Janthir Wilds" in self.storylines_owned:
            vistas += [
                "Autumn's Vale (Lowland Shore)",
                "Blood Hill (Janthir Syntri)",
                "Coursing Upland Northwest (Lowland Shore)",
                "Coursing Upland Southeast (Lowland Shore)",
                "Echoing Hills (Janthir Syntri)",
                "Haar Mire (Lowland Shore)",
                "Harvest Den East (Lowland Shore)",
                "Harvest Den West (Lowland Shore)",
                "Harvest Shore (Lowland Shore)",
                "Moldering Greenwood (Janthir Syntri)",
                "Moon Camp Covert (Lowland Shore)",
                "Old Hutment Site North (Janthir Syntri)",
                "Old Hutment Site South (Janthir Syntri)",
                "Slithering Outskirts (Janthir Syntri)",
                "Sulfurous Springs (Janthir Syntri)",
                "Tumultuous Sea (Janthir Syntri)",
            ]

        return sorted(vistas)

    def jumping_puzzles(self) -> List[str]:
        jumping_puzzles = [
            "Antre of Adjournment (Malchor's Leap)",
            "Behem Gauntlet (Blazeridge Steppes)",
            "Branded Mine (Fields of Ruin)",
            "Buried Archives (Cursed Shore)",
            "Chaos Crystal Cavern (Iron Marches)",
            "Coddler's Cove (Timberline Falls)",
            "Conundrum Cubed (Mount Maelstrom)",
            "Craze's Folly (Blazeridge Steppes)",
            "Crimson Plateau (Diessa Plateau)",
            "Dark Reverie (Calendon Forest)",
            "Demongrub Pits (Queensdale)",
            "Fawcett's Bounty (Harathi Hinterlands)",
            "Goemm's Lab (Metrica Province)",
            "Grendich Gamble (Diessa Plateau)",
            "Griffonrook Run (Lornar's Pass)",
            "Hexfoundry Unhinged (Sparkfly Fen)",
            "Hidden Garden (Mount Maelstrom)",
            "King Jalis's Refuge (Snowden Drifts)",
            "Loreclaw Expanse (Plains of Ashford)",
            "Morgan's Leap (Caledon Forest)",
            "Not So Secret (Gendarran Fields)",
            "Only Zuhl (Timberline Falls)",
            "Pig Iron Quarry (Fireheart Rise)",
            "Professor Portmatt's Lab (Bloodtide Coast)",
            "Prospect Valley Crash Site (Dry Top)",
            "Retrospective Runaround (The Silverwastes)",
            "Scavenger's Chasm (Malchor's Leap)",
            "Shaman's Rookery (Wayfarer Foothills)",
            "Shattered Ice Ruins (Frostgorge Sound)",
            "Skipping Stones (Southsun Cove)",
            "Spekk's Labortory (Caledon Forest)",
            "Spelunker's Delve (Caledon Forest)",
            "The Collapsed Observatory (Gendarran Fields)",
            "Tribulation Caverns (Dredgehaunt Cliffs)",
            "Tribulation Rift Scaffolding (Dredgehaunt Cliffs)",
            "Troll's Revenge (Lion's Arch)",
            "Under New Management (Southsun Cove)",
            "Urmaug's Secret (Lion's Arch)",
            "Verarium Delves (Sparkfly Fen)",
            "Vizier's Tower (Straits of Devastation)",
            "Wall Breach Blitz (Diessa Plateau)",
            "Weyandt's Revenge (Lion's Arch)",
        ]

        if "Season 1" in self.storylines_owned:
            jumping_puzzles += [
                "Troll's End (Memory of Old Lion's Arch)",
            ]

        if "Heart of Thorns" in self.storylines_owned:
            jumping_puzzles += [
                "Disco Dancing Delver (Tangled Depths)",
                "Egg Bearer (Auric Basin)",
                "Highest Gear (Auric Basin)",
                "Master Mushroom Spelunker (Tangled Depths)",
            ]

        if "Season 3" in self.storylines_owned:
            jumping_puzzles += [
                "Abbadon's Ascent (Siren's Landing)",
                "Searing Ascent (Draconis Mons)",
                "Skip up the Volcano (Ember Bay)",
            ]

        if "Season 4" in self.storylines_owned:
            jumping_puzzles += [
                "Displaced Vizier's Tower (Jahai Bluffs)",
            ]

        if "Icebrood Saga" in self.storylines_owned:
            jumping_puzzles += [
                "Gauntlet of the Khan-Ur (Grothmar Valley)",
            ]

        if "End of Dragons" in self.storylines_owned:
            jumping_puzzles += [
                "Trials of the Tengu (Seitung Province)",
                "Wind through the Walls (New Kaineng City)",
            ]

        if "Janthir Wilds" in self.storylines_owned:
            jumping_puzzles += [
                "Queen's Confidence (Lowland Shore)",
                "Treetop Beehive (Lowland Shore)",
                "Vale Brazier (Lowland Shore)",
            ]

        return sorted(jumping_puzzles)

    @staticmethod
    def harvest_count_range() -> range:
        return range(12, 41)

    def harvestables(self) -> List[str]:
        harvestables = [
            "Artichoke",
            "Asparagus Spear",
            "Bay Leaf",
            "Beet",
            "Black Peppercorn",
            "Blackberry",
            "Blueberry",
            "Butternut Squash",
            "Carrot",
            "Cayenne Pepper",
            "Chili Pepper",
            "Clam",
            "Clove",
            "Coral Chunk",
            "Coral Orb",
            "Coral Tentacle",
            "Coriander Seed",
            "Dill Sprig",
            "Ghost Pepper",
            "Grape",
            "Green Onion",
            "Head of Cabbage",
            "Head of Cauliflower",
            "Head of Garlic",
            "Head of Lettuce",
            "Kale Leaf",
            "Leek",
            "Lemongrass",
            "Lotus Root",
            "Mint Leaf",
            "Mushroom",
            "Nopal",
            "Omnomberry",
            "Onion",
            "Oregano Leaf",
            "Orrian Truffle",
            "Parsley Leaf",
            "Parsnip",
            "Passion Flower",
            "Passion Fruit",
            "Pearl",
            "Portobello Mushroom",
            "Potato",
            "Prickly Pear",
            "Raspberry",
            "Rosemary Sprig",
            "Rutabaga",
            "Saffron Thread",
            "Sage Leaf",
            "Seaweed",
            "Sesame Seed",
            "Snow Truffle",
            "Spinach Leaf",
            "Strawberry",
            "Sugar Pumpkin",
            "Tarragon Leaves",
            "Thyme Leaf",
            "Turnip",
            "Vanilla Bean",
            "Yam",
            "Zucchini",
        ]

        if "Heart of Thorns" in self.storylines_owned:
            harvestables += [
                "Cassava Root",
                "Flax Blossom",
                "Flax Fiber",
                "Freshwater Pearl",
                "Giant Mushroom Spore",
                "Jungle Grass Seed",
                "Maguuma Lily",
                "Mussel",
                "Piece of Mother-of-Pearl",
                "Pile of Allspice Berries",
                "Pile of Flax Seeds",
                "Sawgill Mushroom",
            ]

        if "Path of Fire" in self.storylines_owned:
            harvestables += [
                "Handful of Red Lentils",
            ]

        return sorted(harvestables)

    @staticmethod
    def logging_count_range_low() -> range:
        return range(3, 10)

    @staticmethod
    def logging_count_range_high() -> range:
        return range(50, 101)

    @staticmethod
    def loggables() -> List[str]:
        return [
            "Ancient Wood Log",
            "Elder Wood Log",
            "Green Wood Log",
            "Hard Wood Log",
            "Seasoned Wood Log",
            "Soft Wood Log",
        ]

    @staticmethod
    def loggables_extra() -> List[str]:
        return [
            "Amber Pebble",
            "Cinnamon Stick",
            "Foxfire Cluster",
            "Walnut",
        ]

    @staticmethod
    def mining_count_range_low() -> range:
        return range(10, 31)

    @staticmethod
    def mining_count_range_high() -> range:
        return range(50, 101)

    @staticmethod
    def mineables() -> List[str]:
        return [
            "Copper Ore",
            "Gold Ore",
            "Iron Ore",
            "Mithril Ore",
            "Orichalcum Ore",
            "Platinum Ore",
            "Silver Ore",
        ]

    @staticmethod
    def mineables_gemstones() -> List[str]:
        return [
            "Amethyst Lump",
            "Amethyst Nugget",
            "Beryl Crystal",
            "Beryl Orb",
            "Beryl Shard",
            "Carnelian Lump",
            "Carnelian Nugget",
            "Chrysocola Crystal",
            "Chrysocola Orb",
            "Chrysocola Shard",
            "Emerald Crystal",
            "Emerald Orb",
            "Emerald Shard",
            "Garnet Pebble",
            "Lapis Lump",
            "Lapis Nugget",
            "Malachite Pebble",
            "Opal Crystal",
            "Opal Orb",
            "Opal Shard",
            "Peridot Lump",
            "Peridot Nugget",
            "Ruby Crystal",
            "Ruby Orb",
            "Ruby Shard",
            "Sapphire Crystal",
            "Sapphire Orb",
            "Sapphire Shard",
            "Spinel Lump",
            "Spinel Nugget",
            "Sunstone Lump",
            "Sunstone Nugget",
            "Tiger's Eye Pebble",
            "Topaz Lump",
            "Topaz Nugget",
            "Turquoise Pebble",
        ]

    @staticmethod
    def fishing_count_range() -> range:
        return range(5, 16)

    def fishables(self) -> List[str]:
        fishables = [
            "Abyssal Squid",
            "Alabaster Oscar",
            "Albino Axolotl",
            "Albino Blindfish",
            "Albino Gourami",
            "Alewife",
            "Alpine Char",
            "Amber Trout",
            "Amberjack",
            "Aquatic Frog",
            "Arapaima",
            "Armored Scalefish",
            "Arowana",
            "Aurelian Herring",
            "Axolotl",
            "Beacon's Perch",
            "Benthic Behemoth",
            "Bicuda",
            "Bitterling",
            "Black Bass",
            "Black Carp",
            "Black Crappie",
            "Black Lionfish",
            "Blobfish",
            "Bloodfish",
            "Blowfish",
            "Blue Dorado",
            "Bluefin Trevally",
            "Bluefin Tuna",
            "Bluegill",
            "Bonefish",
            "Boreal Cod",
            "Boxfish",
            "Brackish Goby",
            "Branded Eel",
            "Bream",
            "Brook Trout",
            "Bullhead Catfish",
            "Canthan Carp",
            "Catfish",
            "Cerulean Salamander",
            "Chain Pickerel",
            "Chambered Nautilus",
            "Cherry Barb",
            "Cherry Salmon",
            "Chestnut Sea Bream",
            "Clawfish",
            "Corvina",
            "Crimson Snapper",
            "Croaker",
            "Cutlass Fish",
            "Cutthroat Trout",
            "Cuttlefish",
            "Daijun Blackfin",
            "Dark Sleeper",
            "Dead Alewife",
            "Delavan Guppy",
            "Dhuum Fish",
            "Divinity Angelfin",
            "Dragonet",
            "Dragonfish",
            "Dunkleosteus",
            "Dusky Grouper",
            "Dustfish",
            "Electric Eel",
            "Emerald Snapper",
            "Emperor Fish",
            "Fangfish",
            "Fire Eel",
            "Firemouth",
            "Flamefin Betta",
            "Flapjack Octopus",
            "Flayfin",
            "Flying Fish",
            "Freshwater Eel",
            "Frilled Shark",
            "Fugu Fish",
            "Gar",
            "Garnet Ram",
            "Geyser Batfin",
            "Ghostfish",
            "Giant Catfish",
            "Giant Gourami",
            "Giant Octopus",
            "Giant Trevally",
            "Glacial Snakehead",
            "Globefish",
            "Glowing Coalfish",
            "Golden Dorado",
            "Golden Trout",
            "Goldfish",
            "Goliath Grouper",
            "Googly-Eyed Squid",
            "Gourami",
            "Grayling",
            "Green Sawfish",
            "Hagfish",
            "Halibut",
            "Holy Mackerel",
            "Honeycomb Grouper",
            "Horseshoe Crab",
            "Humphead Wrasse",
            "Icefish",
            "Icy Lumpfish",
            "Igneous Rockfish",
            "Jade Lamprey",
            "Jade Sea Turtle",
            "Jundia",
            "Kahawai",
            "King Salmon",
            "Knifefish",
            "Krytan Crawfish",
            "Krytan Puffer",
            "Largemouth Bass",
            "Leafy Sea Dragon",
            "Lornar's Bass",
            "Magma Ray",
            "Maguuma Jack",
            "Maguuma Trout",
            "Man-of-War",
            "Mantis Shrimp",
            "Mega Prawn",
            "Melandru's Lurker",
            "Monkfish",
            "Moonfin Striker",
            "Mud Skate",
            "Mullet",
            "Murkwater Darter",
            "Muskellunge",
            "Mystic Remora",
            "Northern Pike",
            "Oarfish",
            "Old Whiskers",
            "Orrian Anglerfish",
            "Oscar",
            "Pacu",
            "Payara",
            "Peacock Bass",
            "Petrifish",
            "Piranha",
            "Pollock",
            "Porgy",
            "Pufferfish",
            "Quagmire Eel",
            "Queenfish",
            "Rainbow Glowfish",
            "Rainbow Trout",
            "Red Gurnard",
            "Red Herring",
            "Redfin Barb",
            "Redtail Catfish",
            "Ripsaw Catfish",
            "Risen Sea Bass",
            "Rock Bass",
            "Rockfish",
            "Rohu",
            "Round Goby",
            "Royal Featherback",
            "Royal Pike",
            "Royal Starfish",
            "Sailfin Molly",
            "Sailfish",
            "Sardinata",
            "Scorpion Fish",
            "Sea Perch",
            "Sea Robin",
            "Seahorse",
            "Sheatfish",
            "Shimmering Squid",
            "Shinota Blackfin",
            "Shipwreck Moray",
            "Silver Drum",
            "Silver Moony",
            "Silverfish",
            "Skipjack Tuna",
            "Slaughterfish",
            "Smallmouth Bass",
            "Snakehead",
            "Snook",
            "Snow Crab",
            "Snowflake Eel",
            "Sockeye",
            "Speckled Perch",
            "Spectral Jellyfish",
            "Spotted Flounder",
            "Spotted Pufferfish",
            "Spotted Stingray",
            "Stargazer",
            "Starry Flounder",
            "Steelhead Trout",
            "Stingray",
            "Stone Guiyu",
            "Stone Loach",
            "Striped Barracuda",
            "Striped Bass",
            "Sturgeon",
            "Sunfish",
            "Sunscale Striker",
            "Surubim",
            "Swampblight Lamprey",
            "Swordfish",
            "Taimen",
            "Tarpon",
            "Toadfish",
            "Totemfish",
            "Tripletail",
            "Twilight Striker",
            "Unholy Mackerel",
            "Unicorn Fish",
            "Vampire Squid",
            "Venomfish",
            "Viperfish",
            "Volcanic Blackfish",
            "Walleye",
            "Warmouth",
            "Weever",
            "White Bass",
            "Wolffish",
            "Yellow Perch",
        ]

        if "Path of Fire" in self.storylines_owned:
            fishables += [
                "Barramundi",
                "Elon Tetra",
                "Elonian Bass",
                "Giant Barb",
                "Giant Paddlefish",
                "Gilded Loach",
                "Golden Mahseer",
                "Kaluga",
                "Lungfish",
                "Mahseer",
                "Marbled Lungfish",
                "Mudskipper",
                "Paddlefish",
                "Red-Eyed Piranha",
                "Sand Carp",
                "Silver Bichir",
                "Striped Catfish",
                "Tigerfish",
                "Tilapia",
                "Vundu",
                "Zander",
            ]

        if "Season 4" in self.storylines_owned:
            fishables += [
                "Beluga",
                "Blue Marlin",
                "Cobia",
                "Dandan",
                "Diamond Trevally",
                "King Crab",
                "Opah",
                "Parrotfish",
                "Pompano",
                "Roosterfish",
                "Sea Trout",
                "Sheepshead",
                "Wahoo",
                "Yellowtail Snapper",
            ]

        if "Secrets of the Obscure" in self.storylines_owned:
            fishables += [
                "Balance Fish",
                "Bastion Fish",
                "Blightbob",
                "Buried Angst",
                "Celestial Fish",
                "Codmander",
                "Daydream",
                "Empress Fish",
                "Fractured Fish",
                "Frenzied Cephalopod",
                "Glutfish",
                "Jokopu",
                "Knowledge Fish",
                "Maddened Mackerel",
                "Natural Fish",
                "Obscure Fish",
                "Phantom Pollock",
                "Primal Maguuma Trout",
                "Queen's Flipper",
                "Strength Fish",
                "Three-Eyed Carp",
            ]

        if "Janthir Wilds" in self.storylines_owned:
            fishables += [
                "Flowerhead",
                "Indigo Drakefish",
                "Juvenile Frogfish",
                "Longhorn Boxfish",
                "Lowland Grunt",
                "Mohawk Bream",
                "Mouse-Eared Octopus",
                "Queen Parrotfish",
                "Shaderock Salamander",
                "Spectacled Lumper",
                "Violet Screamer",
                "Viperfish",
            ]

        return sorted(fishables)

    @staticmethod
    def crafting_discipline_level_range() -> range:
        return range(50, 301)

    def crafting_disciplines(self) -> List[str]:
        crafting_disciplines = [
            "Armorsmith",
            "Artificer",
            "Chef",
            "Huntsman",
            "Jeweler",
            "Leatherworker",
            "Scribe",
            "Tailor",
            "Weaponsmith",
        ]

        if "Janthir Wilds" in self.storylines_owned:
            crafting_disciplines += [
                "Handiworker",
            ]

        return sorted(crafting_disciplines)

    def meta_events(self) -> List[str]:
        events = [
            "Svanir Shaman Chief",
            "Fire Elemental",
            "Shadow Behemoth",
            "Great Jungle Wurm",
            "Modniir Ulgoth",
            "Admiral Taidha Covington",
            "The Shatterer",
            "Megadestroyer",
            "Inquest Golem Mark II",
            "Claw of Jormag",
            "Triple Trouble",
            "Tequatl the Sunless"
            "Karka Queen",
            "Ley-Line Anomaly",
            "Scarlet's Invastion",
            "Awakened Invasion",
        ]

        if "Season 2" in self.storylines_owned:
            events += ["RIBA"]

        if "Heart of Thorns" in self.storylines_owned:
            events += [
                "Verdant Brink Night Bosses",
                "Octovine",
                "Chak Gerent",
                "Dragon's Stand",
            ]

        if "Path of Fire" in self.storylines_owned:
            events += [
                "Choya Pinata",
                "Buried Treasure",
                "Doppelganger",
                "Junundu Rising",
                "Maws of Torment",
                "Forged with Fire",
                "Serpent's Ire",
            ]

        if "Season 4" in self.storylines_owned:
            events += [
                "Palawadan",
                "Death-Branded Shatterer",
                "Thunderhead Keep",
                "The Oil Floes"
            ]

        if "Icebrood Saga" in self.storylines_owned:
            events += [
                "Effigy",
                "Doomlore Shrine",
                "Ooze Pits",
                "Metal Concert",
                "Jora's Keep",
                "Drakkar",
                "Drizzlewood Coast",
            ]

        if "End of Dragons" in self.storylines_owned:
            events += [
                "Aetherblade Assault",
                "Kaineng Blackout",
                "Gang War",
                "Aspenwood",
                "Jade Maw",
                "The Battle for the Jade Sea",
            ]

        if "Secrets of the Obscure" in self.storylines_owned:
            events += [
                "Unlocking the Wizard's Tower",
                "Defense of Amnytas",
                "The Road to Heitor",
                "The Fangs That Gnash",
                "Into the Spider's Lair",
            ]

        if "Janthir Wilds" in self.storylines_owned:
            events += [
                "Bog Queen",
                "Of Mists and Monsters",
            ]

        return events

    @staticmethod
    def wvw_objectives() -> List[str]:
        return [
            "Ruin",
            "Sentry Point",
            "Shrine",
            "Supply Camp",
            "Tower",
            "Keep",
            "Stonemist Castle"
        ]

    @staticmethod
    def pvp_match_counts() -> range:
        return range(1, 4)

    @staticmethod
    def fractal_tiers() -> range:
        return range(1, 5)

    @staticmethod
    def fractals() -> List[str]:
        return [
            "Aetherblade",
            "Aquatic Ruins",
            "Captain Mai Trin Boss",
            "Chaos",
            "Cliffside",
            "Deepstone",
            "Lonely Tower",
            "Molten Boss",
            "Molten Furnace",
            "Nightmare",
            "Shattered Observatory",
            "Silent Surf",
            "Siren's Reef",
            "Snowblind",
            "Sunqua Peak",
            "Solid Ocean",
            "Swampland",
            "Thaumanova Reactor"
            "Twilight Oasis"
            "Uncategorized",
            "Underground Facility",
            "Urban Battleground",
            "Volcanic",
        ]

    @staticmethod
    def dungeons() -> List[str]:
        dungeons = [
            "Ascalonian Catacombs",
            "Caudecus's Manor",
            "Twilight Arbor",
            "Sorrow's Embrace",
            "Citadel of Flame",
            "Honor of the Waves",
            "Crucible of Eternity",
        ]

        dungeon_paths = list()

        for dungeon in dungeons:
            dungeon_paths += [f"{dungeon} - Story Mode"]

        dungeons += ["The Ruined City of Arah"]

        for dungeon in dungeons:
            for path in [1, 2, 3]:
                dungeon_paths += [f"{dungeon} - Explorable Path {path}"]

        dungeon_paths += ["The Ruined City of Arah - Explorable Path 4"]

        return dungeon_paths

    def raids(self) -> List[str]:
        raids = list()

        if "Heart of Thorns" in self.storylines_owned:
            raids += [
                "Spirit Vale",
                "Salvation Pass",
                "Stronghold of the Faithful",
                "Bastion of the Penitent"
            ]

        if "Path of Fire" in self.storylines_owned:
            raids += [
                "Hall of Chains",
                "Mythwright Gambit",
                "The Key of Ahdashim"
            ]

        if "Janthir Wilds" in self.storylines_owned:
            raids += ["Mount Balrior"]

        return raids

    def strikes(self) -> List[str]:
        strikes = ["Old Lion's Court"]

        if "Icebrood Saga" in self.storylines_owned:
            strikes += [
                "Shiverpeaks Pass",
                "Voice of the Fallen and Claw of the Fallen",
                "Fraenir of Jormag",
                "Boneskinner",
                "Whisper of Jormag",
                "Forging Steel",
                "Cold War",
            ]

        if "End of Dragons" in self.storylines_owned:
            strikes += [
                "Aetherblade Hideout",
                "Xunlai Jade Junkyard",
                "Kaineng Overlook",
                "Harvest Temple",
            ]

        if "Secrets of the Obscure" in self.storylines_owned:
            strikes += [
                "Cosmic Observatory",
                "Temple of Febe",
            ]

        return strikes

    def convergences(self) -> List[str]:
        convergences = [
            "Tower of Nightmares",
            "Twisted Marionette",
            "Battle for Lion's Arch",
        ]

        if "Icebrood Saga" in self.storylines_owned:
            convergences.append("Dragonstorm")
        if "Secrets of the Obscure" in self.storylines_owned:
            convergences.append("Kryptis Convergence")
        if "Janthir Wilds" in self.storylines_owned:
            convergences.append("Titan Convergence")

        return convergences

    @staticmethod
    def ap_amounts() -> List[int]:
        return [1, 3, 5]


# Archipelago Options
class GuildWars2StorylinesOwned(OptionSet):
    """
    Indicates which Guild Wars 2 expansions and living world seasons the player owns.
    """

    display_name = "Guild Wars 2 Storylines Owned"
    valid_keys = [
        "Core",
        "Season 1",
        "Season 2",
        "Heart of Thorns",
        "Season 3",
        "Path of Fire",
        "Season 4",
        "Icebrood Saga",
        "End of Dragons",
        "Secrets of the Obscure",
        "Janthir Wilds",
    ]

    default = valid_keys


class GuildWars2GameModes(OptionSet):
    """
    Indicates which Guild Wars 2 game modes the player plays.
    """

    display_name = "Guild Wars 2 Game Modes"
    valid_keys = [
        "Jumping Puzzles",
        "Exploration",
        "Fishing",
        "Gathering",
        "Crafting",
        "Open World",
        "Story",
        "PvP",
        "WvW",
        "Dungeons",
        "Fractals",
        "Raids",
        "Strikes",
        "Convergences",  # includes things like The Twisted Marrionette, Battle for Lion's Arch, and Dragonstorm
    ]

    default = valid_keys
