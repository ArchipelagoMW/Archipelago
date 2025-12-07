from worlds.LauncherComponents import Component, Type, components, launch, icon_paths

def run_client(*args: str) -> None:
    from .client.Launch import launch_portal_2_client

    launch(launch_portal_2_client, name="Portal 2 Client", args=args)

icon_paths["portalpelago"] = f"ap:{__name__}/data/Portalpelago.png"

components.append(
    Component(
        "Portal 2 Client",
        func=run_client,
        game_name="Portal2",
        component_type=Type.CLIENT,
        supports_uri=True,
        icon='portalpelago'
    )
)