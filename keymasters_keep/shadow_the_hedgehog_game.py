from __future__ import annotations

import functools
from typing import Dict, List

from dataclasses import dataclass

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class ShadowTheHedgehogArchipelagoOptions:
    shadow_the_hedgehog_include_expert_mode: ShadowTheHedgehogIncludeExpertMode


class ShadowTheHedgehogGame(Game):
    name = "Shadow The Hedgehog"
    platform = KeymastersKeepGamePlatforms.GC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS2,
        KeymastersKeepGamePlatforms.XBOX,
    ]

    is_adult_only_or_unrated = False

    options_cls = ShadowTheHedgehogArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Don't use Select Mode",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Don't use Special Weapon Containers",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="A-rank every level",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Play Story Mode Path: PATH",
                data={
                    "PATH": (self.paths, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Complete STAGE's Hero Mission",
                data={
                    "STAGE": (self.stages_hero, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete STAGE's Neutral Mission",
                data={
                    "STAGE": (self.stages_neutral, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete STAGE's Dark Mission",
                data={
                    "STAGE": (self.stages_dark, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS",
                data={
                    "BOSS": (self.bosses, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Play Last Story and defeat Devil Doom",
                data=dict(),
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

        if self.include_expert_mode:
            templates.append(
                GameObjectiveTemplate(
                    label="Clear Expert Mode",
                    data=dict(),
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            )

        return templates

    @property
    def include_expert_mode(self) -> bool:
        return bool(self.archipelago_options.shadow_the_hedgehog_include_expert_mode.value)

    @functools.cached_property
    def stage_graph(self) -> Dict[str, Dict[str, str]]:
        return {
            "Westopolis": {
                "D": "Digital Circuit",
                "N": "Glyphic Canyon",
                "H": "Lethal Highway",
            },
            "Digital Circuit": {
                "D": "Cryptic Castle",
                "H": "Prison Island",
            },
            "Glyphic Canyon": {
                "D": "Cryptic Castle",
                "N": "Prison Island",
                "H": "Circus Park",
            },
            "Lethal Highway": {
                "D": "Prison Island",
                "H": "Circus Park",
            },
            "Cryptic Castle": {
                "D": "Central City",
                "N": "The Doom",
                "H": "Sky Troops",
            },
            "Prison Island": {
                "D": "The Doom",
                "N": "Sky Troops",
                "H": "Mad Matrix",
            },
            "Circus Park": {
                "D": "Sky Troops",
                "N": "Mad Matrix",
                "H": "Death Ruins",
            },
            "Central City": {
                "D": "The ARK",
                "H": "Air Fleet",
            },
            "The Doom": {
                "D": "The ARK",
                "N": "Air Fleet",
                "H": "Iron Jungle",
            },
            "Sky Troops": {
                "D": "Air Fleet",
                "N": "Iron Jungle",
                "H": "Space Gadget",
            },
            "Mad Matrix": {
                "D": "Iron Jungle",
                "N": "Space Gadget",
                "H": "Lost Impact",
            },
            "Death Ruins": {
                "D": "Space Gadget",
                "H": "Lost Impact",
            },
            "The ARK": {
                "D": "GUN Fortress",
                "N": "Black Comet",
            },
            "Air Fleet": {
                "D": "GUN Fortress",
                "N": "Black Comet",
                "H": "Lava Shelter",
            },
            "Iron Jungle": {
                "D": "Black Comet",
                "N": "Lava Shelter",
                "H": "Cosmic Fall",
            },
            "Space Gadget": {
                "D": "Lava Shelter",
                "N": "Cosmic Fall",
                "H": "Final Haunt",
            },
            "Lost Impact": {
                "N": "Cosmic Fall",
                "H": "Final Haunt",
            },
            "GUN Fortress": {
                "D": "Sonic & Diablon",
                "H": "Black Doom",
            },
            "Black Comet": {
                "D": "Sonic & Diablon",
                "H": "Egg Dealer",
            },
            "Lava Shelter": {
                "D": "Egg Dealer",
                "H": "Egg Dealer",
            },
            "Cosmic Fall": {
                "D": "Egg Dealer",
                "H": "Black Doom",
            },
            "Final Haunt": {
                "D": "Sonic & Diablon",
                "H": "Black Doom",
            },
        }

    @staticmethod
    def paths_base() -> List[str]:
        return [
            "1: Punishment, Thy Name is Ruin  DDDDDD",
            "2: Prologue to World Conquest  DDDDDH",
            "3: The March to a Darker World  DDDDND",
            "4: The Ultimate Ego  DDDDNH",
            "5: Purification via Ruination  DDDHDD",
            "6: Apogee of Darkness  DDDHDH",
            "7: True Soldier of Destruction  DDDHND",
            "8: Believe in Yourself  DDDHNH",
            "9: An Android’s Determination  DDDHHD",
            "10: For Machine, By Machine...  DDDHHH",
            "11: Revenge at Last  DDNDDD",
            "12: Ego’s Awakening  DDNDDH",
            "13: Destruction and Scorn  DDNDND",
            "14: The Last Remaining Purpose  DDNDNH",
            "15: The Nightmare’s Insulation  DDNNDD",
            "16: The Nightmare’s Sublimation  DDNNDH",
            "17: The Loner’s Choice  DDNNND",
            "18: Subjugation in Black  DDNNNH",
            "19: Replica’s Depression  DDNNHD",
            "20: Machine, Machine  DDNNHH",
            "21: Disciple from the Darkness  DDNHDD",
            "22: Beloved Clone  DDNHDH",
            "23: Revenge Upon the Doctor  DDNHND",
            "24: The Ultimate Replica  DDNHNH",
            "25: Sanction’s Demise  DDNHHD",
            "26: Along With My Home  DDNHHH",
            "27: The Cleansing of Darkness  DDHDDD",
            "28: Birth of a God  DDHDDH",
            "29: The Last Soldier’s Grim Fate  DDHDND",
            "30: Isolation and Solitude  DDHDNH",
            "31: Archimedes and the Tortoise  DDHDHD",
            "32: Where Is My Happiness?  DDHDHH",
            "33: Seduced By Taste of Blood  DDHNDD",
            "34: A Machine Made for War  DDHNDH",
            "35: Original Definition  DDHNND",
            "36: Machine Paradise  DDHNNH",
            "37: Last Will and Testament  DDHNHD",
            "38: Enveloped in Solitude  DDHNHH",
            "39: Parricidal Savior  DDHHDD",
            "40: Copy of a Savior  DDHHDH",
            "41: Excess of Intellect  DDHHND",
            "42: Crystallization of Intellect  DDHHNH",
            "43: The Ultimate Confrontation  DDHHHD",
            "44: Miracle of Love  DDHHHH",
            "45: The World’s Demise  DHDDDD",
            "46: The Ultimate Power  DHDDDH",
            "47: Dyed in Lovely Darkness...  DHDDND",
            "48: Vainglory or Abandonment?  DHDDNH",
            "49: Messenger of Ruination  DHDNDD",
            "50: Standing at the Summit  DHDNDH",
            "51: Controller from the Capsule  DHDNND",
            "52: Beyond One’s Own Power...  DHDNNH",
            "53: A Clone’s Determination  DHDNHD",
            "54: Machine Utopia  DHDNHH",
            "55: A Toast to the Ruler  DHDHDD",
            "56: Answer from the Black Comet  DHDHDH",
            "57: Transcendentalism  DHDHND",
            "58: Imperialism  DHDHNH",
            "59: The Weight of One’s Crimes  DHDHHD",
            "60: Imprisoned by the Past...  DHDHHH",
            "61: The Ultimate World Conquest  DHNDDD",
            "62: Black Angel  DHNDDH",
            "63: Under Darkness’ Control  DHNDND",
            "64: To Love Oneself  DHNDNH",
            "65: Revenge and Determination  DHNDHD",
            "66: Birth of the Robot Emperor  DHNDHH",
            "67: Shadow, the Black Android  DHNNDD",
            "68: A Solitary Android  DHNNDH",
            "69: Over the Original  DHNNND",
            "70: Machine Sunshine  DHNNNH",
            "71: Life is Guilty  DHNNHD",
            "72: Fallen Angel of Despair  DHNNHH",
            "73: An Eternal Rival...  DHNHDD",
            "74: This is Just the Beginning  DHNHDH",
            "75: Crystal of Tragic Knowledge  DHNHND",
            "76: Shadow’s Second Death...?  DHNHNH",
            "77: The Legend of Shadow  DHNHHD",
            "78: Power of Love  DHNHHH",
            "79: Deep Black  DHHDDD",
            "80: Walk My Way  DHHDDH",
            "81: This is Shadow’s Way of Life  DHHDND",
            "82: A Monarch’s Style  DHHDNH",
            "83: In the Gap of Sadness  DHHDHD",
            "84: To Be Ignorant of the Past  DHHDHH",
            "85: At Vengeance’s End  DHHNDD",
            "86: Machine Boys  DHHNDH",
            "87: Reborn Along with Sorrow  DHHNND",
            "88: With a Fate of Self-Denial  DHHNNH",
            "89: I Am Shadow  DHHNHD",
            "90: Shining Within Memory...  DHHNHH",
            "91: The Rise and Fall of the ARK  DHHHND",
            "92: Requiem for a Fallen Angel  DHHHNH",
            "93: Ultimate Shadow  DHHHHD",
            "94: For Love’s Sake  DHHHHH",
            "95: A Heart Awoken from Darkness  NDDDDD",
            "96: Destruction From Perfection  NDDDDH",
            "97: Darkness’ Strongest Soldier  NDDDND",
            "98: Severed Chains  NDDDNH",
            "99: Retribution Against Humanity  NDDHDD",
            "100: To Be Known as ‘Ultimate’  NDDHDH",
            "101: Dark Warrior’s Advent  NDDHND",
            "102: Arriving at the Ego  NDDHNH",
            "103: Determination of a Fake  NDDHHD",
            "104: Path to the Machine Empire  NDDHHH",
            "105: Demise Wrought by Tragedy  NDNDDD",
            "106: Turning Sorrow Into Strength  NDNDDH",
            "107: The Liberated Soldier  NDNDND",
            "108: Stupefaction’s End  NDNDNH",
            "109: Humanity’s Folly  NDNNDD",
            "110: Surpassing All Else  NDNNDH",
            "111: Soldier of Grief  NDNNND",
            "112: Reclaimed Heart  NDNNNH",
            "113: Fighting Spirit of Steel  NDNNHD",
            "114: Machine Soldier Uprising  NDNNHH",
            "115: The Devil Born From Betrayal  NDNHDD",
            "116: Beyond the Truth of Impact  NDNHDH",
            "117: The Immortal Android  NDNHND",
            "118: The New, Coldhearted Empire  NDNHNH",
            "119: A Singular Atonement  NDNHHD",
            "120: Spawn of the Devil  NDNHHH",
            "121: Black Doom’s Scheme  NDHDDD",
            "122: Subjugating Heaven and Earth  NDHDDH",
            "123: Road of the Dark Soldier  NDHDND",
            "124: Dark Finale  NDHDNH",
            "125: Realization While On Board  NDHDHD",
            "126: Birth of a Champion  NDHDHH",
            "127: With the Black Arms  NDHNDD",
            "128: The Road to Self-Assurance  NDHNDH",
            "129: The Pursuit of Dr. Eggman  NDHNND",
            "130: Surpassing His Creator  NDHNNH",
            "131: ARK, Colony of Pathos  NDHNHD",
            "132: Perfection Lost to Darkness  NDHNHH",
            "133: A New Challenge  NDHHDD",
            "134: The Machines’ Coup d’Etat  NDHHDH",
            "135: A Vow for the Victims  NDHHND",
            "136: The Truth of Sadness  NDHHNH",
            "137: The Destined Sonic Showdown  NDHHHD",
            "138: The Black Hero’s Rebirth  NDHHHH",
            "139: Truth, Thy Name is Vengeance  NNDDDD",
            "140: Searching for ‘Ultimate’  NNDDDH",
            "141: Reborn Hatred for Humanity  NNDDND",
            "142: A Future Taken from the Past  NNDDNH",
            "143: The Devils’ Victory Song  NNDNDD",
            "144: One to Succeed a God  NNDNDH",
            "145: Disappointed in Humanity  NNDNND",
            "146: Faith Taken from Solitude  NNDNNH",
            "147: Planted Memories  NNDNHD",
            "148: To Unite Humanity  NNDNHH",
            "149: Isolated Soldier Shadow  NNDHDD",
            "150: Answer Derived from Truth  NNDHDH",
            "151: A Fake’s Disposition  NNDHND",
            "152: A New World Without Betrayal  NNDHNH",
            "153: Together With Maria...  NNDHHD",
            "154: The Tragedy’s Conclusion  NNDHHH",
            "155: The Day That Hope Died  NNNDDD",
            "156: Dark Destroyer  NNNDDH",
            "157: Diabolical Power  NNNDND",
            "158: For Freedom  NNNDNH",
            "159: At Least, Be Like Shadow...  NNNDHD",
            "160: Seeking a Silent Paradise  NNNDHH",
            "161: The Lion’s Awakening  NNNNDD",
            "162: Identity  NNNNDH",
            "163: An Android’s Rebellion  NNNNND",
            "164: A New Empire’s Beginning  NNNNNH",
            "165: Bullets from Tears  NNNNHD",
            "166: Journey to Nihility  NNNNHH",
            "167: Shadow Surpassing Shadow  NNNHDD",
            "168: Dr. Eggman’s Miscalculation  NNNHDH",
            "169: Along with the ARK  NNNHND",
            "170: Requiem for the Heavens  NNNHNH",
            "171: Sonic Dethroned!  NNNHHD",
            "172: Justice Reborn in Space  NNNHHH",
            "173: Steel Ruler  NNHDDD",
            "174: For the Sake of the Self  NNHDDH",
            "175: Farewell to the Past  NNHDND",
            "176: Steel Paradise  NNHDNH",
            "177: The Guardian With No Past  NNHDHD",
            "178: The Ultimate Atonement  NNHDHH",
            "179: A Fake’s Aspiration  NNHNDD",
            "180: Machine World  NNHNDH",
            "181: Twilight Ark  NNHNND",
            "182: Compensation for a Miracle  NNHNNH",
            "183: The Strongest Hedgehog  NNHNHD",
            "184: The Ultimate Punisher  NNHNHH",
            "185: Voyage of Reminiscence  NNHHND",
            "186: Wandering’s End  NNHHNH",
            "187: The Ultimate Proof  NNHHHD",
            "188: Punisher of Love  NNHHHH",
            "189: Messenger from the Darkness  NHDDDD",
            "190: The New Ruler  NHDDDH",
            "191: Dark Soldier  NHDDND",
            "192: The Road of Light  NHDDNH",
            "193: The Machine-Laden Kingdom  NHDDHD",
            "194: New Determination  NHDDHH",
            "195: Birth of the Dark Soldier  NHDNDD",
            "196: A New Journey  NHDNDH",
            "197: The Android’s Opposition  NHDNND",
            "198: Founding of the Robot Nation  NHDNNH",
            "199: The Eternal Protector  NHDNHD",
            "200: The Sinner’s Repose  NHDNHH",
            "201: A Hero’s Resolution  NHDHDD",
            "202: The Weapons’ Empire  NHDHDH",
            "203: Perpetual Voyage  NHDHND",
            "204: A Hero’s Atonement  NHDHNH",
            "205: Dark Hegemony  NHDHHD",
            "206: And the Dream Continues  NHDHHH",
            "207: Fighter for Darkness  NHNDDD",
            "208: The Path I Believed In  NHNDDH",
            "209: Determination’s Daybreak  NHNDND",
            "210: Machine Kingdom at Dawn  NHNDNH",
            "211: Sinful Protector  NHNDHD",
            "212: At the End of the Journey  NHNDHH",
            "213: Surmounting the Nightmare  NHNNDD",
            "214: Dawn of the Machines  NHNNDH",
            "215: Wandering for Eternity  NHNNND",
            "216: At Vagrancy’s End  NHNNNH",
            "217: The Summit of Power  NHNNHD",
            "218: Under the Name of Love  NHNNHH",
            "219: Eternally Drifting  NHNHND",
            "220: The Importance of Truth  NHNHNH",
            "221: The Beginning of Judgment  NHNHHD",
            "222: This World’s Guardian  NHNHHH",
            "223: Light Born from Darkness  NHHDDD",
            "224: The Order of Steel  NHHDDH",
            "225: Solitary Journey  NHHDND",
            "226: The Fall Home  NHHDNH",
            "227: Sovereign of All Creation  NHHDHD",
            "228: I Shall Be the One to Judge  NHHDHH",
            "229: Gone With the Darkness  NHHHND",
            "230: The Ultimate Choice  NHHHNH",
            "231: I Am the Strongest!  NHHHHD",
            "232: Justice’s Awakening  NHHHHH",
            "233: Prelude to Ruination  HDDDDD",
            "234: A World United by Darkness  HDDDDH",
            "235: The Pulse of Darkness  HDDDND",
            "236: To Just Be Myself  HDDDNH",
            "237: Punishment in Jet Black  HDDNDD",
            "238: The Ruler’s First Cry  HDDNDH",
            "239: Darkness’ Conspiracy  HDDNND",
            "240: The Faint Light of Tomorrow  HDDNNH",
            "241: Time of Departure  HDDNHD",
            "242: Rise of the Machine Kingdom  HDDNHH",
            "243: Despair’s Quickening  HDDHDD",
            "244: The Beginning  HDDHDH",
            "245: Setting Out in the Morning  HDDHND",
            "246: The Weapons’ Dawn  HDDHNH",
            "247: Pure Ark  HDDHHD",
            "248: Making Up For It in the End  HDDHHH",
            "249: The Coming of the Dark Time  HDNDDD",
            "250: The Throne of God  HDNDDH",
            "251: God of War  HDNDND",
            "252: Howl of Solitude  HDNDNH",
            "253: Proof of Existence  HDNDHD",
            "254: Ardent Vow  HDNDHH",
            "255: A Deal With the Devil  HDNNDD",
            "256: A Reason to Live  HDNNDH",
            "257: Induplicable Thoughts  HDNNND",
            "258: Steel Struck With Flame  HDNNNH",
            "259: A Heart Bound to the ARK  HDNNHD",
            "260: Tears Shed by the Stars  HDNNHH",
            "261: Imitation Complex  HDNHDD",
            "262: Steel Combat Boots  HDNHDH",
            "263: Protector of the Ashen Moon  HDNHND",
            "264: A Demon Drifting  HDNHNH",
            "265: The Ultimate Pride  HDNHHD",
            "266: I Know the Will of Heaven  HDNHHH",
            "267: Ego Dyed in Black  HDHDDD",
            "268: Isolation By Choice  HDHDDH",
            "269: Faith Without Falsehood  HDHDND",
            "270: Machine Empire  HDHDNH",
            "271: The Eternally-Closed Door  HDHDHD",
            "272: The Sealed-Away Ark of Sin  HDHDHH",
            "273: Silver Emergence  HDHNDD",
            "274: Pulsating Supercurrent  HDHNDH",
            "275: The Reason I Was Born  HDHNND",
            "276: The Dark Part of the Galaxy  HDHNNH",
            "277: The View From Atop the World  HDHNHD",
            "278: Maria’s Testament  HDHNHH",
            "279: A Genius Scientist’s Lineage  HDHHND",
            "280: Distorted Truth  HDHHNH",
            "281: A Counterfeit Existence  HDHHHD",
            "282: Beloved Memories  HDHHHH",
            "283: Birth of a Devil  HHDDDD",
            "284: A Dark Myth’s Beginnings  HHDDDH",
            "285: Black Thunder  HHDDND",
            "286: The Torn-Away Necklace  HHDDNH",
            "287: A Soul Sheltered by Iron  HHDDHD",
            "288: Steel Nation’s Decree  HHDDHH",
            "289: Coronation of Darkness  HHDNDD",
            "290: Opened Eyes  HHDNDH",
            "291: The Doctor’s Lie  HHDNND",
            "292: The Uninvited Successor  HHDNNH",
            "293: The Closed Pandora’s Box  HHDNHD",
            "294: A Heart Bound by Sin  HHDNHH",
            "295: Courage from Turning Gears  HHDHDD",
            "296: Fullmetal Prince  HHDHDH",
            "297: Time’s Watchman  HHDHND",
            "298: Galaxy’s Requiem  HHDHNH",
            "299: Charm of the Chaos Emeralds  HHDHHD",
            "300: Promise of a Far-Off Day  HHDHHH",
            "301: The Grim Reaper’s Horn  HHNDDD",
            "302: A Flame Extinguished by Fate  HHNDDH",
            "303: Shouting at the Morning Sun  HHNDND",
            "304: Iron Ambition  HHNDNH",
            "305: Sleeping on Hallowed Ground  HHNDHD",
            "306: Explanation of the Truth  HHNDHH",
            "307: An Android’s Dream  HHNNDD",
            "308: Metallic Quickening  HHNNDH",
            "309: Funeral Procession in Space  HHNNND",
            "310: Lost to the Universe’s Abyss  HHNNNH",
            "311: Destiny for Two  HHNNHD",
            "312: The Spun Threads of Fate  HHNNHH",
            "313: Ark of the Heavens  HHNHND",
            "314: Ghost of the ARK  HHNHNH",
            "315: A Pair of Shooting Stars  HHNHHD",
            "316: The One Who Maria Entrusted  HHNHHH",
            "317: A.I.’s Enlightenment  HHHDDD",
            "318: A Dying Empire’s Cry  HHHDDH",
            "319: Moon of Atonement  HHHDND",
            "320: Tear-Soaked Hometown  HHHDNH",
            "321: Sparks on the Horizon  HHHDHD",
            "322: A Use for a Saved Life  HHHDHH",
            "323: Coffin of Memories  HHHHND",
            "324: The Self-Imposed Seal  HHHHNH",
            "325: Pretense in the Mirror  HHHHHD",
            "326: A Missive from 50 Years Ago  HHHHHH",
        ]

    def paths(self) -> List[str]:
        base_paths: List[str] = self.paths_base()
        stage_graph: Dict[str, Dict[str, str]] = self.stage_graph

        paths: List[str] = list()

        path: str
        for path in base_paths:
            route: str = path[-6:]
            route_expanded: List[str] = list()

            current_stage: str = "Westopolis"

            for connection in route:
                current_stage = stage_graph[current_stage][connection]
                route_expanded.append(current_stage)

            paths.append(path.replace(route, f"({'->'.join(route_expanded)})"))

        return paths

    @staticmethod
    def stages_all_missions() -> List[str]:
        return [
            "Westopolis",
            "Glyphic Canyon",
            "Cryptic Castle",
            "Prison Island",
            "Circus Park",
            "The Doom",
            "Sky Troops",
            "Mad Matrix",
            "Air Fleet",
            "Iron Jungle",
            "Space Gadget",
        ]

    @staticmethod
    def stages_no_neutral_missions() -> List[str]:
        return [
            "Digital Circuit",
            "Lethal Highway",
            "Central City",
            "Death Ruins",
            "GUN Fortress",
            "Black Comet",
            "Lava Shelter",
            "Cosmic Fall",
            "Final Haunt",
        ]

    def stages_hero(self) -> List[str]:
        return sorted(
            self.stages_all_missions()
            + self.stages_no_neutral_missions()
            + ["Lost Impact"]
        )

    def stages_neutral(self) -> List[str]:
        return sorted(
            self.stages_all_missions()
            + ["The ARK", "Lost Impact"]
        )

    def stages_dark(self) -> List[str]:
        stages: List[str] = sorted(
            self.stages_all_missions()
            + self.stages_no_neutral_missions()
            + ["The ARK"]
        )

        if "Mad Matrix" in stages:
            stages.remove("Mad Matrix")
        if "The Doom" in stages:
            stages.remove("The Doom")

        return stages

    @staticmethod
    def bosses() -> List[str]:
        return [
            "Egg Breaker",
            "Blue Falcon",
            "Heavy Dog",
            "Black Bull",
            "Egg Dealer",
        ]


# Archipelago Options
class ShadowTheHedgehogIncludeExpertMode(Toggle):
    """
    Indicates whether to include expert mode when generating objectives.
    """

    display_name = "Shadow The Hedgehog Include Expert Mode"
