"""Protocol fuzz helpers for Kirby AM client behavior tests."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Awaitable, Callable

from ..client import KirbyAmClient

if False:
    from ..types import KirbyAmBizHawkClientContext


@dataclass(frozen=True)
class ProtocolFuzzCase:
    name: str
    execute: Callable[[KirbyAmClient, "KirbyAmBizHawkClientContext"], Awaitable[None]]


@dataclass(frozen=True)
class ProtocolFuzzFinding:
    case_name: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class ProtocolFuzzSummary:
    findings: list[ProtocolFuzzFinding]

    @property
    def total_cases(self) -> int:
        return len(self.findings)

    @property
    def passed_cases(self) -> int:
        return sum(1 for finding in self.findings if finding.passed)

    @property
    def failed_cases(self) -> int:
        return self.total_cases - self.passed_cases

    @property
    def coverage_percent(self) -> float:
        if self.total_cases == 0:
            return 0.0
        return (self.passed_cases / self.total_cases) * 100.0


def build_protocol_fuzz_cases() -> list[ProtocolFuzzCase]:
    async def malformed_item_string(client: KirbyAmClient, ctx: "KirbyAmBizHawkClientContext") -> None:
        ctx.items_received = [SimpleNamespace(item="bad", player=1)]
        client._delivery_pending = False
        client._delivered_item_index = 0
        await client._deliver_items(ctx)

    async def malformed_item_negative(client: KirbyAmClient, ctx: "KirbyAmBizHawkClientContext") -> None:
        ctx.items_received = [SimpleNamespace(item=-1, player=1)]
        client._delivery_pending = False
        client._delivered_item_index = 0
        await client._deliver_items(ctx)

    async def malformed_player_overflow(client: KirbyAmClient, ctx: "KirbyAmBizHawkClientContext") -> None:
        ctx.items_received = [SimpleNamespace(item=3860001, player=0x100000000)]
        client._delivery_pending = False
        client._delivered_item_index = 0
        await client._deliver_items(ctx)

    async def malformed_item_missing_fields(client: KirbyAmClient, ctx: "KirbyAmBizHawkClientContext") -> None:
        ctx.items_received = [object()]
        client._delivery_pending = False
        client._delivered_item_index = 0
        await client._deliver_items(ctx)

    async def malformed_then_valid_item(client: KirbyAmClient, ctx: "KirbyAmBizHawkClientContext") -> None:
        ctx.items_received = [
            SimpleNamespace(item="corrupt", player=1),
            SimpleNamespace(item=3860001, player=1),
        ]
        client._delivery_pending = False
        client._delivered_item_index = 0
        await client._deliver_items(ctx)

    async def duplicate_replay_cursor(client: KirbyAmClient, ctx: "KirbyAmBizHawkClientContext") -> None:
        ctx.items_received = [SimpleNamespace(item=3860001, player=1)]
        client._delivery_pending = False
        client._delivered_item_index = 5
        await client._deliver_items(ctx)

    async def unexpected_command_sequence(client: KirbyAmClient, ctx: "KirbyAmBizHawkClientContext") -> None:
        client.on_package(ctx, "UnknownCommand", {"data": "x"})
        client.on_package(ctx, "ReceivedItems", {"items": "invalid", "index": "bad"})

    return [
        ProtocolFuzzCase("malformed_item_string", malformed_item_string),
        ProtocolFuzzCase("malformed_item_negative", malformed_item_negative),
        ProtocolFuzzCase("malformed_player_overflow", malformed_player_overflow),
        ProtocolFuzzCase("malformed_item_missing_fields", malformed_item_missing_fields),
        ProtocolFuzzCase("malformed_then_valid_item", malformed_then_valid_item),
        ProtocolFuzzCase("duplicate_replay_cursor", duplicate_replay_cursor),
        ProtocolFuzzCase("unexpected_command_sequence", unexpected_command_sequence),
    ]


async def run_protocol_fuzz_suite(
    client: KirbyAmClient,
    ctx: "KirbyAmBizHawkClientContext",
) -> ProtocolFuzzSummary:
    findings: list[ProtocolFuzzFinding] = []
    for case in build_protocol_fuzz_cases():
        client.initialize_client()
        try:
            await case.execute(client, ctx)
            findings.append(ProtocolFuzzFinding(case.name, True, "ok"))
        except Exception as exc:  # pragma: no cover - expected only on regressions
            findings.append(ProtocolFuzzFinding(case.name, False, f"{type(exc).__name__}: {exc}"))
    return ProtocolFuzzSummary(findings)


def render_markdown_report(summary: ProtocolFuzzSummary) -> str:
    lines = [
        "# KirbyAM Protocol Fuzz Report",
        "",
        f"Coverage: {summary.passed_cases}/{summary.total_cases} ({summary.coverage_percent:.1f}%)",
        "",
        "| Case | Status | Detail |",
        "| --- | --- | --- |",
    ]
    for finding in summary.findings:
        status = "PASS" if finding.passed else "FAIL"
        lines.append(f"| {finding.case_name} | {status} | {finding.detail} |")
    lines.append("")
    return "\n".join(lines)


def write_markdown_report(summary: ProtocolFuzzSummary, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_markdown_report(summary), encoding="utf-8")
