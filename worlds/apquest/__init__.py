from worlds.LauncherComponents import Component, Type, components, launch_subprocess

from .world import APQuestWorld as APQuestWorld


def run_client(*args) -> None:
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
