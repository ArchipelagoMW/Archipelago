"""Tests for KirbyAM test logging support."""

import asyncio

import pytest


@pytest.mark.asyncio
async def test_kirbyam_test_logging_records_protocol_traffic(
    kirbyam_test_log_file,
    mock_bizhawk_context,
    mock_bizhawk_read,
    mock_bizhawk_write,
) -> None:
    await mock_bizhawk_read(mock_bizhawk_context.bizhawk_ctx, [(0x0202C000, 4, "System Bus")])
    await mock_bizhawk_write(mock_bizhawk_context.bizhawk_ctx, [(0x0202C004, (1).to_bytes(4, "little"), "System Bus")])
    await mock_bizhawk_context.send_msgs([{"cmd": "LocationChecks", "locations": [3860101]}])

    assert kirbyam_test_log_file.exists()
    log_text = ""
    for _ in range(20):
        log_text = kirbyam_test_log_file.read_text(encoding="utf-8")
        if "bizhawk.read" in log_text and "bizhawk.write" in log_text and "ap.send_msgs" in log_text:
            break
        await asyncio.sleep(0.05)

    assert "bizhawk.read" in log_text
    assert "bizhawk.write" in log_text
    assert "ap.send_msgs" in log_text
