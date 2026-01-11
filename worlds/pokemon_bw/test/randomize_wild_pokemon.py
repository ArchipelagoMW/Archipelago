import random

from test.bases import WorldTestBase


class PokemonBWTestBase(WorldTestBase):
    game = "Pokemon Black and White"


class TestRandomizeWildPokemonCustom(PokemonBWTestBase):
    options = {"randomize_wild_pokemon": [
        "Randomize",
        "Ensure all obtainable",
        "Similar base stats",
        "Type themed areas",
        "Area 1-to-1",
        "Merge phenomenons",
        "Prevent rare encounters",
    ]}


def random_combination() -> list[str]:
    ret = ["Randomize"]
    for i in [
        "Ensure all obtainable",
        "Similar base stats",
        "Type themed areas",
        "Area 1-to-1",
        "Merge phenomenons",
        "Prevent rare encounters",
    ]:
        if random.random() < 0.5:
            ret.append(i)
    return ret


class TestRandomizeWildPokemon(PokemonBWTestBase):
    options = {"randomize_wild_pokemon": random_combination()}

    def setUp(self) -> None:
        print("Modifiers: "+", ".join(self.options["randomize_wild_pokemon"]))
        super().setUp()


class TestRandomizeWildPokemon1(TestRandomizeWildPokemon):
    options = {"randomize_wild_pokemon": random_combination()}


class TestRandomizeWildPokemon2(TestRandomizeWildPokemon):
    options = {"randomize_wild_pokemon": random_combination()}


class TestRandomizeWildPokemon3(TestRandomizeWildPokemon):
    options = {"randomize_wild_pokemon": random_combination()}


class TestRandomizeWildPokemon4(TestRandomizeWildPokemon):
    options = {"randomize_wild_pokemon": random_combination()}


class TestRandomizeWildPokemon5(TestRandomizeWildPokemon):
    options = {"randomize_wild_pokemon": random_combination()}


class TestRandomizeWildPokemon6(TestRandomizeWildPokemon):
    options = {"randomize_wild_pokemon": random_combination()}


class TestRandomizeWildPokemon7(TestRandomizeWildPokemon):
    options = {"randomize_wild_pokemon": random_combination()}


class TestRandomizeWildPokemon8(TestRandomizeWildPokemon):
    options = {"randomize_wild_pokemon": random_combination()}


class TestRandomizeWildPokemon9(TestRandomizeWildPokemon):
    options = {"randomize_wild_pokemon": random_combination()}


class TestRandomizeWildPokemon10(TestRandomizeWildPokemon):
    options = {"randomize_wild_pokemon": random_combination()}

