
from worlds.LauncherComponents import Component, components, launch as launch_component



def launch_client():
    from .client.TeardownClient import launch
    launch_component(launch, name="TeardownClient")

components.append(Component(
    display_name="Teardown Client",
    func=launch_client,
    #icon="icon",
    #description="Archipelago Bridge for Teardown"
))





from .world import TeardownWorld as TeardownWorld

