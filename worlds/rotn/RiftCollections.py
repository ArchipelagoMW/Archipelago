from .items import SongData, ExtraSongData
from typing import Dict, List, Set
from collections import ChainMap

class RotNCollections:
    DIAMOND_NAME: str = "Diamond"
    DIAMOND_CODE: int = 1

    # Thanks to DeamonHunter for genning this info
    SONG_DATA: Dict[str, SongData] = {
        "Disco Disaster": SongData(50, "TrackName_DiscoDisaster", "Base", 1, 4, 7, 22),
        "Elusional": SongData(51, "TrackName_Elusional", "Base", 2, 6, 11, 21),
        "Visualize Yourself": SongData(52, "TrackName_VisualizeYourself", "Base", 3, 7, 14, 24),
        "Spookhouse Pop": SongData(53, "TrackName_SpookhousePop", "Base", 4, 6, 16, 23),
        "Om and On": SongData(54, "TrackName_OmAndOn", "Base", 4, 6, 18, 26),
        "Morning Dove": SongData(55, "TrackName_MorningDove", "Base", 6, 8, 16, 22),
        "Heph's Mess": SongData(56, "TrackName_HephsMess", "Base", 2, 5, 13, 19),
        "Amalgamaniac": SongData(57, "TrackName_Amalgamaniac", "Base", 4, 7, 14, 24),
        "Hang Ten Heph": SongData(58, "TrackName_HangTenHeph", "Base", 4, 8, 17, 25),
        "Count Funkula": SongData(59, "TrackName_CountFunkula", "Base", 3, 7, 19, 29),
        "Overthinker": SongData(60, "TrackName_Overthinker", "Base", 4, 9, 13, 28),
        "Cryp2que": SongData(61, "TrackName_Cryp2que", "Base", 3, 8, 13, 27),
        "Nocturning": SongData(62, "TrackName_Nocturning", "Base", 3, 6, 12, 23),
        "Glass Cages (feat. Sarah Hubbard)": SongData(63, "TrackName_GlassCages", "Base", 4, 8, 17, 25),
        "Hallow Queen": SongData(64, "TrackName_HallowQueen", "Base", 4, 8, 16, 18),
        "Progenitor": SongData(65, "TrackName_Progenitor", "Base", 3, 13, 19, 25),
        "Matriarch": SongData(66, "TrackName_Matriarch", "Base", 7, 11, 18, 23),
        "Under the Thunder": SongData(67, "TrackName_Thunder", "Base", 4, 12, 17, 27),
        "Eldritch House": SongData(68, "TrackName_EldritchHouse", "Base", 4, 9, 16, 25),
        "RAVEVENGE (feat. Aram Zero)": SongData(69, "TrackName_RAVEvenge", "Base", 5, 9, 14, 27),
        "Rift Within": SongData(70, "TrackName_RiftWithin", "Base", 4, 10, 17, 26),
        "Suzu's Quest": SongData(71, "TrackName_SuzusQuest", "Base", 6, 12, 19, 24),
        "Necropolis": SongData(72, "TrackName_Necropolis", "Base", 4, 10, 16, 18),
        "Baboosh": SongData(73, "TrackName_Baboosh", "Base", 6, 12, 19, 30),
        "Necro Sonatica": SongData(74, "TrackName_NecroSonatica", "Base", 8, 16, 21, 30),
        "She Banned": SongData(75, "TrackName_SheBanned", "Base", 5, 11, 17, 22),
        "King's Ruse": SongData(76, "TrackName_KingsRuse", "Base", 3, 11, 15, 28),
        "What's in the Box": SongData(77, "TrackName_WhatsInTheBox", "Base", 4, 9, 14, 26),
        "Brave the Harvester": SongData(78, "TrackName_BravetheHarvester", "Base", 6, 14, 20, 27),
        "Final Fugue": SongData(79, "TrackName_FinalFugue", "Base", 6, 13, 20, 30),
        "Twombtorial": SongData(80, "TrackName_Twombtorial", "Base", 5, 13, 19, 23),
        "Portamello": SongData(81, "TrackName_Portamello", "Base", 5, 10, 15, 20),
        #Meat Boy
        "Slugger's Refrain": SongData(82, "TrackName_DLC_Apricot01", "MeatBoy", 6, 14, 21, 30),
        "Got Danged": SongData(83, "TrackName_DLC_Apricot02", "MeatBoy", 5, 12, 20, 30),
        "Bootus Bleez": SongData(84, "TrackName_DLC_Apricot03", "MeatBoy", 6, 10, 19, 29),
        #Celeste
        "Resurrections (dannyBstyle Remix)": SongData(85, "TrackName_DLC_Banana01", "Free Promo", 6, 10, 17, 27),
        "Scattered and Lost": SongData(86, "Scattered and Lost", "Celeste", 4, 8, 16, 25),
        "Reach for the Summit": SongData(87, "Reach for the Summit", "Celeste", 7, 11, 18, 30),
        "Confronting Myself": SongData(88, "Confronting Myself", "Celeste", 6, 9, 17, 26),
        "Resurrections": SongData(89, "Resurrections", "Celeste", 6, 10, 17, 27),
        #Anniversary
        "Crypteque": SongData(90, "Crypteque", "Anniversary", 5, 9, 13, 24),
        "Power Cords": SongData(91, "Power Cords", "Anniversary", 2, 7, 12, 23),
        "Fungal Funk": SongData(92, "Fungal Funk", "Anniversary", 4, 12, 17, 24),
        #Pizza Tower
        "It's Pizza Time!": SongData(93, "It's Pizza Time!", "Pizza Tower", 7, 13, 19, 24),
        "The Death That I Deservioli": SongData(94, "The Death That I Deservioli", "Pizza Tower", 7, 11, 18, 26),
        "Unexpectancy, Pt. 3": SongData(95, "Unexpectancy, Pt. 3", "Pizza Tower", 8, 16, 21, 29),
        "World Wide Noise": SongData(96, "World Wide Noise", "Pizza Tower", 5, 10, 19, 28),
        #Miku
        "Too Real": SongData(97, "Too Real", "Free Promo", 4, 9, 16, 25),
        "M@GICAL☆CURE! LOVE ♥ SHOT!": SongData(98, "M@GICAL☆CURE! LOVE ♥ SHOT!", "Hatsune Miku", 5, 11, 18, 26),
        "Intergalactic Bound": SongData(99, "Intergalactic Bound", "Hatsune Miku", 3, 8, 15, 23),
        "Just 1dB Louder": SongData(100, "Just 1dB Louder", "Hatsune Miku", 4, 11, 18, 26),
        "MikuFiesta": SongData(101, "MikuFiesta", "Hatsune Miku", 3, 9, 16, 24),
        "Radiant Revival": SongData(102, "Radiant Revival", "Hatsune Miku", 4, 7, 16, 23),
        #Hololive
        "REFLECT": SongData(103, "REFLECT", "Free Promo", 7, 12, 17, 23),
        "BIBBIDIBA": SongData(104, "BIBBIDIBA", "Hololive", 4, 9, 14, 22),
        "Play Dice!": SongData(105, "Play Dice!", "Hololive", 8, 13, 19, 25),
        "Ahoy!! 我ら宝鐘海賊団☆": SongData(106, "Ahoy!! 我ら宝鐘海賊団☆", "Hololive", 7, 14, 20, 30),
        "Carbonated Love": SongData(107, "Carbonated Love", "Hololive", 5, 10, 15, 23),
        #Everhood
        "Powers Of Destruction": SongData(108, "Powers of Destruction", "Free Promo", 7, 11, 14, 20),
        "The Final Battle": SongData(109, "The Final Battle", "Everhood", 6, 10, 16, 22),
        "Feisty Flowers": SongData(110, "Feisty Flowers", "Everhood", 5, 10, 19, 29),
        "Revenge": SongData(111, "Revenge", "Everhood", 5, 12, 20, 29),
        "Why Oh You Are LOVE": SongData(112, "Why Oh You Are LOVE", "Everhood", 5, 15, 21, 30),
        #Monstercat
        "Crab Rave": SongData(113, "Crab Rave", "Monstercat", 5, 11, 18, 24),
        "Final Boss": SongData(114, "Final Boss", "Monstercat", 2, 9, 17, 25),
        "New Game": SongData(115, "New Game", "Monstercat", 6, 11, 19, 25),
        "PLAY": SongData(116, "PLAY", "Monstercat", 6, 11, 16, 26),
        "Waiting For You (feat. Joanna Jones)": SongData(117, "Waiting for you (feat. Joanna Jones)", "Monstercat", 5, 11, 16, 22),
        #Shovel Knight
        "Main Theme": SongData(118, "Main Theme", "Free Promo", 4, 9, 17, 24),
        "La Danse Macabre (Lich Yard)": SongData(119, "La Danse Macabre (Lich Yard)", "Shovel Knight", 5, 7, 20, 27),
        "Strike the Earth! (Plains of Passage)": SongData(120, "Strike the Earth! (Plains of Passage)", "Shovel Knight", 2, 8, 16, 27),
        "In the Halls of the Usurper (Pridemoor Keep)": SongData(121, "In the Halls of the Usurper (Pridemoor Keep)", "Shovel Knight", 5, 9, 17, 22),
        "High Above the Land (The Flying Machine)": SongData(122, "High Above the Land (The Flying Machine)", "Shovel Knight", 4, 7, 16, 21),
        "An Underlying Problem (The Lost City)": SongData(123, "An Underlying Problem (The Lost City)", "Shovel Knight", 4, 11, 18, 23),
        #Friday Night Funkin'
        "Dad Battle": SongData(124, "Dad Battle", "Free Promo", 4, 10, 16, 21),
        "Blammed": SongData(125, "Blammed", "Friday Night Funkin'", 7, 12, 18, 25),
        "Stress": SongData(126, "Stress", "Friday Night Funkin'", 7, 15, 21, 28),
        "Darnell": SongData(127, "Darnell", "Friday Night Funkin'", 6, 10, 19, 27),
        "Ugh": SongData(185, "Ugh", "Friday Night Funkin'", 5, 12, 17, 24),
        "Senpai": SongData(129, "Senpai", "Friday Night Funkin'", 2, 10, 16, 24),
        #Unbeatable
        "WORN OUT TAPES [tally-ho version]": SongData(130, "WORN OUT TAPES [tally-ho version]", "Free Promo", 5, 12, 16, 25),
    }

    EXTRA_DATA: Dict[str, ExtraSongData] = {
        #Minigames
        "A Bit of a Stretch": ExtraSongData(2000, "Minigame", 0),
        "Lunch Rush": ExtraSongData(2003, "Minigame", 0),
        "Voguelike": ExtraSongData(2006, "Minigame", 0),
        "Show Time!": ExtraSongData(2009, "Minigame", 0),
        "Take a Breather": ExtraSongData(2012, "Minigame", 0),
        #Bosses
        "Harmonie": ExtraSongData(2100, "Boss", 0),
        "Deep Blues": ExtraSongData(2103, "Boss", 0),
        "Matron": ExtraSongData(2106, "Boss", 0),
        "Reaper": ExtraSongData(2109, "Boss", 0),
        "The NecroDancer": ExtraSongData(2112, "Boss", 0),
    }

    FREE_PACKS: List[str] = [
        "Base",
        "MeatBoy",
        "Anniversary",
        "Free Promo",
        "Minigame",
        "Boss"
    ]

    DLC: List[str] = [
        "Celeste",
        "Pizza Tower",
        "Hatsune Miku",
        "Hololive",
        "Everhood",
        "Monstercat",
        "Shovel Knight",
        "Friday Night Funkin'",

        "Resurrections (dannyBstyle Remix)",
        "Scattered and Lost",
        "Reach for the Summit",
        "Confronting Myself",
        "Resurrections",

        "It's Pizza Time!",
        "The Death That I Deservioli",
        "Unexpectancy, Pt. 3",
        "World Wide Noise",

        "M@GICAL☆CURE! LOVE ♥ SHOT!",
        "Intergalactic Bound",
        "Just 1dB Louder",
        "MikuFiesta",
        "Radiant Revival",

        "BIBBIDIBA",
        "Play Dice!",
        "Ahoy!! 我ら宝鐘海賊団☆",
        "Carbonated Love",

        "The Final Battle",
        "Feisty Flowers",
        "Revenge",
        "Why Oh You Are LOVE",

        "Crab Rave",
        "Final Boss",
        "New Game",
        "PLAY",
        "Waiting For You (feat. Joanna Jones)",

        "Main Theme",
        "La Danse Macabre (Lich Yard)",
        "Strike the Earth! (Plains of Passage)",
        "In the Halls of the Usurper (Pridemoor Keep)",
        "High Above the Land (The Flying Machine)",
        "An Underlying Problem (The Lost City)",

        "Blammed",
        "Stress",
        "Darnell",
        "Ugh",
        "Senpai",
    ]

    song_locations: Dict[str, int] = {}
    song_items: Dict[str, SongData] = {}

    filler_items: Dict[str, int] = {
        "Apple": 2,
        "Cheese": 3,
        "Chicken": 4,
        "Ham": 5,
        "Vibe Charge": 6,
    }

    filler_weights: Dict[str, int] = {
        "Apple": 10,
        "Cheese": 7,
        "Chicken": 4,
        "Ham": 1,
        "Vibe Charge": 5,
    }

    item_names_to_id: ChainMap = ChainMap({}, filler_items)
    location_names_to_id: ChainMap = ChainMap(song_locations)

    def __init__(self) -> None:
        self.item_names_to_id[self.DIAMOND_NAME] = self.DIAMOND_CODE

        for key, data in self.SONG_DATA.items():
            self.song_items[key] = data
            self.song_items[key + " (Remix)"] = SongData(data.code + 1000, data.song_name, data.DLC, data.diff_easy, data.diff_medium, data.diff_hard, data.diff_impossible, "Remix")

        for key, data in self.EXTRA_DATA.items():
            self.song_items[key] = SongData(data.code, key, data.DLC, 1, 0, 0, 0, data.DLC)
            self.song_items[key + " (Medium)"] = SongData(data.code + 1, key, data.DLC, 0, 1, 0, 0, data.DLC)
            self.song_items[key + " (Hard)"] = SongData(data.code + 1, key, data.DLC, 0, 0, 1, 0, data.DLC)

        self.item_names_to_id.update({name: data.code for name, data in self.song_items.items()})

        location_id_index = 1
        for name in self.SONG_DATA.keys():
            self.song_locations[f"{name}-0"] = location_id_index 
            self.song_locations[f"{name}-1"] = location_id_index + 1
            self.song_locations[f"{name} (Remix)-0"] = location_id_index + 1000
            self.song_locations[f"{name} (Remix)-1"] = location_id_index + 1001
            location_id_index += 2

        location_id_index = 2000
        for name in self.EXTRA_DATA.keys():
            self.song_locations[f"{name}-0"] = location_id_index 
            self.song_locations[f"{name}-1"] = location_id_index + 1
            self.song_locations[f"{name} (Medium)-0"] = location_id_index + 2
            self.song_locations[f"{name} (Medium)-1"] = location_id_index + 3
            self.song_locations[f"{name} (Hard)-0"] = location_id_index + 4
            self.song_locations[f"{name} (Hard)-1"] = location_id_index + 5
            location_id_index += 6

    def getSongsWithSettings(self, options, diff_lower: int, diff_higher:int) -> List[str]:
        dlc_songs = options.dlc_songs
        filtered_list = []

        for key, data in self.song_items.items():
            if data.DLC == "Minigame":
                if options.include_minigames == 1 and data.diff_easy == 1:
                    filtered_list.append(key)
                elif options.include_minigames == 2 and data.diff_easy == 0:
                    filtered_list.append(key)
                continue

            if data.DLC == "Boss":
                if options.include_boss_battle == 1 and data.diff_easy == 1:
                    filtered_list.append(key)
                elif options.include_boss_battle == 2 and data.diff_easy == 0:
                    filtered_list.append(key)
                continue
            
            if data.type == "Remix" and not options.include_remix:
                continue

            if not self.songMatchesDlcFilter(data, dlc_songs):
                continue

            if data.diff_easy != -1 and "Easy" in options.difficulty_option and diff_lower <= data.diff_easy <= diff_higher:
                filtered_list.append(key)
                continue

            if data.diff_medium != -1 and "Medium" in options.difficulty_option and diff_lower <= data.diff_medium <= diff_higher:
                filtered_list.append(key)
                continue

            if data.diff_hard != -1 and "Hard" in options.difficulty_option and diff_lower <= data.diff_hard <= diff_higher:
                filtered_list.append(key)
                continue

            if data.diff_impossible != -1 and "Impossible" in options.difficulty_option and diff_lower <= data.diff_impossible <= diff_higher:
                filtered_list.append(key)
                continue

        return filtered_list
    
    def songMatchesDlcFilter(self, song: SongData, dlc_songs: Set[str]) -> bool:
        if song.DLC in self.FREE_PACKS:
            return True

        if song.DLC in dlc_songs or song.song_name in dlc_songs:
            return True

        return False
    
    def getItemNameGroups(self) -> Dict[str, str]:
        groups = {
            "Rhythm Rift": {name for name, data, in self.song_items.items() if data.type == "Rift"},
            "Remix Rift": {name for name, data, in self.song_items.items() if data.type == "Remix"},
            "Minigame": {name for name, data, in self.song_items.items() if data.type == "Minigame"},
            "Boss Battle": {name for name, data, in self.song_items.items() if data.type == "Boss"},

            "Base Songs": {name for name, data, in self.song_items.items() if data.DLC == "base"},
            "Meat Boy": {name for name, data, in self.song_items.items() if data.DLC == "MeatBoy"},
            "Anniversary": {name for name, data, in self.song_items.items() if data.DLC == "Anniversary"},
            "Free Promo": {name for name, data, in self.song_items.items() if data.DLC == "Free Promo"},
            "Celeste": {name for name, data, in self.song_items.items() if data.DLC == "Celeste"},
            "Pizza Tower": {name for name, data, in self.song_items.items() if data.DLC == "Pizza Tower"},
            "Hatsune Miku": {name for name, data, in self.song_items.items() if data.DLC == "Hatsune Miku"},
            "Hololive": {name for name, data, in self.song_items.items() if data.DLC == "Hololive"},
            "Everhood": {name for name, data, in self.song_items.items() if data.DLC == "Everhood"},
            "Monstercat": {name for name, data, in self.song_items.items() if data.DLC == "Monstercat"},
            "Friday Night Funkin'": {name for name, data, in self.song_items.items() if data.DLC == "Friday Night Funkin'"}
        }

        return groups