from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class BackpackBattlesArchipelagoOptions:
    pass


class BackpackBattlesGame(Game):
    ##############################
    ## Created by ManNamedGarbo ##
    ##############################

    name = "Backpack Battles"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = BackpackBattlesArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Craft RECIPE in a match",
                data={
                    "RECIPE": (self.rangerrecipe, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),              
            GameObjectiveTemplate(
                label="Craft RECIPE in a match",
                data={
                    "RECIPE": (self.reaperrecipe, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),               
            GameObjectiveTemplate(
                label="Craft RECIPE in a match",
                data={
                    "RECIPE": (self.berserkerrecipe, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),              
            GameObjectiveTemplate(
                label="Craft RECIPE in a match",
                data={
                    "RECIPE": (self.pyromancerrecipe, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),               
            GameObjectiveTemplate(
                label="Craft RECIPE in a match",
                data={
                    "RECIPE": (self.neutralrecipe, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=7,
            ),            
            GameObjectiveTemplate(
                label="Might Need a Loan for That - Purchase an item worth more 12 or more gold",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),            
            GameObjectiveTemplate(
                label="Empty Pockets - Spend gold until you reach 0 remaining in the shop",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),            
            GameObjectiveTemplate(
                label="Win a Ranked Match as CLASS",
                data={
                    "CLASS": (self.classes, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),           
            GameObjectiveTemplate(
                label="Win a Casual Match as CLASS",
                data={
                    "CLASS": (self.classes, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),           
            GameObjectiveTemplate(
                label="Deadly Ego - Enter Sudden Death and Win the Match",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),           
            GameObjectiveTemplate(
                label="Consistent Hoarder - Obtain 3 of a single bag type",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),           
            GameObjectiveTemplate(
                label="Rising Power - Gain RANDOMRANGE of any buff at the end of a round",
                data={
                    "RANDOMRANGE": (self.randomrange, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),           
            GameObjectiveTemplate(
                label="Woe Upon Ye - Inflict RANDOMRANGE of any debuff at the end of a round",
                data={
                    "RANDOMRANGE": (self.randomrange, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),                     
            GameObjectiveTemplate(
                label="You Call That a Fight? - Win a Round with at least 50% Health remaining",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ), 
            GameObjectiveTemplate(
                label="Not Even Close - Win a Round with less than 10% Health remaining",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),                
            GameObjectiveTemplate(
                label="I Can Do It Better! - Create any Class Recipe as an opposing class",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),           
            GameObjectiveTemplate(
                label="Suited Up - Wear at least a Helmet, Chest, Glove, and Boot item inside your backpack at once",
                data=dict(),
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="No Rest Allowed - Reach 3.0 Stamina Consumption in your backpack at once",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),           
            GameObjectiveTemplate(
                label="Truly Crafty - Have at least 3 unique crafted items in your backpack at once (Non-Potion)",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),           
            GameObjectiveTemplate(
                label="Alchemist - Have 4 unique potions in a potion's bag",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Weapons Master - Fill a Stamina Bag with 3 Unique Weapons",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),   
            GameObjectiveTemplate(
                label="Swift Battle - Defeat an enemy before Fatigue phase",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),   
            GameObjectiveTemplate(
                label="Jack of All Trades - Win a game as each Class",
                data=dict(),
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),   
            GameObjectiveTemplate(
                label="Tense Yet Alive - Survive Sudden Death with only one life remaining",
                data=dict(),
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),               
            GameObjectiveTemplate(
                label="Indomiatable - Survive Sudden Death without losing a round",
                data=dict(),
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),   
            GameObjectiveTemplate(
                label="I'm Just Better! - Win 10 rounds against the same class (Across any number of Matches)",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),   
            GameObjectiveTemplate(
                label="Doppelganger - Win 3 rounds against the someone using the same Starting bag (Across any number of Matches)",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),   
            GameObjectiveTemplate(
                label="Big Number Funny - Equip Just Stats and More Stats in the same Backpack",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ), 
            GameObjectiveTemplate(
                label="Not again... - With a maximum sized Backpack completely filled with items, Shuffle your Backpack", # I'm not sorry for this. You've know you've done it at least once before.
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),    
            GameObjectiveTemplate(
                label="Archaeologist - Have a Shovel dig up SMALLRANGE items total",
                data={
                    "SMALLRANGE": (self.smallrange, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),    
            GameObjectiveTemplate(
                label="Special Dig - Have a Shovel dig up an item of RARITY rarity",
                data={
                    "RARITY": (self.rarity, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),    
            GameObjectiveTemplate(
                label="Frugal Shopper - Have a Customer Card and Piggy Bank equipped for more than 3 rounds",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),    
            GameObjectiveTemplate(
                label="Artisan - Craft any two of the following recipes and equip them at the same time: RECIPES",
                data={
                    "RECIPES": (self.anyrecipe, 3)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),    
            GameObjectiveTemplate(
                label="Shiny! - Upgrade a GEMSTONE to a higher tier",
                data={
                    "GEMSTONE": (self.gemstones, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),    
            GameObjectiveTemplate(
                label="Fire Sale - Buy SMALLRANGE Items on Sale from the Shop across any amount of matches",
                data={
                    "SMALLRANGE": (self.smallrange, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),    
            GameObjectiveTemplate(
                label="There are some who call him... - As a Reaper, find Tim",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ), 
            GameObjectiveTemplate(
                label="As a Berserker, craft two of the following: RECIPES",
                data={
                    "RECIPES": (self.berserkerrecipe, 3)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="As a Reaper, craft two of the following: RECIPES",
                data={
                    "RECIPES": (self.reaperrecipe, 3)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="As a Pyromancer, craft two of the following: RECIPES",
                data={
                    "RECIPES": (self.pyromancerrecipe, 3)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="As a Ranger, craft two of the following: RECIPES",
                data={
                    "RECIPES": (self.rangerrecipe, 3)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Scared to Get Hurt? - Equip at least 5 Armor items in your Backpack at once",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Picky Assassin - Craft one of Each Dagger in a single match",
                data=dict(),
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Why... - Sell any Subclass Item",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Gamba! - Play a Match using the Random Class option",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Pandora's Bag - Play a Match as CLASS while using the Sack of Surprises option",
                data={
                    "CLASS": (self.classes, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),            
        ]   

    @staticmethod
    def randomrange() -> range:
        return range(1, 21)
        
    @staticmethod
    def smallrange() -> range:
        return range(1, 6)        

    @staticmethod
    def classes() -> List[str]:
        return [
            "Ranger",
            "Reaper",
            "Pyromancer",
            "Berserker",
        ]

    @staticmethod
    def rarity() -> List[str]:
        return [
            "Common",
            "Rare",
            "Epic",
            "Legendary",
            "Godly",
        ]

    @staticmethod
    def gemstones() -> List[str]:
        return [
            "Amethyst",
            "Emerald",
            "Topaz",
            "Ruby",
            "Sapphire",
        ]
                
    @staticmethod
    def neutralrecipe() -> List[str]:
        return [
            "Shovel",
            "Eggscalibur",
            "Pandamonium",
            "Magic Staff",
            "Claws of Attack",
            "Unlit Torch",
            "Burning Torch",
            "Magic Torch",
            "Poison Dagger",
            "Bloody Dagger",
            "Spectral Dagger",
            "Hero Sword",
            "Hero Longsword",
            "Falcon Blade",
            "Crossblades",
            "Manathirst",
            "Bloodthorne",
            "Darksaber",
            "Holy Spear",
            "Spiked Shield",
            "Moon Shield",
            "Moon Armor",
            "Gloves of Power",
            "Stone Armor",
            "Stone Helm",
            "Stone Shoes",
            "Vampiric Gloves",
            "Vampiric Armor",
            "Vampiric Potion",
            "Corrupted Armor",
            "Cap of Discomfort",
            "Bunch of Coins",
            "Burning Coal",
            "Platinum Customer Card",
            "Strong Health Potion",
            "Mana Potion",
            "Strong Stone Skin Potion",
            "Strong Heroic Potion",
            "Heart of Darkness",
            "Steel Goobert",
            "Blood Goobert",
            "Light Goobert",
            "King Goobert",
            "Box of Prosperity",
            "Shepherd's Crook",
            "King Crown",
            "Katana",
            "Shell Totem",
            "Thornbloom",
            "Stone Golem",
            "Prismatic Sword",
        ]

    @staticmethod
    def rangerrecipe() -> List[str]:
        return [
            "Critwood Staff",
            "Carrot Goobert",
            "Rat Chef ",
            "Squirrel Archer",
            "Tusk Piercer",
            "Belladona's Whisper",
            "Belladona's Shade",
            "Fortuna's Grace",
            "Fortuna's Hope",
            "Tusk Poker",
            "Lucky Piggy",
        ]
        
    @staticmethod
    def reaperrecipe() -> List[str]:
        return [
            "Staff Of Unhealing",
            "Poison Goobert",
            "Doom Cap",
            "Strong Vampiric Potion",
            "Strong Mana Potion",
            "Strong Divine Potion",
            "Strong Pestilence Flask",
            "Strong Demonic Flask",
            "Ruby Chonk",
            "Ice Dragon",
        ]
        
    @staticmethod
    def berserkerrecipe() -> List[str]:
        return [
            "Spiked Staff",
            "Cheese Goobert",
            "Busted Blade",
            "Chain Whip",
            "Armored Power Puppy",
            "Armored Courage Puppy",
            "Armored Wisdom Puppy",
            "Double Axe",
            "Dragonscale  Armor",
            "Dragonskin Boots",
            "Dragon Claws",
        ]        
        
    @staticmethod
    def pyromancerrecipe() -> List[str]:
        return [
            "Staff of Fire",
            "Chili Goobert",
            "Burning Sword",
            "Burning Blade",
            "Molten Spear",
            "Molten Dagger",
            "Sun Armor",
            "Sun Shield",
            "Flame Whip",
            "Obsidian Dragon",
        ]        

    @staticmethod
    def rainbowgoobert() -> List[str]:
        return [
            "Rainbow Goobert Deathslushy Mansquisher",
            "Rainbow Goobert Epicglob Uberviscous",
            "Rainbow Goobert Omegaooze Primeslime",
            "Rainbow Goobert MegaSludge Alphapuddle",
        ]
            
    def anyrecipe(self) -> List[str]:
        return sorted(
            self.rangerrecipe()
            + self.reaperrecipe()
            + self.berserkerrecipe()
            + self.pyromancerrecipe()
            + self.rainbowgoobert()
            + self.neutralrecipe()
        )


# Archipelago Options
# ...
