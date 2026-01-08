import os

import worlds.LauncherComponents as LauncherComponents

from Utils import user_path

from .world import KeymastersKeepWorld


games_path: str = user_path("keymasters_keep")

if not os.path.exists(games_path):
    os.makedirs(games_path)

init_path: str = os.path.join(games_path, "__init__.py")

if not os.path.exists(init_path):
    with open(init_path, "w") as init_file:
        pass


def launch_client() -> None:
    from .client import main
    LauncherComponents.launch_subprocess(main, name="KeymastersKeepClient")


LauncherComponents.components.append(
    LauncherComponents.Component(
        "Keymaster's Keep Client",
        func=launch_client,
        component_type=LauncherComponents.Type.CLIENT
    )
)
