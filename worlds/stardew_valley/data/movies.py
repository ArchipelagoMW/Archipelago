from typing import List

from ..strings.season_names import Season
from ..strings.villager_names import NPC

movies_by_name = dict()
snacks_by_name = dict()
npc_snacks = dict()


def movie(movie_name: str, season: str, loving_npcs: List[str]):
    movie = Movie(movie_name, season, loving_npcs)
    movies_by_name[movie_name] = movie
    return movie


def snack(snack_name: str, category: str, loving_npcs: List[str]):
    snack = Snack(snack_name, category, loving_npcs)
    snacks_by_name[snack_name] = snack
    for npc in loving_npcs:
        if npc not in npc_snacks:
            npc_snacks[npc] = []
        npc_snacks[npc].append(snack)
    return snack


class Movie:
    name: str
    season: str
    loving_npcs: List[str]

    def __init__(self, name: str, season: str, loving_npcs: List[str]):
        self.name = name
        self.season = season
        self.loving_npcs = loving_npcs


class Snack:
    name: str
    category: str
    loving_npcs: List[str]

    def __init__(self, name: str, category: str, loving_npcs: List[str]):
        self.name = name
        self.category = category
        self.loving_npcs = loving_npcs


class MovieName:
    brave_sapling = movie("The Brave Little Sapling", Season.spring, [NPC.caroline, NPC.dwarf, NPC.jas, NPC.penny, NPC.sandy, NPC.vincent])
    prairie_king = movie("Journey Of The Prairie King: The Motion Picture", Season.summer, [NPC.caroline, NPC.dwarf, NPC.jas, NPC.robin, NPC.sandy, NPC.vincent])
    mysterium = movie("Mysterium", Season.fall, [NPC.abigail, NPC.dwarf, NPC.elliott, NPC.leah, NPC.sandy, NPC.sebastian, NPC.wizard])
    miracle_coldstar_ranch = movie("The Miracle At Coldstar Ranch", Season.winter, [NPC.dwarf, NPC.emily, NPC.evelyn, NPC.gus, NPC.harvey, NPC.marnie, NPC.sandy])
    natural_wonders = movie("Natural Wonders: Exploring Our Vibrant World", Season.spring, [NPC.demetrius, NPC.dwarf, NPC.jas, NPC.leo, NPC.lewis, NPC.maru, NPC.sandy])
    wumbus = movie("Wumbus", Season.summer, [NPC.alex, NPC.demetrius, NPC.dwarf, NPC.gus, NPC.jas, NPC.maru, NPC.pierre, NPC.sam, NPC.sandy, NPC.shane, NPC.vincent])
    howls_in_rain = movie("It Howls In The Rain", Season.fall, [NPC.abigail, NPC.alex, NPC.dwarf, NPC.sandy, NPC.sebastian, NPC.shane])
    zuzu_city_express = movie("The Zuzu City Express", Season.winter, [NPC.dwarf, NPC.evelyn, NPC.george, NPC.harvey, NPC.jodi, NPC.sandy])


class SnackCategory:
    salty = "Movie Salty Snacks"
    sweet = "Movie Sweet Snacks"
    drinks = "Movie Drinks"
    meals = "Movie Meals"


class SnackName:
    apple_slices = snack("Apple Slices", SnackCategory.sweet, [NPC.harvey])
    black_licorice = snack("Black Licorice", SnackCategory.sweet, [NPC.george, NPC.krobus, NPC.wizard])
    cappuccino_mousse_cake = snack("Cappuccino Mousse Cake", SnackCategory.sweet, [NPC.elliott, NPC.evelyn, NPC.gus, NPC.haley])
    chocolate_popcorn = snack("Chocolate Popcorn", SnackCategory.sweet, [NPC.jodi])
    cotton_candy = snack("Cotton Candy", SnackCategory.sweet, [NPC.penny, NPC.sandy])
    fries = snack("Fries", SnackCategory.salty, [NPC.clint])
    hummus_snack_pack = snack("Hummus Snack Pack", SnackCategory.salty, [NPC.shane])
    ice_cream_sandwich = snack("Ice Cream Sandwich", SnackCategory.sweet, [NPC.marnie])
    jasmine_tea = snack("Jasmine Tea", SnackCategory.drinks, [NPC.caroline, NPC.harvey, NPC.lewis, NPC.sebastian])
    jawbreaker = snack("Jawbreaker", SnackCategory.sweet, [NPC.vincent])
    joja_cola = snack("Joja Cola", SnackCategory.drinks, [NPC.shane])
    jojacorn = snack("JojaCorn", SnackCategory.salty, [NPC.shane])
    kale_smoothie = snack("Kale Smoothie", SnackCategory.drinks, [NPC.emily])
    nachos = snack("Nachos", SnackCategory.meals, [NPC.pam, NPC.shane])
    panzanella_salad = snack("Panzanella Salad", SnackCategory.meals, [NPC.gus, NPC.leah])
    personal_pizza = snack("Personal Pizza", SnackCategory.meals, [NPC.pierre, NPC.sam, NPC.shane])
    popcorn = snack("Popcorn", SnackCategory.salty, [NPC.demetrius, NPC.kent])
    rock_candy = snack("Rock Candy", SnackCategory.sweet, [NPC.abigail, NPC.dwarf])
    salmon_burger = snack("Salmon Burger", SnackCategory.meals, [NPC.alex, NPC.linus, NPC.willy])
    salted_peanuts = snack("Salted Peanuts", SnackCategory.salty, [NPC.robin])
    sour_slimes = snack("Sour Slimes", SnackCategory.sweet, [NPC.jas])
    star_cookie = snack("Star Cookie", SnackCategory.sweet, [NPC.evelyn, NPC.maru, NPC.wizard])
    stardrop_sorbet = snack("Stardrop Sorbet", SnackCategory.sweet, [NPC.alex, NPC.harvey, NPC.sam, NPC.sebastian, NPC.shane, NPC.abigail, NPC.emily, NPC.haley,
                                                NPC.leah, NPC.maru, NPC.penny, NPC.caroline, NPC.clint, NPC.demetrius, NPC.dwarf, NPC.evelyn,
                                                NPC.george, NPC.gus, NPC.jas, NPC.jodi, NPC.kent, NPC.lewis, NPC.linus, NPC.marnie, NPC.pam,
                                                NPC.pierre, NPC.robin, NPC.sandy, NPC.vincent, NPC.willy, NPC.wizard])
    truffle_popcorn = snack("Truffle Popcorn", SnackCategory.salty, [NPC.caroline, NPC.elliott, NPC.gus])


# For some unknown reason, Leo doesn't love ANY snack
npc_snacks[NPC.leo] = []

