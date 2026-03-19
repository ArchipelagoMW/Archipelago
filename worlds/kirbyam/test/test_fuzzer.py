"""Tests for Kirby AM protocol fuzz helpers."""

from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from ..client import KirbyAmClient
from .fuzzer import run_protocol_fuzz_suite, write_markdown_report


@pytest.mark.asyncio
async def test_protocol_fuzz_suite_completes_without_failures(mock_bizhawk_context, tmp_path: Path):
    client = KirbyAmClient()

    async def mock_read(_bizhawk_ctx, reads):
        return [(0).to_bytes(size, "little") for _addr, size, _bus in reads]

    with patch("worlds.kirbyam.client.bizhawk.read", new=AsyncMock(side_effect=mock_read)), \
         patch("worlds.kirbyam.client.bizhawk.write", new=AsyncMock(return_value=None)):
        summary = await run_protocol_fuzz_suite(client, mock_bizhawk_context)

    assert summary.total_cases >= 7
    assert summary.failed_cases == 0
    assert summary.coverage_percent == pytest.approx(100.0)

    report_path = tmp_path / "protocol_fuzz_report.md"
    write_markdown_report(summary, report_path)
    report_text = report_path.read_text(encoding="utf-8")
    assert "KirbyAM Protocol Fuzz Report" in report_text
    assert "Coverage:" in report_text
