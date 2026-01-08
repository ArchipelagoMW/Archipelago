from __future__ import annotations

from typing import List, Dict, Callable

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms

from Options import OptionSet


@dataclass
class MonsterRancher2DXArchipelagoOptions:
    monster_rancher_2_dx_unlocked_main_breeds: MonsterRancher2DXUnlockedMainBreeds
    monster_rancher_2_dx_unlocked_sub_breeds: MonsterRancher2DXUnlockedSubBreeds


class MonsterRancher2DXGame(Game):
    name = "Monster Rancher 2 DX"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.PS1,
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False
    options_cls = MonsterRancher2DXArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        tech_functions: Dict[str, Callable[[], List[str]]] = {
            "Ape": self.ape_techs,
            "Arrow Head": self.arrowhead_techs,
            "Bajarl": self.bajarl_techs,
            "Baku": self.baku_techs,
            "Beaclon": self.beaclon_techs,
            "Centaur": self.centaur_techs,
            "ColorPandora": self.colorpandora_techs,
            "Dragon": self.dragon_techs,
            "Ducken": self.ducken_techs,
            "Durahan": self.durahan_techs,
            "Gaboo": self.gaboo_techs,
            "Gali": self.gali_techs,
            "Ghost": self.ghost_techs,
            "Golem": self.golem_techs,
            "Hare": self.hare_techs,
            "Henger": self.henger_techs,
            "Hopper": self.hopper_techs,
            "Jell": self.jell_techs,
            "Jill": self.jill_techs,
            "Joker": self.joker_techs,
            "Metalner": self.metalner_techs,
            "Mew": self.mew_techs,
            "Mocchi": self.mocchi_techs,
            "Mock": self.mock_techs,
            "Monol": self.monol_techs,
            "Naga": self.naga_techs,
            "Niton": self.niton_techs,
            "Phoenix": self.phoenix_techs,
            "Pixie": self.pixie_techs,
            "Plant": self.plant_techs,
            "Suezo": self.suezo_techs,
            "Tiger": self.tiger_techs,
            "Undine": self.undine_techs,
            "Worm": self.worm_techs,
            "Wracky": self.wracky_techs,
            "Zilla": self.zilla_techs,
            "Zuum": self.zuum_techs,
        }

        objectives = [
            GameObjectiveTemplate(
                label="Win the following tournaments with a MONSTER: TOURNAMENT",
                data={
                    "TOURNAMENT": (self.tournaments, range(1, 5)),
                    "MONSTER": (self.monsters, 1),
                },
                is_time_consuming=False,  # Can be, luck of the draw
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Win the TOURNAMENT with a Sueki Suezo",
                data={
                    "TOURNAMENT": (self.sueki_tournaments, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Defeat the Boss Monster at the end of an Errantry to ERR_DEST with a MONSTER",
                data={
                    "ERR_DEST": (self.errantries, 1),
                    "MONSTER": (self.monsters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Go on an expedition to EXPEDITION",
                data={
                    "EXPEDITION": (self.expeditions, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete NUM jobs in the Town",
                data={
                    "NUM": ((lambda: list(range(5, 26))), 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Raise a MONSTER until it dies from natural causes",
                data={
                    "MONSTER": (self.monsters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Cocoon a Worm MODIFIER",
                data={
                    "MODIFIER": ((lambda: ["", "", "into a Beaclon"]), 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Obtain a ITEM",
                data={
                    "ITEM": (self.nonshop_items, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]

        for monster, tech_function in tech_functions.items():
            objectives.append(
                GameObjectiveTemplate(
                    label=f"Obtain two of the following techs on a {monster} main breed: TECHS",
                    data={
                        "TECHS": (tech_function, range(3, min(5, len(tech_function())) + 1)),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                )
            )

        return objectives

    def unlocked_monster(self, monster: str) -> bool:
        default_mons = [
            "Ape",
            "Arrow Head",
            "ColorPandora",
            "Gaboo",
            "Jell",
            "Hare",
            "Hopper",
            "Kato",
            "Mocchi",
            "Monol",
            "Naga",
            "Pixie",
            "Plant",
            "Suezo",
            "Tiger",
            "Zuum",
        ]
        return (monster in default_mons or
                monster in self.archipelago_options.monster_rancher_2_dx_unlocked_main_breeds or
                monster in self.archipelago_options.monster_rancher_2_dx_unlocked_sub_breeds)

    def apes(self) -> List[str]:
        apes = [
            "Ape",
            "Bossy",
            "Rock Ape",
            "Gibberer",
            "Tropical Ape",
            "Gold Dust",
        ]

        if self.unlocked_monster("King Ape"):
            apes.append("King Ape")

        return apes

    def arrowheads(self) -> List[str]:
        arrowheads = [
            "Arrow Head",
            "Priarocks",
            "Renocraft",
            "MustardArrow",
            "Sumopion"
        ]

        if self.unlocked_monster("Durahan"):
            arrowheads.append("Plated Arrow")

        if self.unlocked_monster("Joker"):
            arrowheads.append("Selketo")

        if self.unlocked_monster("Mock"):
            arrowheads.append("Log Sawer")

        if self.unlocked_monster("Silver Face"):
            arrowheads.append("Silver Face")

        return arrowheads

    def bajarls(self) -> List[str]:
        bajarls = [
            "Bajarl",
            "Boxer Bajarl",
            "Magic Bajarl",
            "Gym Bajarl",
            "Ultrarl",
        ]

        if self.unlocked_monster("Joker"):
            bajarls.append("Jaba")

        return bajarls

    def bakus(self) -> List[str]:
        bakus = [
            "Baku",
            "Magmax",
            "Higante",
            "Gontar",
            "Giga Pint",
            "Nussie",
            "Icebergy",
            "Shishi",
            "Dango"
        ]

        if self.unlocked_monster("Durahan"):
            bakus.append("War Baku")

        if self.unlocked_monster("Joker"):
            bakus.append("Baku Clown")

        return bakus

    def beaclons(self) -> List[str]:
        beaclons = [
            "Beaclon",
            "Bethelgeus",
            "Rocklon",
            "Melcarba",
            "Sloth Beetle",
            "Eggplantern"
        ]

        if self.unlocked_monster("Bajarl"):
            beaclons.append("KautRoarKaut")

        if self.unlocked_monster("Ducken"):
            beaclons.append("Ducklon")

        if self.unlocked_monster("Durahan"):
            beaclons.append("Centurion")

        if self.unlocked_monster("Joker"):
            beaclons.append("Jaggernaut")

        return beaclons

    def centaurs(self) -> List[str]:
        centaurs = [
            "Centaur",
            "Antares",
            "Dragoon",
            "Trojan",
            "Ferious",
            "Celious",
            "Blue Thunder",
            "Trotter"
        ]

        if self.unlocked_monster("Bajarl"):
            centaurs.append("Bazoo")

        if self.unlocked_monster("Durahan"):
            centaurs.append("Chariot")

        if self.unlocked_monster("Joker"):
            centaurs.append("Reaper")

        if self.unlocked_monster("Sniper"):
            centaurs.append("Sniper")

        return centaurs

    @staticmethod
    def colorpandoras() -> List[str]:
        return [
            "ColorPandora",
            "Liquid Cube",
            "PeachTreeBug",
            "Dice",
            "Tram"
        ]

    def dragons(self) -> List[str]:
        dragons = [
            "Dragon",
            "Crab Dragon",
            "Gariel",
            "Stone Dragon",
            "Tecno Dragon",
            "Oscerot",
            "Ragnaroks",
            "Tiamat",
            "Hound Dragon",
            "Moo"
        ]

        if self.unlocked_monster("Bajarl"):
            dragons.append("Dodongo")

        if self.unlocked_monster("Beaclon"):
            dragons.append("Corkasus")

        if self.unlocked_monster("Durahan"):
            dragons.append("Armor Dragon")

        if self.unlocked_monster("Joker"):
            dragons.append("Death Dragon")

        if self.unlocked_monster("Metalner"):
            dragons.append("Gidras")

        if self.unlocked_monster("Magma Heart"):
            dragons.append("Magma Heart")

        return dragons

    @staticmethod
    def duckens() -> List[str]:
        return [
            "Ducken",
            "Blocken",
            "Ticken",
            "Cawken",
            "Watermelony",
        ]

    def durahans(self) -> List[str]:
        durahans = [
            "Durahan",
            "Lorica",
            "Vesuvius",
            "Kelmadics",
            "Leziena",
            "Hound Knight",
            "Kokushi Muso",
            "Ruby Knight",
            "Shogun",
        ]

        if self.unlocked_monster("Beaclon"):
            durahans.append("Hercules")

        if self.unlocked_monster("Joker"):
            durahans.append("Genocider")

        if self.unlocked_monster("Metalner"):
            durahans.append("Metal Glory")

        if self.unlocked_monster("Mock"):
            durahans.append("Wood Knight")

        if self.unlocked_monster("Phoenix"):
            durahans.append("Garuda")

        return durahans

    def gaboos(self) -> List[str]:
        gaboos = [
            "Gaboo",
            "Jelly Gaboo",
            "Frozen Gaboo",
            "GabooSoldier",
            "Mad Gaboo",
        ]

        if self.unlocked_monster("Joker"):
            gaboos.append("Dokoo")

        return gaboos

    @staticmethod
    def galis() -> List[str]:
        return [
            "Gali",
            "Stone Mask",
            "Furred Mask",
            "Aqua Mask",
            "Galirous",
            "Purple Mask",
            "Pink Mask",
            "Colorful",
            "Suezo Mask",
            "Fanged Mask",
            "Brown Mask",
            "Scaled Mask",
        ]

    @staticmethod
    def ghosts() -> List[str]:
        return ["Ghost", "Chef"]

    def golems(self) -> List[str]:
        golems = [
            "Golem",
            "Dagon",
            "Tyrant",
            "Amenhotep",
            "Moaigon",
            "Gobi",
            "Poseidon",
            "Black Golem",
            "Marble Guy",
            "Pink Golem",
            "Ecologuardia",
            "Titan",
            "Big Blue",
            "Magna",
            "Scaled Golem",
            "Forward Golem",
            "Dream Golem",
        ]

        if self.unlocked_monster("Bajarl"):
            golems.append("Dao")

        if self.unlocked_monster("Baku"):
            golems.append("Sleepyhead")

        if self.unlocked_monster("Beaclon"):
            golems.append("Strong Horn")

        if self.unlocked_monster("Durahan"):
            golems.append("Battle Rocks")

        if self.unlocked_monster("Joker"):
            golems.append("Angolmor")

        if self.unlocked_monster("Metalner"):
            golems.append("Astro")

        if self.unlocked_monster("Mock"):
            golems.append("Wood Golem")

        if self.unlocked_monster("Wracky"):
            golems.append("Mariomax")

        if self.unlocked_monster("Zilla"):
            golems.append("Pressure")

        if self.unlocked_monster("Sand Golem"):
            golems.append("Sand Golem")

        return golems

    @staticmethod
    def hares() -> List[str]:
        return [
            "Hare",
            "Prince Hare",
            "Rocky Fur",
            "Jelly Hare",
            "Evil Hare",
            "Purple Hare",
            "Fairy Hare",
            "Leaf Hare",
            "Four Eyed",
            "Blue Hare",
            "Wild Hare",
            "Scaled Hare",
            "Kung Fu Hare",
            "Tornado"
        ]

    def hengers(self) -> List[str]:
        hengers = [
            "Henger",
            "Garlant",
            "Proto",
            "Gaia",
            "Black Henger",
            "Omega",
            "Skeleton",
        ]

        if self.unlocked_monster("Joker"):
            hengers.append("End Bringer")

        if self.unlocked_monster("Metalner"):
            hengers.append("Heuy")

        if self.unlocked_monster("Mock"):
            hengers.append("Automaton")

        return hengers

    def hoppers(self) -> List[str]:
        hoppers = [
            "Hopper",
            "Draco Hopper",
            "Mustachios",
            "Pink Hopper",
            "Fairy Hopper",
            "Rear Eyed",
            "Skipper",
            "Frog Hopper",
        ]

        if self.unlocked_monster("Bajarl"):
            hoppers.append("Emerald Eye")

        if self.unlocked_monster("Jill"):
            hoppers.append("Snow Hopper")

        if self.unlocked_monster("Joker"):
            hoppers.append("Sneak Hopper")

        if self.unlocked_monster("Metalner"):
            hoppers.append("Springer")

        if self.unlocked_monster("Mock"):
            hoppers.append("Woody Hopper")

        if self.unlocked_monster("Bloody Eye"):
            hoppers.append("Bloody Eye")

        return hoppers

    @staticmethod
    def jells() -> List[str]:
        return [
            "Jell",
            "Noble Jell",
            "Wall Mimic",
            "Muddy Jell",
            "Clay",
            "Purple Jell",
            "Pink Jam",
            "Chloro Jell",
            "Eye Jell",
            "Icy Jell",
            "Worm Jell",
            "Scaled Jell",
            "Metal Jell"
        ]

    def jills(self) -> List[str]:
        jills = [
            "Jill",
            "Wondar",
            "Bengal",
            "Pong Pong",
            "Zorjil",
            "Pierry",
            "Pithecan"
        ]

        if self.unlocked_monster("Joker"):
            jills.append("Skull Capped")

        if self.unlocked_monster("Bighand"):
            jills.append("Bighand")

        return jills

    def jokers(self) -> List[str]:
        jokers = [
            "Joker",
            "Flare Death",
            "Tombstone",
            "Hell Heart",
            "Blue Terror",
            "Bloodshed",
        ]

        if self.unlocked_monster("Bajarl"):
            jokers.append("Odium")

        return jokers

    def katos(self) -> List[str]:
        katos = [
            "Kato",
            "Draco Kato",
            "Gordish",
            "Pink Kato",
            "Citronie",
            "Blue Kato",
            "Ninja Kato",
            "Axer",
        ]

        if self.unlocked_monster("Joker"):
            katos.append("Tainted Cat")

        if self.unlocked_monster("Crescent"):
            katos.append("Crescent")

        return katos

    @staticmethod
    def metalners() -> List[str]:
        return ["Metalner", "Love Seeker", "Metazorl", "Chinois"]

    @staticmethod
    def mews() -> List[str]:
        return ["Mew", "Eared Mew", "Aqua Mew", "Mum Mew", "Bowwow", "Swimmer"]

    def mocchis(self) -> List[str]:
        mocchis = [
            "Mocchi",
            "Draco Mocchi",
            "Gelatine",
            "Nyankoro",
            "Manna",
            "Fake Penguin",
            "Caloriena",
            "GentleMocchi",
            "Mocchini",
        ]

        if self.unlocked_monster("Durahan"):
            mocchis.append("KnightMocchi")

        if self.unlocked_monster("Joker"):
            mocchis.append("Hell Pierrot")

        if self.unlocked_monster("White Mocchi"):
            mocchis.append("White Mocchi")

        return mocchis

    def mocks(self) -> List[str]:
        mocks = [
            "Mock",
            "Pole Mock",
            "White Birch",
        ]

        if self.unlocked_monster("Joker"):
            mocks.append("Ebony")

        return mocks

    def monols(self) -> List[str]:
        monols = [
            "Monol",
            "Ivory Wall",
            "Obelisk",
            "Furred Wall",
            "Ice Candy",
            "Asphaultum",
            "Romper Wall",
            "New Leaf",
            "Sandy",
            "Blue Sponge",
            "Soboros",
            "Jura Wall",
            "Dominos",
            "Galaxy",
            "Scribble",
        ]

        if self.unlocked_monster("Burning Wall"):
            monols.append("Burning Wall")

        return monols

    def nagas(self) -> List[str]:
        nagas = [
            "Naga",
            "Bazula",
            "Trident",
            "Edgehog",
            "Aqua Cutter",
            "Crimson Eyed",
            "Ripper",
            "Jungler",
            "Cyclops",
            "Striker",
            "Earth Keeper",
            "Stinger",
            "Time Noise"
        ]

        if self.unlocked_monster("Punisher"):
            nagas.append("Punisher")

        return nagas

    def nitons(self) -> List[str]:
        nitons = [
            "Niton",
            "Ammon",
            "Clear Shell",
            "Stripe Shell",
            "Disc Niton",
            "Dribbler",
            "Radial Niton",
        ]

        if self.unlocked_monster("Bajarl"):
            nitons.append("Alabia Niton")

        if self.unlocked_monster("Durahan"):
            nitons.append("Knight Niton")

        if self.unlocked_monster("Metalner"):
            nitons.append("Metal Shell")

        if self.unlocked_monster("Mock"):
            nitons.append("Baum Kuchen")

        return nitons

    def phoenixes(self) -> List[str]:
        phoenixes = [
            "Phoenix",
            "Cinder Bird",
        ]

        if self.unlocked_monster("Blue Phoenix"):
            phoenixes.append("Blue Phoenix")

        return phoenixes

    def pixies(self) -> List[str]:
        pixies = [
            "Pixie",
            "Daina",
            "Angel",
            "Granity",
            "Lepus",
            "Nagisa",
            "Kitten",
            "Silhouette",
            "Allure",
            "Serenity",
            "Vanity",
            "Mint",
            "Night Flyer",
            "Dixie",
            "Kasumi",
            "Mia",
            "Poison",
        ]

        if self.unlocked_monster("Bajarl"):
            pixies.append("Jinnee")

        if self.unlocked_monster("Centaur"):
            pixies.append("Unico")

        if self.unlocked_monster("Durahan"):
            pixies.append("Janne")

        if self.unlocked_monster("Jill"):
            pixies.append("Snowy")

        if self.unlocked_monster("Joker"):
            pixies.append("Lilim")

        if self.unlocked_monster("Metalner"):
            pixies.append("Futurity")

        if self.unlocked_monster("Mock"):
            pixies.append("Dryad")

        if self.unlocked_monster("Wracky"):
            pixies.append("Jilt")

        return pixies

    @staticmethod
    def plants() -> List[str]:
        return [
            "Plant",
            "Gold Plant",
            "Rock Plant",
            "Hare Plant",
            "Mirage Plant",
            "Black Plant",
            "Weeds",
            "Queen Plant",
            "Usaba",
            "Blue Plant",
            "Fly Plant",
            "Scaled Plant"
        ]

    def suezos(self) -> List[str]:
        suezos = [
            "Suezo",
            "Orion",
            "Rocky Suezo",
            "Furred Suezo",
            "Clear Suezo",
            "Red Eye",
            "Purple Suezo",
            "Pink Eye",
            "Green Suezo",
            "Horn",
            "Fly Eye",
            "Melon Suezo",
            "Birdie",
            "Bronze Suezo",
            "Silver Suezo",
            "Gold Suezo",
            # Sueki Suezo cannot be used here, Sueki lives for a single week
        ]

        if self.unlocked_monster("White Suezo"):
            suezos.append("White Suezo")

        return suezos

    def tigers(self) -> List[str]:
        tigers = [
            "Tiger",
            "Balon",
            "Rock Hound",
            "Hare Hound",
            "Jelly Hound",
            "Terror Dog",
            "Cabalos",
            "Daton",
            "Tropical Dog",
            "Mono Eyed",
            "Jagd Hound",
            "Datonare",
            "White Hound"
        ]

        if self.unlocked_monster("Kamui"):
            tigers.append("Kamui")

        return tigers

    def undines(self) -> List[str]:
        undines = ["Undine", "Mermaid"]

        if self.unlocked_monster("Joker"):
            undines.append("Siren")

        return undines

    @staticmethod
    def worms() -> List[str]:
        return [
            "Worm",
            "Mask Worm",
            "Rock Worm",
            "Corone",
            "Jelly Worm",
            "Black Worm",
            "Purple Worm",
            "Red Worm",
            "Flower Worm",
            "Eye Worm",
            "Drill Tusk",
            "Scaled Worm",
            "Express Worm",
        ]

    def wrackys(self) -> List[str]:
        wrackys = [
            "Wracky",
            "Draco Doll",
            "Pebbly",
            "Henger Doll",
            "Baby Doll",
            "Satan Clause",
            "Santy"
        ]

        if self.unlocked_monster("Bajarl"):
            wrackys.append("Bakky")

        if self.unlocked_monster("Durahan"):
            wrackys.append("Petit Knight")

        if self.unlocked_monster("Joker"):
            wrackys.append("Tricker")

        if self.unlocked_monster("Metalner"):
            wrackys.append("Metal Glay")

        if self.unlocked_monster("Mock"):
            wrackys.append("Mocky")

        return wrackys

    def zillas(self) -> List[str]:
        zillas = [
            "Zilla",
            "Gigalon",
            "Pink Zilla",
            "Gooji",
            "Deluxe Liner"
        ]

        if self.unlocked_monster("Zilla King"):
            zillas.append("Zilla King")

        return zillas

    def zuums(self) -> List[str]:
        zuums = [
            "Zuum",
            "Crab Saurian",
            "Hachiro",
            "Salamander",
            "NobleSaurian",
            "Rock Saurian",
            "Spot Saurian",
            "JellySaurian",
            "Tasman",
            "BlackSaurian",
            "Naga Saurian",
            "FairySaurian",
            "AlohaSaurian",
            "Mustardy",
            "HoundSaurian",
            "ShellSaurian",
            "ZebraSaurian",
        ]

        if self.unlocked_monster("Bajarl"):
            zuums.append("Sand Saurian")

        if self.unlocked_monster("Joker"):
            zuums.append("Basilisk")

        if self.unlocked_monster("Mock"):
            zuums.append("Wood Saurian")

        if self.unlocked_monster("Wild Saurian"):
            zuums.append("Wild Saurian")

        return zuums

    def monsters(self):
        monster_functions: Dict[str, Callable[[], List[str]]] = {
            "Ape": self.apes,
            "Arrow Head": self.arrowheads,
            "Bajarl": self.bajarls,
            "Baku": self.bakus,
            "Beaclon": self.beaclons,
            "Centaur": self.centaurs,
            "ColorPandora": self.colorpandoras,
            "Dragon": self.dragons,
            "Ducken": self.duckens,
            "Durahan": self.durahans,
            "Gaboo": self.gaboos,
            "Gali": self.galis,
            "Ghost": self.ghosts,
            "Golem": self.golems,
            "Hare": self.hares,
            "Henger": self.hengers,
            "Hopper": self.hoppers,
            "Jell": self.jells,
            "Jill": self.jills,
            "Joker": self.jokers,
            "Metalner": self.metalners,
            "Mew": self.mews,
            "Mocchi": self.mocchis,
            "Mock": self.mocks,
            "Monol": self.monols,
            "Naga": self.nagas,
            "Niton": self.nitons,
            "Phoenix": self.phoenixes,
            "Pixie": self.pixies,
            "Plant": self.plants,
            "Suezo": self.suezos,
            "Tiger": self.tigers,
            "Undine": self.undines,
            "Worm": self.worms,
            "Wracky": self.wrackys,
            "Zilla": self.zillas,
            "Zuum": self.zuums,
        }

        monsters = []
        for monster, function in monster_functions.items():
            if self.unlocked_monster(monster):
                monsters.extend(function())

        return monsters

    @staticmethod
    def sueki_tournaments() -> List[str]:
        return [
            "New Year Cup",
            "Torles Tourney",
            "Blizzard Cup",
            "Parepare Cup (Spring)",
            "IMa Official Cup (E)",
            "IMa Official Cup (D)",
            "Spring Carnival (D)",
            "Blue Sky Cup",
            "Gemini Cup",
            "Freshmen's Cup",
            "Nageel Cup",
            "Desert Moon Cup",
            "Monster Pups' Cup",
            "Artemis Cup",
            "Rookie Cup",
            "Galoe Cup",
            "Maple Cup",
            "Parepare Cup (Winter)"
        ]

    @staticmethod
    def tournaments() -> List[str]:
        return [
            # January
            "Sirius Cup",
            "Torble University Cup",
            "New Year Cup",
            # February
            "Greatest 4",
            "Poannka Cup",
            "Torles Tourney",
            "Kawrea Cup",
            "Blizzard Cup",
            "Durahan Invitational",
            # March
            "Parepare Cup (Spring)",
            "Troron Cup",
            # April
            "Spring Carnival (D)",
            "Phoenix Cup"
            "Spring Carnival (C)",
            "Legend Cup",
            "Spring Carnival (B)",
            # May
            "IMa Chairman Cup (Spring)",
            "M-1 Grand Prix",
            "Colart Cup",
            "Taurus Cup",
            "Blue Sky Cup",
            "Gemini Cup",
            # June
            "Freshmen's Cup",
            "Elder's Cup",  # Might be issues with this one, can cause fun situations
            # July
            "Papas' Cup (Summer)",
            "Crab Cup",
            "Nageel Cup",
            "IMa - FIMBa Elimination Qualifier",
            # August
            "Torble Sea Cup",
            "Winner's Cup",
            "Dragon Invitational",
            "Desert Moon Cup",
            "Summer Carnival",
            "Monster Pups' Cup",
            "IMa - FIMBA Meet",
            # September
            "Telomeann Cup",
            "Manseitan Cup",
            "Artemis Cup",
            # October
            "Papas' Cup (Autumn)",
            "Kasseitan Cup",
            "Rookie Cup",
            "Hero's Cup",
            "Heel's Cup",  # might also be problematic? nature is difficult to manip
            # November
            "World Monsters Cup",
            "Torble Port Cup",
            "Galoe Cup",
            "Mandy Cup",
            "Maple Cup",
            "IMa Chairman Cup (Autumn)",
            # December
            "Parepare Cup (Winter)",
            "Larox Cup",
            # IMa Official
            "IMa Official Cup (S)",
            "IMa Official Cup (A)",
            "IMa Official Cup (B)",
            "IMa Official Cup (C)",
            "IMa Official Cup (D)",
            "IMa Official Cup (E)",
        ]

    @staticmethod
    def expeditions() -> List[str]:
        return ["Kawrea", "Torles Mountains", "Parepare"]

    @staticmethod
    def nonshop_items() -> List[str]:
        return [
            "Gold Peach",
            "Paradoxine",
            "Half Eaten",
            "Rock Candy",
            "Irritater",
            "Griever",
            "Teromeann",
            "Silver Peach",
            "Quack Doll",
            "Sculpture",
            "Dino Tail",
            "Fire Stone",
            "Flower",
            "Gemini's Pot",
            "Hero Badge",
            "Heel Badge",
            "Lump of Ice",
            "Pure Gold",
            "Pure Silver",
            "Pure Platina",
            "God's Slate",
            "Gold Medal",
            "Music Box",
            "Taurus' Horn",
            "Old Sheath",
            "Crab's Claw",

        ]

    @staticmethod
    def errantries() -> List[str]:
        return ["Kawrea", "Parepare", "Torble Sea", "Mandy", "Papas"]

    # Techs!

    @staticmethod
    def ape_techs() -> List[str]:
        return [
            "Sneeze",
            "Swing-Throw",
            "Blast",
            "Boomerang",
            "Grab-Throw",
            "Big Banana",
            "Roll Assault",
            "Bomb",
            "Big Bomb",
            "Tasty Banana"
        ]

    @staticmethod
    def arrowhead_techs() -> List[str]:
        return [
            "Claw Pinch",
            "Bloodsuction",
            "Somersault",
            "Somersaults",
            "Sting Slash",
            "Long Punch",
            "Sting",
            "TripleStings",
            "Tail Swing",
            "Tail Swings",
            "Death Scythe",
            "Jumping Claw",
            "Aerial Claw",
            "Acrobatics",
            "Meteor",
            "Cyclone",
            "Hidden Sting",
            "Energy Shot",
            "Energy Shots",
            "Javelin",
            "Roll Assault",
            "Fist Missile",
        ]

    @staticmethod
    def bajarl_techs() -> List[str]:
        return [
            "Hook",
            "1-2-Hook",
            "Straight",
            "Uppercut",
            "1-2-Uppercut",
            "1-2-Smash",
            "Magic Punch",
            "Mystic Combo",
            "Mystic Punch",
            "Magic Pot",
            "Mystic Pot",
            "Miracle Pot",
            "Bajarl Beam"
        ]

    @staticmethod
    def baku_techs() -> List[str]:
        return [
            "Bite",
            "Two Bites",
            "Three Bites",
            "Tongue Slap",
            "Roar",
            "Two Roars",
            "MillionRoars",
            "Diving Press",
            "Sneeze",
            "Mating Song",
            "Gust Breath",
            "Hypnotism",
            "Nap"
        ]

    @staticmethod
    def beaclon_techs() -> List[str]:
        return [
            "Heavy Punch",
            "MaximalPunch",
            "Horn Attack",
            "SpinningHorn",
            "Punch Combo",
            "Beaclon Combo",
            "Triple Stabs",
            "Dive Assault",
            "Spiral Dive",
            "Tremor",
            "Horn Combo",
            "Horn Smash",
            "Earthquake",
            "Top Assault",
            "Rolling Bomb",
            "Flying Press",
            "Horn Cannon",
            "Frantic Horn",
            "Fist Missile",
        ]

    @staticmethod
    def centaur_techs() -> List[str]:
        return [
            "Stab Combo",
            "Triple Stabs",
            "Stab-Throw",
            "Z Slash",
            "Turn Stab",
            "Mind Flare",
            "Mind Blast",
            "Cross Slash",
            "Energy Shot",
            "Javelin",
            "Death Thrust",
            "Rush Slash",
            "Energy Shots",
            "Jump Javelin",
            "Meteor Drive",
        ]

    @staticmethod
    def colorpandora_techs() -> List[str]:
        return [
            "Giant Whip",
            "Two Swings",
            "Kamikaze",
            "Vital Ritual",
            "Cracker",
            "Megacracker",
            "Triple Shots",
            "Delta Attack",
            "Shotgun",
            "Megashotgun",
            "Giant Wheel",
            "Spiral Rush",
            "Meteor Drive"
        ]

    @staticmethod
    def dragon_techs() -> List[str]:
        return [
            "Tail Attack",
            "Two Bites",
            "Dragon Punch",
            "Wing Attack",
            "Wing Combo",
            "Claw Combo",
            "Claw",
            "Spinning Claw",
            "Flutter",
            "Flutters",
            "Trample",
            "Fire Breath",
            "Dragon Combo",
            "Inferno",
            "Glide Charge",
            "SlammingDown",
            "Flying Combo",
        ]

    @staticmethod
    def ducken_techs() -> List[str]:
        return [
            "Explosion",
            "Ducken Dance",
            "Surprise",
            "Bound Charge",
            "Bound Stamp",
            "Bound",
            "Eye Beam",
            "Beam Shower",
            "Maximal Beam",
            "Bombing",
            "Boomerang",
            "Missile",
            "Two Missiles",
            "Big Missile",
            "Falling Beak",
            "Frantic Beam"
        ]

    @staticmethod
    def durahan_techs() -> List[str]:
        return [
            "Swing",
            "TwisterSlash",
            "Thunderbolt",
            "Flash Slash",
            "Triple Slash",
            "Slash Combo",
            "MillionStabs",
            "Punch Combo",
            "DeathBringer",
            "Kick Combo",
            "V Slash",
            "Dash Slash",
            "Charge",
            "Air Shot",
            "Jumping Stab",
            "RollingSlash",
            "Lightning",
            "Blast Shot",
            "Sword Throw",
            "Gust Slash",
        ]

    @staticmethod
    def gaboo_techs() -> List[str]:
        return [
            "Acid Spit",
            "Diving Press",
            "Chop Combo",
            "Samurai Kick",
            "Rolling Chop",
            "Shock Wave",
            "Back Blow",
            "ElectricBlow",
            "Ninja Kick",
            "Straight",
            "Cyclone",
            "Kiss",
            "Long Punch",
            "Spit",
            "Jumping Chop"
        ]

    @staticmethod
    def gali_techs() -> List[str]:
        return [
            "Back Blow",
            "Fire Wall",
            "Blaze Wall",
            "Napalm",
            "Heavy Blow",
            "Thwack",
            "Whirlwind",
            "Typhoon",
            "Hurricane",
            "Spirit Blow",
            "Smash Whack",
            "Red Wisp",
            "Blue Wisp",
            "Flying Mask",
            "Spirit Punch",
            "Giant Blow",
            "Giant Thwack",
            "Cutting Mask",
            "Hashing Mask",
            "Spirit Smash",
        ]

    @staticmethod
    def ghost_techs() -> List[str]:
        return [
            "Uppercut",
            "Combination",
            "Energy Shot",
            "Surprise",
            "Astonishment",
            "Necromancy",
            "Dove Bomb",
            "Pigeon Bomb",
            "Magic Card",
            "Magic Cards",
        ]

    @staticmethod
    def golem_techs() -> List[str]:
        return [
            "Heavy Punch",
            "Heavy Kick",
            "Slap",
            "Uppercut",
            "Thwack",
            "Brow Hit",
            "Smash Thwack",
            "Clap Attack",
            "Palm Strike",
            "Double Palms",
            "Heavy Slap",
            "Diving Press",
            "Charge",
            "Roll Assault",
            "Brow Smash",
            "Earthquake",
            "Giant Clap",
            "Fist Shot",
            "Fist Missile",
            "Cyclone"
        ]

    @staticmethod
    def hare_techs() -> List[str]:
        return [
            "Straight",
            "HardStraight",
            "Kung Fu Fist",
            "Kung Fu Blow",
            "Bang",
            "Big Bang",
            "Back Blow",
            "Rolling Blow"
            "Smash",
            "Heavy Smash",
            "High Kick",
            "Spin Kick",
            "Foul Gas",
            "Kung Fu Kick",
            "Stinking Gas",
        ]

    @staticmethod
    def henger_techs() -> List[str]:
        return [
            "Kick",
            "Heavy Chop",
            "Laser Cutter",
            "Yoyo",
            "Laser Sword",
            "Laser Swords",
            "Two Cutters",
            "Two Yoyos",
            "Arm Cannon",
            "Napalm Shot",
            "Hammer Fall",
            "Burst Cannon",
            "Sledge Fall",
            "Sound Wave",
            "Fist Missile",
            "Drill Shot",
            "Drill Shots",
            "Eye Beam"
        ]

    def hopper_techs(self) -> List[str]:
        techs = [
            "Jump Blow",
            "2 Jump Blows",
            "3 Jump Blows",
            "1-2 Jump Blow",
            "Hopper Combo",
            "Flick",
            "Rapid Flick",
            "Flick Combo",
        ]

        # Hopper has two mutually exclusive tech sets
        if self.random.random() > 0.5:
            techs.append("Phantom Claw")
        else:
            techs.extend(["Lightning", "Flame"])

        return techs

    @staticmethod
    def jell_techs() -> List[str]:
        return [
            "Pierce",
            "Suffocation",
            "Bloodsuction",
            "Two Whips",
            "Jell Press",
            "Jell Cube",
            "Three Cubes",
            "Jell Top",
            "Spiked Top",
            "Fly Swatter",
            "Fly Smasher",
            "Beam Gun",
            "Beam Cannon",
            "Cannon",
            "Slingshot",
            "Pyramid",
            "Gatling Gun",
            "Jell Copter",
        ]

    @staticmethod
    def jill_techs() -> List[str]:
        return [
            "Ice Spikes",
            "Clap Attack",
            "Punch Combo",
            "Slap Combo",
            "Cold Breath",
            "Ice Wave",
            "Frantic Rush",
            "Jill Combo",
            "Ice Meteor",
            "Snowstorm",
        ]

    @staticmethod
    def joker_techs() -> List[str]:
        return [
            "Death Slash",
            "Death Cutter",
            "Death Energy",
            "Death Final",
        ]

    def kato_techs(self) -> List[str]:
        techs = [
            "Slash Claws",
            "Claw Combo",
            "Smoke Breath",
            "Oil Spray",
            "Turn Claw",
            "Turn Claws",
            "Rolling Claw",
            "Oil Fire",
            "Oil Flame",  # Remove for explicit PSX support
            "Drill Claw",
            "Twister Claw",
            "Tornado Claw",
            "Phantom Claw",
            "Hopping Claw",
            "Jumping Claw",
            "Aerial Claw",
            "Oil Drinking"
        ]

        rand_num = self.random.random()
        if rand_num < 0.33:
            techs.append("Lick")
        elif rand_num < 0.66:
            techs.append("Licking")  # yes, these two are separate AND mutually exclusive
        else:
            techs.append("Bolt")

        return techs

    @staticmethod
    def metalner_techs() -> List[str]:
        return [
            "Back Charge",
            "Straight",
            "High Kick",
            "Double Kicks",
            "Dash Straight",
            "Elbow Strike",
            "Double Palms",
            "Palm Strike",
            "Metalner Ray",
            "Burning Palms",
            "UFO Attack"
        ]

    @staticmethod
    def mew_techs() -> List[str]:
        return [
            "Head Butt",
            "Head Assault",
            "Scratch",
            "Stab",
            "RushingPunch",
            "Diving Press",
            "HundredBlows",
            "MillionBlows",
            "Twiddling",
            "Twiddling-2",
            "Twiddling-Z",
            "Miaow",
            "Song of Mew",
            "Recital",
            "Zap",
            "Maximal Zap"
        ]

    @staticmethod
    def mocchi_techs() -> List[str]:
        return [
            "Thrust",
            "1-2 Thrust",
            "Thrusts",
            "Licking",
            "Press",
            "Diving Press",
            "Giant Press",
            "Roll Attack",
            "DazzlingRoll",
            "Petal Swirl",
            "Petal Vortex",
            "Petal Storm",
            "Mocchi Ray",
            "Mocchi Beam",
            "MocchiCannon",
            "Flame",  # Mocchi/Dragon only
            "Roll Assault",
            "Petal Roll"
        ]

    @staticmethod
    def mock_techs() -> List[str]:
        return [
            "Leaf Cutter",
            "Leaf Gatling",
            "Twig Gun",
            "Twig Gatling",
            "Energy Steal",
            "Twister",
            "Twisters",
        ]

    @staticmethod
    def monol_techs() -> List[str]:
        return [
            "Needle Stabs",
            "Spike Stabs",
            "Ray",
            "Double Rays",
            "Triple Rays",
            "Spike Bite",
            "Scratch",
            "Knock",
            "Two Knocks",
            "Three Knocks",
            "Flattening-L",
            "Screech",
            "StrangeLight",
            "Flattening-X",
            "Sound Wave",
            "Tentacles",
            "Beam",
            "Double Beams",
            "Triple Beams",
        ]

    @staticmethod
    def naga_techs() -> List[str]:
        return [
            "Stab",
            "Pierce",
            "Tail Assault",
            "Life Steal",
            "Poison Gas",
            "Energy Shot",
            "Turn Assault",
            "Drill Attack",
            "Eye Beam",
            "Energy Shots",
        ]

    @staticmethod
    def niton_techs() -> List[str]:
        return [
            "Numbing Stab",
            "ElectricStab",
            "Sound Wave",
            "Sound Wave-L",
            "Sound Wave-X",
            "Shock",
            "Severe Shock",
            "MaximalShock",
            "Niton Ink",
            "Shell Attack",
            "Spiked Shell",
            "ViolentShell",
        ]

    @staticmethod
    def phoenix_techs() -> List[str]:
        return [
            "Rapid Beaks",
            "Flame Shot",
            "Flame Cannon",
            "Fire Twister",
            "Fire Tornado",
            "Heat Beam",
            "Fire Stream",
            "Fire Wave",
        ]

    def pixie_techs(self) -> List[str]:
        techs = [
            "Slap",
            "High Kick",
            "Heel Raid",
            "Bang",
            "Big Bang",
            "Bolt",
            "Lightning",
            "Kiss",
            "Life Steal",
            "Refreshment",
            "Flame",
            "Gigaflame",
            "Ray",
            "Megaray",
            "Gigaray",
        ]

        rand_num = self.random.random()
        if rand_num < 0.25:
            techs.append("Phantom Claw")
        elif rand_num < 0.5:
            techs.append("Death Final")
        elif rand_num < 0.75:
            techs.append("1-2 Punch")
        else:
            techs.append("Fire Breath")

        return techs

    @staticmethod
    def plant_techs() -> List[str]:
        return [
            "Root Attack",
            "Root Combo",
            "Life Steal",
            "Jab Combo",
            "Plant Combo",
            "Toxic Nectar",
            "Toxic Pollen",
            "Face Drill",
            "Seed Gun",
            "Seed Gatling"
        ]

    @staticmethod
    def suezo_techs() -> List[str]:
        return [
            "Tongue Slap",
            "Kiss",
            "Bite",
            "Lick",
            "Chewing",
            "Teleport",
            "Telekinesis",
            "Telepathy",
            "Eye Beam",
            "Yodel"
        ]

    @staticmethod
    def tiger_techs() -> List[str]:
        return [
            "Bolt",
            "One-Two",
            "Lightning",
            "Charge",
            "Combination",
            "Ice Bomb",
            "Stab",
            "Roll Assault",
            "Blizzard",
            "Roar",
        ]

    @staticmethod
    def undine_techs() -> List[str]:
        return [
            "Ice Swords",
            "Dolphin Blow",
            "Splash",
            "Aqua Whip",
            "Two Whips",
            "Kiss",
            "Arrow",
            "Aqua Wave",
            "Aqua Waves",
            "Ice Coffin",
            "Ice Arrow",
            "Aqua Whirl",
            "Water Gun",
            "Icicle Arrow",
            "Hailstorm",
            "Cold Storm",
            "Vitalization",
            "Cold Geyser",
            "Water Cannon",
        ]

    @staticmethod
    def worm_techs() -> List[str]:
        return [
            "Somersault",
            "Somersaults",
            "Tail Lash",
            "Two Lashes",
            "Three Lashes",
            "Roll Assault",
            "Pierce-Throw",
            "Pinch-Throw",
            "Pierce",
            "Tusk Slash",
            "Injection",
            "Poison Gas",
            "Wheel Attack",
        ]

    def wracky_techs(self) -> List[str]:
        techs = [
            "Weapon Combo",
            "Kick",
            "Spin Kick",
            "Twister Kick",
            "Punch",
            "Heavy Punch",
            "Wracky Combo",
            "Necromancy",
            "Sneak Attack",
            "Sneak Combo",
            "Spin Slash",
            "Trick",
            "Head Spike",
            "Fire Spike",
            "Air Shot",
            "Blast Shot",
            "TwisterSlash",
            "Beat Dance",
            "Cursed Dance",
            "Flame"
        ]

        if self.random.random() > 0.5:
            techs.append("Explosion")
        else:
            techs.append("Fire-Juggler")

        return techs

    @staticmethod
    def zilla_techs() -> List[str]:
        return [
            "Head Butt",
            "Knocking-Up",
            "Tail Lashes",
            "Sneeze",
            "Body Press",
            "Wave Riding",
            "Earthquake",
            "Bubbles",
            "Charge",
            "Zilla Rush",
            "Roll Assault",
            "Tidal Wave",
        ]

    @staticmethod
    def zuum_techs() -> List[str]:
        return [
            "MillionClaws",
            "Bite",
            "Bite-Throw",
            "Claw Combo",
            "MillionBites",
            "Tail Lash",
            "Tail Lashes",
            "Dust Cloud",
            "Hypnotism",
            "Tail Combo",
            "Jumping Claw",
            "Diving Claw",
            "Aerial Claw",
            "Fire Ball",
            "Fire Breath",
            "Jumping Fire",
            "Charge",
            "Fire Charge",
            "Roll Assault",
            "Five Balls",
            "Fire Bomb",
            "Burning Roll",
        ]


class MonsterRancher2DXUnlockedMainBreeds(OptionSet):
    """
    Indicates which unlockable main breeds can be rolled for objectives in Monster Rancher 2 DX
    """
    valid_keys = {
        "Baku",
        "Bajarl",
        "Beaclon",
        "Centaur",
        "Dragon",
        "Ducken",
        "Durahan",
        "Gali",
        "Ghost",
        "Golem",
        "Henger",
        "Jill",
        "Joker",
        "Metalner",
        "Mew",
        "Mock",
        "Niton",
        "Phoenix",
        "Undine",
        "Worm",
        "Wracky",
        "Zilla",
    }

    default = sorted(valid_keys)


class MonsterRancher2DXUnlockedSubBreeds(OptionSet):
    """
    Indicates which unlockable sub breeds can be rolled for objectives in Monster Rancher 2 DX
    """
    valid_keys = {
        "White Mocchi",
        "White Suezo",
        "Bighand",
        "Kamui",
        "Crescent",
        "Sniper",
        "Sand Golem",
        "Burning Wall",
        "King Ape",
        "Wild Saurian",
        "Mad Clay",
        "Zilla King",
        "Silver Face",
        "Bloody Eye",
        "Blue Phoenix",
        "Punisher",
        "Magma Heart",
    }

    default = sorted(valid_keys)
