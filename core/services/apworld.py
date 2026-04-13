from __future__ import annotations

import asyncio
import bisect
import pathlib
import shutil
from dataclasses import dataclass

from ..requests import BasicError, InstallApworldData
from ..result import Err, Ok, Result
from .install import InstallService


@dataclass
class ApworldService:
    """Validate and install `.apworld` archives into the custom worlds directory."""

    install_service: InstallService

    async def install(self, apworld_path: str) -> Result[InstallApworldData, BasicError]:
        """Validate and install an APWorld archive."""

        validation = await self.install_service.validate(apworld_path)
        match validation:
            case Err():
                return validation
            case Ok(value=validated):
                if not validated.valid or not validated.module_name or not validated.apworld_name:
                    return Err(BasicError(validated.error or f"APWorld is not installable: {apworld_path}"))

        source = pathlib.Path(apworld_path)
        module_name = validated.module_name
        apworld_name = validated.apworld_name

        import worlds
        from Utils import is_kivy_running

        assert worlds.user_folder is not None, "validated install must have a writable custom worlds directory"
        target = pathlib.Path(worlds.user_folder) / apworld_name
        await asyncio.to_thread(shutil.copyfile, source, target)

        found_already_loaded = False
        for loaded_world in worlds.world_sources:
            loaded_name = pathlib.Path(loaded_world.path).stem
            if module_name == loaded_name:
                found_already_loaded = True
                break

        if found_already_loaded and is_kivy_running():
            return Err(
                BasicError(
                    f"Installed APWorld successfully, but '{module_name}' is already loaded, "
                    "so a Launcher restart is required to use the new installation."
                )
            )

        world_source = worlds.WorldSource(str(target), is_zip=True, relative=False)
        bisect.insort(worlds.world_sources, world_source)
        world_source.load()

        return Ok(
            InstallApworldData(
                source_path=str(source),
                target_path=str(target),
                restart_required=found_already_loaded,
            )
        )
