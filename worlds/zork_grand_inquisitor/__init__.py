import worlds.LauncherComponents as LauncherComponents

from .world import ZorkGrandInquisitorWorld


def launch_client():
    from .client import main
    LauncherComponents.launch_subprocess(main, name="ZorkGrandInquisitorClient")


LauncherComponents.components.append(
    LauncherComponents.Component(
        "Zork Grand Inquisitor Client",
        "ZorkGrandInquisitorClient",
        func=launch_client,
        component_type=LauncherComponents.Type.CLIENT
    )
)
