from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar
from uuid import uuid4


def new_id() -> str:
    """Return a unique request identifier."""

    return str(uuid4())


T = TypeVar("T")
E = TypeVar("E")


@dataclass(slots=True)
class Request(Generic[T, E]):
    """Base type for all dispatcher requests."""

    request_id: str = field(default_factory=new_id)


class Query(Request[T, E], Generic[T, E]):
    """Marker type for read-only requests."""

    pass


class Command(Request[T, E], Generic[T, E]):
    """Marker type for requests that may change process state."""

    pass


@dataclass(slots=True)
class BasicError:
    """Default error payload for core request failures."""

    message: str


@dataclass(slots=True)
class SupportedGamesData:
    """Supported game names exposed by the install service."""

    games: list[str]


@dataclass(slots=True)
class JobAcceptedData:
    """Identifier returned when work is accepted for background execution."""

    job_id: str


@dataclass(slots=True)
class JobStatusData:
    """Current status snapshot for a tracked job."""

    job_id: str
    status: str
    progress: float
    result: Any | None
    error: str | None


@dataclass(slots=True)
class RecentLogsData:
    """Recent log lines emitted by a tracked job."""

    job_id: str
    logs: list[str]


@dataclass(slots=True)
class ValidateInstallData:
    """Validation details for a candidate `.apworld` archive."""

    valid: bool
    apworld_name: str | None
    module_name: str | None
    checks: dict[str, bool]
    error: str | None = None


@dataclass(slots=True)
class StartLocalHostData:
    """Current local hosting state exposed to adapters."""

    running: bool
    host: str
    port: int | None
    job_id: str | None


@dataclass(slots=True)
class GetSupportedGames(Query[SupportedGamesData, BasicError]):
    """Query the list of supported games."""

    pass


@dataclass(slots=True)
class GetJobStatus(Query[JobStatusData, BasicError]):
    """Query the current state of a background job."""

    job_id: str = ""


@dataclass(slots=True)
class GetRecentLogs(Query[RecentLogsData, BasicError]):
    """Query recent log lines for a background job."""

    job_id: str = ""
    limit: int = 100


@dataclass(slots=True)
class ValidateInstall(Command[ValidateInstallData, BasicError]):
    """Validate whether an `.apworld` file is installable."""

    apworld_path: str = ""


@dataclass(slots=True)
class LaunchGame(Command[JobAcceptedData, BasicError]):
    """Start a launcher component as a managed background job."""

    game_name: str = ""
    profile_name: str = ""


@dataclass(slots=True)
class StartLocalHost(Command[StartLocalHostData, BasicError]):
    """Start a local `MultiServer` host as a managed background job."""

    multidata_path: str = ""
    host: str = "127.0.0.1"
    port: int = 38281


@dataclass(slots=True)
class StopJob(Command[None, BasicError]):
    """Request cancellation of a tracked background job."""

    job_id: str = ""
