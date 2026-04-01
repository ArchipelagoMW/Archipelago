



def launch_client():
    from .client.TeardownClient import launch
    launch()




from worlds.LauncherComponents import Component, components

components.append(Component(
    display_name="Teardown Client",
    func=launch_client,
    icon="icon",
    #description="Archipelago Bridge for Teardown"
))





from .world import TeardownWorld as TeardownWorld

