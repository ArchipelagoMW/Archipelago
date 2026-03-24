"""Tests for KirbyAM test logging support."""

import logging
import uuid

import pytest


@pytest.mark.asyncio
async def test_kirbyam_test_logging_records_protocol_traffic(
    kirbyam_test_log_file,
    mock_bizhawk_context,
    mock_bizhawk_read,
    mock_bizhawk_write,
    caplog,
) -> None:
    test_logger = logging.getLogger("worlds.kirbyam.test")
    previous_level = test_logger.level
    test_file_handler = logging.FileHandler(kirbyam_test_log_file, mode="a", encoding="utf-8")
    test_file_handler.setLevel(logging.DEBUG)
    test_logger.setLevel(logging.DEBUG)
    test_logger.addHandler(test_file_handler)
    caplog.set_level(logging.DEBUG)
    try:
        marker = f"TEST_MARKER {uuid.uuid4().hex}"
        test_logger.info(marker)

        await mock_bizhawk_read(mock_bizhawk_context.bizhawk_ctx, [(0x0202C000, 4, "System Bus")])
        await mock_bizhawk_write(mock_bizhawk_context.bizhawk_ctx, [(0x0202C004, (1).to_bytes(4, "little"), "System Bus")])
        await mock_bizhawk_context.send_msgs([{"cmd": "LocationChecks", "locations": [3860101]}])

        for handler in logging.getLogger().handlers:
            flush = getattr(handler, "flush", None)
            if callable(flush):
                flush()
        test_file_handler.flush()

        assert kirbyam_test_log_file.exists()
        log_text = kirbyam_test_log_file.read_text(encoding="utf-8", errors="replace")
        marker_index = log_text.rfind(marker)
        assert marker_index != -1
        log_section = log_text[marker_index:]
        assert "bizhawk.read" in log_section
        assert "bizhawk.write" in log_section
        assert "ap.send_msgs" in log_section
        assert "bizhawk.read" in caplog.text
        assert "bizhawk.write" in caplog.text
        assert "ap.send_msgs" in caplog.text
    finally:
        test_logger.removeHandler(test_file_handler)
        test_file_handler.close()
        test_logger.setLevel(previous_level)
