from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class CytusIIArchipelagoOptions:
    cytus_ii_dlc_owned: CytusIIDLCOwned
    cytus_ii_difficulties: CytusIIDifficulties


class CytusIIGame(Game):
    name = "Cytus II"
    platform = KeymastersKeepGamePlatforms.AND

    platforms_other = [
        KeymastersKeepGamePlatforms.IOS,
    ]

    is_adult_only_or_unrated = False

    options_cls = CytusIIArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play the Special Difficulty of the song (if applicable)",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete SONG on DIFFICULTY difficulty",
                data={
                    "SONG": (self.songs, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Full Combo SONG on DIFFICULTY difficulty",
                data={
                    "SONG": (self.songs, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Million Master SONG on Easy difficulty",
                data={
                    "SONG": (self.songs, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @property
    def dlc_owned(self) -> List[str]:
        return sorted(self.archipelago_options.cytus_ii_dlc_owned.value)

    @property
    def has_dlc_capso(self) -> bool:
        return "CAPSO!" in self.dlc_owned

    @property
    def has_dlc_marvelous_mix_9(self) -> bool:
        return "Marvelous Mix vol.9" in self.dlc_owned

    @property
    def has_dlc_chunithm(self) -> bool:
        return "CHUNITHM" in self.dlc_owned

    @property
    def has_dlc_marvelous_mix_10(self) -> bool:
        return "Marvelous Mix vol.10" in self.dlc_owned

    @property
    def has_dlc_marvelous_mix_11(self) -> bool:
        return "Marvelous Mix vol.11" in self.dlc_owned

    @property
    def has_dlc_deemo_2_pt_1(self) -> bool:
        return "DEEMO II pt.1" in self.dlc_owned

    @property
    def has_dlc_deemo_2_pt_2(self) -> bool:
        return "DEEMO II pt.2" in self.dlc_owned

    @property
    def has_dlc_marvelous_mix_12(self) -> bool:
        return "Marvelous Mix vol.12" in self.dlc_owned

    @property
    def has_dlc_rayark_12th_collection(self) -> bool:
        return "Rayark 12th Collection" in self.dlc_owned

    @property
    def has_dlc_b_b_k_k_b_k_k_2023_remake_selection(self) -> bool:
        return "B.B.K.K.B.K.K. 2023 Remake Selection" in self.dlc_owned

    @property
    def has_dlc_rhythm_games_party_2024(self) -> bool:
        return "Rhythm Games Party 2024" in self.dlc_owned

    @property
    def has_dlc_ravon(self) -> bool:
        return "RAVON" in self.dlc_owned

    @property
    def has_dlc_paradigm_reboot_pt_1(self) -> bool:
        return "Paradigm: Reboot pt.1" in self.dlc_owned

    @property
    def has_dlc_paradigm_reboot_pt_2(self) -> bool:
        return "Paradigm: Reboot pt.2" in self.dlc_owned

    @property
    def has_dlc_neko(self) -> bool:
        return "Neko" in self.dlc_owned

    @property
    def has_dlc_neko_ii(self) -> bool:
        return "NEKO_II" in self.dlc_owned

    @property
    def has_dlc_tairitsu(self) -> bool:
        return "Tairitsu" in self.dlc_owned

    @property
    def has_dlc_amiya(self) -> bool:
        return "Amiya" in self.dlc_owned

    @property
    def has_dlc_kaf(self) -> bool:
        return "Kaf" in self.dlc_owned

    @property
    def has_dlc_alice(self) -> bool:
        return "Alice" in self.dlc_owned

    @property
    def has_dlc_hans(self) -> bool:
        return "Hans" in self.dlc_owned

    @property
    def has_dlc_kitzuna_ai(self) -> bool:
        return "Kitzuna AI" in self.dlc_owned

    @property
    def has_dlc_miku(self) -> bool:
        return "Miku" in self.dlc_owned

    @property
    def has_dlc_ilka(self) -> bool:
        return "Ilka" in self.dlc_owned

    @property
    def has_dlc_xenon(self) -> bool:
        return "Xenon" in self.dlc_owned

    @property
    def has_dlc_conne_r(self) -> bool:
        return "ConneR" in self.dlc_owned

    @property
    def has_dlc_cherry(self) -> bool:
        return "Cherry" in self.dlc_owned

    @property
    def has_dlc_joe(self) -> bool:
        return "JOE" in self.dlc_owned

    @property
    def has_dlc_sagar(self) -> bool:
        return "Sagar" in self.dlc_owned

    @property
    def has_dlc_rin(self) -> bool:
        return "Rin" in self.dlc_owned

    @property
    def has_dlc_aroma(self) -> bool:
        return "Aroma" in self.dlc_owned

    @property
    def has_dlc_nora(self) -> bool:
        return "Nora" in self.dlc_owned

    @property
    def has_dlc_miku_extend_2025(self) -> bool:
        return "Miku Extend 2025" in self.dlc_owned

    @property
    def has_dlc_game_disc_vol_1(self) -> bool:
        return "Game Disc vol.1" in self.dlc_owned

    @property
    def has_dlc_memory_unit_a1(self) -> bool:
        return "Memory Unit [A1]" in self.dlc_owned

    @property
    def has_dlc_game_disc_vol_2(self) -> bool:
        return "Game Disc vol.2" in self.dlc_owned

    @property
    def has_dlc_memory_unit_a2(self) -> bool:
        return "Memory Unit [A2]" in self.dlc_owned

    @property
    def has_dlc_marvelous_mix_vol_6(self) -> bool:
        return "Marvelous Mix vol.6" in self.dlc_owned

    @property
    def has_dlc_marvelous_mix_vol_1(self) -> bool:
        return "Marvelous Mix vol.1" in self.dlc_owned

    @property
    def has_dlc_marvelous_mix_vol_2(self) -> bool:
        return "Marvelous Mix vol.2" in self.dlc_owned

    @property
    def has_dlc_marvelous_mix_vol_3(self) -> bool:
        return "Marvelous Mix vol.3" in self.dlc_owned

    @property
    def has_dlc_battle_chaos_2019(self) -> bool:
        return "Battle CHAOS 2019" in self.dlc_owned

    @property
    def has_dlc_marvelous_mix_vol_4(self) -> bool:
        return "Marvelous Mix vol.4" in self.dlc_owned

    @property
    def has_dlc_emotion_samples_01(self) -> bool:
        return "Emotion Samples 01" in self.dlc_owned

    @property
    def has_dlc_emotion_samples_02(self) -> bool:
        return "Emotion Samples 02" in self.dlc_owned

    @property
    def has_dlc_featured_article_vol_1(self) -> bool:
        return "Featured Article Vol.1" in self.dlc_owned

    @property
    def has_dlc_emotion_samples_03(self) -> bool:
        return "Emotion Samples 03" in self.dlc_owned

    @property
    def has_dlc_marvelous_mix_vol_5(self) -> bool:
        return "Marvelous Mix vol.5" in self.dlc_owned

    @property
    def has_dlc_djmax_vol_1(self) -> bool:
        return "DJMAX vol.1" in self.dlc_owned

    @property
    def has_dlc_djmax_vol_2(self) -> bool:
        return "DJMAX vol.2" in self.dlc_owned

    @property
    def has_dlc_muse_dash_vol_1(self) -> bool:
        return "Muse Dash vol.1" in self.dlc_owned

    @property
    def has_dlc_muse_dash_vol_2(self) -> bool:
        return "Muse Dash vol.2" in self.dlc_owned

    @property
    def has_dlc_marvelous_mix_vol_7(self) -> bool:
        return "Marvelous Mix vol.7" in self.dlc_owned

    @property
    def has_dlc_punk_ep_01(self) -> bool:
        return "PuNK EP 01" in self.dlc_owned

    @property
    def has_dlc_maimai_dx_plus(self) -> bool:
        return "maimai DX+" in self.dlc_owned

    @property
    def has_dlc_initial_g_1st_stage(self) -> bool:
        return "Initial G 1st Stage" in self.dlc_owned

    @property
    def has_dlc_initial_g_2nd_stage(self) -> bool:
        return "Initial G 2nd Stage" in self.dlc_owned

    @property
    def has_dlc_marvelous_mix_vol_8(self) -> bool:
        return "Marvelous Mix vol.8" in self.dlc_owned

    def difficulties(self) -> List[str]:
        return sorted(self.archipelago_options.cytus_ii_difficulties.value)

    @functools.cached_property
    def songs_base(self) -> List[str]:
        return [
            "[Vanessa] Ra",
            "[Vanessa] Incyde",
            "[Vanessa] Risoluto",
            "[Vanessa] Installation",
            "[Vanessa] XYZ",
            "[Vanessa] The End Years",
            "[Vanessa] Installation",
            "[Vanessa] Rosa Rubus",
            "[Vanessa] II-V",
            "[Vanessa] The Whole Rest",
            "[Vanessa] Anchor",
            "[Vanessa] Risoluto",
            "[Vanessa] Ⅱ́̕",
            "[Vanessa] CHAOS //System Offline//",
            "[Vanessa] V. //System Offline//",
            "[Vanessa] THE BEGINNING",
            "[Vanessa] Chaos and Abyss -3rd Movement-",
            "[Vanessa] Duality",
            "[Vanessa] Blessing Reunion",
            "[Vanessa] 3:00 a.m.",
            "[Vanessa] syūten",
            "[Paff] Baptism of Fire (CliqTrack remix)",
            "[Paff] Blossoms for Life",
            "[Paff] Body Talk",
            "[Paff] Bullet Waiting for Me (James Landino remix)",
            "[Paff] Fight Another Day (Andy Tunstall remix)",
            "[Paff] Fireflies (Funk Fiction remix)",
            "[Paff] Gravity",
            "[Paff] Green Hope",
            "[Paff] illMenate",
            "[Paff] KANATA",
            "[Paff] Lilac for Anabel",
            "[Paff] Mirror (ft. tiki)",
            "[Paff] More Than Diamond",
            "[Paff] New World",
            "[Paff] Re:Boost",
            "[Paff] Recall",
            "[Paff] Save me Now",
            "[Paff] SECRET;WEAPON",
            "[Paff] Sleeping Beast",
            "[Paff] Streetlights (ft. CassieGemini)",
            "[Paff] Survive",
            "[Paff] Under the same sky",
            "[Paff] Who Am I?",
            "[Paff] Winter Games",
            "[NEKO#ΦωΦ] Afterlife",
            "[NEKO#ΦωΦ] Alterna Pt.1 -Cosmogony-",
            "[NEKO#ΦωΦ] Better than your error system",
            "[NEKO#ΦωΦ] Blow my mind",
            "[NEKO#ΦωΦ] Brain Power",
            "[NEKO#ΦωΦ] Chrome VOX",
            "[NEKO#ΦωΦ] CODE NAME: GAMMA",
            "[NEKO#ΦωΦ] Dropping Lightspeed",
            "[NEKO#ΦωΦ] extinguisher",
            "[NEKO#ΦωΦ] For You the Bellz Toll",
            "[NEKO#ΦωΦ] Happiness Breeze",
            "[NEKO#ΦωΦ] Hard Landing",
            "[NEKO#ΦωΦ] Keep it up",
            "[NEKO#ΦωΦ] One Way Love",
            "[NEKO#ΦωΦ] Rei",
            "[NEKO#ΦωΦ] Resurrection",
            "[NEKO#ΦωΦ] The Spark",
            "[NEKO#ΦωΦ] Zealous Hearts (Rayark Edit)",
            "[NEKO#ΦωΦ] 気楽なCloudy",
            "[NEKO#ΦωΦ] 響け！",
            "[ROBO_Head] Urgency",
            "[ROBO_Head] Contact",
            "[ROBO_Head] Devillic Sphere",
            "[ROBO_Head] Dasein",
            "[ROBO_Head] Make Me Burn",
            "[ROBO_Head] Nocturnal Type",
            "[ROBO_Head] Subconscious Mind",
            "[ROBO_Head] Dead Point",
            "[ROBO_Head] Midnight",
            "[ROBO_Head] EMber",
            "[ROBO_Head] CHAOS",
            "[ROBO_Head] Grimoire of Crimson",
            "[ROBO_Head] Celestial Sounds (KIVΛ Remix)",
            "[ROBO_Head] Pure Powerstomper",
            "[ROBO_Head] Claim the Game",
            "[ROBO_Head] Luolimasi",
            "[ROBO_Head] Restriction",
            "[ROBO_Head] Deadly Slot Game",
            "[Ivy] Dystopia",
            "[Ivy] Heroic Age",
            "[Ivy] UTOPIA",
            "[Ivy] Area184",
            "[Ivy] Halloween Party",
            "[Ivy] Secret Garden",
            "[Ivy] paradigm-paragramme-program",
            "[Ivy] conflict",
            "[Ivy] D R G",
            "[Ivy] Biotonic",
            "[Ivy] Sovereign",
            "[Ivy] Summer Zephyr",
            "[Ivy] V.",
            "[Ivy] Pressure",
            "[Ivy] 99 Glooms",
            "[Ivy] Lunar Mare",
            "[Ivy] AssaultMare",
            "[Ivy] BloodyMare",
            "[Ivy] Purge",
            "[Ivy] Tokiwatari",
            "[Ivy] Alexandrite",
            "[Ivy] Sentimental Journey",
            "[Ivy] Reset",
            "[Crystal PuNK] Chandelier XIII",
            "[Crystal PuNK] Collide",
            "[Crystal PuNK] Dark Madness",
            "[Crystal PuNK] Deep Dive",
            "[Crystal PuNK] Effervesce",
            "[Crystal PuNK] 眷戀",
            "[Crystal PuNK] Prema Flowers",
            "[Crystal PuNK] Still (Piano Version)",
            "[Crystal PuNK] Sunshine Duration",
            "[Crystal PuNK] The Cross (feat. Silvia Su)",
            "[Crystal PuNK] βinαrΨ",
            "[Bo Bo] バステット (Cytus II Edit)",
            "[Bo Bo] tRinity saga",
            "[Bo Bo] New Quest",
            "[Bo Bo] Tomb Robber",
            "[Bo Bo] King of Desert",
            "[Bo Bo] Vox Enchanted",
            "[Bo Bo] TSUBAKI",
            "[Bo Bo] Heliopolis Project",
            "[Bo Bo] Firstborns",
            "[Bo Bo] The breath of the soul",
            "[Bo Bo] IBUKI",
            "[Bo Bo] NORDLYS",
            "[Bo Bo] Snow Blossom",
            "[Bo Bo] Quinsialyn",
            "[Bo Bo] 黎明-REIMEI-",
            "[Bo Bo] Äventyr",
            "[Graff.J] Drop",
            "[Graff.J (Deemo II)] Dandelion Girls, Dandelion Boys",
            "[Graff.J (Deemo II)] Kokoro Odoro",
            "[Graff.J (Deemo II)] Forest of Clock",
            "[Graff.J (Deemo II)] Echo over you...",
            "[Graff.J] Game on Together!",
            "[Graff.J (Alice Fiction)] 非・現実逃避",
            "[Graff.J (Alice Fiction)] 非・現実逃避 Rabpit Remix",
            "[Graff.J (Muse Dash)] Stargazer",
            "[Graff.J (Muse Dash)] Lights of Muse",
            "[Graff.J (Deemo)] Red Storm Sentiment",
            "[Graff.J (Deemo)] Kaguya",
            "[Graff.J (Groove Coaster)] FUJIN Rumble",
            "[Graff.J (Sdorica)] Stewrica -Cross-",
            "[Graff.J (Sdorica)] Pounding Destination",
            "[Graff.J (Sdorica)] Hesitant Blade",
            "[Graff.J (Sdorica)] Sdorica The Story Unfolds",
            "[Graff.J] Conundrum",
            "[Graff.J (Voez)] Nyx -Fatal arousal of Madness-",
            "[Graff.J (Voez)] Flash Gun",
            "[Graff.J (Voez)] Time Traveller",
            "[Graff.J (Voez)] 双龍飛閃-Dual Dragoon-",
            "[Graff.J (Voez)] Like Asian Spirit",
            "[Graff.J (Voez)] Tsukiyura",
            "[Graff.J (Voez)] Until the Blue Moon Rises",
            "[Graff.J (Voez)] Magical Toy Box",
            "[Graff.J (Voez)] Fading Star",
            "[Graff.J (Voez)] そんなに私を期待させないで",
            "[Graff.J (Voez)] Hop Step Adventure☆",
            "[Graff.J (Voez)] Silent Voice",
            "[Graff.J (Voez)] Spring",
            "[Graff.J (Voez)] Interstellar Experience",
            "[Graff.J (Voez)] dynamo",
            "[Graff.J (Voez)] Hello Days",
            "[Graff.J (Voez)] Gigantic Saga",
            "[Graff.J (Voez)] FUSE",
            "[Graff.J (Voez)] popotnik ~The Traveller of Ljubljana",
            "[Graff.J (Voez)] Ascension to Heaven",
            "[Graff.J (Voez)] Lifill",
            "[Vanessa] Cocytus",
            "[Vanessa] Used to be",
            "[Graff.J] Go Adventure!",
        ]

    @functools.cached_property
    def songs_amiya(self) -> List[str]:
        return [
            "[Amiya] Operation Pyrite",
            "[Amiya] Operation Blade",
            "[Amiya] Evolutionary Mechanization",
            "[Amiya] Keep the torch",
            "[Amiya] ManiFesto",
            "[Amiya] Renegade",
            "[Amiya] Speed of Light",
            "[Amiya] ALIVE",
            "[Amiya] Boiling Blood",
            "[Amiya] El Brillo Solitario",
        ]

    @functools.cached_property
    def songs_alice(self) -> List[str]:
        return [
            "[Alice] Legacy",
            "[Alice] The Beautiful Moonlight",
            "[Alice] To next page",
            "[Alice] Friction",
            "[Alice] I hate to tell you",
            "[Alice] Marigold",
            "[Alice] Living In The One",
            "[Alice] ANiMA",
        ]

    @functools.cached_property
    def songs_aroma(self) -> List[str]:
        return [
            "[Aroma] 漂流",
            "[Aroma] Beautiful Lie",
            "[Aroma] Anzen Na Kusuri",
            "[Aroma] Make Y Mine",
            "[Aroma] Spotlight On",
            "[Aroma] No One Can't Stop Me",
            "[Aroma] 風の声",
            "[Aroma] Neon Escape",
            "[Aroma] Bring the Light",
            "[Aroma] Perspectives",
            "[Aroma] change",
        ]

    @functools.cached_property
    def songs_nora(self) -> List[str]:
        return [
            "[Nora] Starlight (KIVΛ Remix)",
            "[Nora] Bastard of Hardcore",
            "[Nora] Accelerator",
            "[Nora] Grand Emotion",
            "[Nora] Phagy Mutation",
            "[Nora] Jakarta PROGRESSION",
            "[Nora] Dance till Dawn",
            "[Nora] Uranus",
            "[Nora] Drop The World",
            "[Nora] ATONEMENT",
            "[Nora] Eternity",
        ]

    @functools.cached_property
    def songs_xenon(self) -> List[str]:
        return [
            "[Xenon] Black Hole",
            "[Xenon] Whispers in my Head",
            "[Xenon] Fighting",
            "[Xenon] Phantom Razor",
            "[Xenon] To the Light",
            "[Xenon] IOLITE-SUNSTONE",
            "[Xenon] INSPION",
            "[Xenon] Samurai",
            "[Xenon] Return",
            "[Xenon] Karma",
            "[Xenon] Sairai",
            "[Xenon] concentric circles",
            "[Xenon] Violet",
            "[Xenon] Asylum",
            "[Xenon] Ultimate feat. 放課後のあいつ",
            "[Xenon] Chosen",
        ]

    @functools.cached_property
    def songs_neko(self) -> List[str]:
        return [
            "[Neko] Chocolate Missile",
            "[Neko] Pink Graduation",
            "[Neko] Mammal",
            "[Neko] Blah!!",
            "[Neko] リラ",
            "[Neko] Log In",
            "[Neko] DJ Mashiro is dead or alive",
            "[Neko] R.I.P.",
            "[Neko] I can avoid it.#φωφ",
            "[Neko] 一啖兩啖",
            "[Neko] Re:incRnaTiØN ～夕焼ケ世界ノ決別ヲ～",
        ]

    @functools.cached_property
    def songs_tairitsu(self) -> List[str]:
        return [
            "[Tairitsu] Grievous Lady",
            "[Tairitsu] Malicious Mischance",
            "[Tairitsu] Axium Crisis",
            "[Tairitsu] Lucid Traveler",
            "[Tairitsu] Auxesia",
            "[Tairitsu] init()",
            "[Tairitsu] Fracture Ray",
            "[Tairitsu] GLORY:ROAD",
            "[Tairitsu] 九番目の迷路",
            "[Tairitsu] 彩る夏の恋花火",
        ]

    @functools.cached_property
    def songs_kaf(self) -> List[str]:
        return [
            "[Kaf] 糸",
            "[Kaf] 帰り路",
            "[Kaf] 過去を喰らう",
            "[Kaf] 未確認少女進行形",
            "[Kaf] 心臓と絡繰",
            "[Kaf] そして花になる",
            "[Kaf] 不可解 (Cytus II Edit.)",
            "[Kaf] 雛鳥",
            "[Kaf] 夜行バスにて",
            "[Kaf] メルの黄昏",
        ]

    @functools.cached_property
    def songs_hans(self) -> List[str]:
        return [
            "[Hans] Aragami",
            "[Hans] Dream",
            "[Hans] Ephemeral",
            "[Hans] Leviathan",
            "[Hans] Lost in the Nowhere",
            "[Hans] Path and Period",
            "[Hans] Platinum",
            "[Hans] Rhuzerv",
            "[Hans] Ruins in the Mirage",
            "[Hans] Run Go Run",
            "[Hans] Sunset",
        ]

    @functools.cached_property
    def songs_kitzuna_ai(self) -> List[str]:
        return [
            "[Kizuna AI] AIAIAI (feat. 中田ヤスタカ)",
            "[Kizuna AI] Hello, Morning (Prod. Nor)",
            "[Kizuna AI] future base (Prod. Yunomi)",
            "[Kizuna AI] mirai (Prod. ☆Taku Takahashi)",
            "[Kizuna AI] over the reality (Prod. Avec Avec)",
            "[Kizuna AI] melty world (Prod. TeddyLoid)",
            "[Kizuna AI] meet you (Prod. DÉ DÉ MOUSE)",
            "[Kizuna AI] hello, alone (Prod. MATZ)",
        ]

    @functools.cached_property
    def songs_miku(self) -> List[str]:
        return [
            "[Miku] Blue Star",
            "[Miku] BREAK IT",
            "[Miku] Sharing The World",
            "[Miku] 月西江",
            "[Miku] Ten Thousand Stars",
            "[Miku] Glass Wall",
            "[Miku] Cybernetic",
            "[Miku] ラッキー☆オーブ(3R2 Remix)",
            "[Miku] Decade",
            "[Miku] Can't Make a Song!!",
            "[Miku] Miku",
            "[Miku] 魔法みたいなミュージック！",
            "[Miku] ラッキー☆オーブ",
            "[Miku] Venus di Ujung Jari",
            "[Miku] Highlight",
            "[Miku] Plaything",
        ]

    @functools.cached_property
    def songs_rin(self) -> List[str]:
        return [
            "[Rin] The Siege",
            "[Rin] The Grand Debate",
            "[Rin] 「妖怪録、我し来にけり。」",
            "[Rin] Starry Summoner",
            "[Rin] Mari-Temari",
            "[Rin] Inari",
            "[Rin] 三灯火",
            "[Rin] 彩",
            "[Rin] 決戦",
            "[Rin] すゝめ☆クノイチの巻",
        ]

    @functools.cached_property
    def songs_sagar(self) -> List[str]:
        return [
            "[Sagar] Amenemhat",
            "[Sagar] Elysium",
            "[Sagar] Immram Brain",
            "[Sagar] Space Brain",
            "[Sagar] Doldrums",
            "[Sagar] Return of the Lamp",
            "[Sagar] Nídhögg",
            "[Sagar] Sacrifice",
            "[Sagar] A Portent of the Silver Wheel",
            "[Sagar] Legacy",

        ]

    @functools.cached_property
    def songs_cherry(self) -> List[str]:
        return [
            "[Cherry] SYSTEMFEIT",
            "[Cherry] Stop at nothing (Andy Tunstall remix)",
            "[Cherry] Still",
            "[Cherry] Scenery in your eyes",
            "[Cherry] RETRIEVE",
            "[Cherry] Realize",
            "[Cherry] Capture me",
            "[Cherry] CREDENCE",
            "[Cherry] hunted",
            "[Cherry] I'M NOT",
            "[Cherry] LEVEL4",
            "[Cherry] Living for you (Andy Tunstall remix)",
        ]

    @functools.cached_property
    def songs_ilka(self) -> List[str]:
        return [
            "[Ilka] CODE:RED",
            "[Ilka] Rebellion Trigger",
            "[Ilka] Elysian Volitation",
            "[Ilka] Victims of Will",
            "[Ilka] Silver Lotus",
            "[Ilka] Levolution",
            "[Ilka] Re:The END - 再 -",
            "[Ilka] History Dstr∅yeR",
            "[Ilka] IɅVɅVI",
            "[Ilka] Lamentation",
            "[Ilka] Samuel's Farewell",
            "[Ilka] Noir",
            "[Ilka] Oneiroi",
            "[Ilka] 3GO",
        ]

    @functools.cached_property
    def songs_conne_r(self) -> List[str]:
        return [
            "[ConneR] Xiorc",
            "[ConneR] REBELLIUM",
            "[ConneR] Imprinting",
            "[ConneR] Gekkouka",
            "[ConneR] Light of Buenos Aires",
            "[ConneR] Abduction",
            "[ConneR] Nostalgia Sonatina",
            "[ConneR] I Luv U",
            "[ConneR] Instinct",
            "[ConneR] Aphasia",
            "[ConneR] Olympia",
            "[ConneR] Demetrius",
            "[ConneR] Deus Ex Machina",
            "[ConneR] Fur War, Pur War",
            "[ConneR] L'Ultima Cena",
            "[ConneR] tondari-hanetari",
            "[ConneR] Re:boot",
            "[ConneR] Last Landing",
            "[ConneR] Floor of Lava",
        ]

    @functools.cached_property
    def songs_joe(self) -> List[str]:
        return [
            "[JOE] Absolutely",
            "[JOE] Bass Music",
            "[JOE] Childish",
            "[JOE] Higher and Higher",
            "[JOE] Hydrangea",
            "[JOE] Juicy Gossip",
            "[JOE] Nautilus",
            "[JOE] Open the Game",
            "[JOE] Standby for Action",
            "[JOE] Take me to the Future",
            "[JOE] Turnstile Jumper",
        ]

    @functools.cached_property
    def songs_neko_ii(self) -> List[str]:
        return [
            "[NEKO_II] Heart Factorisation",
            "[NEKO_II] Is This Real Life?",
            "[NEKO_II] COLORFUL☆SPRINKLES",
            "[NEKO_II] Starchaser",
            "[NEKO_II] CYBERCAT",
            "[NEKO_II] ALL OK!!",
            "[NEKO_II] blueade",
            "[NEKO_II] Whatever You Wish",
            "[NEKO_II] Candy Cat",
            "[NEKO_II] LIT",
        ]

    @functools.cached_property
    def songs_paradigm_reboot_pt_2(self) -> List[str]:
        return [
            "[Graff.J (Paradigm: Reboot)] Artificial Existence",
            "[Graff.J (Paradigm: Reboot)] Awaken in Ruins",
            "[Graff.J (Paradigm: Reboot)] Final Farewell",
            "[Graff.J (Paradigm: Reboot)] Cybernetic Vampire",
            "[Graff.J (Paradigm: Reboot)] Prayers for the Colourless",
        ]

    @functools.cached_property
    def songs_paradigm_reboot_pt_1(self) -> List[str]:
        return [
            "[Graff.J (Paradigm: Reboot)] WORLDCALL",
            "[Graff.J (Paradigm: Reboot)] Chase",
            "[Graff.J (Paradigm: Reboot)] Restricted Access",
            "[Graff.J (Paradigm: Reboot)] Rebooted Mind",
            "[Graff.J (Paradigm: Reboot)] Forgotten Asteroid",
        ]

    @functools.cached_property
    def songs_ravon(self) -> List[str]:
        return [
            "[Graff.J (RAVON)] CYBER DIVER",
            "[Graff.J (RAVON)] Euouae",
            "[Graff.J (RAVON)] LAST Re;SØRT",
            "[Graff.J (RAVON)] Nebula Traveller",
            "[Graff.J (RAVON)] RE:dshift",
        ]

    @functools.cached_property
    def songs_rhythm_games_party_2024(self) -> List[str]:
        return [
            "[Graff.J (Rizline)] Pastel Lines",
            "[Graff.J (Rizline)] LINK x LIN♯S",
            "[Graff.J (Rizline)] BRAVE:ROAD",
            "[Graff.J (Muse Dash)] Dance Dance 晚安舞会",
            "[Graff.J (Muse Dash)] DOMINATOR",
        ]

    @functools.cached_property
    def songs_b_b_k_k_b_k_k_2023_remake_selection(self) -> List[str]:
        return [
            "[Graff.J (B.B.K.K.B.K.K.)] B.B.K.K.B.K.K. (2023 Remake)",
            "[Graff.J (B.B.K.K.B.K.K.)] B.B.K.K.B.K.K. (Nizikawa Remix)",
            "[Graff.J (B.B.K.K.B.K.K.)] B.B.K.K.B.K.K. (USAO Remix)",
            "[Graff.J (B.B.K.K.B.K.K.)] B.B.K.K.B.K.K. (立秋ちょこ Remix)",
            "[Graff.J (B.B.K.K.B.K.K.)] B.B.K.K.B.K.K. (影虎。& siqlo PsyReMix)",
        ]

    @functools.cached_property
    def songs_rayark_12th_collection(self) -> List[str]:
        return [
            "[Graff.J] 白の影、蒼の影。 ft. Kanae Asaba",
            "[Graff.J] Xing-Lai Heaven",
            "[Graff.J] Noël",
            "[Graff.J] CHAOS MAGNVM",
            "[Graff.J] But I Know",
        ]

    @functools.cached_property
    def songs_marvelous_mix_12(self) -> List[str]:
        return [
            "[Paff] favorite color ft. マナ",
            "[NEKO#ΦωΦ] MAYAKASHI Merry-go-round",
            "[NEKO#ΦωΦ] Bone Born Bomb",
            "[ROBO_Head] Acquire",
            "[Graff.J] CTRL",
        ]

    @functools.cached_property
    def songs_deemo_2_pt_2(self) -> List[str]:
        return [
            "[Graff.J (DEEMO II)] Tenkiame",
            "[Graff.J (DEEMO II)] BUBBLE TEA",
            "[Graff.J (DEEMO II)] Ao",
            "[Graff.J (DEEMO II)] Gemini about the Darkness",
            "[Graff.J (DEEMO II)] Stand Steel",
        ]

    @functools.cached_property
    def songs_deemo_2_pt_1(self) -> List[str]:
        return [
            "[Graff.J (DEEMO II)] AMEMOYOU",
            "[Graff.J (DEEMO II)] Fairy's Crown",
            "[Graff.J (DEEMO II)] INNOCENCE",
            "[Graff.J (DEEMO II)] felzione",
            "[Graff.J (DEEMO II)] Reverie",
        ]

    @functools.cached_property
    def songs_marvelous_mix_11(self) -> List[str]:
        return [
            "[NEKO#ΦωΦ] Human Extinction",
            "[NEKO#ΦωΦ] UNIVERSAL RENDA AWESOME",
            "[ROBO_Head] [SILENT[[・-・]]MOMENT]",
            "[ROBO_Head] SATELLITE",
            "[Ivy] 地下の雑踏",
        ]

    @functools.cached_property
    def songs_marvelous_mix_10(self) -> List[str]:
        return [
            "[Paff] Fly With Love",
            "[Paff] 变身 (Feat. Dirty Androids)",
            "[NEKO#ΦωΦ] ゴーストアウト",
            "[ROBO_Head] Destructed Empire",
            "[Graff.J] Accelerate",
        ]

    @functools.cached_property
    def songs_chunithm(self) -> List[str]:
        return [
            "[Graff.J (CHUNITHM)] Climax",
            "[Graff.J (CHUNITHM)] SNIPE WHOLE",
            "[Graff.J (CHUNITHM)] Trrricksters!!",
            "[Graff.J (CHUNITHM)] 光線チューニング",
            "[Graff.J (CHUNITHM)] 最愛テトラグラマトン",
        ]

    @functools.cached_property
    def songs_marvelous_mix_9(self) -> List[str]:
        return [
            "[Paff] So...",
            "[Paff] Eutopia",
            "[ROBO_Head] LIFE is GAME",
            "[Graff.J] ACID BASILISK",
            "[Graff.J] TIGER LILY",
        ]

    @functools.cached_property
    def songs_capso(self) -> List[str]:
        return [
            "[Ivy] Bloody Purity",
            "[Ivy] To Further Dream",
            "[Ivy] Qualia",
            "[Ivy] Halcyon",
            "[Ivy] Masquerade",
            "[Ivy] Saika",
            "[Ivy] Libera Me",
            "[Ivy] FREEDOM DiVE",
            "[Ivy] First Gate",
            "[Ivy] Oriens",
            "[Ivy] AXION",
            "[Ivy] Quantum Labyrinth",
            "[Ivy] Visions",
            "[Ivy] The Last Illusion",
        ]

    @functools.cached_property
    def songs_miku_extend_2025(self) -> List[str]:
        return [
            "[Miku] imaginary love story",
            "[Miku] Intergalactic Bound",
            "[Miku] M@GICAL☆CURE! LOVE♥SHOT!",
            "[Miku] Miku Fiesta",
            "[Miku] Thousand Little Voices",
        ]

    @functools.cached_property
    def songs_game_disc_vol_1(self) -> List[str]:
        return [
            "[NEKO#ΦωΦ] PrayStation (HiTECH NINJA Remix)",
            "[NEKO#ΦωΦ] 100sec Cat Dreams",
            "[NEKO#ΦωΦ] REmorse",
            "[NEKO#ΦωΦ] Stranger",
            "[NEKO#ΦωΦ] 小悪魔×3の大脫走！？",
        ]

    @functools.cached_property
    def songs_memory_unit_a1(self) -> List[str]:
        return [
            "[ROBO_Head] Sickest City",
            "[ROBO_Head] Jazzy Glitch Machine",
            "[ROBO_Head] dimensionalize nervous breakdown (rev.flat)",
            "[ROBO_Head] cold",
            "[ROBO_Head] NRG_Tech",
        ]

    @functools.cached_property
    def songs_game_disc_vol_2(self) -> List[str]:
        return [
            "[NEKO#ΦωΦ] Blow My Mind (tpz Overheat Remix)",
            "[NEKO#ΦωΦ] Maboroshi",
            "[NEKO#ΦωΦ] TOKONOMA Spacewalk",
            "[NEKO#ΦωΦ] UnNOT!CED",
            "[NEKO#ΦωΦ] 下水鳴動して鼠一匹",
        ]

    @functools.cached_property
    def songs_memory_unit_a2(self) -> List[str]:
        return [
            "[ROBO_Head] Accelerator",
            "[ROBO_Head] Armaros",
            "[ROBO_Head] Break the Core",
            "[ROBO_Head] Milky Way Galaxy (SIHanatsuka Remix)",
            "[ROBO_Head] ViRUS",
        ]

    @functools.cached_property
    def songs_marvelous_mix_vol_6(self) -> List[str]:
        return [
            "[Crystal PuNK] Imprint",
            "[ROBO_Head] Symbol (PTB10 Remix)",
            "[ROBO_Head] Breaching BIOS",
            "[Graff.J] Curiosity killed the cat",
            "[Graff.J] REBELLIA",
        ]

    @functools.cached_property
    def songs_marvelous_mix_vol_1(self) -> List[str]:
        return [
            "[Paff] So In Love",
            "[NEKO#ΦωΦ] Online",
            "[NEKO#ΦωΦ] Sunday Night Blues",
            "[ROBO_Head] Break Through The Barrier",
            "[ROBO_Head] Dead Master",
        ]

    @functools.cached_property
    def songs_marvelous_mix_vol_2(self) -> List[str]:
        return [
            "[Paff] I Wish You Were Mine",
            "[Paff] PIXIE DUST",
            "[NEKO#ΦωΦ] Capybara Kids' Paradise",
            "[ROBO_Head] Awakening",
            "[ROBO_Head] Hagiasmos",
        ]

    @functools.cached_property
    def songs_marvelous_mix_vol_3(self) -> List[str]:
        return [
            "[NEKO#ΦωΦ] Walnuts Walkers",
            "[ROBO_Head] Fade Into Darkness",
            "[ROBO_Head] SHIRO",
            "[ROBO_Head] Tunnef's Nightmare",
            "[Crystal PuNK] Darling Staring...",
        ]

    @functools.cached_property
    def songs_battle_chaos_2019(self) -> List[str]:
        return [
            "[NEKO#ΦωΦ] Hydra",
            "[NEKO#ΦωΦ] Liberation",
            "[NEKO#ΦωΦ] Ramen is God",
            "[NEKO#ΦωΦ] Re:VeLΔTiØN ～光道ト破壊ノ双白翼～",
            "[NEKO#ΦωΦ] Rebirth",
        ]

    @functools.cached_property
    def songs_marvelous_mix_vol_4(self) -> List[str]:
        return [
            "[Bo Bo] End of fireworks",
            "[Bo Bo] 神様と羊飼い",
            "[Paff] Inspiration",
            "[Paff] No-Effected World",
            "[NEKO#ΦωΦ] LOUDER MACHINE",
        ]

    @functools.cached_property
    def songs_emotion_samples_01(self) -> List[str]:
        return [
            "[Ivy] Cristalisia",
            "[Ivy] Occidens",
            "[Ivy] Red Five",
            "[Ivy] Homebound Train & Moving Thoughts",
            "[Ivy] iL",
        ]

    @functools.cached_property
    def songs_emotion_samples_02(self) -> List[str]:
        return [
            "[Ivy] CODE NAME:SIGMA",
            "[Ivy] New Challenger Approaching",
            "[Ivy] What's Your PR.Ice?",
            "[Ivy] VIS::CRACKED",
            "[Ivy] Wicked Ceremony",
        ]

    @functools.cached_property
    def songs_featured_article_vol_1(self) -> List[str]:
        return [
            "[Paff] Cityscape",
            "[Paff] Favorites",
            "[Paff] Make Me Alive",
            "[Paff] Light up my love!!",
            "[Paff] Super attractor",
        ]

    @functools.cached_property
    def songs_emotion_samples_03(self) -> List[str]:
        return [
            "[Ivy] DigiGroove",
            "[Ivy] Heat Ring",
            "[Ivy] Leaving All Behind",
            "[Ivy] Symmetry",
            "[Ivy] Time to Fight",
        ]

    @functools.cached_property
    def songs_marvelous_mix_vol_5(self) -> List[str]:
        return [
            "[Paff] Orison",
            "[NEKO#ΦωΦ] Headrush",
            "[ROBO_Head] tundra",
            "[ROBO_Head] Zeus",
            "[Ivy] Drifted Fragments",
        ]

    @functools.cached_property
    def songs_djmax_vol_1(self) -> List[str]:
        return [
            "[Graff.J (DJMAX)] BlythE",
            "[Graff.J (DJMAX)] glory day",
            "[Graff.J (DJMAX)] OBLIVION",
            "[Graff.J (DJMAX)] Play The Future",
            "[Graff.J (DJMAX)] We're All Gonna Die",
        ]

    @functools.cached_property
    def songs_djmax_vol_2(self) -> List[str]:
        return [
            "[Graff.J (DJMAX)] Ask to Wind Live Mix",
            "[Graff.J (DJMAX)] End of the Moonlight",
            "[Graff.J (DJMAX)] Hello Pinky",
            "[Graff.J (DJMAX)] Nightmare",
            "[Graff.J (DJMAX)] U.A.D",
        ]

    @functools.cached_property
    def songs_muse_dash_vol_1(self) -> List[str]:
        return [
            "[Graff.J (Muse Dash)] Blackest Luxury Car",
            "[Graff.J (Muse Dash)] 粉骨砕身カジノゥ",
            "[Graff.J (Muse Dash)] 時計の部屋と精神世界",
            "[Graff.J (Muse Dash)] XING",
            "[Graff.J (Muse Dash)] Brave My Heart",
        ]

    @functools.cached_property
    def songs_muse_dash_vol_2(self) -> List[str]:
        return [
            "[Graff.J (Muse Dash)] Final Step!",
            "[Graff.J (Muse Dash)] Medusa",
            "[Graff.J (Muse Dash)] XODUS",
            "[Graff.J (Muse Dash)] The 89's Momentum",
            "[Graff.J (Muse Dash)] The 90's Decision",
        ]

    @functools.cached_property
    def songs_marvelous_mix_vol_7(self) -> List[str]:
        return [
            "[NEKO#ΦωΦ] Ready to Take the Next Step",
            "[ROBO_Head] The Devil Will Pray",
            "[ROBO_Head] ArkLight",
            "[Graff.J] Code Interceptor",
            "[Graff.J] La Prière",
        ]

    @functools.cached_property
    def songs_punk_ep_01(self) -> List[str]:
        return [
            "[Crystal PuNK] Crimson Fate",
            "[Crystal PuNK] Familiar Craze",
            "[Crystal PuNK] Malstream",
            "[Crystal PuNK] V.R.W (feat. shully)",
            "[Crystal PuNK] velkinta feat. Cikado & A-Tse",
        ]

    @functools.cached_property
    def songs_maimai_dx_plus(self) -> List[str]:
        return [
            "[Graff.J (maimai DX+)] Caliburne ~Story of the Legendary sword~",
            "[Graff.J (maimai DX+)] DON'T STOP ROCKIN'",
            "[Graff.J (maimai DX+)] Glorious Crown",
            "[Graff.J (maimai DX+)] Oshama Scramble!",
            "[Graff.J (maimai DX+)] 超常マイマイン",
        ]

    @functools.cached_property
    def songs_initial_g_1st_stage(self) -> List[str]:
        return [
            "[Graff.J] Circus Time",
            "[Graff.J] Dead V-Code (Special Edit)",
            "[Graff.J] sweet conflict",
            "[Graff.J] Centimeter Johnny",
            "[Graff.J] Obey",
        ]

    @functools.cached_property
    def songs_initial_g_2nd_stage(self) -> List[str]:
        return [
            "[Graff.J] BREAK FREE",
            "[Graff.J] DON'T LISTEN TO THIS WHILE DRIVING",
            "[Graff.J] RESET MAN",
            "[Graff.J] PERSONA",
            "[Graff.J] OUT OF THE MATRIX",
        ]

    @functools.cached_property
    def songs_marvelous_mix_vol_8(self) -> List[str]:
        return [
            "[ROBO_Head] honeykill",
            "[ROBO_Head] Exoseven",
            "[Graff.J] Phantom",
            "[Graff.J] Whirlwind",
            "[Graff.J] 東京Funk",
        ]

    def songs(self) -> List[str]:
        songs: List[str] = self.songs_base[:]

        if self.has_dlc_amiya:
            songs.extend(self.songs_amiya)
        if self.has_dlc_alice:
            songs.extend(self.songs_alice)
        if self.has_dlc_aroma:
            songs.extend(self.songs_aroma)
        if self.has_dlc_nora:
            songs.extend(self.songs_nora)
        if self.has_dlc_xenon:
            songs.extend(self.songs_xenon)
        if self.has_dlc_neko:
            songs.extend(self.songs_neko)
        if self.has_dlc_tairitsu:
            songs.extend(self.songs_tairitsu)
        if self.has_dlc_kaf:
            songs.extend(self.songs_kaf)
        if self.has_dlc_hans:
            songs.extend(self.songs_hans)
        if self.has_dlc_kitzuna_ai:
            songs.extend(self.songs_kitzuna_ai)
        if self.has_dlc_miku:
            songs.extend(self.songs_miku)
        if self.has_dlc_rin:
            songs.extend(self.songs_rin)
        if self.has_dlc_sagar:
            songs.extend(self.songs_sagar)
        if self.has_dlc_cherry:
            songs.extend(self.songs_cherry)
        if self.has_dlc_ilka:
            songs.extend(self.songs_ilka)
        if self.has_dlc_conne_r:
            songs.extend(self.songs_conne_r)
        if self.has_dlc_joe:
            songs.extend(self.songs_joe)
        if self.has_dlc_neko_ii:
            songs.extend(self.songs_neko_ii)
        if self.has_dlc_paradigm_reboot_pt_2:
            songs.extend(self.songs_paradigm_reboot_pt_2)
        if self.has_dlc_paradigm_reboot_pt_1:
            songs.extend(self.songs_paradigm_reboot_pt_1)
        if self.has_dlc_ravon:
            songs.extend(self.songs_ravon)
        if self.has_dlc_rhythm_games_party_2024:
            songs.extend(self.songs_rhythm_games_party_2024)
        if self.has_dlc_b_b_k_k_b_k_k_2023_remake_selection:
            songs.extend(self.songs_b_b_k_k_b_k_k_2023_remake_selection)
        if self.has_dlc_rayark_12th_collection:
            songs.extend(self.songs_rayark_12th_collection)
        if self.has_dlc_marvelous_mix_12:
            songs.extend(self.songs_marvelous_mix_12)
        if self.has_dlc_deemo_2_pt_2:
            songs.extend(self.songs_deemo_2_pt_2)
        if self.has_dlc_deemo_2_pt_1:
            songs.extend(self.songs_deemo_2_pt_1)
        if self.has_dlc_marvelous_mix_11:
            songs.extend(self.songs_marvelous_mix_11)
        if self.has_dlc_marvelous_mix_10:
            songs.extend(self.songs_marvelous_mix_10)
        if self.has_dlc_chunithm:
            songs.extend(self.songs_chunithm)
        if self.has_dlc_marvelous_mix_9:
            songs.extend(self.songs_marvelous_mix_9)
        if self.has_dlc_capso:
            songs.extend(self.songs_capso)
        if self.has_dlc_miku_extend_2025:
            songs.extend(self.songs_miku_extend_2025)
        if self.has_dlc_game_disc_vol_1:
            songs.extend(self.songs_game_disc_vol_1)
        if self.has_dlc_memory_unit_a1:
            songs.extend(self.songs_memory_unit_a1)
        if self.has_dlc_game_disc_vol_2:
            songs.extend(self.songs_game_disc_vol_2)
        if self.has_dlc_memory_unit_a2:
            songs.extend(self.songs_memory_unit_a2)
        if self.has_dlc_marvelous_mix_vol_6:
            songs.extend(self.songs_marvelous_mix_vol_6)
        if self.has_dlc_marvelous_mix_vol_1:
            songs.extend(self.songs_marvelous_mix_vol_1)
        if self.has_dlc_marvelous_mix_vol_2:
            songs.extend(self.songs_marvelous_mix_vol_2)
        if self.has_dlc_marvelous_mix_vol_3:
            songs.extend(self.songs_marvelous_mix_vol_3)
        if self.has_dlc_battle_chaos_2019:
            songs.extend(self.songs_battle_chaos_2019)
        if self.has_dlc_marvelous_mix_vol_4:
            songs.extend(self.songs_marvelous_mix_vol_4)
        if self.has_dlc_emotion_samples_01:
            songs.extend(self.songs_emotion_samples_01)
        if self.has_dlc_emotion_samples_02:
            songs.extend(self.songs_emotion_samples_02)
        if self.has_dlc_featured_article_vol_1:
            songs.extend(self.songs_featured_article_vol_1)
        if self.has_dlc_emotion_samples_03:
            songs.extend(self.songs_emotion_samples_03)
        if self.has_dlc_marvelous_mix_vol_5:
            songs.extend(self.songs_marvelous_mix_vol_5)
        if self.has_dlc_djmax_vol_1:
            songs.extend(self.songs_djmax_vol_1)
        if self.has_dlc_djmax_vol_2:
            songs.extend(self.songs_djmax_vol_2)
        if self.has_dlc_muse_dash_vol_1:
            songs.extend(self.songs_muse_dash_vol_1)
        if self.has_dlc_muse_dash_vol_2:
            songs.extend(self.songs_muse_dash_vol_2)
        if self.has_dlc_marvelous_mix_vol_7:
            songs.extend(self.songs_marvelous_mix_vol_7)
        if self.has_dlc_punk_ep_01:
            songs.extend(self.songs_punk_ep_01)
        if self.has_dlc_maimai_dx_plus:
            songs.extend(self.songs_maimai_dx_plus)
        if self.has_dlc_initial_g_1st_stage:
            songs.extend(self.songs_initial_g_1st_stage)
        if self.has_dlc_initial_g_2nd_stage:
            songs.extend(self.songs_initial_g_2nd_stage)
        if self.has_dlc_marvelous_mix_vol_8:
            songs.extend(self.songs_marvelous_mix_vol_8)

        return sorted(songs)


# Archipelago Options
class CytusIIDLCOwned(OptionSet):
    """
    Indicates which Cytus II DLC the player owns, if any.
    """

    display_name = "Cytus II DLC Owned"
    valid_keys = [
        "Alice",
        "Amiya",
        "Aroma",
        "B.B.K.K.B.K.K. 2023 Remake Selection",
        "Battle CHAOS 2019",
        "CAPSO!",
        "CHUNITHM",
        "Cherry",
        "ConneR",
        "DEEMO II pt.1",
        "DEEMO II pt.2",
        "DJMAX vol.1",
        "DJMAX vol.2",
        "Emotion Samples 01",
        "Emotion Samples 02",
        "Emotion Samples 03",
        "Featured Article Vol.1",
        "Game Disc vol.1",
        "Game Disc vol.2",
        "Hans",
        "Ilka",
        "Initial G 1st Stage",
        "Initial G 2nd Stage",
        "JOE",
        "Kaf",
        "Kitzuna AI",
        "maimai DX+",
        "Marvelous Mix vol.1",
        "Marvelous Mix vol.2",
        "Marvelous Mix vol.3",
        "Marvelous Mix vol.4",
        "Marvelous Mix vol.5",
        "Marvelous Mix vol.6",
        "Marvelous Mix vol.7",
        "Marvelous Mix vol.8",
        "Marvelous Mix vol.9",
        "Marvelous Mix vol.10",
        "Marvelous Mix vol.11",
        "Marvelous Mix vol.12",
        "Memory Unit [A1]",
        "Memory Unit [A2]",
        "Miku Extend 2025",
        "Miku",
        "Muse Dash vol.1",
        "Muse Dash vol.2",
        "NEKO_II",
        "Neko",
        "Nora",
        "Paradigm: Reboot pt.1",
        "Paradigm: Reboot pt.2",
        "PuNK EP 01",
        "RAVON",
        "Rayark 12th Collection",
        "Rhythm Games Party 2024",
        "Rin",
        "Sagar",
        "Tairitsu",
        "Xenon",
    ]

    default = valid_keys


class CytusIIDifficulties(OptionSet):
    """
    Indicates which Cytus II difficulties the player wants to play.
    """

    display_name = "Cytus II Difficulties"
    valid_keys = [
        "Easy",
        "Hard",
        "Chaos",
    ]

    default = valid_keys
