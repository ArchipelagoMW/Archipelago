from worlds.LauncherComponents import components, Component, launch_subprocess, Type


def launch_client():
    from .client import launch
    launch_subprocess(launch, "Yaml Creator")


components.append(Component("Yaml Creator", "YamlCreator", func=launch_client, component_type=Type.ADJUSTER))
