from BaseClasses import Location, MultiWorld
from . import Options
import re

class DLCquestLocation(Location):
    game: str = "DLCquest"

offset = 120_000

location_table ={
        "Movement Pack": offset + 0,
        "Animation Pack": offset + 1,
        "Audio Pack": offset + 2,
        "Pause Menu Pack": offset + 3,
        "Time is Money Pack": offset + 4,
        "Double Jump Pack": offset + 5,
        "Pet Pack": offset + 6,
        "Sexy Outfits Pack": offset + 7,
        "Top Hat Pack": offset + 8,
        "Map Pack": offset + 9,
        "Gun Pack": offset + 10,
        "The Zombie Pack": offset + 11,
        "Night Map Pack": offset + 12,
        "Psychological Warfare Pack": offset + 13,
        "Armor for your Horse Pack": offset + 14,
        "Finish the Fight Pack": offset + 15,
        "Particles Pack": offset + 16,
        "Day One Patch Pack": offset + 17,
        "Checkpoint Pack": offset + 18,
        "Incredibly Important Pack": offset + 19,
        "Wall Jump Pack": offset + 20,
        "Health Bar Pack": offset + 21,
        "Parallax Pack": offset + 22,
        "Harmless Plants Pack": offset + 23,
        "Death of Comedy Pack": offset + 24,
        "Canadian Dialog Pack": offset + 25,
        "DLC NPC Pack": offset + 26,
        "Cut Content Pack": offset + 27,
        "Name Change Pack": offset + 28,
        "Season Pass": offset + 29,
        "High Definition Next Gen Pack": offset + 30,
        "Increased HP Pack": offset + 31,
        "Remove Ads Pack": offset + 32,
        "Big Sword Pack": offset + 33,
        "Really Big Sword Pack": offset + 34,
        "Unfathomable Sword Pack": offset + 35,
        "Pickaxe": offset + 36,
        "Gun": offset + 37,
        "DLC Quest Sword": offset + 38,
        "Live Freemium or Die Sword": offset + 39,
        "Box of Various Supplies": offset + 40,
        "Humble Indie Bindle": offset + 41,

}

for i in range(825):
        item_coin = "DLC Quest: number Coin"
        item_coin_loc = re.sub("number", str(i+1), item_coin)
        location_table.update({item_coin_loc: offset + 42 +i})

for i in range(889):
        item_coin_freemium = "Live Freemium or Die: number Coin"
        item_coin_loc_freemium = re.sub("number", str(i+1), item_coin_freemium)
        location_table.update({item_coin_loc_freemium: offset + 825 +42 + i})

