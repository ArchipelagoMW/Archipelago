from __future__ import annotations

"""Public exports for the additive core API layer."""

from .dispatcher import Dispatcher, create_dispatcher
from .events import Event, EventBus, create_bus
from .jobs import JobContext, JobManager, JobRecord, JobStatus
from .requests import (
    BasicError,
    Command,
    GetJobStatus,
    GetRecentLogs,
    GetSupportedGames,
    JobAcceptedData,
    JobStatusData,
    LaunchGame,
    Query,
    RecentLogsData,
    Request,
    StartLocalHost,
    StartLocalHostData,
    StopJob,
    SupportedGamesData,
    ValidateInstall,
    ValidateInstallData,
)
from .result import Err, Ok, Result
from .services import HostService, InstallService, LaunchService, ProcessRunner

__all__ = [
    "BasicError",
    "Command",
    "Dispatcher",
    "Err",
    "Event",
    "EventBus",
    "GetJobStatus",
    "GetRecentLogs",
    "GetSupportedGames",
    "HostService",
    "InstallService",
    "JobAcceptedData",
    "JobContext",
    "JobManager",
    "JobRecord",
    "JobStatus",
    "JobStatusData",
    "LaunchGame",
    "LaunchService",
    "Ok",
    "ProcessRunner",
    "Query",
    "RecentLogsData",
    "Request",
    "Result",
    "StartLocalHost",
    "StartLocalHostData",
    "StopJob",
    "SupportedGamesData",
    "ValidateInstall",
    "ValidateInstallData",
    "create_bus",
    "create_dispatcher",
]
