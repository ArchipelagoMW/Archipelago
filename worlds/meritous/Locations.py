# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from BaseClasses import Location


class MeritousLocation(Location):
    game: str = "Meritous"


offset = 593_000

alpha_store = {
    f"Alpha Cache {i + 1}": offset + i for i in range(0, 24)
}

beta_store = {
    f"Beta Cache {i + 1}": offset + i + 24 for i in range(0, 24)
}

gamma_store = {
    f"Gamma Cache {i + 1}": offset + i + 48 for i in range(0, 24)
}

chest_store = {
    f"Reward Chest {i + 1}": offset + i + 72 for i in range(0, 24)
}

special_store = {
    "PSI Key Storage 1": offset + 96,
    "PSI Key Storage 2": offset + 97,
    "PSI Key Storage 3": offset + 98,
    "Meridian": offset + 99,
    "Ataraxia": offset + 100,
    "Merodach": offset + 101,
    "Place of Power": offset + 102,
    "The Last Place You'll Look": offset + 103
}

location_table = {
    **alpha_store,
    **beta_store,
    **gamma_store,
    **chest_store,
    **special_store
}
