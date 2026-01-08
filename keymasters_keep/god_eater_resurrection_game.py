from __future__ import annotations

from typing import List, Set

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class GodEaterResurrectionArchipelagoOptions:
    god_eater_resurrection_included_missions: GodEaterResurrectionIncludedMissions


class GodEaterResurrection(Game):
    name = "God Eater Resurrection"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.VITA,
    ]

    is_adult_only_or_unrated = False

    options_cls = GodEaterResurrectionArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Use the following God Arc part types: MELEE, GUN, SHIELD",
                data={
                    "MELEE": (self.melee, 1),
                    "GUN": (self.guns, 1),
                    "SHIELD": (self.shields, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Complete MISSION",
                data={
                    "MISSION": (self.missions_all, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete MISSION on Perilous Challenge PERILOUS",
                data={
                    "MISSION": (self.missions_all, 1),
                    "PERILOUS": (self.perilous, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete MISSION with CHARACTERS",
                data={
                    "MISSION": (self.missions, 1),
                    "CHARACTERS": (self.characters, range(1, 4)),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete MISSION solo",
                data={
                    "MISSION": (self.missions_all, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Defeat ARAGAMI",
                data={
                    "ARAGAMI": (self.aragami, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

        return templates

    @property
    def included_missions(self) -> List[str]:
        return sorted(self.archipelago_options.god_eater_resurrection_included_missions.value)

    @property
    def one(self) -> bool:
        return "Difficulty 1" in self.included_missions

    @property
    def two(self) -> bool:
        return "Difficulty 2" in self.included_missions

    @property
    def three(self) -> bool:
        return "Difficulty 3" in self.included_missions

    @property
    def four(self) -> bool:
        return "Difficulty 4" in self.included_missions

    @property
    def five(self) -> bool:
        return "Difficulty 5" in self.included_missions

    @property
    def six(self) -> bool:
        return "Difficulty 6" in self.included_missions

    @property
    def seven(self) -> bool:
        return "Difficulty 7" in self.included_missions

    @property
    def eight(self) -> bool:
        return "Difficulty 8" in self.included_missions

    @property
    def nine(self) -> bool:
        return "Difficulty 9" in self.included_missions

    @property
    def ten(self) -> bool:
        return "Difficulty 10" in self.included_missions

    @property
    def eleven(self) -> bool:
        return "Difficulty 11" in self.included_missions

    @property
    def twelve(self) -> bool:
        return "Difficulty 12" in self.included_missions

    @property
    def thirteen(self) -> bool:
        return "Difficulty 13" in self.included_missions

    @property
    def fourteen(self) -> bool:
        return "Difficulty 14" in self.included_missions

    @property
    def challenge(self) -> bool:
        return "Challenge" in self.included_missions

    @property
    def predator_pack_1(self) -> bool:
        return "Predator Pack 1" in self.included_missions

    @property
    def predator_pack_2(self) -> bool:
        return "Predator Pack 2" in self.included_missions

    @property
    def urgent(self) -> bool:
        return "Urgent" in self.included_missions

    @staticmethod
    def melee() -> List[str]:
        return [
            "Short",
            "Long",
            "Buster",
            "Hammer",
            "Spear",
            "Scythe",
        ]

    @staticmethod
    def guns() -> List[str]:
        return [
            "Sniper",
            "Assault",
            "Blast",
            "Shotgun",
        ]

    @staticmethod
    def shields() -> List[str]:
        return [
            "Buckler",
            "Shield",
            "Tower Shield",
        ]

    @staticmethod
    def characters() -> List[str]:
        return [
            "Lindow",
            "Sakuya",
            "Soma",
            "Kota",
            "Alisa",
            "Shio",
            "Ren",
            "Tatsumi",
            "Brendan",
            "Kanon",
            "Karel",
            "Gina",
            "Shun",
            "Annette",
            "Federico",
            "Masked Ogre",
            "Lindow (Alt)",
            "Sakuya (Alt)",
            "Soma (Alt)",
            "Kota (Alt)",
            "Alisa (Alt)",
            "Shio (Alt)",
            "Ren (Alt)",
            "Tatsumi (Alt)",
            "Brendan (Alt)",
            "Kanon (Alt)",
            "Karel (Alt)",
            "Gina (Alt)",
            "Shun (Alt)",
            "Annette (Alt)",
            "Federico (Alt)",
            "Masked Ogre (Alt)",
            "Alisa (Alt 2)",
        ]

    @staticmethod
    def perilous() -> range:
        return range(1, 100)  # max 99

    def missions(self) -> List[str]:
        missions: List[str] = list()

        if self.one:
            missions.extend([
                "Devil’s Tail (Difficulty 1)",
                "Fallen Angel Egg (Difficulty 1)",
                "Cowboy (Difficulty 1)",
                "Corrupt Cocoon (Difficulty 1)",
                "Iron Rain (Difficulty 1)",
            ])

        if self.two:
            missions.extend([
                "Kongou Giant (Difficulty 2)",
                "Whirlwind (Difficulty 2)",
                "Crocodile One (Difficulty 2)",
                "Mouse Trap (Difficulty 2)",
                "Crocodile Two (Difficulty 2)",
                "Glow of Prestige (Difficulty 2)",
                "Concrete Jungle (Difficulty 2)",
                "Snowball (Difficulty 2)",
                "Awakening God of War (Difficulty 2)",
                "Ocean Wall (Difficulty 2)",
                "First Frost (Difficulty 2)",
                "Snail’s Shell (Difficulty 2)",
                "Watermill (Difficulty 2)",
                "Setting Sun (Difficulty 2)",
                "Green Purebreeds (Difficulty 2)",
                "Aurora (Difficulty 2)",
                "Rat Trap (Difficulty 2)",
            ])

        if self.three:
            missions.extend([
                "Moon in the Welkin (Difficulty 3)",
                "Hailstorm (Difficulty 3)",
                "Salty Dog (Difficulty 3)",
                "Cracked Sanidine (Difficulty 3)",
                "Rebellion’s Beacon (Difficulty 3)",
                "Molten Iron (Difficulty 3)",
                "Return (Difficulty 3)",
                "City Riot (Difficulty 3)",
                "Rusted Edge (Difficulty 3)",
                "Crocodile Swagger (Difficulty 3)",
                "Daytime Owl (Difficulty 3)",
                "Supply Retrieval (Difficulty 3)",
                "Red Antares (Difficulty 3)",
                "Black Trojan (Difficulty 3)",
                "Snow Mouse (Difficulty 3)",
                "Scarlet Charger (Difficulty 3)",
                "Picnic Fields (Difficulty 3)",
                "Rabbit Hunt (Difficulty 3)",
                "Tyrant Breath (Difficulty 3)",
                "Monkey Guts (Difficulty 3)",
                "Flame Shield (Difficulty 3)",
                "Winter’s Dawn (Difficulty 3)",
                "Iron Blizzard (Difficulty 3)",
                "Idle Warrior (Difficulty 3)",
            ])

        if self.four:
            missions.extend([
                "Storm Baptism (Difficulty 4)",
                "Sewer Crocodile (Difficulty 4)",
                "Basement Fire-Croc (Difficulty 4)",
                "Lone Monkey (Difficulty 4)",
                "Twilight Monkey (Difficulty 4)",
                "Rampage (Difficulty 4)",
                "Lone Evil Eye (Difficulty 4)",
                "Knight’s Mind (Difficulty 4)",
                "Venus Trap (Difficulty 4)",
                "Sunlight on Snow (Difficulty 4)",
                "Proud Bird (Difficulty 4)",
                "Jungle Tiger (Difficulty 4)",
                "Tequila Sunrise (Difficulty 4)",
                "Hell’s Kitchen (Difficulty 4)",
                "Sleet (Difficulty 4)",
                "Symbol of Swords (Difficulty 4)",
                "God of Thunder (Difficulty 4)",
                "Troika (Difficulty 4)",
                "Slingshot (Difficulty 4)",
                "Hematite Rose (Difficulty 4)",
                "Treacherous Temple (Difficulty 4)",
            ])

        if self.five:
            missions.extend([
                "Carnage Feast (Difficulty 5)",
                "Grouse of the Mist (Difficulty 5)",
                "Dancing Ogre (Difficulty 5)",
                "Sea Breeze (Difficulty 5)",
                "Summer Horsefly (Difficulty 5)",
                "Svampside Heron (Difficulty 5)",
                "Bow and Spear (Difficulty 5)",
                "Black Alligator (Difficulty 5)",
                "Pilgrim (Difficulty 5)",
                "Frozen Elephant (Difficulty 5)",
                "Poison Butterfly (Difficulty 5)",
                "Swirl Fire (Difficulty 5)",
                "Purple Spark (Difficulty 5)",
                "Spring Thunder (Difficulty 5)",
                "Shopping Mall (Difficulty 5)",
                "Sweet Home (Difficulty 5)",
                "Hunting Cloak (Difficulty 5)",
                "Primordial Spiral (Difficulty 5)",
                "Drosera (Difficulty 5)",
                "Bison Grass Vodka (Difficulty 5)",
                "Steady Flare (Difficulty 5)",
                "Sarracenia (Difficulty 5)",
                "Nut Cracker (Difficulty 5)",
            ])

        if self.six:
            missions.extend([
                "Icy Damsel (Difficulty 6)",
                "Empress’s Forest (Difficulty 6)",
                "Dragon’s Breath (Difficulty 6)",
                "Cavern Bears (Difficulty 6)",
                "Break Shot (Difficulty 6)",
                "Avalanche (Difficulty 6)",
                "Bestial Twilight (Difficulty 6)",
                "Exiled Emperor (Difficulty 6)",
                "Nepenthes (Difficulty 6)",
                "Collector (Difficulty 6)",
                "Cephalotus (Difficulty 6)",
                "Thermal Jacket (Difficulty 6)",
                "Hellfire Shield (Difficulty 6)",
                "Obsidian Sacrifice (Difficulty 6)",
                "Sunken Beacon (Difficulty 6)",
                "Ice-Croc’s Slumber (Difficulty 6)",
                "Big Smile (Difficulty 6)",
                "Ancient Battle Tank (Difficulty 6)",
                "Devourer of Tomorrow (Difficulty 6)",
                "Big Family (Difficulty 6)",
                "Home of Souls (Difficulty 6)",
                "Shark Fin (Difficulty 6)",
                "Regal Bones (Difficulty 6)",
                "Death Stalker (Difficulty 6)",
                "Dead Proof (Difficulty 6)",
                "An Aloof Dream (Difficulty 6)",
                "Ruffians (Difficulty 6)",
            ])

        if self.seven:
            missions.extend([
                "Little Ruler (Difficulty 7)",
                "Angels in a Refuge (Difficulty 7)",
                "West-southwest (Difficulty 7)",
                "Missile Fire (Difficulty 7)",
                "Lion’s Revenge (Difficulty 7)",
                "Wicked Fruit (Difficulty 7)",
                "Croc Three (Difficulty 7)",
                "Submarine (Difficulty 7)",
                "Sunken Arrow (Difficulty 7)",
                "Phoenix Nest (Difficulty 7)",
                "Moth’s Grave (Difficulty 7)",
                "Rice Chase (Difficulty 7)",
                "Gold Coast (Difficulty 7)",
                "Sweeper (Difficulty 7)",
                "Vortex of Chaos (Difficulty 7)",
                "Waterline Repair (Difficulty 7)",
                "Firelords in a Storm (Difficulty 7)",
                "Thor’s Banquet (Difficulty 7)",
                "Fifth Element (Difficulty 7)",
                "Naked Monkey (Difficulty 7)",
                "Frozen City (Difficulty 7)",
                "Needles and Sewage (Difficulty 7)",
                "Burning Tracks (Difficulty 7)",
                "Nightfall Scam (Difficulty 7)",
                "Fire and Ice (Difficulty 7)",
                "Alligator Hunter (Difficulty 7)",
                "Undertaker (Difficulty 7)",
                "Devourer of Future (Difficulty 7)",
            ])

        if self.eight:
            missions.extend([
                "Tandoor (Difficulty 8)",
                "Dark Shimmer (Difficulty 8)",
                "Dark Wing (Difficulty 8)",
                "Knight and Rust (Difficulty 8)",
                "Scaly Thrush (Difficulty 8)",
                "Storm Queen (Difficulty 8)",
                "Separated Kings (Difficulty 8)",
                "Molecular Eyes (Difficulty 8)",
                "Onyx Smoke (Difficulty 8)",
                "Cerberus (Difficulty 8)",
                "Screw Driver (Difficulty 8)",
                "Fake Sun (Difficulty 8)",
                "Coyote Warrior (Difficulty 8)",
                "Dirty Bomb (Difficulty 8)",
                "The End to Vice (Difficulty 8)",
                "Dog Mines (Difficulty 8)",
                "Fire Engine (Difficulty 8)",
                "Purple Sparks (Difficulty 8)",
                "Tsunami (Difficulty 8)",
                "Devourer of World (Difficulty 8)",
                "Double Date (Difficulty 8)",
                "Invasive Swarm (Difficulty 8)",
            ])

        if self.nine:
            missions.extend([
                "Dragon-Tiger Fang (Difficulty 9)",
                "Buddha Smile (Difficulty 9)",
                "Monkey Wrath (Difficulty 9)",
                "Unidentified (Difficulty 9)",
                "Goddess’ Duty (Difficulty 9)",
                "Newcomer Trials (Difficulty 9)",
                "Ruler’s City (Difficulty 9)",
                "Runaway Tank (Difficulty 9)",
                "Sidecar (Difficulty 9)",
                "Nocturnal Axe (Difficulty 9)",
                "Dutch Oven (Difficulty 9)",
                "Looters’ Night (Difficulty 9)",
                "Guardians (Difficulty 9)",
                "Divine Shadows (Difficulty 9)",
                "Tropical Fish (Difficulty 9)",
                "A Devil’s Heart (Difficulty 9)",
                "Thunderstorm (Difficulty 9)",
                "Rumbling Treads (Difficulty 9)",
                "Icebreaker Scouts (Difficulty 9)",
                "The Venus (Difficulty 9)",
                "Chimera (Difficulty 9)",
                "Fires of Caldera (Difficulty 9)",
                "Poison Garnish (Difficulty 9)",
            ])

        if self.ten:
            missions.extend([
                "Devourer of All (Difficulty 10)",
                "Ice-Cold Glare (Difficulty 10)",
                "Firefly (Difficulty 10)",
                "Wing Scales (Difficulty 10)",
                "Into Thin Air (Difficulty 10)",
                "King’s Tryst (Difficulty 10)",
                "Ones Who Devour the End (Difficulty 10)",
                "Pest Purge (Difficulty 10)",
                "Tower of Ivory (Difficulty 10)",
                "Death Mask (Difficulty 10)",
                "Noble Dining (Difficulty 10)",
                "Sea Fire (Difficulty 10)",
                "St. Elmo’s Fire (Difficulty 10)",
                "Evil Princess (Difficulty 10)",
                "Lady Butterfly (Difficulty 10)",
                "Restoration of Myth (Difficulty 10)",
                "Road to Idavollr (Difficulty 10)",
                "The Fall of Mankind (Difficulty 10)",
                "Devourer of the Mind (Difficulty 10)",
                "Spiral of Reminiscence (Difficulty 10)",
                "True Moon Welkin (Difficulty 10)",
            ])

        if self.eleven:
            missions.extend([
                "Radiant Halo (Difficulty 11)",
                "Angel’s Ladder (Difficulty 11)",
                "Devil Bear (Difficulty 11)",
                "Braggart’s Heart (Difficulty 11)",
                "Mole’s Tunnel (Difficulty 11)",
                "Fire Prevention (Difficulty 11)",
                "Insulation (Difficulty 11)",
                "September Shadow (Difficulty 11)",
                "Red Tape (Difficulty 11)",
                "Heliamphora (Difficulty 11)",
                "Sanghyang Jaran (Difficulty 11)",
                "Garimpeiro (Difficulty 11)",
            ])

        if self.twelve:
            missions.extend([
                "Fool’s Gold (Difficulty 12)",
                "Corn Snow (Difficulty 12)",
                "Ink Clouds (Difficulty 12)",
                "Obsidian Heart (Difficulty 12)",
                "Corroded Gorget (Difficulty 12)",
                "Grimsvotn (Difficulty 12)",
                "Bog Offering (Difficulty 12)",
                "Sailing Rock (Difficulty 12)",
                "Wispy Clouds (Difficulty 12)",
                "Water Lily (Difficulty 12)",
                "Archvillain (Difficulty 12)",
            ])

        if self.thirteen:
            missions.extend([
                "Triumvirate (Difficulty 13)",
                "Wildfire (Difficulty 13)",
                "Sacred Rhythm (Difficulty 13)",
                "Speculum Dianae (Difficulty 13)",
                "Enceladus Rapids (Difficulty 13)",
                "Dead Charger (Difficulty 13)",
                "Great Black (Difficulty 13)",
                "Test Tube (Difficulty 13)",
                "Dionaea (Difficulty 13)",
                "Cardinal (Difficulty 13)",
                "Snow Firefly (Difficulty 13)",
                "Grounded Lightning (Difficulty 13)",
                "Drifting Snow (Difficulty 13)",
                "Dance of the Lunar Hare (Difficulty 13)",
            ])

        if self.fourteen:
            missions.extend([
                "Artifacts (Difficulty 14)",
                "Pilgrim 2 (Difficulty 14)",
                "Grand Prize (Difficulty 14)",
                "Kanon’s Secret Training (Difficulty 14)",
                "God Eater (Difficulty 14)",
                "The Little Ones’ Revenge (Difficulty 14)",
                "Deadly Sisters’ Dance (Difficulty 14)",
                "Giant Spin (Difficulty 14)",
                "Forty-Niner (Difficulty 14)",
                "Mama’s Boy (Difficulty 14)",
                "Icarus’s Wing (Difficulty 14)",
                "Hard Case (Difficulty 14)",
                "Backstabber (Difficulty 14)",
                "Anantaboga (Difficulty 14)",
                "Chatterbox (Difficulty 14)",
                "Avalanche (2) (Difficulty 14)",
                "Haze (Difficulty 14)",
                "White-Out (Difficulty 14)",
                "Red River (Difficulty 14)",
                "Sting Ray (Difficulty 14)",
                "Thunder (Difficulty 14)",
                "Holy Moon in the Welkin (Difficulty 14)",
                "Pilgrim 0 (Difficulty 14)",
                "Live Prey (Difficulty 14)",
                "Monochrome (Difficulty 14)",
                "Summer Gnats (Difficulty 14)",
                "Closed City (Difficulty 14)",
                "Dust Trail (Difficulty 14)",
                "Black Ore (Difficulty 14)",
                "Watch Out Overhead (Difficulty 14)",
                "One On One (Difficulty 14)",
            ])

        if self.challenge:
            missions.extend([
                "Beauty’s End (Challenge)",
                "Certainly Clear (Challenge)",
                "Gboro-Gboro Panic (Challenge)",
                "Blue Blade Dance (Challenge)",
                "Quick Draw (Challenge)",
                "Here, Here, Here (Challenge)",
                "Snow Dragon’s Garden (Challenge)",
                "Fallen Vortex (Challenge)",
                "Supernova (Challenge)",
                "Origin (Challenge)",
                "Three Gun Turret (Challenge)",
                "Eton Blazer (Challenge)",
                "Humpty Dumpty (Challenge)",
                "Focus Forever (Challenge)",
                "Merciless Commander (Challenge)",
                "Martial Drill (Challenge)",
                "Soulmate (Challenge)",
                "Quick Draw 2 (Challenge)",
                "Assortment (Challenge)",
                "God Eater Burst (Challenge)",
                "Demon Slaying (Challenge)",
                "Quick Draw 3 (Challenge)",
                "Reminiscence (Challenge)",
                "Demonic Parade (Challenge)",
                "Quick Draw X (Challenge)",
                "One Breath (Challenge)",
                "Devils’ Festival (Challenge)",
                "Big Over Small (Challenge)",
                "Disastrous Dance (Challenge)",
                "Deadly Flock (Challenge)",
                "Jewel Hoard (Challenge)",
                "Bloody Rose (Challenge)",
                "Harvest Festival (Challenge)",
                "Poison Needle Fence (Challenge)",
                "Flash of Light (Challenge)",
                "Dragon God (Challenge)",
                "Trick Shot (Challenge)",
                "Lantern Cutting (Challenge)",
                "Today’s Fortune (Challenge)",
                "Gboro-Gboro Paradise (Challenge)",
            ])

        if self.predator_pack_1:
            missions.extend([
                "Fukumuya Moat (Predator Pack 1)",
                "Junk-Eating Beast (Predator Pack 1)",
                "Malevolence in the Darkness (Predator Pack 1)",
                "Carnevale (Predator Pack 1)",
                "Spiritus (Predator Pack 1)",
                "Front and Back (Predator Pack 1)",
                "Intermedia (Predator Pack 1)",
                "Perseverance (Predator Pack 1)",
                "Diligence (Predator Pack 1)",

            ])

        if self.predator_pack_2:
            missions.extend([
                "Bandersnatch (Predator Pack 2)",
                "Phantom Embrace (Predator Pack 2)",
                "The Lion and the Peonies (Predator Pack 2)",
                "Snowdrop (Predator Pack 2)",
                "Disjunction (Predator Pack 2)",
                "Spider Lily (Predator Pack 2)",
            ])

        if self.urgent:
            missions.extend([
                "Mayflies (Urgent)",
                "Midpoint (Urgent)",
                "Triple Cross (Urgent)",
                "Infantry Swarm (Urgent)",
                "Thunderstorm (Urgent)",
                "Queen of Obstruction (Urgent)",
                "Incense Bonfire (Urgent)",
                "Flame Madness (Urgent)",
                "Ranger Yell (Urgent)",
                "Split Milk (Urgent)",
                "Material Age (Urgent)",
                "Big Trouble (Urgent)",
                "Cabin Fever (Urgent)",
                "Tempest (Urgent)",
                "Frozen Murder (Urgent)",
            ])

        return missions

    def missions_all(self) -> List[str]:
        missions: List[str] = self.missions()

        # Missions that can't be done with a full party
        if self.one:
            missions.extend([
                "Tutorial 1 (Difficulty 1)",
                "Tutorial 2 (Difficulty 1)",
            ])

        if self.two:
            missions.extend([
                "Practice Tutorial (Difficulty 2)",
            ])

        if self.fourteen:
            missions.extend([
                "A Pair of Predators (Difficulty 14)",
                "New Moon in the Welkin (Difficulty 14)",
            ])

        if self.challenge:
            missions.extend([
                "Danse Macabre (Challenge)",
                "Oskopnir (Challenge)",
                "Mars Sublime (Challenge)",
                "Coven Tea Party (Challenge)",
                "Soldier’s Grave (Challenge)",
                "Storm and Stress (Challenge)",
                "King of the Hill (Challenge)",
                "Marianne (Challenge)",
            ])

        return missions

    def aragami(self):
        aragami: Set[str] = set()

        if self.one:
            aragami.add("a Zygote")
            aragami.add("an Ogretail")
            aragami.add("a Cocoon Maiden")

        if self.two:
            aragami.add("a Zygote")
            aragami.add("a Kongou")
            aragami.add("a Chi-You")
            aragami.add("an Ogretail")
            aragami.add("a Gboro-Gboro")
            aragami.add("a Cocoon Maiden")

        if self.three:
            aragami.add("a Vajra")
            aragami.add("a Zygote")
            aragami.add("a Kongou")
            aragami.add("a Yaksha")
            aragami.add("a Chi-You")
            aragami.add("a Quadriga")
            aragami.add("an Ogretail")
            aragami.add("a Gboro-Gboro")
            aragami.add("a Borg Camlann")
            aragami.add("a Cocoon Maiden")
            aragami.add("a Fallen Ogretail")
            aragami.add("a Fallen Zygote (Blaze)")
            aragami.add("a Fallen Cocoon Maiden (Blaze)")

        if self.four:
            aragami.add("a Vajra")
            aragami.add("a Zygote")
            aragami.add("a Sariel")
            aragami.add("a Kongou")
            aragami.add("a Chi-You")
            aragami.add("a Quadriga")
            aragami.add("an Ogretail")
            aragami.add("a Yaksha Raja")
            aragami.add("a Gboro-Gboro")
            aragami.add("a Borg Camlann")
            aragami.add("a Cocoon Maiden")
            aragami.add("a Fallen Kongou")
            aragami.add("a Fallen Ogretail")
            aragami.add("a Vajratail (Blaze)")
            aragami.add("a Fallen Zygote (Blaze)")
            aragami.add("a Fallen Gboro-Gboro (Blaze)")
            aragami.add("a Fallen Cocoon Maiden (Blaze)")

        if self.five:
            aragami.add("a Vajra")
            aragami.add("a Sariel")
            aragami.add("a Zygote")
            aragami.add("a Kongou")
            aragami.add("a Chi-You")
            aragami.add("a Quadriga")
            aragami.add("an Ogretail")
            aragami.add("an Ouroboros")
            aragami.add("a Gboro-Gboro")
            aragami.add("a Borg Camlann")
            aragami.add("a Fallen Sariel")
            aragami.add("a Fallen Kongou")
            aragami.add("a Fallen Chi-You")
            aragami.add("a Fallen Ogretail")
            aragami.add("a Fallen Quadriga")
            aragami.add("a Vajratail (Spark)")
            aragami.add("a Vajratail (Blaze)")
            aragami.add("a Fallen Zygote (Spark)")
            aragami.add("a Fallen Zygote (Blaze)")
            aragami.add("a Fallen Zygote (Freeze)")
            aragami.add("a Fallen Gboro-Gboro (Blaze)")
            aragami.add("a Fallen Borg Camlann (Blaze)")
            aragami.add("a Fallen Borg Camlann (Spark)")
            aragami.add("a Fallen Cocoon Maiden (Spark)")
            aragami.add("a Fallen Cocoon Maiden (Blaze)")

        if self.six:
            aragami.add("a Vajra")
            aragami.add("a Sariel")
            aragami.add("a Yaksha")
            aragami.add("a Kongou")
            aragami.add("a Chi-You")
            aragami.add("a Susano’o")
            aragami.add("a Quadriga")
            aragami.add("an Ogretail")
            aragami.add("an Ouroboros")
            aragami.add("an Arda Nova")
            aragami.add("a Dyaus Pita")
            aragami.add("a Gboro-Gboro")
            aragami.add("a Borg Camlann")
            aragami.add("a Tezcatlipoca")
            aragami.add("a Prithvi Mata")
            aragami.add("a Fallen Sariel")
            aragami.add("a Fallen Kongou")
            aragami.add("a Fierce Kongou")
            aragami.add("a Fallen Chi-You")
            aragami.add("a Fallen Ogretail")
            aragami.add("a Fallen Quadriga")
            aragami.add("a Vajratail (Spark)")
            aragami.add("a Vajratail (Blaze)")
            aragami.add("a Fallen Zygote (Spark)")
            aragami.add("a Fallen Zygote (Blaze)")
            aragami.add("a Fallen Zygote (Freeze)")
            aragami.add("a Fallen Gboro-Gboro (Blaze)")
            aragami.add("a Fallen Gboro-Gboro (Freeze)")
            aragami.add("a Fallen Borg Camlann (Blaze)")
            aragami.add("a Fallen Borg Camlann (Spark)")
            aragami.add("a Fallen Cocoon Maiden (Spark)")
            aragami.add("a Fallen Cocoon Maiden (Blaze)")
            aragami.add("a Fallen Cocoon Maiden (Freeze)")

        if self.seven:
            aragami.add("a Vajra")
            aragami.add("a Zygote")
            aragami.add("a Kongou")
            aragami.add("an Aether")
            aragami.add("a Sekhmet")
            aragami.add("a Chi-You")
            aragami.add("a Hannibal")
            aragami.add("a Quadriga")
            aragami.add("a Susano’o")
            aragami.add("a Gboro-Gboro")
            aragami.add("a Fallen Kongou")
            aragami.add("a Fierce Kongou")
            aragami.add("a Cocoon Maiden")
            aragami.add("a Fallen Sariel")
            aragami.add("a Fallen Ogretail")
            aragami.add("a Fallen Quadriga")
            aragami.add("a Fallen Ouroboros")
            aragami.add("a Vajratail (Spark)")
            aragami.add("a Vajratail (Blaze)")
            aragami.add("a Golden Gboro-Gboro")
            aragami.add("a Fallen Zygote (Spark)")
            aragami.add("a Fallen Zygote (Blaze)")
            aragami.add("a Fallen Zygote (Freeze)")
            aragami.add("a Fallen Gboro-Gboro (Blaze)")
            aragami.add("a Fallen Gboro-Gboro (Freeze)")
            aragami.add("a Fallen Borg Camlann (Blaze)")
            aragami.add("a Fallen Cocoon Maiden (Spark)")
            aragami.add("a Fallen Cocoon Maiden (Blaze)")
            aragami.add("a Fallen Cocoon Maiden (Freeze)")

        if self.eight:
            aragami.add("a Vajra")
            aragami.add("a Yaksha")
            aragami.add("a Sariel")
            aragami.add("an Aether")
            aragami.add("a Sekhmet")
            aragami.add("a Hannibal")
            aragami.add("a Quadriga")
            aragami.add("an Ogretail")
            aragami.add("an Amaterasu")
            aragami.add("an Arda Nova")
            aragami.add("a Dyaus Pita")
            aragami.add("a Yaksha Raja")
            aragami.add("a Tezcatlipoca")
            aragami.add("a Prithvi Mata")
            aragami.add("a Fallen Sariel")
            aragami.add("a Fallen Kongou")
            aragami.add("a Fierce Kongou")
            aragami.add("a Fallen Chi-You")
            aragami.add("a Fallen Quadriga")
            aragami.add("a Fallen Ouroboros")
            aragami.add("a Vajratail (Blaze)")
            aragami.add("a Fallen Zygote (Blaze)")
            aragami.add("a Fallen Zygote (Freeze)")
            aragami.add("a Fallen Borg Camlann (Spark)")
            aragami.add("a Fallen Borg Camlann (Blaze)")
            aragami.add("a Fallen Gboro-Gboro (Freeze)")
            aragami.add("a Fallen Cocoon Maiden (Spark)")
            aragami.add("a Fallen Cocoon Maiden (Blaze)")

        if self.nine:
            aragami.add("a Vajra")
            aragami.add("a Sekhmet")
            aragami.add("a Hannibal")
            aragami.add("a Quadriga")
            aragami.add("a Dyaus Pita")
            aragami.add("a Yaksha Raja")
            aragami.add("a Borg Camlann")
            aragami.add("a Tezcatlipoca")
            aragami.add("a Fallen Sariel")
            aragami.add("a Fallen Kongou")
            aragami.add("a Fierce Kongou")
            aragami.add("a Fallen Quadriga")
            aragami.add("a Fallen Ouroboros")
            aragami.add("a Fallen Arda Nova")
            aragami.add("a Vajratail (Spark)")
            aragami.add("a Fallen Zygote (Spark)")
            aragami.add("a Fallen Zygote (Blaze)")
            aragami.add("a Fallen Gboro-Gboro (Blaze)")
            aragami.add("a Fallen Gboro-Gboro (Freeze)")
            aragami.add("a Fallen Borg Camlann (Spark)")
            aragami.add("a Fallen Cocoon Maiden (Spark)")
            aragami.add("a Fallen Cocoon Maiden (Blaze)")

        if self.ten:
            aragami.add("a Sariel")
            aragami.add("an Aether")
            aragami.add("a Sekhmet")
            aragami.add("a Quadriga")
            aragami.add("a Susano’o")
            aragami.add("a Tsukuyomi")
            aragami.add("an Ouroboros")
            aragami.add("an Arda Nova")
            aragami.add("a Dyaus Pita")
            aragami.add("a Prithvi Mata")
            aragami.add("a Borg Camlann")
            aragami.add("a Tezcatlipoca")
            aragami.add("a Fallen Kongou")
            aragami.add("a Fierce Kongou")
            aragami.add("a Fallen Sariel")
            aragami.add("a Fallen Quadriga")
            aragami.add("a Fallen Arda Nova")
            aragami.add("a Fallen Ouroboros")
            aragami.add("a Corrosive Hannibal")
            aragami.add("a Fallen Gboro-Gboro (Freeze)")

        if self.eleven:
            aragami.add("a Ravana")
            aragami.add("a Yaksha")
            aragami.add("an Aether")
            aragami.add("a Hannibal")
            aragami.add("an Arda Nova")
            aragami.add("a Dyaus Pita")
            aragami.add("a Prithvi Mata")
            aragami.add("a Fierce Kongou")
            aragami.add("a Fallen Kongou")
            aragami.add("a Fallen Sariel")
            aragami.add("a Fallen Chi-You")
            aragami.add("a Fallen Quadriga")
            aragami.add("a Fallen Ouroboros")
            aragami.add("a Vajratail (Blaze)")
            aragami.add("a Fallen Zygote (Spark)")
            aragami.add("a Fallen Zygote (Blaze)")
            aragami.add("a Fallen Zygote (Freeze)")
            aragami.add("a Fallen Gboro-Gboro (Blaze)")
            aragami.add("a Fallen Borg Camlann (Blaze)")
            aragami.add("a Fallen Cocoon Maiden (Spark)")
            aragami.add("a Fallen Cocoon Maiden (Freeze)")

        if self.twelve:
            aragami.add("a Nova")
            aragami.add("a Venus")
            aragami.add("a Ravana")
            aragami.add("a Yaksha")
            aragami.add("an Aether")
            aragami.add("a Sekhmet")
            aragami.add("an Arda Nova")
            aragami.add("an Ouroboros")
            aragami.add("a Yaksha Raja")
            aragami.add("a Tezcatlipoca")
            aragami.add("a Fallen Chi-You")
            aragami.add("a Fallen Ogretail")
            aragami.add("a Vajratail (Spark)")
            aragami.add("a Vajratail (Blaze)")
            aragami.add("a Corrosive Hannibal")
            aragami.add("a Fallen Zygote (Spark)")
            aragami.add("a Fallen Zygote (Freeze)")
            aragami.add("a Fallen Gboro-Gboro (Freeze)")
            aragami.add("a Fallen Borg Camlann (Spark)")
            aragami.add("a Fallen Cocoon Maiden (Spark)")
            aragami.add("a Fallen Cocoon Maiden (Blaze)")

        if self.thirteen:
            aragami.add("a Vajra")
            aragami.add("a Yaksha")
            aragami.add("a Sekhmet")
            aragami.add("a Chi-You")
            aragami.add("a Hannibal")
            aragami.add("a Caligula")
            aragami.add("an Arda Nova")
            aragami.add("an Ouroboros")
            aragami.add("a Dyaus Pita")
            aragami.add("an Arius Nova")
            aragami.add("a Prithvi Mata")
            aragami.add("a Tezcatlipoca")
            aragami.add("a Fallen Sariel")
            aragami.add("a Fallen Kongou")
            aragami.add("a Fierce Kongou")
            aragami.add("a Blitz Hannibal")
            aragami.add("a Fallen Ogretail")
            aragami.add("a Vajratail (Spark)")
            aragami.add("a Vajratail (Blaze)")
            aragami.add("a Fallen Zygote (Blaze)")
            aragami.add("a Fallen Zygote (Freeze)")
            aragami.add("a Fallen Gboro-Gboro (Blaze)")
            aragami.add("a Fallen Gboro-Gboro (Freeze)")
            aragami.add("a Fallen Borg Camlann (Spark)")
            aragami.add("a Fallen Cocoon Maiden (Spark)")
            aragami.add("a Fallen Cocoon Maiden (Freeze)")

        if self.fourteen:
            aragami.add("a Vajra")
            aragami.add("a Sariel")
            aragami.add("a Kongou")
            aragami.add("an Aether")
            aragami.add("a Sekhmet")
            aragami.add("a Chi-You")
            aragami.add("a Hannibal")
            aragami.add("a Quadriga")
            aragami.add("a Susano’o")
            aragami.add("an Ogretail")
            aragami.add("a Tsukuyomi")
            aragami.add("an Amaterasu")
            aragami.add("a Dyaus Pita")
            aragami.add("a Prithvi Mata")
            aragami.add("a Borg Camlann")
            aragami.add("a Tezcatlipoca")
            aragami.add("a Fallen Sariel")
            aragami.add("a Cocoon Maiden")
            aragami.add("a Fierce Kongou")
            aragami.add("a Fallen Kongou")
            aragami.add("a Fallen Chi-You")
            aragami.add("a Fallen Quadriga")
            aragami.add("a Heavenly Father")
            aragami.add("a Vajratail (Blaze)")
            aragami.add("a Vajratail (Spark)")
            aragami.add("a Corrosive Hannibal")
            aragami.add("a Fallen Zygote (Blaze)")
            aragami.add("a Fallen Zygote (Spark)")
            aragami.add("a Fallen Zygote (Freeze)")
            aragami.add("a Fallen Gboro-Gboro (Blaze)")
            aragami.add("a Fallen Gboro-Gboro (Freeze)")
            aragami.add("a Fallen Cocoon Maiden (Spark)")
            aragami.add("a Fallen Cocoon Maiden (Blaze)")

        if self.challenge:
            aragami.add("a Vajra")
            aragami.add("a Venus")
            aragami.add("a Zygote")
            aragami.add("a Sariel")
            aragami.add("a Ravana")
            aragami.add("a Yaksha")
            aragami.add("a Sariel")
            aragami.add("an Aether")
            aragami.add("a Chi-You")
            aragami.add("a Sekhmet")
            aragami.add("a Caligula")
            aragami.add("a Quadriga")
            aragami.add("a Hannibal")
            aragami.add("an Ogretail")
            aragami.add("a Dyaus Pita")
            aragami.add("a Gboro-Gboro")
            aragami.add("a Yaksha Raja")
            aragami.add("a Borg Camlann")
            aragami.add("a Tezcatlipoca")
            aragami.add("a Prithvi Mata")
            aragami.add("a Fallen Sariel")
            aragami.add("a Cocoon Maiden")
            aragami.add("a Fallen Kongou")
            aragami.add("a Fierce Kongou")
            aragami.add("a Fallen Chi-You")
            aragami.add("a Vajratail (Spark)")
            aragami.add("a Fallen Ouroboros")
            aragami.add("a Fallen Arda Nova")
            aragami.add("a Corrosive Hannibal")
            aragami.add("a Golden Gboro-Gboro")
            aragami.add("a Fallen Gboro-Gboro (Freeze)")
            aragami.add("a Fallen Borg Camlann (Spark)")
            aragami.add("a Fallen Borg Camlann (Blaze)")
            aragami.add("a Fallen Cocoon Maiden (Spark)")
            aragami.add("a Fallen Cocoon Maiden (Blaze)")
            aragami.add("a Fallen Cocoon Maiden (Freeze)")

        if self.predator_pack_1:
            aragami.add("a Vajra")
            aragami.add("a Sariel")
            aragami.add("a Ravana")
            aragami.add("a Yaksha")
            aragami.add("an Aether")
            aragami.add("a Sekhmet")
            aragami.add("a Chi-You")
            aragami.add("a Quadriga")
            aragami.add("a Hannibal")
            aragami.add("a Quadriga")
            aragami.add("a Caligula")
            aragami.add("a Dyaus Pita")
            aragami.add("a Yaksha Raja")
            aragami.add("a Gboro-Gboro")
            aragami.add("a Borg Camlann")
            aragami.add("a Prithvi Mata")
            aragami.add("a Fallen Sariel")
            aragami.add("a Fierce Kongou")
            aragami.add("a Fallen Chi-You")
            aragami.add("a Blitz Hannibal")
            aragami.add("a Fallen Ogretail")
            aragami.add("a Fallen Zygote (Blaze)")
            aragami.add("a Fallen Zygote (Freeze)")
            aragami.add("a Fallen Gboro-Gboro (Blaze)")
            aragami.add("a Fallen Cocoon Maiden (Freeze)")

        if self.predator_pack_2:
            aragami.add("a Vajra")
            aragami.add("a Sariel")
            aragami.add("an Aether")
            aragami.add("a Sekhmet")
            aragami.add("a Caligula")
            aragami.add("a Quadriga")
            aragami.add("a Susano’o")
            aragami.add("a Tsukuyomi")
            aragami.add("a Balfa Mata")
            aragami.add("a Yaksha Raja")
            aragami.add("a Tezcatlipoca")
            aragami.add("a Borg Camlann")
            aragami.add("a Fierce Kongou")
            aragami.add("a Cocoon Maiden")
            aragami.add("a Blitz Hannibal")
            aragami.add("a Fallen Arda Nova")
            aragami.add("a Fallen Gboro-Gboro (Freeze)")

        if self.urgent:
            aragami.add("a Venus")
            aragami.add("a Vajra")
            aragami.add("a Zygote")
            aragami.add("a Kongou")
            aragami.add("a Ravana")
            aragami.add("a Sariel")
            aragami.add("an Aether")
            aragami.add("a Sekhmet")
            aragami.add("a Chi-You")
            aragami.add("a Quadriga")
            aragami.add("a Susano’o")
            aragami.add("a Hannibal")
            aragami.add("an Ogretail")
            aragami.add("an Arda Nova")
            aragami.add("a Dyaus Pita")
            aragami.add("an Arius Nova")
            aragami.add("a Gboro-Gboro")
            aragami.add("a Yaksha Raja")
            aragami.add("a Borg Camlann")
            aragami.add("a Prithvi Mata")
            aragami.add("a Tezcatlipoca")
            aragami.add("a Fallen Kongou")
            aragami.add("a Fierce Kongou")
            aragami.add("a Cocoon Maiden")
            aragami.add("a Fallen Sariel")
            aragami.add("a Blitz Hannibal")
            aragami.add("a Fallen Chi-You")
            aragami.add("a Fallen Ogretail")
            aragami.add("a Fallen Quadriga")
            aragami.add("a Vajratail (Blaze)")
            aragami.add("a Corrosive Hannibal")
            aragami.add("a Fallen Zygote (Blaze)")
            aragami.add("a Fallen Zygote (Spark)")
            aragami.add("a Fallen Zygote (Freeze)")
            aragami.add("a Fallen Gboro-Gboro (Blaze)")
            aragami.add("a Fallen Gboro-Gboro (Freeze)")
            aragami.add("a Fallen Borg Camlann (Spark)")
            aragami.add("a Fallen Borg Camlann (Blaze)")
            aragami.add("a Fallen Cocoon Maiden (Blaze)")

        return sorted(aragami)


# Archipelago Options
class GodEaterResurrectionIncludedMissions(OptionSet):
    """
    Indicates which difficulties and extra missions to include in objectives.
    """

    display_name = "God Eater Resurrection Included Missions"
    valid_keys = [
        "Difficulty 1",
        "Difficulty 2",
        "Difficulty 3",
        "Difficulty 4",
        "Difficulty 5",
        "Difficulty 6",
        "Difficulty 7",
        "Difficulty 8",
        "Difficulty 9",
        "Difficulty 10",
        "Difficulty 11",
        "Difficulty 12",
        "Difficulty 13",
        "Difficulty 14",
        "Challenge",
        "Predator Pack 1",
        "Predator Pack 2",
        "Urgent",
    ]

    default = valid_keys
