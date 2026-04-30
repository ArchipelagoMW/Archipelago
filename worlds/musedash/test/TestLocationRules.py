from . import MuseDashTestBase
from typing import List


class LocationRules(MuseDashTestBase):
    CHECK_SONGS: List[str] = [
        "Magical Wonderland",
        "Iyaiya",
        "Wonderful Pain",
        "Breaking Dawn",
        "One-Way Subway",
        "Frost Land",
        "Heart-Pounding Flight",
        "Pancake is Love",
        "Shiguang Tuya",
        "Evolution",
        "Dolphin and Broadcast",
        "Yuki no Shizuku Ame no Oto",
        "Best One feat.tooko",
        "Candy-coloured Love Theory",
        "Night Wander",
        "Dohna Dohna no Uta",
        "Spring Carnival",
        "DISCO NIGHT",
        "Koi no Moonlight"
    ]
    
    options = {
        "starting_song_count": 3,
        "additional_song_count": 15,
        "streamer_mode_enabled": True,
        "include_songs": CHECK_SONGS
    }
    
    
    def test_rules(self):
        """Due to me typoing the second rule of a location, this test exists to ensure that doesn't happen again"""
        muse_dash_world = self.get_world()
        
        for song in self.CHECK_SONGS:
            if song == muse_dash_world.victory_song_name:
                continue
                
            if song in muse_dash_world.starting_songs:
                self.assertTrue(self.can_reach_location(song + "-0"), f"Starting Location {song}-0 was not beatable.")
                self.assertTrue(self.can_reach_location(song + "-1"), f"Starting Location {song}-1 was not beatable.")
                continue
                
            
            self.assertFalse(self.can_reach_location(song + "-0"), f"Location {song}-0 was unlocked without an item.")
            self.assertFalse(self.can_reach_location(song + "-1"), f"Location {song}-1 was unlocked without an item.")
            self.collect_by_name(song)
            self.assertTrue(self.can_reach_location(song + "-0"), f"Location {song}-0 was not unlocked with its item.")
            self.assertTrue(self.can_reach_location(song + "-1"), f"Location {song}-1 was not unlocked with its item.")
        
        
        sheets = self.get_items_by_name("Music Sheet")
        sheets_to_win = muse_dash_world.get_music_sheet_win_count()
        
        for sheet in sheets:
            if sheets_to_win <= 0:
                break
            
            self.assertBeatable(False)
            self.collect(sheet)
            sheets_to_win -= 1
            
        self.assertBeatable(True)
        