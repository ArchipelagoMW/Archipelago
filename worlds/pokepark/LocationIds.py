from enum import Enum

from worlds.pokepark import BERRIES, FRIENDSHIP_ITEMS, POWERS


class MinigameLocationIds(Enum):
    # Bulbasaur's Daring Dash
    PIKACHU_DASH = BERRIES["100 Berries"] + 1
    TURTWIG_DASH = BERRIES["100 Berries"] + 2
    MUNCHLAX_DASH = BERRIES["100 Berries"] + 3
    CHIMCHAR_DASH = BERRIES["100 Berries"] + 4
    TREECKO_DASH = BERRIES["100 Berries"] + 5
    BIBAREL_DASH = BERRIES["100 Berries"] + 6
    BULBASAUR_DASH = BERRIES["100 Berries"] + 7
    BIDOOF_DASH = BERRIES["100 Berries"] + 8
    ODDISH_DASH = BERRIES["100 Berries"] + 9
    SHROOMISH_DASH = BERRIES["100 Berries"] + 10
    BONSLY_DASH = BERRIES["100 Berries"] + 11
    LOTAD_DASH = BERRIES["100 Berries"] + 12
    WEEDLE_DASH = BERRIES["100 Berries"] + 13
    CATERPIE_DASH = BERRIES["100 Berries"] + 14
    MAGIKARP_DASH = BERRIES["100 Berries"] + 15
    JOLTEON_DASH = BERRIES["100 Berries"] + 16  # Not implemented
    ARCANINE_DASH = BERRIES["100 Berries"] + 17  # Not implemented
    LEAFEON_DASH = BERRIES["100 Berries"] + 18
    SCYTHER_DASH = BERRIES["100 Berries"] + 19
    PONYTA_DASH = BERRIES["100 Berries"] + 20  # Not implemented
    SHINX_DASH = BERRIES["100 Berries"] + 21
    EEVEE_DASH = BERRIES["100 Berries"] + 22  # Not implemented
    PACHIRISU_DASH = BERRIES["100 Berries"] + 23
    BUNEARY_DASH = BERRIES["100 Berries"] + 24
    CROAGUNK_DASH = BERRIES["100 Berries"] + 25

    # Venusaur's Vine Swing
    PIKACHU_VINE_SWING = BERRIES["100 Berries"] + 26
    MUNCHLAX_VINE_SWING = BERRIES["100 Berries"] + 27
    MAGIKARP_VINE_SWING = BERRIES["100 Berries"] + 28
    BLAZIKEN_VINE_SWING = BERRIES["100 Berries"] + 29  # Not implemented
    INFERNAPE_VINE_SWING = BERRIES["100 Berries"] + 30  # Not implemented
    LUCARIO_VINE_SWING = BERRIES["100 Berries"] + 31  # Not implemented
    PRIMEAPE_VINE_SWING = BERRIES["100 Berries"] + 32  # Not implemented
    TANGROWTH_VINE_SWING = BERRIES["100 Berries"] + 33  # Not implemented
    AMBIPOM_VINE_SWING = BERRIES["100 Berries"] + 34
    CROAGUNK_VINE_SWING = BERRIES["100 Berries"] + 35
    MANKEY_VINE_SWING = BERRIES["100 Berries"] + 36
    AIPOM_VINE_SWING = BERRIES["100 Berries"] + 37
    CHIMCHAR_VINE_SWING = BERRIES["100 Berries"] + 38
    TREECKO_VINE_SWING = BERRIES["100 Berries"] + 39
    PACHIRISU_VINE_SWING = BERRIES["100 Berries"] + 40

    # Pelipper's Circle Circuit
    PIKACHU_CIRCLE = BERRIES["100 Berries"] + 41
    STARAPTOR_CIRCLE = BERRIES["100 Berries"] + 42  # Not implemented
    TOGEKISS_CIRCLE = BERRIES["100 Berries"] + 43  # Not implemented
    HONCHKROW_CIRCLE = BERRIES["100 Berries"] + 44  # Not implemented
    GLISCOR_CIRCLE = BERRIES["100 Berries"] + 45  # Not implemented
    PELIPPER_CIRCLE = BERRIES["100 Berries"] + 46
    STARAVIA_CIRCLE = BERRIES["100 Berries"] + 47
    PIDGEOTTO_CIRCLE = BERRIES["100 Berries"] + 48
    BUTTERFREE_CIRCLE = BERRIES["100 Berries"] + 49
    TROPIUS_CIRCLE = BERRIES["100 Berries"] + 50
    MURKROW_CIRCLE = BERRIES["100 Berries"] + 51  # Not implemented
    TAILLOW_CIRCLE = BERRIES["100 Berries"] + 52
    SPEAROW_CIRCLE = BERRIES["100 Berries"] + 53
    STARLY_CIRCLE = BERRIES["100 Berries"] + 54
    WINGULL_CIRCLE = BERRIES["100 Berries"] + 55

    # Gyarados' Aqua Dash
    PIKACHU_AQUA = BERRIES["100 Berries"] + 56
    PSYDUCK_AQUA = BERRIES["100 Berries"] + 57
    AZURILL_AQUA = BERRIES["100 Berries"] + 58
    SLOWPOKE_AQUA = BERRIES["100 Berries"] + 59
    EMPOLEON_AQUA = BERRIES["100 Berries"] + 60  # Not implemented
    FLOATZEL_AQUA = BERRIES["100 Berries"] + 61
    FERALIGATR_AQUA = BERRIES["100 Berries"] + 62
    GOLDUCK_AQUA = BERRIES["100 Berries"] + 63
    VAPOREON_AQUA = BERRIES["100 Berries"] + 64
    PRINPLUP_AQUA = BERRIES["100 Berries"] + 65  # Not implemented
    BIBAREL_AQUA = BERRIES["100 Berries"] + 66
    BUIZEL_AQUA = BERRIES["100 Berries"] + 67
    CORSOLA_AQUA = BERRIES["100 Berries"] + 68
    PIPLUP_AQUA = BERRIES["100 Berries"] + 69
    LOTAD_AQUA = BERRIES["100 Berries"] + 70

    #Empoleon's Snow Slide
    PIKACHU_SLIDE = BERRIES["100 Berries"]+71
    TEDDIURSA_SLIDE = BERRIES["100 Berries"]+72
    MAGIKARP_SLIDE = BERRIES["100 Berries"]+73
    EMPOLEON_SLIDE = BERRIES["100 Berries"]+74
    GLACEON_SLIDE = BERRIES["100 Berries"]+ 75
    BLASTOISE_SLIDE = BERRIES["100 Berries"]+ 76
    GLALIE_SLIDE = BERRIES["100 Berries"]+77
    LAPRAS_SLIDE = BERRIES["100 Berries"]+78
    DELIBIRD_SLIDE = BERRIES["100 Berries"] + 79
    PILOSWINE_SLIDE = BERRIES["100 Berries"]+ 80
    PRINPLUP_SLIDE = BERRIES["100 Berries"]+ 81
    SQUIRTLE_SLIDE = BERRIES["100 Berries"]+ 82
    PIPLUP_SLIDE = BERRIES["100 Berries"]+ 83
    QUAGSIRE_SLIDE = BERRIES["100 Berries"]+ 84
    SPHEAL_SLIDE = BERRIES["100 Berries"]+ 85

class OverworldPokemonLocationIds(Enum):
    STARLY_BEACH = FRIENDSHIP_ITEMS["Starly"] +1000
    KRABBY_ICE = FRIENDSHIP_ITEMS["Krabby"] +1000
    CORPHISH_ICE = FRIENDSHIP_ITEMS["Corphish"] +1000
    MUDKIP_ICE = FRIENDSHIP_ITEMS["Mudkip"] +1000
    TAILLOW_ICE = FRIENDSHIP_ITEMS["Taillow"] +1000
    STARAVIA_ICE = FRIENDSHIP_ITEMS["Staravia"] +1000
    STARLY_ICE = FRIENDSHIP_ITEMS["Starly"] +2000
    WINGULL_ICE = FRIENDSHIP_ITEMS["Wingull"]+1000

class QuestLocationIds(Enum):
    MEADOW_BIDOOF_HOUSING1 = BERRIES["10 Berries"] + 1
    MEADOW_BIDOOF_HOUSING2 = BERRIES["10 Berries"] + 2
    MEADOW_BIDOOF_HOUSING3 = BERRIES["10 Berries"] + 3
    MEADOW_BIDOOF_HOUSING4 = BERRIES["10 Berries"] + 4

    BEACH_BOTTLE1 = BERRIES["10 Berries"] + 5
    BEACH_BOTTLE2 = BERRIES["10 Berries"] + 6
    BEACH_BOTTLE3 = BERRIES["10 Berries"] + 7
    BEACH_BOTTLE4 = BERRIES["10 Berries"] + 8
    BEACH_BOTTLE5 = BERRIES["10 Berries"] + 9
    BEACH_BOTTLE6 = BERRIES["10 Berries"] + 10

    IGLOO_QUEST1 = BERRIES["10 Berries"] + 11
    IGLOO_QUEST2 = BERRIES["10 Berries"] + 12
    IGLOO_QUEST3 = BERRIES["10 Berries"] + 13

    CHRISTMAS_TREE1 = BERRIES["10 Berries"] + 14
    CHRISTMAS_TREE2 = BERRIES["10 Berries"] + 15
    CHRISTMAS_TREE3 = BERRIES["10 Berries"] + 16
    CHRISTMAS_TREE4 = BERRIES["10 Berries"] + 17


    THUNDERBOLT_POWERUP1 = POWERS["Progressive Thunderbolt"] + 1
    THUNDERBOLT_POWERUP2 = POWERS["Progressive Thunderbolt"] + 2
    THUNDERBOLT_POWERUP3 = POWERS["Progressive Thunderbolt"] + 3

    DASH_POWERUP1 = POWERS["Progressive Dash"] + 1
    DASH_POWERUP2 = POWERS["Progressive Dash"] + 2
    DASH_POWERUP3 = POWERS["Progressive Dash"] + 3

    HEALTH_POWERUP1 = POWERS["Progressive Health"] + 1
    HEALTH_POWERUP2 = POWERS["Progressive Health"] + 2
    HEALTH_POWERUP3 = POWERS["Progressive Health"] + 3

    IRON_TAIL_POWERUP1 = POWERS["Progressive Iron Tail"] +1
    IRON_TAIL_POWERUP2 = POWERS["Progressive Iron Tail"] +2
    IRON_TAIL_POWERUP3 = POWERS["Progressive Iron Tail"] +3

