from __future__ import annotations

import asyncio
from dataclasses import dataclass

import Utils

from ..requests import BasicError, TemplateGenerationData
from ..result import Ok, Result


@dataclass
class TemplateService:
    """Generate template YAMLs without adapter-side file browsing."""

    async def generate(self, skip_open_folder: bool = False) -> Result[TemplateGenerationData, BasicError]:
        """Generate template YAMLs for installed games."""

        from Options import generate_yaml_templates

        target = Utils.user_path("Players", "Templates")
        await asyncio.to_thread(generate_yaml_templates, target, False)
        return Ok(TemplateGenerationData(output_directory=target))
