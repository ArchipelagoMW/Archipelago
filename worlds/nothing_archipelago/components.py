from worlds.LauncherComponents import Component, Type, components, launch


def run_client(*args: str) -> None:
    from .client.launch import launch_nothing_archipelago
    launch(launch_nothing_archipelago, name = "Nothing Archipelago Client",args=args)


components.append(
    Component(
        "Nothing Archipelago",
        func=run_client,
        game_name="Nothing Archipelago",
        component_type=Type.CLIENT,
        supports_uri=True
        )
)