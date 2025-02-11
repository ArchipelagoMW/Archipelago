import worlds.LauncherComponents as LauncherComponents

from .world import ZorkGrandInquisitorWorld


def launch_client() -> None:
    from .client import main
    LauncherComponents.launch(main, name="ZorkGrandInquisitorClient")


LauncherComponents.components.append(
    LauncherComponents.Component(
        "Zork Grand Inquisitor Client",
        func=launch_client,
        component_type=LauncherComponents.Type.CLIENT
    )
)
