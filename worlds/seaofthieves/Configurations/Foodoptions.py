import typing
from dataclasses import dataclass

import Options
from Options import Choice
from Options import PerGameCommonOptions, Range
from Options import DefaultOnToggle, TextChoice

DefaultOffToggle = Options.Toggle


class ChoiceForEach(Choice):
    option_Off = 0
    option_On = 1
    option_On_For_Each = 2


class ChoiceForEachSpecies(ChoiceForEach):
    option_Species_Sanity = 3


class MunchSanityFruit(ChoiceForEach):
    """If shuffle EAT, removes on eat fruit check, adds a check on each fruit"""
    display_name = "(EAT) Fruit"


class MunchSanityFish(ChoiceForEachSpecies):
    """If shuffle EAT, removes on eat fish check, adds a check on each type of fish"""
    display_name = "(EAT) Fish"


class MunchSanitySeamonster(ChoiceForEach):
    """If shuffle EAT, removes on eat seamonster check, adds a check on each seamonster"""
    display_name = "(EAT) Seamonster"


class MunchSanityLandAnimal(ChoiceForEach):
    """If shuffle EAT, removes on eat land animal check, adds a check on each land animal"""
    display_name = "(EAT) Animal"


class MunchSanityBug(ChoiceForEach):
    """If shuffle EAT, removes on eat Bug check, adds a check on each Bug"""
    display_name = "(EAT) Bug"


class CookSanityFish(ChoiceForEachSpecies):
    """If shuffle COOK, removes on cook fish check, adds a check on each fish"""
    display_name = "(COOK) Fish"


class CookSanitySeamonster(ChoiceForEach):
    """If shuffle COOK, removes on cook fish check, adds a check on each type of fish"""
    display_name = "(COOK) Seamonster"


class CookSanityLandAnimal(ChoiceForEach):
    """If shuffle COOK, removes on cook land animal check, adds a check on each land animal"""
    display_name = "(COOK) Animal"


class BurnSanityFish(ChoiceForEachSpecies):
    """If shuffle Burn, removes on Burn fish check, adds a check on each fish"""
    display_name = "(BURN) Fish"


class BurnSanitySeamonster(ChoiceForEach):
    """If shuffle Burn, removes on Burn fish check, adds a check on each type of fish"""
    display_name = "(BURN) Seamonster"


class BurnSanityLandAnimal(ChoiceForEach):
    """If shuffle Burn, removes on Burn land animal check, adds a check on each land animal"""
    display_name = "(BURN) land animal"
