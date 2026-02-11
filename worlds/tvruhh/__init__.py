from .world import TVRUHHWorld as TVRUHHWorld

from worlds.LauncherComponents import Component, components, launch as launch_component, Type

def launch_client(*args: str):
    from .client import launch
    launch_component(launch, name="TVRUHH Client", args=args)

components.append(Component("TVRUHH Client", "TVRUHH Client", func=launch_client, component_type=Type.CLIENT))