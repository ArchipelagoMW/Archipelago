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
                            icon="kiki",
                            supports_uri=True,
                            game_name="Gato Roboto B-Side"))

icon_paths['kiki'] = f"ap:{__name__}/data/Kiki.png"


def data_path(file_name: str):
    import pkgutil
    return pkgutil.get_data(__name__, f"data/{file_name}")