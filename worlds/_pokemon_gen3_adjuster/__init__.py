"""
A module that adds the Pokemon Gen 3 Adjuster if a compatible Pokemon Emerald world
or Pokemon Firered/Leafgreen world is in the Archipelago installation.
"""
from worlds.LauncherComponents import Component, components, Type, launch as launch_component
from .adjuster import launch


def launch_adjuster(*args) -> None:
    launch_component(launch, name="PokemonGen3Adjuster", args=args)


components.append(Component("Pokemon Gen 3 Adjuster", func=launch_adjuster, component_type=Type.ADJUSTER))
