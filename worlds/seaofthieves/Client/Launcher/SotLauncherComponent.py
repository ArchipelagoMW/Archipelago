
import worlds.LauncherComponents as LauncherComponents

LAUNCHER_FILE_IDENTIFIER = "apsot"

def __is_valid_file_extension(ext: str) -> bool:
    return ext == LAUNCHER_FILE_IDENTIFIER
def add_sot_to_client_laucher():
    LauncherComponents.components.append(
        LauncherComponents.Component(
            "Sea of Thieves",
            func=__launch_client,
            component_type=LauncherComponents.Type.CLIENT,
            file_identifier=__is_valid_file_extension
        )
    )
def __launch_client() -> None:
    from .ClientLauncher import launch
    LauncherComponents.launch_subprocess(launch, name="SOTmClient")


