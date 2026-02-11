"""This package contains the apworld implementation for Ratchet and Clank 3: Up Your Arsenal for the PlayStation 2"""
from logging import DEBUG, getLogger
from typing import Optional

from worlds.LauncherComponents import Component, components, icon_paths, launch_subprocess, SuffixIdentifier, Type
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.world import RaC3World


def run_client(_url: Optional[str] = None):
    """Launch the client for connecting to RaC3"""
    from worlds.rac3.client.client import launch_client
    launch_subprocess(launch_client, name=f"{RAC3OPTION.GAME_TITLE}Client")


components.append(Component(f"{RAC3OPTION.GAME_TITLE_FULL} Client",
                            func=run_client,
                            component_type=Type.CLIENT,
                            file_identifier=SuffixIdentifier(".aprac3"),
                            icon="uya_icon",
                            description="Launch the Client for connecting to Ratchet and Clank 3 [PlayStation 2]",
                            ))

icon_paths["uya_icon"] = f"ap:{__name__}/images/uya_icon.png"

rac3_logger = getLogger(RAC3OPTION.GAME_TITLE_FULL)
rac3_logger.setLevel(DEBUG)
