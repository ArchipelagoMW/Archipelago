from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class GTFOArchipelagoOptions:
    pass


class GTFOGame(Game):
    ################################################
    ## Created by ManNamedGarbo and TheBreadstick ##
    ################################################

    name = "GTFO"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = GTFOArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete EASYMISSION using only WEAPONCATEGORY",
                data={
                    "EASYMISSION": (self.easymissions, 1),
                    "WEAPONCATEGORY": (self.weaponcategories, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete HARDMISSION without letting your weapons reach 0%",
                data={
                    "HARDMISSION": (self.hardmissions, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Kill UNIQUESPECIAL using SPECIALWEAPON",
                data={
                    "UNIQUESPECIAL": (self.uniquespecials, 1),
                    "SPECIALWEAPON": (self.specialweapons, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Kill COMMONSPECIAL using MAINWEAPON",
                data={
                    "COMMONSPECIAL": (self.commonspecials, 1),
                    "MAINWEAPON": (self.mainweapons, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Use exclusively WEAPONCATEGORIES weapons to complete a mission",
                data={
                    "WEAPONCATEGORIES": (self.weaponcategories, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Encounter an Immortal",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Loot at least 2 ARTIFACTS artifacts in a single mission",
                data={
                    "ARTIFACTS": (self.artifactlevels, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Equip an ARTIFACTLEVEL with any one of the following traits ARTIFACTTRAITS",
                data={
                    "ARTIFACTLEVEL": (self.artifactlevels, 1),
                    "ARTIFACTTRAITS": (self.artifacttraits, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Use CONSUMABLES on a scout and survive the horde",
                data={
                    "CONSUMABLES": (self.consumables, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Kill a Scout using MELEEWEAPON",
                data={
                    "MELEEWEAPON": (self.meleeweapons, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Have TOOLS run completely out of charge then get it back up to 100% in a single mission",
                data={
                    "TOOLS": (self.tools, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Throw a rave to COMMONSPECIALS using the Long Range Flashlight",
                data={
                    "COMMONSPECIALS": (self.commonspecials, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Clear a bloody door horde using TOOLS",
                data={
                    "TOOLS": (self.tools, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete AMISSION using the following loadout: MAINWEAPON | SPECIALWEAPON | TOOL | MELEEWEAPON",
                data={
                    "AMISSION": (self.a_missions, 1),
                    "MAINWEAPON": (self.mainweapons, 1),
                    "SPECIALWEAPON": (self.specialweapons, 1),
                    "TOOL": (self.tools, 1),
                    "MELEEWEAPON": (self.meleeweapons, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Find and use up 2 of either CONSUMABLE inside CMISSION",
                data={
                    "CONSUMABLE": (self.consumables, 2),
                    "CMISSION": (self.c_missions, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Successfully clear EASYALARMCLASS with your flashlight off",
                data={
                    "EASYALARMCLASS": (self.easyalarmclass, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Successfully clear HARDALARMCLASS without closing any doors",
                data={
                    "HARDALARMCLASS": (self.hardalarmclass, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Clear out a ALARMTYPES without anyone going down",
                data={
                    "ALARMTYPES": (self.alarmtypes, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="For the duration of a EASYALARMCLASS, Communicate only through pings",
                data={
                    "EASYALARMCLASS": (self.easyalarmclass, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Land a 360 headshot on COMMONSPECIALS using a sniper",
                data={
                    "COMMONSPECIALS": (self.commonspecials, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete SECONDARYOBJECTIVES",
                data={
                    "SECONDARYOBJECTIVES": (self.secondaryobjectives, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete OVERLOADOBJECTIVES",
                data={
                    "OVERLOADOBJECTIVES": (self.overloadobjectives, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Take damage from Falling",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete any Prisoner Efficiency Objective",
                data=dict(),
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Reach Maximum Infection level",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="With a RANDOMARTIFACT Artifact equipped, complete any mission",
                data={
                    "RANDOMARTIFACT": (self.artifactlevels, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Enter the ??? Dimension",
                data=dict(),
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Immobilize COMMONSPECIALS using C-Foam",
                data={
                    "COMMONSPECIALS": (self.commonspecials, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete any level in under 30 minutes",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]    

    @staticmethod
    def a_missions() -> List[str]:
        return [
            "R1A1",
            "R2A1",  
            "R3A1",
            "R3A2",
            "R3A3",
            "R4A1",
            "R4A2",
            "R4A3", 
            "R5A1",
            "R6A1",
            "R6AX",
            "R7A1",
            "R8A1",
        ]

    @staticmethod
    def b_missions() -> List[str]:
        return [
            "R1B1",
            "R1B2",
            "R2B1",
            "R2B2",
            "R2B3",
            "R2B4",
            "R3B1",
            "R3B2",
            "R4B1",
            "R4B2",
            "R4B3",
            "R5B1",
            "R5B2",
            "R5B3",
            "R5B4",
            "R6B1",
            "R6B2",
            "R6B1",
            "R6B2",
            "R2BX",
            "R7B1",
            "R7B2",
            "R7B3",            
            "R8B1",
            "R8B2",
            "R8B3",
            "R8B4",            
        ]

    @staticmethod
    def c_missions() -> List[str]:
        return [
            "R1C1",
            "R1C2",
            "R2C1",
            "R2C2",
            "R3C1",
            "R4C1",
            "R4C2",
            "R4C3",
            "R5C1",
            "R5C2",
            "R5C3",
            "R6C1",
            "R6C2",
            "R6C3",
            "R6CX",
            "R7C1",
            "R7C2",
            "R7C3",
            "R7D1",
            "R7D2",
            "R2D1",
            "R2D2",
            "R3D1",            
        ]

    @staticmethod
    def d_missions() -> List[str]:
        return [
            "R1D1",
            "R4D1",
            "R4D2",
            "R3D1",
            "R4D1",
            "R4D2",
            "R5D1",
            "R5D2",
            "R6D1",
            "R6D2",
            "R6D3",
            "R6D4",
            "R7D1",
            "R7D2",
            "R8D1",
            "R8D2",
        ]

    @staticmethod
    def e_missions() -> List[str]:
        return [
            "R2E1",
            "R4E1",
            "R5E1",
            "R7E1",
            "R8E1",
            "R8E2",
        ]

    @staticmethod
    def altrundown1() -> List[str]:
        return [
            "R1A1",
            "R1B1",
            "R1B2",
            "R1C1",
            "R1C2",
            "R1D1",
        ]

    @staticmethod
    def altrundown2() -> List[str]:
        return [
            "R2A1",
            "R2B1",
            "R2B2",
            "R2B3",
            "R2B4",
            "R2C1",
            "R2C2",
            "R2D1",
            "R2D2",
            "R2E1",
        ]
        
    @staticmethod
    def altrundown3() -> List[str]:
        return [
            "R3A1",
            "R3A2",
            "R3A3",
            "R3B1",
            "R3B2",
            "R3C1",
            "R3D1",
        ]

    @staticmethod
    def altrundown4() -> List[str]:
        return [
            "R4A1",
            "R4A2",
            "R4A3",
            "R4B1",
            "R4B2",
            "R4B3",
            "R4C1",
            "R4C2",
            "R4C3",
            "R4D1",
            "R4D2",
            "R4E1",
        ]

    @staticmethod
    def altrundown5() -> List[str]:
        return [
            "R5A1",
            "R5A2",
            "R5A3",
            "R5B1",
            "R5B2",
            "R5B3",
            "R5B4",
            "R5C1",
            "R5C2",
            "R5C3",
            "R5D1",
            "R5D2",
            "R5E1",            
        ]

    @staticmethod
    def altrundown6() -> List[str]:
        return [
            "R6A1",
            "R6B1",
            "R6B2",
            "R6C1",
            "R6C2",
            "R6C3",
            "R6D1",
            "R6D2",
            "R6D3",
            "R6D4",
            "R6AX",
            "R6BX",
            "R6CX",            
        ] 

    @staticmethod
    def rundown7() -> List[str]:
        return [
            "R7A1",
            "R7B1",
            "R7B2",
            "R7B3",
            "R7C1",
            "R7C2",
            "R7C3",
            "R7D1",
            "R7D2",
            "R7E1",            
        ]

    @staticmethod
    def rundown8() -> List[str]:
        return [
            "R8A1",
            "R8A2",
            "R8B1",
            "R8B2",
            "R8B3",
            "R8B4",
            "R8C1",
            "R8C2",
            "R8D1",
            "R8D2",
            "R8E1",
            "R8E2",            
        ]

    @staticmethod
    def secondaryobjectives() -> List[str]:
        return [
            "ESTABLISH UPLINK Secondary Objective in R4A1",
            "RETRIEVE HSU Secondary Objective in R4A2",
            "GATHER ITEMS Secondary Objective in R4A3",
            "REACTOR STARTUP Secondary Objective in R4B1",
            "TERMINAL COMMAND Secondary Objective in R4B2",
            "RETRIEVE ITEM Secondary Objective in R4B3",
            "ESTABLISH UPLINK Secondary Objective in R4C1",
            "GATHER ITEMS Secondary Objective in R4C2",
            "ACTIVATE GENERATOR CLUSTER Secondary Objective in R4C3",
            "TERMINAL COMMAND Secondary Objective in R4D1",
            "ACTIVATE GENERATOR CLUSTER Secondary Objective in R4D2",
            "REACTOR STARTUP Secondary Objective in R4E1",
            "GATHER ITEMS Secondary Objective in R5A1",
            "TERMINAL COMMAND Secondary Objective in R5A2",
            "RETRIEVE HSU Secondary Objective in R5A3",
            "DISTRIBUTE POWERCELLS Secondary Objective in R5B1",
            "ESTABLISH UPLINK Secondary Objective in R5B2",
            "TERMINAL COMMAND Secondary Objective in R5B3",
            "ESTABLISH UPLINK Secondary Objective in R5C1",
            "REACTOR STARTUP Secondary Objective in R5C2",
            "PROCESS ITEM Secondary Objective in R5C3",
            "TERMINAL COMMAND Secondary Objective in R5D1",
            "ESTABLISH UPLINK Secondary Objective in R6B2",
            "SURVIVE WARDEN PROTOCOL Secondary Objective in R6BX",
            "RETRIEVE ITEM Secondary Objective in R6C2",
            "ACTIVATE GENERATOR CLUSTER Secondary Objective in R6C3",
            "GATHER ITEMS Secondary Objective in R6D2",
            "GATHER ITEMS Secondary Objective in R7B2",
            "GATHER ITEMS Secondary Objective in R7B3",
            "TERMINAL COMMAND Secondary Objective in R7C2",
            "TERMINAL COMMAND Secondary Objective in R7C3",
            "TERMINAL COMMAND Secondary Objective in R7D1",
            "GATHER ITEMS Secondary Objective in R8B1",
            "GATHER ITEMS Secondary Objective in R8B3",
            "TERMINAL COMMAND Secondary Objective in R8C1",
            "TERMINAL COMMAND Secondary Objective in R8E1",
            "REACTOR STARTUP Secondary Objective in R8E2",
        ]
        
    @staticmethod
    def overloadobjectives() -> List[str]:
        return [
            "TERMINAL COMMAND Overload Objective in R4A2",
            "TERMINAL COMMAND Overload Objective in R4A3",
            "GATHER ITEMS Overload Objective in R4B2",
            "TERMINAL COMMAND Overload Objective in R4B3",
            "RETRIEVE ITEM Overload Objective in R4C2",
            "RETRIEVE HSU Overload Objective in R4C3",
            "RETRIEVE ITEM Overload Objective in R4D2",
            "GATHER ITEMS Overload Objective in R5A2",
            "ACTIVATE GENERATOR CLUSTER Overload Objective in R5A3",
            "REACTOR STARTUP Overload Objective in R5B1",
            "GATHER ITEMS Overload Objective in R5B2",
            "TERMINAL COMMAND Overload Objective in R5C2",
            "TERMINAL COMMAND Overload Objective in R6C3",
            "REACTOR SHUTDOWN Overload Objective in R6D3",
            "RETRIEVE ITEM Overload Objective in R7B3",
            "GATHER ITEMS Overload Objective in R7C2",
            "EXTERNAL UPLINK Overload Objective in R7C3",
            "TERMINAL COMMAND Overload Objective in R7D1",
            "TIMED SEQUENCE Overload Objective in R8C1",
        ]        
        
    @staticmethod
    def weaponcategories() -> List[str]:
        return [
            "Single fire",
            "Burst",
            "Two-Tap",
            "Charge Up",
            "Full Auto",
            "Thermal Scope",
            "Pump Action",
        ]

    @staticmethod
    def consumables() -> List[str]:
        return [
            "Ammunition Pack",
            "Medical Pack",
            "Tool Refill Pack",
            "Disinfection Pack",
            "Fog Repeller",
            "C-Foam Grenade",
            "Lock Melter",
            "Glow Sticks",
            "Syringe",
            "Explosive Tripmine",
            "C-Foam Tripmine",
        ]

    @staticmethod
    def artifactlevels() -> List[str]:
        return [
            "Muted",
            "Bold",
            "Aggressive",
        ]

    @staticmethod
    def mainweapons() -> List[str]:
        return [
            "Pistol",
            "Burst Pistol",
            "HEL Revolver",
            "Machine Pistol",
            "HEL Autopistol",
            "Bullpup Rifle",
            "SMG",
            "PDW",
            "Heavy SMG",
            "Carbine",
            "DMR",
            "Double Tap Rifle",
            "Assault Rifle",
            "Burst Rifle",
            "Rifle",
            "Sawed-off Shotgun",
            "Hel Shotgun",
            "Slug Shotgun",
        ]

    @staticmethod
    def specialweapons() -> List[str]:
        return [
            "Heavy Assault Rifle",
            "Short Rifle",
            "Shotgun ",
            "Combat Shotgun",
            "Scattergun",
            "Choke Mod Shotgun",
            "Revolver",
            "Machine Gun V",
            "Machine Gun XII",
            "Burst Cannon",
            "Hel Gun",
            "High Cal Pistol",
            "Precision Rifle",
            "Sniper",
            "HEL Rifle",
        ]

    @staticmethod
    def meleeweapons() -> List[str]:
        return [
            "Sledgehammer",
            "Knife",
            "Bat",
            "Spear",
        ]

    @staticmethod
    def tools() -> List[str]:
        return [
            "Burst Sentry",
            "Shotgun Sentry",
            "Sniper Sentry",
            "HEL Auto Sentry",
            "C-Foam Launcher",
            "Mine Deployer",
        ]

    @staticmethod
    def nonconsumabletools() -> List[str]:
        return [
            "Long Range Flashlight",
            "Bio Tracker",
        ]

    @staticmethod
    def commonspecials() -> List[str]:
        return [
            "Scout",
            "Giant",
            "Big Shooter",
            "Hybrid",
        ]

    @staticmethod
    def uniquespecials() -> List[str]:
        return [
            "Big Charger",
            "Charger Scout",
            "Big Shadow",
            "Shadow Scout",
            "Snatcher",
        ]

    @staticmethod
    def alarmtypes() -> List[str]:
        return [
            "Error Alarm",
            "Diminished Alarm",
            "Surge Alarm",
            "S Scan",
            "Cluster Scan",
            "T Scan",
        ]

    @staticmethod
    def easyalarmclass() -> List[str]:
        return [
            "Class II",
            "Class III",
            "Class IV",
        ]

    @staticmethod
    def hardalarmclass() -> List[str]:
        return [
            "Class V",
            "Class VI",
            "Class VII",
            "Class VIII",
        ]

    @staticmethod
    def artifacttraits() -> List[str]:
        return [
            "Regen Speed",
            "Melee Resist",
            "Projectile Resist",
            "Rev.Speed",
            "Med Efficiency",
            "Supply Efficiency",
            "Infection Resist",
            "Main Ammo",
            "Special Ammo",
            "Tool Ammo",
            "Regen Cap",
            "C-Foam Portion",
            "Sentry CPU Speed",
            "Sentry Damage",
            "SR Sentry Damage",
            "Trip Mine Damage",
            "Glow Stick Power",
            "Fog Rep.Power",
            "Tracker CPU Speed",
            "Hacking Skill",
            "Bioscan Speed",
            "Condition: Human Proximity",
            "Condition: Below 50 % Health",
            "Condition: Is Close to Enemy",
            "Condition: Enemy Distant",
        ]

    def allalarmclass(self) -> List[str]:
        return sorted(
            self.easyalarmclass()
            + self.hardalarmclass()
        )

    def alltools(self) -> List[str]:
        return sorted(
            self.tools()
            + self.nonconsumabletools()
        )

    def rundowns(self) -> List[str]:
        return sorted(
            self.a_missions()
            + self.b_missions()
            + self.c_missions()
            + self.d_missions()
            + self.e_missions()
        )

    def missionranks(self) -> List[str]:
        return sorted(
            self.altrundown1()
            + self.altrundown2()
            + self.altrundown3()
            + self.altrundown4()
            + self.altrundown5()
            + self.altrundown6()
            + self.rundown7()
            + self.rundown8()
        )

    def easymissions(self) -> List[str]:
        return sorted(
            self.a_missions()
            + self.b_missions()
        )

    def hardmissions(self) -> List[str]:
        return sorted(
            self.c_missions()
            + self.d_missions()
            + self.e_missions()
        )


# Archipelago Options
## Future: Include Bosses?
## Future: Include Painful?
