import random

from .world import GatoRobotoWorld as GatoRobotoWorld
from worlds.LauncherComponents import launch_subprocess, components, Component, Type, icon_paths


def launch_client(*args):
    """
    Launch the Gato Roboto Client
    """
    from .GatoRobotoClient import launch
    from CommonClient import gui_enabled
    if gui_enabled:
        launch_subprocess(launch, name="GatoRobotoClient", args=args)
    else:
        launch()


components.append(Component("Gato Roboto Client B-Side",
                            func=launch_client,
                            component_type=Type.CLIENT,
                            icon="gato",
                            supports_uri=True,
                            game_name="Gato Roboto B-Side"))

if random.random() > 0.01:
    icon_paths['gato'] = f"ap:{__name__}/data/main_gato.webp"
else:
    icon_paths['gato'] = f"ap:{__name__}/data/evil_gato.webp"

def data_path(file_name: str):
    import pkgutil
    return pkgutil.get_data(__name__, f"data/{file_name}")