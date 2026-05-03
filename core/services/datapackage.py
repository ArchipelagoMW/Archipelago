from __future__ import annotations

import asyncio
import json
import os
from dataclasses import dataclass

import Utils

from ..requests import BasicError, DatapackageExportData
from ..result import Ok, Result


@dataclass
class DatapackageService:
    """Export the installed data package to a JSON file."""

    async def export(self) -> Result[DatapackageExportData, BasicError]:
        """Export the current network data package to disk."""

        from worlds import network_data_package

        path = Utils.user_path("datapackage_export.json")

        def write() -> None:
            directory = os.path.dirname(path)
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(network_data_package, handle, indent=4)

        await asyncio.to_thread(write)
        return Ok(DatapackageExportData(output_path=path))
