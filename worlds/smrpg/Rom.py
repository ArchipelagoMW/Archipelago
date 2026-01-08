import hashlib
import os
from enum import Enum, auto
from typing import Dict

import Utils
from worlds.Files import APDeltaPatch

treasure_chest_base_address = 0xE03D80
base_memory_address = 0xE00000
rom_name_location = 0x007FC0
md5_hash = "d0b68d68d9efc0558242f5476d1c5b81"
items_received_address = 0xE03FF0
items_sendable_address_1 = 0xE03062  # Is the Map/Star Piece menu available?
items_sendable_address_2 = 0xF51D04  # Current music
items_sendable_address_3 = 0xE03076  # Is a star active?
items_sendable_address_4 = 0xF53021  # In a battle?
# Silence, battle musics, victory musics, and star music are all forbidden
nonsendable_music_values = [0x00, 0x03, 0x06, 0x08, 0x09, 0x0C, 0x19, 0x1D, 0x23, 0x36, 0x37, 0x3B, 0x3C, 0x44, 0x45]
victory_music_values = [0x40, 0x46, 0x47, 0x48, 0x49]
bit_positions = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]
items_inventory_address = 0xF6F882
gear_inventory_address = 0xF6F864
keys_inventory_address = 0xF6F8A0
coins_address = 0xF6F8AF
frog_coins_address = 0xF6F8B3
max_flowers_address = 0xF6F8B2
current_flowers_address = 0xF6F8B1

max_coins = 9999
max_frog_coins = 999
max_flowers = 99

characters = ["Mario", "Mallow", "Geno", "Bowser", "Toadstool"]

hit_points = { # (Current, Max)
    "Mario": (0xF6F801, 0xF6F803),
    "Mallow": (0xF6F851, 0xF6F853),
    "Geno": (0xF6F83D, 0xF6F83F),
    "Bowser": (0xF6F829, 0xF6F82B),
    "Toadstool": (0xF6F815, 0xF6F817),
}

class SMRPGDeltaPatch(APDeltaPatch):
    hash = md5_hash
    game = "Super Mario RPG Legend of the Seven Stars"
    patch_file_ending = ".apsmrpg"
    result_file_ending = ".sfc"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


class MemoryLocation():
    def __init__(self, address, bit, set_when_checked):
        self.address = address
        self.bit = bit_positions[bit]
        self.set_when_checked = set_when_checked


class ItemCategory(Enum):
    item = auto()
    gear = auto()
    key = auto()
    coin = auto()
    frog_coin = auto()
    flower = auto()
    recovery = auto()


class ItemData():
    def __init__(self, id, category: ItemCategory):
        self.id = id
        self.category = category


location_data: Dict[str, MemoryLocation] = dict({
    "Chest - Mushroom Way 1": MemoryLocation(treasure_chest_base_address + 9, 6, False),
    "Chest - Mushroom Way 2": MemoryLocation(treasure_chest_base_address + 9, 7, False),
    "Chest - Mushroom Way 3": MemoryLocation(treasure_chest_base_address + 10, 0, False),
    "Chest - Mushroom Way 4": MemoryLocation(treasure_chest_base_address + 10, 1, False),
    "Chest - Mushroom Kingdom Vault 1": MemoryLocation(treasure_chest_base_address + 0, 3, False), # non-static RAM map
    "Chest - Mushroom Kingdom Vault 2": MemoryLocation(treasure_chest_base_address + 0, 4, False), # non-static RAM map
    "Chest - Mushroom Kingdom Vault 3": MemoryLocation(treasure_chest_base_address + 0, 5, False), # non-static RAM map
    "Chest - Bandit's Way Flower Jump": MemoryLocation(treasure_chest_base_address + 10, 3, False),
    "Chest - Bandit's Way Guard Dog": MemoryLocation(treasure_chest_base_address + 2, 0, False),
    "Chest - Bandit's Way Invincibility Star": MemoryLocation(treasure_chest_base_address + 2, 1, False),
    "Chest - Bandit's Way Dog Jump": MemoryLocation(treasure_chest_base_address + 2, 2, False),
    "Chest - Bandit's Way Croco Room": MemoryLocation(treasure_chest_base_address + 10, 2, False),
    "Chest - Kero Sewers Pandorite Room": MemoryLocation(treasure_chest_base_address + 1, 6, False),
    "Chest - Kero Sewers Invincibility Star": MemoryLocation(treasure_chest_base_address + 1, 5, False),
    # "Kero Sewers Recovery Chest": MemoryLocation(treasure_chest_base_address + 15, 4, False),
    "Key Item - Kero Sewers Key Chest (Cricket Jam)": MemoryLocation(treasure_chest_base_address + 15, 5, False),
    "Chest - Rose Way Platform Jump": MemoryLocation(treasure_chest_base_address + 2, 3, False),
    "Chest - Rose Town Store 1": MemoryLocation(treasure_chest_base_address + 3, 1, False),
    "Chest - Rose Town Store 2": MemoryLocation(treasure_chest_base_address + 3, 2, False),
    "Chest - Lazy Shell 1": MemoryLocation(treasure_chest_base_address + 19, 7, False),
    "Chest - Lazy Shell 2": MemoryLocation(treasure_chest_base_address + 20, 0, False),
    "Chest - Forest Maze 1": MemoryLocation(treasure_chest_base_address + 10, 4, False),
    "Chest - Forest Maze 2": MemoryLocation(treasure_chest_base_address + 10, 5, False),
    "Chest - Forest Maze Underground 1": MemoryLocation(treasure_chest_base_address + 13, 3, False), # non-static RAM map
    "Chest - Forest Maze Underground 2": MemoryLocation(treasure_chest_base_address + 13, 4, False), # non-static RAM map
    "Chest - Forest Maze Underground 3": MemoryLocation(treasure_chest_base_address + 13, 5, False), # non-static RAM map
    "Chest - Forest Maze Red Essence": MemoryLocation(treasure_chest_base_address + 10, 6, False),
    "Chest - Pipe Vault Slide 1": MemoryLocation(treasure_chest_base_address + 5, 7, False), # non-static RAM map
    "Chest - Pipe Vault Slide 2": MemoryLocation(treasure_chest_base_address + 5, 6, False), # non-static RAM map
    "Chest - Pipe Vault Slide 3": MemoryLocation(treasure_chest_base_address + 6, 0, False), # non-static RAM map
    "Chest - Pipe Vault Nippers 1": MemoryLocation(treasure_chest_base_address + 6, 1, False),
    "Chest - Pipe Vault Nippers 2": MemoryLocation(treasure_chest_base_address + 6, 2, False),
    "Chest - Yo'ster Isle": MemoryLocation(treasure_chest_base_address + 0, 6, False),
    "Chest - Moleville Mines Invincibility Star": MemoryLocation(treasure_chest_base_address + 15, 1, False),
    "Chest - Moleville Mines Coins": MemoryLocation(treasure_chest_base_address + 15, 0, False),
    "Chest - Moleville Mines Punchinello 1": MemoryLocation(treasure_chest_base_address + 15, 2, False),
    "Chest - Moleville Mines Punchinello 2": MemoryLocation(treasure_chest_base_address + 15, 3, False),
    "Chest - Booster Pass 1": MemoryLocation(treasure_chest_base_address + 4, 5, False),
    "Chest - Booster Pass 2": MemoryLocation(treasure_chest_base_address + 4, 6, False),
    "Chest - Booster Pass Secret 1": MemoryLocation(treasure_chest_base_address + 19, 2, False),
    "Chest - Booster Pass Secret 2": MemoryLocation(treasure_chest_base_address + 19, 3, False),
    "Chest - Booster Pass Secret 3": MemoryLocation(treasure_chest_base_address + 19, 4, False),
    "Chest - Booster Tower Spookum": MemoryLocation(treasure_chest_base_address + 9, 0, False),
    "Chest - Booster Tower Thwomp": MemoryLocation(treasure_chest_base_address + 1, 0, False),
    "Chest - Booster Tower Masher": MemoryLocation(treasure_chest_base_address + 9, 1, False),
    "Chest - Booster Tower Parachute": MemoryLocation(treasure_chest_base_address + 0, 7, False),
    "Chest - Booster Tower Zoom Shoes": MemoryLocation(treasure_chest_base_address + 1, 1, False),
    "Chest - Booster Tower Top 1": MemoryLocation(treasure_chest_base_address + 9, 2, False), # non-static RAM map
    "Chest - Booster Tower Top 2": MemoryLocation(treasure_chest_base_address + 9, 4, False), # non-static RAM map
    "Chest - Booster Tower Top 3": MemoryLocation(treasure_chest_base_address + 9, 5, False), # non-static RAM map
    "Chest - Marrymore Inn Second Floor": MemoryLocation(treasure_chest_base_address + 0, 0, False),
    "Chest - Sea Invincibility Star": MemoryLocation(treasure_chest_base_address + 6, 7, False),
    "Chest - Sea Save Room 1": MemoryLocation(treasure_chest_base_address + 6, 3, False),
    "Chest - Sea Save Room 2": MemoryLocation(treasure_chest_base_address + 6, 4, False),
    "Chest - Sea Save Room 3": MemoryLocation(treasure_chest_base_address + 6, 5, False),
    "Chest - Sea Save Room 4": MemoryLocation(treasure_chest_base_address + 6, 6, False),
    "Chest - Sunken Ship Rat Stairs": MemoryLocation(treasure_chest_base_address + 7, 7, False),
    "Chest - Sunken Ship Shop": MemoryLocation(treasure_chest_base_address + 8, 0, False),
    "Chest - Sunken Ship Coins 1": MemoryLocation(treasure_chest_base_address + 8, 1, False),
    "Chest - Sunken Ship Coins 2": MemoryLocation(treasure_chest_base_address + 8, 2, False),
    "Chest - Sunken Ship Clone Room": MemoryLocation(treasure_chest_base_address + 8, 3, False),
    "Chest - Sunken Ship Frog Coin Room": MemoryLocation(treasure_chest_base_address + 8, 4, False),
    "Chest - Sunken Ship Hidon Mushroom": MemoryLocation(treasure_chest_base_address + 8, 5, False),
    "Chest - Sunken Ship Safety Ring": MemoryLocation(treasure_chest_base_address + 8, 7, False),
    "Chest - Sunken Ship Bandana Reds": MemoryLocation(treasure_chest_base_address + 0, 2, False),
    "Chest - Land's End Red Essence": MemoryLocation(treasure_chest_base_address + 7, 0, False),
    "Chest - Land's End Chow Pit 1": MemoryLocation(treasure_chest_base_address + 7, 1, False),
    "Chest - Land's End Chow Pit 2": MemoryLocation(treasure_chest_base_address + 7, 2, False),
    "Chest - Land's End Bee Room": MemoryLocation(treasure_chest_base_address + 7, 3, False),
    "Chest - Land's End Secret 1": MemoryLocation(treasure_chest_base_address + 14, 7, False),
    "Chest - Land's End Secret 2": MemoryLocation(treasure_chest_base_address + 14, 6, False),
    "Chest - Land's End Shy Away": MemoryLocation(treasure_chest_base_address + 19, 1, False),
    "Chest - Land's End Invincibility Star 1": MemoryLocation(treasure_chest_base_address + 14, 3, False),
    "Chest - Land's End Invincibility Star 2": MemoryLocation(treasure_chest_base_address + 14, 1, False),
    "Chest - Land's End Invincibility Star 3": MemoryLocation(treasure_chest_base_address + 14, 2, False),
    "Chest - Belome Temple Fortune Teller": MemoryLocation(treasure_chest_base_address + 20, 1, False),
    "Chest - Belome Temple After Fortune 1": MemoryLocation(treasure_chest_base_address + 20, 2, False),
    "Chest - Belome Temple After Fortune 2": MemoryLocation(treasure_chest_base_address + 20, 3, False),
    "Chest - Belome Temple After Fortune 3": MemoryLocation(treasure_chest_base_address + 20, 5, False),
    "Chest - Belome Temple After Fortune 4": MemoryLocation(treasure_chest_base_address + 20, 4, False),
    # "Belome Temple Before Belome 1": MemoryLocation(treasure_chest_base_address + 20, 7, False),
    # "Belome Temple Before Belome 2": MemoryLocation(treasure_chest_base_address + 20, 6, False),
    # "Belome Temple Before Belome 3": MemoryLocation(treasure_chest_base_address + 21, 0, False),
    "Chest - Monstro Town Entrance": MemoryLocation(treasure_chest_base_address + 14, 5, False),
    "Chest - Bean Valley 1": MemoryLocation(treasure_chest_base_address + 13, 7, False), # non-static RAM map
    "Chest - Bean Valley 2": MemoryLocation(treasure_chest_base_address + 14, 0, False), # non-static RAM map
    "Chest - Bean Valley Box Boy Room": MemoryLocation(treasure_chest_base_address + 17, 1, False),
    "Chest - Bean Valley Slot Room": MemoryLocation(treasure_chest_base_address + 17, 3, False),
    "Chest - Bean Valley Piranha Plants": MemoryLocation(treasure_chest_base_address + 13, 6, False),
    "Chest - Bean Valley Beanstalk": MemoryLocation(treasure_chest_base_address + 18, 5, False),
    "Chest - Bean Valley Cloud 1": MemoryLocation(treasure_chest_base_address + 18, 1, False),
    "Chest - Bean Valley Cloud 2": MemoryLocation(treasure_chest_base_address + 18, 2, False),
    "Chest - Bean Valley Fall 1": MemoryLocation(treasure_chest_base_address + 18, 3, False),
    "Chest - Bean Valley Fall 2": MemoryLocation(treasure_chest_base_address + 18, 4, False),
    "Chest - Nimbus Land Shop": MemoryLocation(treasure_chest_base_address + 17, 2, False),
    "Chest - Nimbus Castle Before Birdo 1": MemoryLocation(treasure_chest_base_address + 4, 7, False),
    "Chest - Nimbus Castle Before Birdo 2": MemoryLocation(treasure_chest_base_address + 5, 1, False),
    "Chest - Nimbus Castle Out Of Bounds 1": MemoryLocation(treasure_chest_base_address + 19, 5, False),
    "Chest - Nimbus Castle Out Of Bounds 2": MemoryLocation(treasure_chest_base_address + 19, 6, False),
    "Chest - Nimbus Castle Single Gold Bird": MemoryLocation(treasure_chest_base_address + 5, 0, False),
    "Chest - Nimbus Castle Invincibility Star": MemoryLocation(treasure_chest_base_address + 5, 4, False),
    "Chest - Nimbus Castle Star After Valentina": MemoryLocation(treasure_chest_base_address + 5, 5, False),
    "Chest - Barrel Volcano Secret 1": MemoryLocation(treasure_chest_base_address + 17, 6, False),
    "Chest - Barrel Volcano Secret 2": MemoryLocation(treasure_chest_base_address + 18, 7, False),
    "Chest - Barrel Volcano Before Star 1": MemoryLocation(treasure_chest_base_address + 15, 5, False),
    "Chest - Barrel Volcano Before Star 2": MemoryLocation(treasure_chest_base_address + 18, 7, False),
    "Chest - Barrel Volcano Invincibility Star": MemoryLocation(treasure_chest_base_address + 19, 0, False),
    "Chest - Barrel Volcano Save Room 1": MemoryLocation(treasure_chest_base_address + 17, 6, False),
    "Chest - Barrel Volcano Save Room 2": MemoryLocation(treasure_chest_base_address + 17, 7, False),
    "Chest - Barrel Volcano Hinopio": MemoryLocation(treasure_chest_base_address + 18, 0, False),
    "Chest - Bowser's Keep Dark Room": MemoryLocation(treasure_chest_base_address + 22, 2, False),
    "Chest - Bowser's Keep Croco Shop 1": MemoryLocation(treasure_chest_base_address + 22, 0, False),
    "Chest - Bowser's Keep Croco Shop 2": MemoryLocation(treasure_chest_base_address + 22, 1, False),
    "Chest - Bowser's Keep Invisible Bridge 1": MemoryLocation(treasure_chest_base_address + 15, 7, False), # non-static RAM map
    "Chest - Bowser's Keep Invisible Bridge 2": MemoryLocation(treasure_chest_base_address + 16, 0, False), # non-static RAM map
    "Chest - Bowser's Keep Invisible Bridge 3": MemoryLocation(treasure_chest_base_address + 16, 1, False), # non-static RAM map
    "Chest - Bowser's Keep Invisible Bridge 4": MemoryLocation(treasure_chest_base_address + 16, 2, False), # non-static RAM map
    "Chest - Bowser's Keep Moving Platforms 1": MemoryLocation(treasure_chest_base_address + 23, 7, False), # non-static RAM map
    "Chest - Bowser's Keep Moving Platforms 2": MemoryLocation(treasure_chest_base_address + 24, 0, False), # non-static RAM map
    "Chest - Bowser's Keep Moving Platforms 3": MemoryLocation(treasure_chest_base_address + 24, 1, False), # non-static RAM map
    "Chest - Bowser's Keep Moving Platforms 4": MemoryLocation(treasure_chest_base_address + 23, 6, False), # non-static RAM map
    "Chest - Bowser's Keep Elevator Platforms": MemoryLocation(treasure_chest_base_address + 15, 6, False), # non-static RAM map
    "Chest - Bowser's Keep Cannonball Room 1": MemoryLocation(treasure_chest_base_address + 23, 3, False), # non-static RAM map
    "Chest - Bowser's Keep Cannonball Room 2": MemoryLocation(treasure_chest_base_address + 23, 1, False), # non-static RAM map
    "Chest - Bowser's Keep Cannonball Room 3": MemoryLocation(treasure_chest_base_address + 23, 5, False), # non-static RAM map
    "Chest - Bowser's Keep Cannonball Room 4": MemoryLocation(treasure_chest_base_address + 23, 4, False), # non-static RAM map
    "Chest - Bowser's Keep Cannonball Room 5": MemoryLocation(treasure_chest_base_address + 23, 2, False), # non-static RAM map
    "Chest - Bowser's Keep Rotating Platforms 1": MemoryLocation(treasure_chest_base_address + 22, 3, False), # non-static RAM map
    "Chest - Bowser's Keep Rotating Platforms 2": MemoryLocation(treasure_chest_base_address + 22, 6, False), # non-static RAM map
    "Chest - Bowser's Keep Rotating Platforms 3": MemoryLocation(treasure_chest_base_address + 22, 4, False), # non-static RAM map
    "Chest - Bowser's Keep Rotating Platforms 4": MemoryLocation(treasure_chest_base_address + 22, 7, False), # non-static RAM map
    "Chest - Bowser's Keep Rotating Platforms 5": MemoryLocation(treasure_chest_base_address + 22, 5, False), # non-static RAM map
    "Chest - Bowser's Keep Rotating Platforms 6": MemoryLocation(treasure_chest_base_address + 23, 0, False), # non-static RAM map
    "Chest - Bowser's Keep Door Reward 1": MemoryLocation(treasure_chest_base_address + 7, 4, False), # these chests aren't about the number on the door...
    "Chest - Bowser's Keep Door Reward 2": MemoryLocation(treasure_chest_base_address + 21, 7, False),
    "Chest - Bowser's Keep Door Reward 3": MemoryLocation(treasure_chest_base_address + 0, 0, False),  # map me, not obtainable unless you have door requirement set > 2 ?
    "Chest - Bowser's Keep Door Reward 4": MemoryLocation(treasure_chest_base_address + 0, 0, False),  # map me, not obtainable unless you have door requirement set > 3 ?
    "Chest - Bowser's Keep Door Reward 5": MemoryLocation(treasure_chest_base_address + 0, 0, False),  # map me, not obtainable unless you have door requirement set > 4 ?
    "Chest - Bowser's Keep Door Reward 6": MemoryLocation(treasure_chest_base_address + 0, 0, False),  # map me, not obtainable unless you have door requirement set = 6 ?
    "Chest - Factory Save Room": MemoryLocation(treasure_chest_base_address + 13, 1, False),
    "Chest - Factory Bolt Platforms": MemoryLocation(treasure_chest_base_address + 13, 2, False),
    "Chest - Factory Falling Axems": MemoryLocation(treasure_chest_base_address + 21, 2, False), # not obtainable due to chest re-position bug
    "Chest - Factory Treasure Pit 1": MemoryLocation(treasure_chest_base_address + 21, 5, False),
    "Chest - Factory Treasure Pit 2": MemoryLocation(treasure_chest_base_address + 21, 3, False),
    "Chest - Factory Conveyor Platforms 1": MemoryLocation(treasure_chest_base_address + 24, 2, False),
    "Chest - Factory Conveyor Platforms 2": MemoryLocation(treasure_chest_base_address + 24, 3, False),
    "Chest - Factory Behind Snakes 1": MemoryLocation(treasure_chest_base_address + 21, 4, False),
    "Chest - Factory Behind Snakes 2": MemoryLocation(treasure_chest_base_address + 21, 6, False),
    "Key Item - Mario's Bed (Dry Bones Flag)": MemoryLocation(base_memory_address + 0x2DC0, 4, False),
    "Key Item - Croco 1 (Rare Frog Coin)": MemoryLocation(base_memory_address + 0x304D, 3, True),
    "Key Item - Rare Frog Coin Reward (Cricket Pie)": MemoryLocation(base_memory_address + 0x3083, 4, True),
    "Key Item - Melody Bay Song 1 (Alto Card)": MemoryLocation(base_memory_address + 0x3051, 4, True),
    "Key Item - Melody Bay Song 2 (Tenor Card)": MemoryLocation(base_memory_address + 0x3054, 5, True),
    "Key Item - Melody Bay Song 3 (Soprano Card)": MemoryLocation(base_memory_address + 0x3054, 6, True),
    "Key Item - Rose Town Sign (Greaper Flag)": MemoryLocation(base_memory_address + 0x2D68, 2, False),
    "Key Item - Yo'ster Isle Goal (Big Boo Flag)": MemoryLocation(base_memory_address + 0x2D3A, 0, False),
    "Key Item - Croco 2 (Bambino Bomb)": MemoryLocation(base_memory_address + 0x3056, 5, True),
    "Key Item - Booster Tower Genealogy Hall (Elder Key)": MemoryLocation(base_memory_address + 0x3054, 0, True),
    "Key Item - Booster Tower Checkerboard Room (Room Key)": MemoryLocation(base_memory_address + 0x2DCB, 7, False),
    "Key Item - Knife Guy (Bright Card)": MemoryLocation(base_memory_address + 0x3099, 6, True),
    "Key Item - Seaside Town Key (Shed Key)": MemoryLocation(base_memory_address + 0x2E19, 3, False),
    "Key Item - Monstro Town Key (Temple Key)": MemoryLocation(base_memory_address + 0x2E1F, 6, False),
    "Key Item - Smilax (Seed)": MemoryLocation(base_memory_address + 0x2DF6, 1, True),
    "Key Item - Nimbus Land Guard (Castle Key 1)": MemoryLocation(base_memory_address + 0x305F, 6, True),
    "Key Item - Birdo (Castle Key 2)": MemoryLocation(base_memory_address + 0x305F, 5, True),
    "Key Item - Shy Away (Fertilizer)": MemoryLocation(base_memory_address + 0x2E6F, 5, False),
    "Event - Toad Rescue 1": MemoryLocation(base_memory_address + 0x3052, 4, True),
    "Event - Toad Rescue 2": MemoryLocation(base_memory_address + 0x3052, 5, True),
    "Event - Hammer Bros Reward": MemoryLocation(base_memory_address + 0x3052, 6, True),
    "Event - Wallet Guy 1": MemoryLocation(base_memory_address + 0x3083, 2, True),
    "Event - Wallet Guy 2": MemoryLocation(base_memory_address + 0x3083, 2, True),
    "Event - Mushroom Kingdom Store": MemoryLocation(base_memory_address + 0x3089, 6, True),
    "Event - Peach Surprise": MemoryLocation(base_memory_address + 0x3084, 4, True),
    "Event - Invasion Family": MemoryLocation(base_memory_address + 0x3082, 7, True),
    "Event - Invasion Guest Room": MemoryLocation(base_memory_address + 0x3083, 0, True),
    "Event - Invasion Guard": MemoryLocation(base_memory_address + 0x3082, 5, True),
    "Event - Croco 1 Reward": MemoryLocation(base_memory_address + 0x304D, 5, True),
    "Event - Pandorite Reward": MemoryLocation(base_memory_address + 0x3057, 5, True),
    "Event - Midas River First Time": MemoryLocation(base_memory_address + 0x3043, 1, True),
    "Event - Rose Town Toad": MemoryLocation(base_memory_address + 0x3084, 0, True),
    "Event - Gaz": MemoryLocation(base_memory_address + 0x3085, 7, True),
    "Event - Treasure Seller 1": MemoryLocation(base_memory_address + 0x3088, 1, True),
    "Event - Treasure Seller 2": MemoryLocation(base_memory_address + 0x3088, 0, True),
    "Event - Treasure Seller 3": MemoryLocation(base_memory_address + 0x3088, 2, True),
    "Event - Croco Flunkie 1": MemoryLocation(base_memory_address + 0x3057, 0, True),
    "Event - Croco Flunkie 2": MemoryLocation(base_memory_address + 0x3056, 7, True),
    "Event - Croco Flunkie 3": MemoryLocation(base_memory_address + 0x3056, 6, True),
    "Event - Booster Tower Railway": MemoryLocation(base_memory_address + 0x2DC6, 0, False),
    "Event - Booster Tower Chomp": MemoryLocation(base_memory_address + 0x2DCB, 7, False),
    "Event - Booster Tower Curtain Game": MemoryLocation(base_memory_address + 0x3053, 5, True),
    "Event - Seaside Town Rescue": MemoryLocation(base_memory_address + 0x3086, 6, True),
    "Event - Sunken Ship 3D Maze": MemoryLocation(base_memory_address + 0x307D, 2, True),
    "Event - Sunken Ship Cannonball Puzzle": MemoryLocation(base_memory_address + 0x307D, 4, True),
    "Event - Sunken Ship Hidon Reward": MemoryLocation(base_memory_address + 0x3057, 7, True),
    "Event - Belome Temple Treasure 1": MemoryLocation(base_memory_address + 0x2E67, 5, False),
    "Event - Belome Temple Treasure 2": MemoryLocation(base_memory_address + 0x2E67, 6, False),
    "Event - Belome Temple Treasure 3": MemoryLocation(base_memory_address + 0x2E67, 7, False),
    "Event - Jinx Dojo Reward": MemoryLocation(base_memory_address + 0x308A, 5, True),
    "Event - Culex Reward": MemoryLocation(base_memory_address + 0x3093, 4, True),
    "Event - Super Jumps 30": MemoryLocation(base_memory_address + 0x3092, 0, True),
    "Event - Super Jumps 100": MemoryLocation(base_memory_address + 0x3092, 2, True),
    "Event - Three Musty Fears": MemoryLocation(base_memory_address + 0x3089, 7, True),
    "Event - Troopa Climb": MemoryLocation(base_memory_address + 0x3094, 7, True),
    "Event - Dodo Reward": MemoryLocation(base_memory_address + 0x3093, 1, True),
    "Event - Nimbus Land Inn": MemoryLocation(base_memory_address + 0x3098, 6, True),
    "Event - Nimbus Land Prisoners": MemoryLocation(base_memory_address + 0x305F, 7, True),
    "Event - Nimbus Land Signal Ring": MemoryLocation(base_memory_address + 0x3084, 3, True),
    "Event - Nimbus Land Cellar": MemoryLocation(base_memory_address + 0x309F, 3, True),
    "Event - Factory Toad Gift": MemoryLocation(base_memory_address + 0x3059, 5, True),
    "Event - Goomba Thumping 1": MemoryLocation(base_memory_address + 0x3099, 4, True),
    "Event - Goomba Thumping 2": MemoryLocation(base_memory_address + 0x3099, 5, True),
    "Event - Cricket Pie Reward": MemoryLocation(base_memory_address + 0x3051, 2, True),
    "Event - Cricket Jam Reward": MemoryLocation(base_memory_address + 0x3051, 3, False),
    "Boss - Hammer Bros Spot": MemoryLocation(base_memory_address + 0x3052, 6, True),
    "Boss - Croco 1 Spot": MemoryLocation(base_memory_address + 0x304D, 3, True),
    "Boss - Mack Spot": MemoryLocation(base_memory_address + 0x3082, 0, True),
    "Boss - Pandorite Spot": MemoryLocation(base_memory_address + 0x3057, 5, True),
    "Boss - Belome 1 Spot": MemoryLocation(base_memory_address + 0x3055, 2, True),
    "Boss - Bowyer Spot": MemoryLocation(base_memory_address + 0x3083, 6, True),
    "Boss - Croco 2 Spot": MemoryLocation(base_memory_address + 0x3056, 5, True),
    "Boss - Punchinello Spot": MemoryLocation(base_memory_address + 0x3056, 3, True),
    "Boss - Booster Spot": MemoryLocation(base_memory_address + 0x3053, 4, True),
    "Boss - Knife Guy and Crate Guy Spot": MemoryLocation(base_memory_address + 0x3048, 6, True),
    "Boss - Bundt Spot": MemoryLocation(base_memory_address + 0x304C, 6, True),
    "Event - Star Hill Spot": MemoryLocation(base_memory_address + 0x2DAC, 7, True),
    "Boss - King Calamari Spot": MemoryLocation(base_memory_address + 0x3058, 6, True),
    "Boss - Hidon Spot": MemoryLocation(base_memory_address + 0x3057, 7, True),
    "Boss - Johnny Spot": MemoryLocation(base_memory_address + 0x3058, 7, True),
    "Boss - Yaridovich Spot": MemoryLocation(base_memory_address + 0x3086, 0, True),
    "Boss - Belome 2 Spot": MemoryLocation(base_memory_address + 0x307C, 5, True),
    "Boss - Jagger Spot": MemoryLocation(base_memory_address + 0x308A, 2, True),
    # "Jinx 1": MemoryLocation(base_memory_address + 0x308A, 3, True),
    # "Jinx 2": MemoryLocation(base_memory_address + 0x308A, 4, True),
    "Boss - Jinx 3 Spot": MemoryLocation(base_memory_address + 0x308A, 5, True),
    "Boss - Culex Spot": MemoryLocation(base_memory_address + 0x3093, 4, True),
    "Boss - Box Boy Spot": MemoryLocation(base_memory_address + 0x3064, 6, True),
    "Boss - Mega Smilax Spot": MemoryLocation(base_memory_address + 0x308C, 3, True),
    "Boss - Dodo Spot": MemoryLocation(base_memory_address + 0x3092, 7, True),
    "Boss - Birdo Spot": MemoryLocation(base_memory_address + 0x305F, 5, True),
    "Boss - Valentina Spot": MemoryLocation(base_memory_address + 0x304A, 2, True),
    "Boss - Czar Dragon Spot": MemoryLocation(base_memory_address + 0x307E, 0, True),
    "Boss - Axem Rangers Spot": MemoryLocation(base_memory_address + 0x307D, 7, True),
    "Boss - Magikoopa Spot": MemoryLocation(base_memory_address + 0x3093, 6, True),
    "Boss - Boomer Spot": MemoryLocation(base_memory_address + 0x3054, 2, True),
    "Boss - Exor Spot": MemoryLocation(base_memory_address + 0x3093, 7, True),
    "Boss - Countdown Spot": MemoryLocation(base_memory_address + 0x308F, 7, True),
    "Boss - Cloaker and Domino Spot": MemoryLocation(base_memory_address + 0x3096, 0, True),
    "Boss - Clerk Spot": MemoryLocation(base_memory_address + 0x3059, 4, True),
    "Boss - Manager Spot": MemoryLocation(base_memory_address + 0x3091, 3, True),
    "Boss - Director Spot": MemoryLocation(base_memory_address + 0x2E8E, 5, False),
    "Boss - Gunyolk Spot": MemoryLocation(base_memory_address + 0x308F, 6, True),
    "Boss - Smithy Spot": MemoryLocation(base_memory_address + 0x304A, 2, True),
})

min = 0xFFFFFFFF
max = 0
for location in location_data.keys():
    if location_data[location].address < min:
        min = location_data[location].address
    if location_data[location].address > max:
        max = location_data[location].address

item_data: Dict[str, ItemData] = {
    "Hammer": ItemData(0x05, ItemCategory.gear),
    "Froggie Stick": ItemData(0x06, ItemCategory.gear),
    "Nok Nok Shell": ItemData(0x07, ItemCategory.gear),
    "Punch Glove": ItemData(0x08, ItemCategory.gear),
    "Finger Shot": ItemData(0x09, ItemCategory.gear),
    "Cymbals": ItemData(0x0A, ItemCategory.gear),
    "Chomp": ItemData(0x0B, ItemCategory.gear),
    "Masher": ItemData(0x0C, ItemCategory.gear),
    "Chomp Shell": ItemData(0x0D, ItemCategory.gear),
    "Super Hammer": ItemData(0x0E, ItemCategory.gear),
    "Hand Gun": ItemData(0x0F, ItemCategory.gear),
    "Whomp Glove": ItemData(0x10, ItemCategory.gear),
    "Slap Glove": ItemData(0x11, ItemCategory.gear),
    "Troopa Shell": ItemData(0x12, ItemCategory.gear),
    "Parasol": ItemData(0x13, ItemCategory.gear),
    "Hurly Gloves": ItemData(0x14, ItemCategory.gear),
    "Double Punch": ItemData(0x15, ItemCategory.gear),
    "Ribbit Stick": ItemData(0x16, ItemCategory.gear),
    "Spiked Link": ItemData(0x17, ItemCategory.gear),
    "Mega Glove": ItemData(0x18, ItemCategory.gear),
    "War Fan": ItemData(0x19, ItemCategory.gear),
    "Hand Cannon": ItemData(0x1A, ItemCategory.gear),
    "Sticky Glove": ItemData(0x1B, ItemCategory.gear),
    "Ultra Hammer": ItemData(0x1C, ItemCategory.gear),
    "Super Slap": ItemData(0x1D, ItemCategory.gear),
    "Drill Claw": ItemData(0x1E, ItemCategory.gear),
    "Star Gun": ItemData(0x1F, ItemCategory.gear),
    "Sonic Cymbal": ItemData(0x20, ItemCategory.gear),
    "Lazy Shell Weapon": ItemData(0x21, ItemCategory.gear),
    "Frying Pan": ItemData(0x22, ItemCategory.gear),
    "Lucky Hammer": ItemData(0x23, ItemCategory.gear),
    "Shirt": ItemData(0x25, ItemCategory.gear),
    "Pants": ItemData(0x26, ItemCategory.gear),
    "Thick Shirt": ItemData(0x27, ItemCategory.gear),
    "Thick Pants": ItemData(0x28, ItemCategory.gear),
    "Mega Shirt": ItemData(0x29, ItemCategory.gear),
    "Mega Pants": ItemData(0x2A, ItemCategory.gear),
    "Work Pants": ItemData(0x2B, ItemCategory.gear),
    "Mega Cape": ItemData(0x2C, ItemCategory.gear),
    "Happy Shirt": ItemData(0x2D, ItemCategory.gear),
    "Happy Pants": ItemData(0x2E, ItemCategory.gear),
    "Happy Cape": ItemData(0x2F, ItemCategory.gear),
    "Happy Shell": ItemData(0x30, ItemCategory.gear),
    "Polka Dress": ItemData(0x31, ItemCategory.gear),
    "Sailor Shirt": ItemData(0x32, ItemCategory.gear),
    "Sailor Pants": ItemData(0x33, ItemCategory.gear),
    "Sailor Cape": ItemData(0x34, ItemCategory.gear),
    "Nautica Dress": ItemData(0x35, ItemCategory.gear),
    "Courage Shell": ItemData(0x36, ItemCategory.gear),
    "Fuzzy Shirt": ItemData(0x37, ItemCategory.gear),
    "Fuzzy Pants": ItemData(0x38, ItemCategory.gear),
    "Fuzzy Cape": ItemData(0x39, ItemCategory.gear),
    "Fuzzy Dress": ItemData(0x3A, ItemCategory.gear),
    "Fire Shirt": ItemData(0x3B, ItemCategory.gear),
    "Fire Pants": ItemData(0x3C, ItemCategory.gear),
    "Fire Cape": ItemData(0x3D, ItemCategory.gear),
    "Fire Shell": ItemData(0x3E, ItemCategory.gear),
    "Fire Dress": ItemData(0x3F, ItemCategory.gear),
    "Hero Shirt": ItemData(0x40, ItemCategory.gear),
    "Prince Pants": ItemData(0x41, ItemCategory.gear),
    "Star Cape": ItemData(0x42, ItemCategory.gear),
    "Heal Shell": ItemData(0x43, ItemCategory.gear),
    "Royal Dress": ItemData(0x44, ItemCategory.gear),
    "Super Suit": ItemData(0x45, ItemCategory.gear),
    "Lazy Shell Armor": ItemData(0x46, ItemCategory.gear),
    "Zoom Shoes": ItemData(0x4A, ItemCategory.gear),
    "Safety Badge": ItemData(0x4B, ItemCategory.gear),
    "Jump Shoes": ItemData(0x4C, ItemCategory.gear),
    "Safety Ring": ItemData(0x4D, ItemCategory.gear),
    "Amulet": ItemData(0x4E, ItemCategory.gear),
    "Scrooge Ring": ItemData(0x4F, ItemCategory.gear),
    "Exp Booster": ItemData(0x50, ItemCategory.gear),
    "Attack Scarf": ItemData(0x51, ItemCategory.gear),
    "Rare Scarf": ItemData(0x52, ItemCategory.gear),
    "B'tub Ring": ItemData(0x53, ItemCategory.gear),
    "Antidote Pin": ItemData(0x54, ItemCategory.gear),
    "Wake Up Pin": ItemData(0x55, ItemCategory.gear),
    "Fearless Pin": ItemData(0x56, ItemCategory.gear),
    "Trueform Pin": ItemData(0x57, ItemCategory.gear),
    "Coin Trick": ItemData(0x58, ItemCategory.gear),
    "Ghost Medal": ItemData(0x59, ItemCategory.gear),
    "Jinx Belt": ItemData(0x5A, ItemCategory.gear),
    "Feather": ItemData(0x5B, ItemCategory.gear),
    "Troopa Pin": ItemData(0x5C, ItemCategory.gear),
    "Signal Ring": ItemData(0x5D, ItemCategory.gear),
    "Quartz Charm": ItemData(0x5E, ItemCategory.gear),
    "Mushroom": ItemData(0x60, ItemCategory.item),
    "Mid Mushroom": ItemData(0x61, ItemCategory.item),
    "Max Mushroom": ItemData(0x62, ItemCategory.item),
    "Honey Syrup": ItemData(0x63, ItemCategory.item),
    "Maple Syrup": ItemData(0x64, ItemCategory.item),
    "Royal Syrup": ItemData(0x65, ItemCategory.item),
    "Pick Me Up": ItemData(0x66, ItemCategory.item),
    "Able Juice": ItemData(0x67, ItemCategory.item),
    "Bracer": ItemData(0x68, ItemCategory.item),
    "Energizer": ItemData(0x69, ItemCategory.item),
    "Yoshi Ade": ItemData(0x6A, ItemCategory.item),
    "Red Essence": ItemData(0x6B, ItemCategory.item),
    "Kerokero Cola": ItemData(0x6C, ItemCategory.item),
    "Yoshi Cookie": ItemData(0x6D, ItemCategory.item),
    "Pure Water": ItemData(0x6E, ItemCategory.item),
    "Sleepy Bomb": ItemData(0x6F, ItemCategory.item),
    "Bad Mushroom": ItemData(0x70, ItemCategory.item),
    "Fire Bomb": ItemData(0x71, ItemCategory.item),
    "Ice Bomb": ItemData(0x72, ItemCategory.item),
    "Flower Tab": ItemData(0x73, ItemCategory.item),
    "Flower Jar": ItemData(0x74, ItemCategory.item),
    "Flower Box": ItemData(0x75, ItemCategory.item),
    "Yoshi Candy": ItemData(0x76, ItemCategory.item),
    "Froggie Drink": ItemData(0x77, ItemCategory.item),
    "Muku Cookie": ItemData(0x78, ItemCategory.item),
    "Elixir": ItemData(0x79, ItemCategory.item),
    "Megalixir": ItemData(0x7A, ItemCategory.item),
    "See Ya": ItemData(0x7B, ItemCategory.item),
    "Temple Key": ItemData(0x7C, ItemCategory.key),
    "Goodie Bag": ItemData(0x7D, ItemCategory.item),
    "Earlier Times": ItemData(0x7E, ItemCategory.item),
    "Freshen Up": ItemData(0x7F, ItemCategory.item),
    "Rare Frog Coin": ItemData(0x80, ItemCategory.key),
    "Wallet": ItemData(0x81, ItemCategory.item),
    "Cricket Pie": ItemData(0x82, ItemCategory.key),
    "Rock Candy": ItemData(0x83, ItemCategory.item),
    "Castle Key 1": ItemData(0x84, ItemCategory.key),
    "Castle Key 2": ItemData(0x86, ItemCategory.key),
    "Bambino Bomb": ItemData(0x87, ItemCategory.key),
    "Sheep Attack": ItemData(0x88, ItemCategory.item),
    "Carbo Cookie": ItemData(0x89, ItemCategory.item),
    "Shiny Stone": ItemData(0x8A, ItemCategory.item),
    "Room Key": ItemData(0x8C, ItemCategory.key),
    "Elder Key": ItemData(0x8D, ItemCategory.key),
    "Shed Key": ItemData(0x8E, ItemCategory.key),
    "Lamb's Lure": ItemData(0x8F, ItemCategory.item),
    "Fright Bomb": ItemData(0x90, ItemCategory.item),
    "Mystery Egg": ItemData(0x91, ItemCategory.item),
    "Lucky Jewel": ItemData(0x94, ItemCategory.item),
    "Soprano Card": ItemData(0x96, ItemCategory.key),
    "Alto Card": ItemData(0x97, ItemCategory.key),
    "Tenor Card": ItemData(0x98, ItemCategory.key),
    "Crystalline": ItemData(0x99, ItemCategory.item),
    "Power Blast": ItemData(0x9A, ItemCategory.item),
    "Wilt Shroom": ItemData(0x9B, ItemCategory.item),
    "Rotten Mush": ItemData(0x9C, ItemCategory.item),
    "Moldy Mush": ItemData(0x9D, ItemCategory.item),
    "Seed": ItemData(0x9E, ItemCategory.key),
    "Fertilizer": ItemData(0x9F, ItemCategory.key),
    "Big Boo Flag": ItemData(0xA1, ItemCategory.key),
    "Dry Bones Flag": ItemData(0xA2, ItemCategory.key),
    "Greaper Flag": ItemData(0xA3, ItemCategory.key),
    "Cricket Jam": ItemData(0xA6, ItemCategory.key),
    "Bright Card": ItemData(0xAE, ItemCategory.key),
    "Mushroom 2": ItemData(0xAF, ItemCategory.item),
    "Star Egg": ItemData(0xB0, ItemCategory.item),
    "Five Coins": ItemData(5, ItemCategory.coin),
    "Eight Coins": ItemData(8, ItemCategory.coin),
    "Ten Coins": ItemData(10, ItemCategory.coin),
    "Fifty Coins": ItemData(50, ItemCategory.coin),
    "One Hundred Coins": ItemData(100, ItemCategory.coin),
    "One Hundred Fifty Coins": ItemData(150, ItemCategory.coin),
    "Frog Coin": ItemData(1, ItemCategory.frog_coin),
    "Flower": ItemData(1, ItemCategory.flower),
    "Recovery Mushroom": ItemData(0, ItemCategory.recovery),
    "You Missed!": ItemData(0, ItemCategory.coin) # Sends 0 coins as a temporary measure to prevent an SNI Disconnect if "You Missed!" ends up non-local
}


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(open(file_name, "rb").read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if md5_hash != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for NA (1.0) release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = options["smrpg_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.local_path(file_name)
    return file_name
