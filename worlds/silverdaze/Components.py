from worlds.LauncherComponents import Component, Type, components, launch


def run_client(*args: str) -> None:

    from .client.launch import launch_sd_client


    launch(launch_sd_client, name="Silver Daze Client", args=args)



components.append(
    Component(
        "Silver Daze Client",
        func=run_client,
        game_name="Silver Daze",
        component_type=Type.CLIENT,
        supports_uri=True,
    )
)
