from worlds.LauncherComponents import (
    Component,
    Type,
    components,
    icon_paths,
    launch,
)

from . import constants


def run_client(*args: str) -> None:
    from .client.launch import launch_tomba_client

    launch(launch_tomba_client, name=f"{constants.GAME} Client", args=args)


components.append(
    Component(
        f"{constants.GAME} Client",
        func=run_client,
        game_name=constants.GAME,
        component_type=Type.CLIENT,
        icon=constants.GAME,
    )
)

icon_paths[constants.GAME] = f"ap:{__name__}/assets/icon.png"
