from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class MuseDashArchipelagoOptions:
    muse_dash_dlc_owned: MuseDashDLCOwned


class MuseDashGame(Game):
    name = "Muse Dash"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False

    options_cls = MuseDashArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Character: CHARACTER  Elfin: ELFIN  Minimum Grade: GRADE",
                data={
                    "CHARACTER": (self.characters, 1),
                    "ELFIN": (self.elfins, 1),
                    "GRADE": (self.grades, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete SONG",
                data={
                    "SONG": (self.songs, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Get a Full Combo on SONG",
                data={
                    "SONG": (self.songs, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Complete any Song with a Level of at least LEVEL",
                data={
                    "LEVEL": (self.level_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Get a Full Combo on any Song with a Level of at least LEVEL",
                data={
                    "LEVEL": (self.level_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete any Level LEVEL Song",
                data={
                    "LEVEL": (self.level_range_hard, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Get a Full Combo on any Level 10 Song",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Get an All Perfect on any Song",
                data=dict(),
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

    @property
    def dlc_owned(self) -> List[str]:
        return sorted(self.archipelago_options.muse_dash_dlc_owned.value)

    @property
    def has_dlc_muse_plus(self) -> bool:
        return "Muse Plus" in self.dlc_owned

    @property
    def has_dlc_msr_anthology_vol_1(self) -> bool:
        return "MSR Anthology Vol.01" in self.dlc_owned

    @property
    def has_dlc_maimai_dx_limited_time_suite(self) -> bool:
        return "maimai DX Limited-time Suite" in self.dlc_owned

    @property
    def has_dlc_neon_abyss(self) -> bool:
        return "Neon Abyss" in self.dlc_owned

    @property
    def has_dlc_miku_in_museland(self) -> bool:
        return "Miku in Museland" in self.dlc_owned

    @property
    def has_dlc_rin_lens_mirrorland(self) -> bool:
        return "Rin-Len's Mirrorland" in self.dlc_owned

    @property
    def has_dlc_chunithm_course_muse(self) -> bool:
        return "CHUNITHM COURSE MUSE" in self.dlc_owned

    @property
    def has_dlc_msr_anthology_vol_2(self) -> bool:
        return "MSR Anthology Vol.02" in self.dlc_owned

    @staticmethod
    def characters() -> List[str]:
        return [
            "Bassist Rin",
            "Bad Girl Rin",
            "Bunny Girl Rin",
            "Christmas Gift Rin",
            "Part-Time Warrior Rin",
            "Racer Rin",
            "Pilot Buro",
            "Idol Buro",
            "Zombie Girl Buro",
            "Joker Buro",
            "Sailor Suit Buro",
            "Exorcist Master Buro",
            "Boxer Ola",
            "Violinist Marija",
            "Maid Marija",
            "Magical Girl Marija",
            "Little Devil Marija",
            "The Girl in Black Marija",
            "Sister Marija",
            "Mechanical Ballerina Marija",
            "Navigator Yume",
            "Game Streamer NEKO",
            "Red-white Miko Reimu",
            "Rebirth Girl EL_Clear",
            "Black-white Magician Marisa",
            "Leader of Rhodes Island Amiya",
            "Virtual Singer Miku",
            "Virtual Singers Rin & Len",
        ]

    @staticmethod
    def elfins() -> List[str]:
        return [
            "Mio Sir",
            "Angela",
            "Thanatos",
            "Rabot-233",
            "Little Nurse",
            "Little Witch",
            "Dragon Girl",
            "Lilith",
            "Dr.Paige",
            "Silencer",
            "Neon Egg",
            "BetaGo",
        ]

    @functools.cached_property
    def songs_base(self) -> List[str]:
        return [
            "Magical Wonderland (More colorful mix)",
            "Iyaiya",
            "Wonderful Pain",
            "Breaking Dawn",
            "单向地铁 Feat.karin",
            "Echo over you...",
            "Yume Ou Mono Yo feat. Wotoha - Neko Hacker",
            "Frost Land",
            "Heart-Pounding Flight",
            "Pancake is Love",
            "时光涂鸦",
            "Evolution",
            "海豚与广播 feat.Uranyan",
            "Yuki no Shizuku Ame no Oto",
            "Best One feat.tooko",
            "糖果色恋爱学",
            "Night Wander (cnsouka Remix)",
            "Dohna Dohna no Uta",
            "Spring Carnival",
            "DISCO NIGHT",
            "Koi no Moonlight",
            "恋爱语音导航 feat.yousa",
            "Lights of Muse",
            "midstream jam",
            "Nihao",
            "Confession",
            "Galaxy Striker",
            "Departure Road",
            "Bass Telekinesis",
            "Cage of Almeria",
            "Ira",
            "Blackest Luxury Car",
            "Medicine of Sing",
            "irregulyze",
            "I don't care about Christmas though",
            "Imaginary World",
            "Dysthymia",
            "新世界より",
            "NISEGAO",
            "Say! Fanfare!",
            "Star Driver",
            "Formation",
            "Shinsou Masui",
            "Mezame Eurythmics",
            "Shenri Kuaira -repeat-",
            "Latitude",
            "Aqua Stars",
            "Funkotsu Saishin Casino",
            "Yume Ou Mono Yo feat. Wotoha - Neko Hacker",
            "Echo over you...",
            "Clock Room & Spiritual World",
            "INTERNET OVERDOSE（Aiobahn feat.KOTOKO）",
            "徒 花",
            "Mujinku-Vacuum Track#ADD8E6-",
            "MilK",
            "umpopoff",
            "Mopemope",
            "Out of Sense",
            "My Life Is For You",
            "Etude -Sunset-",
            "Goodbye Boss",
            "Stargazer",
            "Lys Tourbillon",
            "Glimmer feat.祈Inory",
            "EXIST feat.米雅",
            "Irreplaceable feat.夏铜子*",
        ]

    @functools.cached_property
    def songs_dlc_muse_plus(self) -> List[str]:
        return [
            "Sunshine and Rainbow after August Rain",
            "Magical Number",
            "Dreaming Girl",
            "Daruma-san Fell Over",
            "Different",
            "The Future of the Phantom",
            "Oriens",
            "PUPA",
            "Luna Express 2032",
            "Ukiyoe Yokochou",
            "Alice in Misanthrope",
            "GOODMEN",
            "Maharajah",
            "keep on running",
            "Käfig",
            "-+",
            "Tenri Kaku Jou",
            "Adjudicatorz-DanZai-",
            "MUSEDASH!!!!",
            "Imprinting",
            "Skyward",
            "La nuit de vif",
            "Bit-alize",
            "GOODTEK(Hyper Edit)",
            "Thirty Million Persona",
            "conflict",
            "Enka Dance Music",
            "XING",
            "Amakakeru Soukyuu no Serenade",
            "Gift box",
            "Brave My Soul",
            "Halcyon",
            "Crimson Nightingale",
            "Invader",
            "Lyrith",
            "GOODBOUNCE (Groove Edit)",
            "Altale",
            "Brain Power",
            "Berry Go!!",
            "Sweet* Witch* Girl*",
            "trippers feeling!",
            "Lilith ambivalence lovers",
            "Leave it Alone",
            "Tsubasa no Oreta Tenshitachi no Requiem",
            "Chronomia",
            "Dandelion's Daydream",
            "Lorikeet ~Flat design~",
            "GOODRAGE",
            "Destr0yer",
            "Noël",
            "Kyoukiranbu",
            "Two Phace",
            "Fly Again",
            "ouroVoros",
            "Brave My Heart",
            "Sakura Fubuki",
            "8bit Adventurer",
            "Suffering of screw",
            "tiny lady",
            "Power Attack",
            "Gaikan Chrysalis",
            "Sterelogue",
            "Cheshire's Dance",
            "Skrik",
            "Soda Pop Canva5!",
            "ЯUBY:LINTe",
            "速溶霓虹 feat.kumako",
            "星球上的追溯诗",
            "我要买买买",
            "约会宣言",
            "初雪",
            "心上华海",
            "Elysion's Old Mans",
            "AXION",
            "Amnesia",
            "Onsen Dai Sakusen",
            "Gleam stone",
            "GOODWORLD",
            "魔咒 feat.早木旋子",
            "斑斓星，彩绘，旅行诗",
            "Satell Knight",
            "Black River Feat.Mes",
            "生而为人，我很抱歉",
            "Ueta Tori Tachi",
            "Future Dive",
            "Re：End of a Dream",
            "Etude -Storm-",
            "Unlimited Katharsis",
            "Magic Knight Girl",
            "Eeliaas",
            "Cotton Candy Wonderland",
            "Punai Punai Taiso",
            "Fly↑High",
            "prejudice",
            "The 89's Momentum",
            "energy night(DASH mix)",
            "SWEETSWEETSWEET",
            "深蓝与夜的呼吸",
            "Joy Connection",
            "Self Willed Girl Ver.B",
            "就是不听话",
            "Holy Shit Grass Snake",
            "INFINITY",
            "Punai Punai Senso",
            "Maxi",
            "YInMn Blue",
            "Plumage",
            "Dr.Techro",
            "Moonlight Banquet",
            "Flashdance",
            "INFiNiTE ENERZY -Overdoze-",
            "One Way Street",
            "This Club is Not 4 U",
            "ULTRA MEGA HAPPY PARTY!!!",
            "The NightScape",
            "FREEDOM DiVE↓",
            "Φ",
            "Lueur de la nuit",
            "Creamy Sugary OVERDRIVE!!!",
            "Disorder (feat.YURI)",
            "雨后甜点",
            "告白应援方程式",
            "Omatsuri feat.兔子ST",
            "FUTUREPOP",
            "The Breeze",
            "I LOVE LETTUCE FRIED RICE!!",
            "The Last Page",
            "IKAROS",
            "Tsukuyomi",
            "Future Stream",
            "FULi AUTO SHOOTER",
            "GOODFORTUNE",
            "tape/stop/night",
            "Pixel Galaxy",
            "Notice",
            "sᴛʀᴀᴡʙᴇʀʀʏ ɢᴏᴅᴢɪʟʟᴀ",
            "OKIMOCHI EXPRESSION",
            "君とpool disco",
            "Legend of Eastern Rabbit -SKY DEFENDER-",
            "ENERGY SYNERGY MATRIX",
            "Punai Punai Genso ~Punai Punai in Wonderland~",
            "Better Graphic Animation",
            "Variant Cross",
            "Ultra Happy Miracle Bazoooooka!!",
            "Can I friend you on Bassbook? lol",
            "Gaming☆Everything",
            "Renji de haochi☆Denshi choriki shiyou chuka ryori 4000nen rekishi shunkan chori kanryo butouteki ryoricho☆",
            "You Make My Life 1UP",
            "Newbies take 3 years, geeks 8 years, and internets are forever",
            "Onegai!Kon kon Oinarisama",
            "Heisha Onsha",
            "Ginevra",
            "Paracelestia",
            "un secret",
            "Good Life",
            "ニニ-nini-",
            "Groove Prayer",
            "FUJIN Rumble",
            "Marry me, Nightmare",
            "HG魔改造ポリビニル少年",
            "聖者の息吹",
            "ouroboros -twin stroke of the end-",
            "Girly Cupid",
            "sheep in the light",
            "Breaker city",
            "heterodoxy",
            "Computer Music Girl",
            "焦点 feat.早木旋子",
            "The 90's Decision",
            "Medusa",
            "Final Step!",
            "MAGENTA POTION",
            "Cross†Ray (feat.月下Lia)",
            "Square Lake",
            "Preparara",
            "Whatcha;Whatcha Doin'",
            "Madara",
            "pICARESq",
            "Desastre",
            "Shoot for the Moon",
            "Fireflies (Funk Fiction remix)",
            "Light up my love!!",
            "Happiness Breeze",
            "Chrome VOX",
            "CHAOS",
            "Saika",
            "Standby for Action",
            "Hydrangea",
            "Amenemhat",
            "Santouka",
            "HEXENNACHTROCK-katashihaya-",
            "Blah!!",
            "CHAOS (Glitch)",
            "ALiVE",
            "BATTLE NO.1",
            "Cthugha",
            "TWINKLE★MAGIC",
            "Comet Coaster",
            "XODUS",
            "MuseDashを作っているPeroPeroGamesさんが倒産しちゃったよ～",
            "MARENOL",
            "僕の和风本当上手",
            "Rush B",
            "DataErr0r",
            "Burn",
            "NightTheater",
            "Cutter",
            "bamboo",
            "enchanted love",
            "c.s.q.n.",
            "Booouncing!!",
            "琉璃色前奏曲",
            "Neonlights",
            "Hope for the flowers",
            "Seaside Cycling on May 30",
            "SKY↑HIGH",
            "Mousou Chu!!",
            "NO ONE YES MAN",
            "雪降り、メリクリ （MD edit）",
            "Igallta",
            "去剪海的日子",
            "happy hour",
            "Seikimatsu no Natsu",
            "twinkle night",
            "ARUYA HARERUYA",
            "Blush (feat. MYLK)",
            "裸のSummer",
            "BLESS ME(Samplingsource)",
            "FM 17314 SUGAR RADIO",
            "Rush-More",
            "Kill My Fortune",
            "Yosari Tsukibotaru Suminoborite",
            "JUMP! HardCandy",
            "Hibari",
            "OCCHOCO-REST-LESS",
            "Super Battleworn Insomniac",
            "Bomb-Sniffing Pomeranian",
            "Rollerdisco Rumble",
            "ROSE GARDEN",
            "EMOMOMO",
            "Heracles",
            "Bad Apple!! feat. Nomico",
            "色は匂へど散りぬるを",
            "Cirno's Perfect Math Class",
            "緋色月下、狂咲ノ絶",
            "Flowery Moonlit Night",
            "Unconscious Requiem",
            "Party in the HOLLOWood feat. ななひら",
            "嘤嘤大作战",
            "Howlin' Pumpkin",
            "ONOMATO Pairing!!!",
            "with U",
            "Chariot",
            "GASHATT",
            "LIN NE KRO NE feat. lasah",
            "ANGEL HALO",
            "Bang!!",
            "Paradise Ⅱ",
            "Symbol",
            "Nekojarashi",
            "A Philosophical Wanderer",
            "Isouten",
            "Haze of Autumn",
            "GIMME DA BLOOD",
            "Libertas",
            "Cyaegha",
            "glory day",
            "Bright Dream",
            "Groovin Up",
            "I Want You",
            "OBLIVION",
            "Elastic STAR",
            "U.A.D",
            "Jealousy",
            "Memory of Beach",
            "Don't Die",
            "Y (CE Ver.)",
            "Fancy Night",
            "Can We Talk",
            "Give Me 5",
            "Nightmare",
            "Pray a LOVE",
            "恋愛回避依存症",
            "Daisuki Dayo feat.Wotoha",
            "NyanCat",
            "PeroPero in the Universe",
            "In-kya Yo-kya Onmyoji",
            "KABOOOOOM!!!!",
            "Doppelganger",
            "假面日记",
            "Reminiscence",
            "DarakuDatenshi",
            "D.I.Y.",
            "男子in☆バーチャランド",
            "kuí",
            "marooned night",
            "daydream girl",
            "Ornamentじゃない(Muse Dash Mix)",
            "Baby Pink (w/ YUC'e)",
            "I'm Here",
            "On And On!!",
            "Trip!",
            "Hoshi no otoshimono",
            "Plucky Race",
            "Fantasia Sonata Destiny",
            "Run through",
            "White Canvas (feat. 藍月なくる)",
            "Gloomy Flash (feat. Mami)",
            "今月のおすすめプレイリストを検索します",
            "Sunday Night (feat. Kanata.N)",
            "Goodbye Goodnight (feat. Shully)",
            "ENDLESS CIDER (feat. Such)",
            "月に叢雲華に風",
            "Patchouli's - Best Hit GSK",
            "物凄いスペースシャトルでこいしが物凄いうた",
            "囲い無き世は一期の月影",
            "Psychedelic Kizakura Doumei",
            "Mischievous Sensation",
            "Psyched Fevereiro",
            "Inferno City",
            "Paradigm Shift",
            "Snapdragon",
            "Prestige and Vestige",
            "Tiny Fate",
            "Tokimeki★Meteostrike",
            "Down Low",
            "LOUDER MACHINE",
            "それはもうらぶちゅ",
            "Rave_Tech",
            "Brilliant & Shining! (Game Edit.)",
            "People People",
            "Endless Error Loop",
            "Forbidden Pizza!",
            "ボーカルに無茶させんな",
            "MuseDashヵヽﾞ何ヵヽ干∋ッ`⊂ぉヵヽＵ＜ﾅょッﾅﾆ気ヵヽﾞ￡ゑょ",
            "Aleph-0",
            "ぶっとばスーパーノヴァ",
            "Rush-Hour",
            "3rd Avenue",
            "WORLDINVADER",
            "【东爱璃Lovely】Lovely",
            "森海の船",
            "Ooi",
            "沼った！！",
            "SATELLITE",
            "Fantasia Sonata Colorful feat. V!C",
            "Doki Doki Jump! (feat. ぷにぷに電機)",
            "100年モノのストリーマーズ・ハイ",
            "Love Patrol",
            "Mahorova feat.omoto",
            "夜の街",
            "INTERNET YAMERO（Aiobahn feat.KOTOKO）",
            "すとり～ま～FIRE!?!?",
            "Tanuki Step",
            "Space Stationery",
            "Songs Are Judged 90% by Chorus feat. Mameko",
            "Kawaiク華麗に宇宙怪盗",
            "Night City Runway",
            "Chaos Shotgun feat. ChumuNote",
            "mew mew magical summer",
            "Rainy Angel",
            "Gullinkambi",
            "RakiRaki Rebuilders!!!",
            "Laniakea",
            "OTTAMA GAZER",
            "Sleep Tight feat.Macoto",
            "New York Back Raise",
            "slic.hertz",
            "Fuzzy-Navel",
            "Swing Edge",
            "Twisted Escape",
            "Swing Sweet Twee Dance",
            "Samayoi no mei ～Amatsu～",
            "INTERNET SURVIVOR",
            "Shuki☆RaiRai!!!",
            "HELLOHELL",
            "Calamity Fortune",
            "つるぺったん",
            "Sweet Dream(VIVINOS - 'Alien Stage OST Part.2')",
            "Ruler Of My Heart(VIVINOS - 'Alien Stage Pt5')",
            "Reality Show",
            "SIG feat.Tobokegao",
            "蔷薇の恋心 feat.AKA",
            "Euphoria",
            "P E R O P E R O兄✰貴✰乱✰舞（feat.音游部, howsoon）",
            "PA☆PPA☆PANIC",
            "How To Make 音ゲ～曲！",
            "Ré：Ré",
            "Marmalade Twins",
            "DOMINATOR",
            "てしかに( TESHiKANi )",
            "Urban Magic",
            "Maid's Prank",
            "Dance Dance 晚安舞会",
            "Ops:Limone",
            "NOVA",
            "Heaven's Gradius",
            "SUPERHERO",
            "Highway_Summer",
            "Mx. Black Box",
            "Sweet Encounter",
            "disco light",
            "room light feat.chancylemon",
            "Invisible",
            "圣诞季-LLABB",
            "Hyouryu",
            "The Whole Rest",
            "Hydra",
            "Pastel Lines",
            "LINK x LIN#S",
            "Arcade ViruZ",
            "Eve Avenir",
            "Silverstring",
            "Melusia",
            "Devil's Castle",
            "Abatement",
            "Azalea",
            "Brightly World",
            "We'll meet in every world ★★★",
            "Collapsar",
            "Parousia",
            "Gunners in the Rain",
            "Halzion",
            "SHOWTIME!!",
            "Achromic Riddle",
            "karanosu",
            "Saishuu kichiku imouto Flandre-S",
            "Kachoufuugetsu",
            "Maid heart is a puppet",
            "Trance dance anarchy",
            "fairy stage",
            "スカーレット警察のゲットーパトロール24時",
            "Unwelcome School",
            "Usagi Flap",
            "RE Aoharu",
            "Operation☆DOTABATA!",
            "The Happycore Idol",
            "Amatsumikaboshi",
            "ARIGA THESIS",
            "ナイト・オブ・ナイツ",
            "#Psychedelic_Meguro_River",
            "can you feel it",
            "Midnight O'clock",
            "Rin",
            "Smile-mileS",
            "Believing and Being",
            "カタリスト",
            "don't！stop！eroero！",
            "pa pi pu pi pu pi pa",
            "Sand Maze",
            "Diffraction",
            "AKUMU / feat.tug",
            "Queen Aluett",
            "DROPS (feat. Such)",
            "物凄い狂っとるフランちゃんが物凄いうた",
            "snooze",
            "Kuishinbo Hacker feat.Kuishinbo Akachan",
            "Inu no outa",
            "Prism Fountain",
            "Gospel",
            "天灵灵地灵灵",
            "Squalldecimator feat. EZ-Ven",
            "Amateras Rhythm",
            "Record one's Dream",
            "Lunatic",
            "旧梦",
            "The Day We Become Family",
            "Silver Bullet",
            "Random",
            "Is there no way I'm defeated by OTOGE-BOSS-KYOKU-CHAN is strongly provoking?????",
            "Crow Rabbit",
            "SyZyGy",
            "人鱼电台",
            "Helixir",
            "Highway Cruisin'",
            "JACK PT BOSS",
            "Time Capsule",
            "NICE TYPE feat. monii",
            "Sanyousei SAY YA!!!",
            "YUKEMURI TAMAONSEN II",
            "暮色小诗",
            "All My Friends (feat. RANASOL)",
            "Heartache",
            "Blue Lemonade",
            "Haunted Dance",
            "Hey Vincent.",
            "Meteor (feat. TEA)",
            "Narcissism Angel",
            "AlterLuna",
            "Niki Tousen",
            "HIT ME UP",
            "Test Me (feat. Uyeon)",
            "Assault TAXI",
            "No",
            "Pop it",
            "HEARTBEAT！キュンキュン！iKz feat.Warma",
            "Necromantic",
        ]

    @functools.cached_property
    def songs_dlc_msr_anthology_vol_1(self) -> List[str]:
        return [
            "Boiling Blood",
            "ManiFesto：",
            "Operation Blade",
            "Radiant",
            "Renegade",
            "Speed of Light",
            "Dossoles Holiday",
            "Autumn Moods",
        ]

    @functools.cached_property
    def songs_dlc_maimai_dx_limited_time_suite(self) -> List[str]:
        return [
            "N3V3R G3T OV3R",
            "Oshama Scramble!",
            "Valsqotch",
            "Paranormal My Mind",
            "Flower, snow and Drum'n'bass.",
            "Amenohoakari",
        ]

    @functools.cached_property
    def songs_dlc_neon_abyss(self) -> List[str]:
        return [
            "BrainDance",
            "My Focus!",
            "ABABABA BURST",
            "ULTRA HIGHER",
        ]

    @functools.cached_property
    def songs_dlc_miku_in_museland(self) -> List[str]:
        return [
            "39みゅーじっく！",
            "Hand in Hand",
            "シニカルナイトプラン",
            "神っぽいな",
            "ダーリンダンス",
            "初音天地開闢神話",
            "ヴァンパイア",
            "フューチャー・イヴ",
            "Unknown・MotherGoose",
            "春嵐",
        ]

    @functools.cached_property
    def songs_dlc_rin_lens_mirrorland(self) -> List[str]:
        return [
            "劣等上等",
            "テレキャスタービーボーイ",
            "い～やい～やい～や",
            "ねぇねぇねぇ。",
            "Chaotic Love Revolution",
            "しかばねの踊り",
            "ビターチョコデコレーション",
            "ダンスロボットダンス",
            "Sweet Devil",
            "Someday'z Coming",
        ]

    @functools.cached_property
    def songs_dlc_chunithm_course_muse(self) -> List[str]:
        return [
            "Ray Tuning",
            "World Vanquisher",
            "月詠に鳴る",
            "The wheel to the right",
            "Climax",
            "Spider's Thread",
        ]

    @functools.cached_property
    def songs_dlc_msr_anthology_vol_2(self) -> List[str]:
        return [
            "Break Through the Dome",
            "Here in Vernal Terrene",
            "Everything's Alright",
            "Operation Ashring",
            "Misty Memory (Day Version)",
            "Arsonist",
            "Operation Deepness",
            "ALL!!!",
        ]

    def songs(self) -> List[str]:
        songs = self.songs_base[:]

        if self.has_dlc_muse_plus:
            songs.extend(self.songs_dlc_muse_plus)
        if self.has_dlc_msr_anthology_vol_1:
            songs.extend(self.songs_dlc_msr_anthology_vol_1)
        if self.has_dlc_maimai_dx_limited_time_suite:
            songs.extend(self.songs_dlc_maimai_dx_limited_time_suite)
        if self.has_dlc_neon_abyss:
            songs.extend(self.songs_dlc_neon_abyss)
        if self.has_dlc_miku_in_museland:
            songs.extend(self.songs_dlc_miku_in_museland)
        if self.has_dlc_rin_lens_mirrorland:
            songs.extend(self.songs_dlc_rin_lens_mirrorland)
        if self.has_dlc_chunithm_course_muse:
            songs.extend(self.songs_dlc_chunithm_course_muse)
        if self.has_dlc_msr_anthology_vol_2:
            songs.extend(self.songs_dlc_msr_anthology_vol_2)

        return sorted(songs)

    @staticmethod
    def level_range() -> range:
        return range(1, 10)

    @staticmethod
    def level_range_hard() -> range:
        return range(10, 12)

    @staticmethod
    def grades() -> List[str]:
        return [
            "C",
            "B",
            "A",
            "Pink S",
            "Silver S",
        ]


# Archipelago Options
class MuseDashDLCOwned(OptionSet):
    """
    Indicates which Muse Dash DLC the player owns, if any.
    """

    display_name = "Muse Dash DLC Owned"
    valid_keys = [
        "Muse Plus",
        "MSR Anthology Vol.01",
        "maimai DX Limited-time Suite",
        "Neon Abyss",
        "Miku in Museland",
        "Rin-Len's Mirrorland",
        "CHUNITHM COURSE MUSE",
        "MSR Anthology Vol.02",
    ]

    default = valid_keys
