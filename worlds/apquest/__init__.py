# In our __init__.py, we just import our world class from our world.py to initialize it.
# Obviously, this world class needs to exist first. For this, read world.py.
from worlds.LauncherComponents import Component, Type, components, launch

from .world import APQuestWorld as APQuestWorld


# Your apworld might have other components than just the generation.
# The most common type of component is a client, but there are other components, such as sprite/palette adjusters.
# APQuest has a CommonClient-derived client that the entire game sits inside.
# APQuest will not teach you how to make a client or any other type of component.
# However, let's quickly talk about how you register a component to be launchable from the Archipelago Launcher.
# First, you'll need a function that takes a list of args (e.g. from the command line) that launches your component.
def run_client(*args: str) -> None:
    # Ideally, you should lazily import your component code so that it doesn't have to be loaded until necessary.
    from .client.launch import launch_client

    # Also, if your component has its own lifecycle, like if it is its own window that can be interacted with,
    # you should use LauncherComponents.launch_subprosses to launch it.
    # Specifically for components that support a gui mode using kivy, but can also be run without gui,
    # you should use the LauncherComponents.launch helper (which itself calls launch_subprocesS).
    # This mainly applies to CommonClient-derived clients.
    launch(launch_client, name="APQuest Client", args=args)


# You then add this function as a component by appending a Component instance to LauncherComponents.components.
# Now, it will show up in the Launcher with its display name,
# and when the user clicks on the "Open" button, your function will be run.
components.append(
    Component(
        "APQuest Client",
        func=run_client,
        game_name="APQuest",
        component_type=Type.CLIENT,
        supports_uri=True,
    )
)
