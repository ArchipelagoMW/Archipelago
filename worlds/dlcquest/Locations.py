from BaseClasses import Location


class DLCQuestLocation(Location):
    game: str = "DLCQuest"


offset = 120_000

location_table = {
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
    "Sword": offset + 38,
    "Wooden Sword": offset + 39,
    "Box of Various Supplies": offset + 40,
    "Humble Indie Bindle": offset + 41,
    "Double Jump Alcove Sheep": offset + 42,
    "Double Jump Floating Sheep": offset + 43,
    "Sexy Outfits Sheep": offset + 44,
    "Forest High Sheep": offset + 45,
    "Forest Low Sheep": offset + 46,
    "Between Trees Sheep": offset + 47,
    "Hole in the Wall Sheep": offset + 48,
    "Shepherd Sheep": offset + 49,
    "Top Hat Sheep": offset + 50,
    "North West Ceiling Sheep": offset + 51,
    "North West Alcove Sheep": offset + 52,
    "West Cave Sheep": offset + 53,
    "Cutscene Sheep": offset + 54,
    "Not Exactly Noble": offset + 55,
    "Story is Important": offset + 56,
    "Nice Try": offset + 57,
    "I Get That Reference!": offset + 58,
}

for i in range(1, 826):
    item_coin = f"DLC Quest: {i} Coin"
    location_table[item_coin] = offset + 58 + i

for i in range(1, 890):
    item_coin_freemium = f"Live Freemium or Die: {i} Coin"
    location_table[item_coin_freemium] = offset + 825 + 58 + i
