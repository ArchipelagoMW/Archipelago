# In our __init__.py, we just import our world class from our world.py to initialize it.
# Obviously, this world class needs to exist first. For this, read world.py.
from ..LauncherComponents import Component, Type, components, launch_subprocess
from .world import APQuestWorld as APQuestWorld

# Client stuff - Don't worry about this.


def run_client(*args: str) -> None:
    from .client.launch import launch_client  # lazy import

    launch_subprocess(launch_client, name="APQuest Client", args=args)


components.append(
    Component(
        "APQuest Client",
        func=run_client,
        game_name="APQuest",
        component_type=Type.CLIENT,
        supports_uri=True,
    )
)
