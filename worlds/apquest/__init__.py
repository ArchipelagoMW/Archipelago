from .world import APQuestWorld as APQuestWorld
from worlds.LauncherComponents import components, Component, launch_subprocess, Type, SuffixIdentifier


def run_client(*args) -> None:
    print("Running Civ6 Client")
    from .client.ap_quest_client import main  # lazy import

    launch_subprocess(main, name="APQuest Client")


components.append(
    Component(
        "APQuest Client",
        func=run_client,
        component_type=Type.CLIENT,
    )
)
