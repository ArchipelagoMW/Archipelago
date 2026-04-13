from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from ..requests import BasicError, ValidateInstallData
from ..result import Ok, Result
from .shared import _default_supported_games_provider, _inspect_apworld


@dataclass(slots=True)
class InstallService:
    """Expose install-oriented read and validation operations.

    Example::

        service = InstallService()
        result = await service.validate("custom_world.apworld")
    """

    supported_games_provider: Callable[[], list[str]] = _default_supported_games_provider

    async def validate(self, apworld_path: str) -> Result[ValidateInstallData, BasicError]:
        """Validate a candidate `.apworld` path."""

        return Ok(_inspect_apworld(apworld_path))

    async def list_supported_games(self) -> list[str]:
        """Return the sorted supported game names."""

        return sorted(self.supported_games_provider())
