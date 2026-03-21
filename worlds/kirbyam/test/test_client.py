"""Integration tests for client polling and delivery logic."""
import pytest
import logging
from unittest.mock import AsyncMock, Mock, patch

from ..data import data
from ..client import KirbyAmClient


@pytest.mark.asyncio
async def test_poll_locations_empty_bitfield(mock_bizhawk_context):
    """Test _poll_locations with no shards collected."""
    client = KirbyAmClient()
    client.initialize_client()
    
    # Mock empty shard bitfield (0x0202C000 = 0x00)
    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(0).to_bytes(4, 'little')]
        
        await client._poll_locations(mock_bizhawk_context)
        
        # No new locations should be checked
        assert len(client._checked_location_bits) == 0


@pytest.mark.asyncio
async def test_poll_locations_single_shard(mock_bizhawk_context):
    """Test _poll_locations when one shard is collected."""
    client = KirbyAmClient()
    client.initialize_client()
    
    # Mock shard bitfield with bit 0 set (first shard)
    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(0x01).to_bytes(4, 'little')]
        
        await client._poll_locations(mock_bizhawk_context)
        
        # Bit 0 should be marked as checked
        assert 0 in client._checked_location_bits


@pytest.mark.asyncio
async def test_poll_locations_prefers_native_shard_address(mock_bizhawk_context):
    """Test _poll_locations reads the native shard bitfield when available."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {"shard_bitfield_native": 0x02038970}, clear=False), \
         patch.dict(data.transport_ram_addresses, {"shard_bitfield": 0x0202C000}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(0x01).to_bytes(1, 'little')]

        await client._poll_locations(mock_bizhawk_context)

        mock_read.assert_awaited_once_with(
            mock_bizhawk_context.bizhawk_ctx,
            [(0x02038970, 1, 'System Bus')]
        )


@pytest.mark.asyncio
async def test_poll_locations_falls_back_to_transport_shard_address(mock_bizhawk_context):
    """Test _poll_locations falls back to transport shard bitfield when native key is missing."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {}, clear=True), \
         patch.dict(data.transport_ram_addresses, {"shard_bitfield": 0x0202C000}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(0x01).to_bytes(4, 'little')]

        await client._poll_locations(mock_bizhawk_context)

        mock_read.assert_awaited_once_with(
            mock_bizhawk_context.bizhawk_ctx,
            [(0x0202C000, 4, 'System Bus')]
        )


@pytest.mark.asyncio
async def test_poll_locations_multiple_shards(mock_bizhawk_context, shard_bitfield_fixtures):
    """Test _poll_locations with multiple shards."""
    client = KirbyAmClient()
    client.initialize_client()
    
    # Test with shard_1_2_3 pattern (bits 0, 1, 2 set)
    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [shard_bitfield_fixtures["shard_1_2_3"].to_bytes(4, 'little')]
        
        await client._poll_locations(mock_bizhawk_context)
        
        # Bits 0, 1, 2 should be marked as checked
        assert 0 in client._checked_location_bits
        assert 1 in client._checked_location_bits
        assert 2 in client._checked_location_bits


@pytest.mark.asyncio
async def test_poll_locations_ignores_unmapped_reserved_bits(mock_bizhawk_context):
    """Test reserved/high bits are ignored when they do not map to any location."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {}, clear=True), \
         patch.dict(data.transport_ram_addresses, {"shard_bitfield": 0x0202C000}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        # Bits 0 and 31 set; only bit 0 maps to current shard locations.
        mock_read.return_value = [(0x80000001).to_bytes(4, 'little')]

        await client._poll_locations(mock_bizhawk_context)

        assert 0 in client._checked_location_bits
        assert 31 not in client._checked_location_bits


@pytest.mark.asyncio
async def test_location_check_sent_on_new_shard(mock_bizhawk_context):
    """Test that LocationChecks is sent when a new shard is detected."""
    client = KirbyAmClient()
    client.initialize_client()
    
    # Pre-populate bizhawk context checked locations
    mock_bizhawk_context.checked_locations = set()
    
    # Mock read returning bit 0 set (first new shard)
    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send:
        
        mock_read.return_value = [(0x01).to_bytes(4, 'little')]
        
        await client._poll_locations(mock_bizhawk_context)

        mock_send.assert_awaited_once_with([
            {"cmd": "LocationChecks", "locations": [data.locations["SHARD_1"].location_id]}
        ])


@pytest.mark.asyncio
async def test_location_check_resent_when_server_missing_location(mock_bizhawk_context):
    """RAM-derived checks should be resent if server checked_locations is missing them."""
    client = KirbyAmClient()
    client.initialize_client()

    first_loc = data.locations["SHARD_1"].location_id
    second_loc = data.locations["SHARD_2"].location_id
    # Simulate server knowing only shard 1 while RAM reports shards 1+2.
    mock_bizhawk_context.checked_locations = {first_loc}

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send, \
         patch('CommonClient.logger') as mock_logger:

        mock_read.return_value = [(0x03).to_bytes(4, 'little')]

        await client._poll_locations(mock_bizhawk_context)

        mock_send.assert_awaited_once_with([
            {"cmd": "LocationChecks", "locations": [second_loc]}
        ])
        assert mock_logger.info.called
        assert "resending RAM-derived LocationChecks missing on server" in mock_logger.info.call_args.args[0]
        assert mock_logger.info.call_args.args[1] == [second_loc]
        assert mock_logger.info.call_args.args[2] == [first_loc]


@pytest.mark.asyncio
async def test_no_location_checks_sent_when_all_already_server_acknowledged(mock_bizhawk_context):
    """No LocationChecks message should be sent when all RAM-derived checks are already on the server."""
    client = KirbyAmClient()
    client.initialize_client()

    shard1 = data.locations["SHARD_1"].location_id
    shard2 = data.locations["SHARD_2"].location_id
    mock_bizhawk_context.checked_locations = {shard1, shard2}

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send, \
         patch('CommonClient.logger') as mock_logger:

        mock_read.return_value = [(0x03).to_bytes(4, 'little')]  # bits 0 and 1 set

        await client._poll_locations(mock_bizhawk_context)

        mock_send.assert_not_awaited()
        assert mock_logger.debug.called
        assert "dedupe suppressed LocationChecks" in mock_logger.debug.call_args.args[0]
        assert mock_logger.debug.call_args.args[1] == [shard1, shard2]


def test_client_initialization():
    """Test client state is properly initialized."""
    client = KirbyAmClient()
    client.initialize_client()
    
    assert client._checked_location_bits == set()
    assert client._delivered_item_index == 0
    assert client._delivery_pending is False
    assert client._delivery_pending_frame is None
    assert client._goal_reported is False


@pytest.mark.asyncio
async def test_deliver_items_resyncs_after_save_loss(mock_bizhawk_context):
    """If ROM counter regresses, client should rewind delivery cursor and resend."""
    client = KirbyAmClient()
    client.initialize_client()
    client._delivered_item_index = 3
    client._delivery_pending = False

    mock_bizhawk_context.items_received = [
        Mock(item=3860001, player=1),
        Mock(item=3860002, player=1),
        Mock(item=3860003, player=1),
        Mock(item=3860004, player=1),
    ]

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        # mailbox empty, ROM says only one item was actually applied
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (1).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

        assert client._delivered_item_index == 1
        assert client._delivery_pending is True
        written = mock_write.await_args.args[1]
        assert written[0][1] == int(3860002).to_bytes(4, 'little')


@pytest.mark.asyncio
async def test_deliver_items_resyncs_forward_after_reconnect(mock_bizhawk_context):
    """If ROM counter is ahead, client should fast-forward and deliver next missing item."""
    client = KirbyAmClient()
    client.initialize_client()
    client._delivered_item_index = 0
    client._delivery_pending = False

    mock_bizhawk_context.items_received = [
        Mock(item=3860001, player=1),
        Mock(item=3860002, player=1),
        Mock(item=3860003, player=1),
    ]

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        # mailbox empty, ROM says first two items were already applied
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (2).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

        assert client._delivered_item_index == 2
        assert client._delivery_pending is True
        written = mock_write.await_args.args[1]
        assert written[0][1] == int(3860003).to_bytes(4, 'little')


@pytest.mark.asyncio
async def test_deliver_items_waits_when_rom_counter_ahead_but_items_partial(mock_bizhawk_context):
    """Do not write items while ReceivedItems list is still behind ROM counter."""
    client = KirbyAmClient()
    client.initialize_client()
    client._delivered_item_index = 0
    client._delivery_pending = False

    mock_bizhawk_context.items_received = [
        Mock(item=3860001, player=1),
    ]

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (2).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

        assert client._delivered_item_index == len(mock_bizhawk_context.items_received)
        assert client._delivery_pending is False
        mock_write.assert_awaited_once()
        persisted = mock_write.await_args.args[1]
        assert persisted == [
            (data.transport_ram_addresses["delivered_item_index"], (1).to_bytes(4, 'little'), "System Bus")
        ]


@pytest.mark.asyncio
async def test_deliver_items_skips_malformed_entries_and_logs_warning(mock_bizhawk_context, caplog):
    """Malformed ReceivedItems entries should be skipped, logged, and not crash delivery."""
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.items_received = [
        Mock(item="bad", player=1),
        Mock(item=3860001, player=1),
    ]

    caplog.set_level(logging.WARNING, logger="Client")

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

        assert client._delivery_pending is True
        assert client._delivered_item_index == 1
        written = mock_write.await_args.args[1]
        assert written[0][1] == int(3860001).to_bytes(4, 'little')

    assert "Skipping malformed ReceivedItems entry" in caplog.text


@pytest.mark.asyncio
async def test_deliver_items_clears_stuck_mailbox_after_timeout(mock_bizhawk_context, caplog):
    """A stuck mailbox flag should time out, clear, and keep the same item index for retry."""
    client = KirbyAmClient()
    client.initialize_client()
    client._delivery_pending = True
    client._delivery_pending_frame = 100
    client._delivered_item_index = 0

    mock_bizhawk_context.items_received = [
        Mock(item=3860001, player=1),
    ]

    caplog.set_level(logging.WARNING, logger="Client")

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [
            (1).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
            (131).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

        mock_write.assert_awaited_once_with(
            mock_bizhawk_context.bizhawk_ctx,
            [(data.transport_ram_addresses["incoming_item_flag"], (0).to_bytes(4, 'little'), 'System Bus')]
        )
        assert client._delivery_pending is False
        assert client._delivery_pending_frame is None
        assert client._delivered_item_index == 0

    assert "Mailbox ACK timeout" in caplog.text


@pytest.mark.asyncio
async def test_deliver_items_records_pending_frame_when_writing(mock_bizhawk_context):
    """Writing a mailbox item should capture the current frame for timeout tracking."""
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.items_received = [
        Mock(item=3860001, player=1),
    ]

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
            (1234).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

        mock_write.assert_awaited_once()
        assert client._delivery_pending is True
        assert client._delivery_pending_frame == 1234


@pytest.mark.asyncio
async def test_goal_dark_mind_native_signal_reports_location_then_goal_status(mock_bizhawk_context):
    """Dark Mind goal should use native 9999 signal and report status after server ack."""
    from NetUtils import ClientStatus

    client = KirbyAmClient()
    client.initialize_client()

    dark_mind_goal_id = data.locations["GOAL_DARK_MIND"].location_id
    mock_bizhawk_context.slot_data["goal"] = 0
    mock_bizhawk_context.checked_locations = set()

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(9999).to_bytes(4, 'little')]

        await client._maybe_report_goal(mock_bizhawk_context)

        mock_bizhawk_context.send_msgs.assert_awaited_once_with([
            {"cmd": "LocationChecks", "locations": [dark_mind_goal_id]}
        ])

    mock_bizhawk_context.send_msgs.reset_mock()
    mock_bizhawk_context.checked_locations.add(dark_mind_goal_id)

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(9999).to_bytes(4, 'little')]

        await client._maybe_report_goal(mock_bizhawk_context)

    mock_bizhawk_context.send_msgs.assert_awaited_once_with([
        {"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}
    ])
    assert client._goal_reported is True


@pytest.mark.asyncio
async def test_goal_100_percent_uses_native_10000_signal(mock_bizhawk_context):
    """100% goal should trigger on native 10000 signal."""
    client = KirbyAmClient()
    client.initialize_client()

    goal_id = data.locations["GOAL_100_PERCENT"].location_id
    mock_bizhawk_context.slot_data["goal"] = 1

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(10000).to_bytes(4, 'little')]

        await client._maybe_report_goal(mock_bizhawk_context)

    mock_bizhawk_context.send_msgs.assert_awaited_once_with([
        {"cmd": "LocationChecks", "locations": [goal_id]}
    ])


@pytest.mark.asyncio
async def test_goal_dark_mind_does_not_trigger_on_10000(mock_bizhawk_context):
    """Dark Mind goal mode must not treat 10000 as first-clear trigger."""
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.slot_data["goal"] = 0

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(10000).to_bytes(4, 'little')]

        await client._maybe_report_goal(mock_bizhawk_context)

    mock_bizhawk_context.send_msgs.assert_not_awaited()


@pytest.mark.asyncio
async def test_goal_native_signal_missing_falls_back_to_noop(mock_bizhawk_context):
    """If native goal signal address is unavailable, goal reporting should no-op safely."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {}, clear=True), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        await client._maybe_report_goal(mock_bizhawk_context)

    mock_read.assert_not_awaited()
    mock_bizhawk_context.send_msgs.assert_not_awaited()


@pytest.mark.asyncio
async def test_goal_location_check_sent_once_before_ack(mock_bizhawk_context):
    """Native signal should not spam duplicate goal location checks before server acknowledgement."""
    client = KirbyAmClient()
    client.initialize_client()

    goal_id = data.locations["GOAL_DARK_MIND"].location_id
    mock_bizhawk_context.slot_data["goal"] = 0

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(9999).to_bytes(4, 'little')]
        await client._maybe_report_goal(mock_bizhawk_context)
        await client._maybe_report_goal(mock_bizhawk_context)

    mock_bizhawk_context.send_msgs.assert_awaited_once_with([
        {"cmd": "LocationChecks", "locations": [goal_id]}
    ])


@pytest.mark.asyncio
async def test_goal_location_uses_locations_checked_for_reconnect_safe_dedup(mock_bizhawk_context):
    """Goal location checks should dedupe via ctx.locations_checked when available."""
    client = KirbyAmClient()
    client.initialize_client()

    goal_id = data.locations["GOAL_DARK_MIND"].location_id
    mock_bizhawk_context.slot_data["goal"] = 0
    mock_bizhawk_context.locations_checked = set()

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(9999).to_bytes(4, 'little')]

        await client._maybe_report_goal(mock_bizhawk_context)
        await client._maybe_report_goal(mock_bizhawk_context)

    assert goal_id in mock_bizhawk_context.locations_checked
    mock_bizhawk_context.send_msgs.assert_awaited_once_with([
        {"cmd": "LocationChecks", "locations": [goal_id]}
    ])


@pytest.mark.asyncio
async def test_probe_boss_candidates_no_address_no_read(mock_bizhawk_context):
    """Boss probe should no-op when native candidate address is not configured."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {}, clear=True), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        await client._probe_boss_defeat_candidates(mock_bizhawk_context)

        mock_read.assert_not_awaited()


@pytest.mark.asyncio
async def test_goal_reporting_logs_native_signal_seen(mock_bizhawk_context):
    """Info log should fire exactly once when native goal signal is first observed."""
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.slot_data["goal"] = 0
    mock_bizhawk_context.checked_locations = set()

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [(9999).to_bytes(4, 'little')]
        await client._maybe_report_goal(mock_bizhawk_context)

    signal_calls = [
        c for c in mock_logger.info.call_args_list
        if "native goal signal seen" in c.args[0]
    ]
    assert len(signal_calls) == 1
    assert signal_calls[0].args[1:] == (0,)  # goal_option=0


@pytest.mark.asyncio
async def test_goal_reporting_logs_location_check_sent(mock_bizhawk_context):
    """Info log should fire when goal location check is sent to server."""
    client = KirbyAmClient()
    client.initialize_client()

    goal_id = data.locations["GOAL_DARK_MIND"].location_id
    mock_bizhawk_context.slot_data["goal"] = 0
    mock_bizhawk_context.checked_locations = set()

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [(9999).to_bytes(4, 'little')]
        await client._maybe_report_goal(mock_bizhawk_context)

    check_calls = [
        c for c in mock_logger.info.call_args_list
        if "sending goal location check" in c.args[0]
    ]
    assert len(check_calls) == 1
    assert check_calls[0].args[1:] == (goal_id,)


@pytest.mark.asyncio
async def test_goal_reporting_logs_client_goal_status(mock_bizhawk_context):
    """Info log should fire when CLIENT_GOAL status is sent."""
    client = KirbyAmClient()
    client.initialize_client()

    goal_id = data.locations["GOAL_DARK_MIND"].location_id
    mock_bizhawk_context.slot_data["goal"] = 0
    mock_bizhawk_context.checked_locations = {goal_id}

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [(9999).to_bytes(4, 'little')]
        # Prime the native signal so it was "seen" before this call.
        client._native_goal_signal_seen = True
        await client._maybe_report_goal(mock_bizhawk_context)

    complete_calls = [
        c for c in mock_logger.info.call_args_list
        if "goal complete" in c.args[0]
    ]
    assert len(complete_calls) == 1
    assert complete_calls[0].args[1:] == (0,)  # goal_option=0


@pytest.mark.asyncio
async def test_probe_boss_candidates_logs_rising_edges(mock_bizhawk_context):
    """Boss probe should log rising bit transitions for candidate mapping."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {"boss_mirror_table_native": 0x02028C14}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        # First probe establishes baseline with all zeros.
        mock_read.return_value = [bytes(32)]
        await client._probe_boss_defeat_candidates(mock_bizhawk_context)

        # Second probe sets one bit at first byte (bit 3).
        payload = bytearray(32)
        payload[0] = 0x08
        mock_read.return_value = [bytes(payload)]
        await client._probe_boss_defeat_candidates(mock_bizhawk_context)

        assert mock_logger.debug.called
        logged_args = mock_logger.debug.call_args.args
        assert "KirbyAM: boss candidate probe rising bits" in logged_args[0]
        assert "0x02028C14[bit3]" in logged_args[1]


@pytest.mark.asyncio
async def test_probe_boss_candidates_resets_baseline_on_stream_change(mock_bizhawk_context):
    """Changing BizHawk stream identity should re-baseline probe snapshots."""
    client = KirbyAmClient()
    client.initialize_client()

    first_stream = object()
    second_stream = object()
    mock_bizhawk_context.bizhawk_ctx.streams = first_stream

    with patch.dict(data.native_ram_addresses, {"boss_mirror_table_native": 0x02028C14}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        # Baseline with first stream.
        mock_read.return_value = [bytes(32)]
        await client._probe_boss_defeat_candidates(mock_bizhawk_context)

        # Switch stream identity and present non-zero state; should be treated as new baseline.
        mock_bizhawk_context.bizhawk_ctx.streams = second_stream
        payload = bytearray(32)
        payload[0] = 0x08
        mock_read.return_value = [bytes(payload)]
        await client._probe_boss_defeat_candidates(mock_bizhawk_context)

        mock_logger.info.assert_not_called()


@pytest.mark.asyncio
async def test_probe_unsafe_delivery_candidates_no_addresses_no_read(mock_bizhawk_context):
    """Unsafe-delivery candidate probe should no-op when no optional addresses are configured."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {}, clear=True), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        await client._probe_unsafe_delivery_candidates(mock_bizhawk_context)

    mock_read.assert_not_awaited()


@pytest.mark.asyncio
async def test_probe_unsafe_delivery_candidates_logs_counter_changes(mock_bizhawk_context):
    """Configured unsafe-delivery candidate counters should log when values change."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(
        data.native_ram_addresses,
        {
            "shadow_kirby_encounters_native": 0x020229D0,
            "mirra_encounters_native": 0x020229D8,
        },
        clear=False,
    ), patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
        ]
        await client._probe_unsafe_delivery_candidates(mock_bizhawk_context)

        mock_read.return_value = [
            (1).to_bytes(4, 'little'),
            (2).to_bytes(4, 'little'),
        ]
        await client._probe_unsafe_delivery_candidates(mock_bizhawk_context)

    assert mock_logger.debug.call_count == 2
    first_args = mock_logger.debug.call_args_list[0].args
    second_args = mock_logger.debug.call_args_list[1].args
    assert "unsafe-delivery candidate probe" in first_args[0]
    assert first_args[1:] == ("shadow_kirby_encounters", 0, 1)
    assert second_args[1:] == ("mirra_encounters", 0, 2)


@pytest.mark.asyncio
async def test_probe_unsafe_delivery_candidates_rebaseline_on_stream_change(mock_bizhawk_context):
    """Unsafe-delivery candidate probe should re-baseline on BizHawk reconnect."""
    client = KirbyAmClient()
    client.initialize_client()

    first_stream = object()
    second_stream = object()
    mock_bizhawk_context.bizhawk_ctx.streams = first_stream

    with patch.dict(
        data.native_ram_addresses,
        {"shadow_kirby_encounters_native": 0x020229D0},
        clear=False,
    ), patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [(0).to_bytes(4, 'little')]
        await client._probe_unsafe_delivery_candidates(mock_bizhawk_context)

        mock_bizhawk_context.bizhawk_ctx.streams = second_stream
        mock_read.return_value = [(3).to_bytes(4, 'little')]
        await client._probe_unsafe_delivery_candidates(mock_bizhawk_context)

    mock_logger.info.assert_not_called()


@pytest.mark.asyncio
async def test_game_watcher_skips_when_server_is_none(mock_bizhawk_context):
    """game_watcher should do nothing when ctx.server is None (AP not connected)."""
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.server = None

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        await client.game_watcher(mock_bizhawk_context)
        mock_read.assert_not_awaited()


@pytest.mark.asyncio
async def test_game_watcher_skips_when_slot_data_is_none(mock_bizhawk_context):
    """game_watcher should do nothing when ctx.slot_data is None (handshake not complete)."""
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.slot_data = None

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        await client.game_watcher(mock_bizhawk_context)
        mock_read.assert_not_awaited()


@pytest.mark.asyncio
async def test_game_watcher_skips_when_server_socket_is_missing(mock_bizhawk_context):
    """game_watcher should do nothing when ctx.server.socket is temporarily unavailable."""
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.server.socket = None

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        await client.game_watcher(mock_bizhawk_context)
        mock_read.assert_not_awaited()


@pytest.mark.asyncio
async def test_game_watcher_skips_when_server_socket_is_closed(mock_bizhawk_context):
    """game_watcher should do nothing when AP socket is closed."""
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.server.socket.closed = True

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        await client.game_watcher(mock_bizhawk_context)
        mock_read.assert_not_awaited()



@pytest.mark.asyncio
async def test_game_watcher_reconnect_entry_resets_transient_state_once(mock_bizhawk_context):
    """First watcher tick after AP session readiness should reset transient reconnect state and log once."""
    client = KirbyAmClient()
    client.initialize_client()

    client._last_runtime_gate_reason = "non_gameplay_cutscene"
    client._last_shard_poll_log = ("resend", (1,), ())
    client._last_boss_poll_log = ("resend", (2,), ())
    client._last_boss_probe_snapshot = bytes(32)
    client._boss_probe_stream_marker = object()
    client._unsafe_delivery_probe_stream_marker = object()
    client._last_unsafe_delivery_counter_values = {"shadow_kirby_encounters": 2}

    with patch('CommonClient.logger') as mock_logger, \
         patch.object(client, '_runtime_gameplay_state', new_callable=AsyncMock) as mock_gate, \
         patch.object(client, '_load_persistent_state', new_callable=AsyncMock) as mock_load, \
         patch.object(client, '_poll_locations', new_callable=AsyncMock) as mock_poll_locations, \
         patch.object(client, '_poll_boss_defeat_locations', new_callable=AsyncMock) as mock_poll_boss, \
         patch.object(client, '_probe_boss_defeat_candidates', new_callable=AsyncMock) as mock_probe, \
         patch.object(client, '_probe_unsafe_delivery_candidates', new_callable=AsyncMock) as mock_probe_unsafe, \
         patch.object(client, '_deliver_items', new_callable=AsyncMock) as mock_deliver, \
         patch.object(client, '_maybe_report_goal', new_callable=AsyncMock) as mock_goal:
        mock_gate.return_value = (True, "gameplay_active", 300)

        await client.game_watcher(mock_bizhawk_context)

        assert client._watcher_server_ready is True
        assert client._last_runtime_gate_reason is None
        assert client._last_shard_poll_log is None
        assert client._last_boss_poll_log is None
        assert client._last_boss_probe_snapshot is None
        assert client._boss_probe_stream_marker is None
        assert client._unsafe_delivery_probe_stream_marker is None
        assert client._last_unsafe_delivery_counter_values == {}
        mock_logger.info.assert_any_call("KirbyAM: AP session ready; reconnect-safe reconciliation active")
        mock_load.assert_awaited_once()
        mock_poll_locations.assert_awaited_once()
        mock_poll_boss.assert_awaited_once()
        mock_probe.assert_awaited_once()
        mock_probe_unsafe.assert_awaited_once()
        mock_deliver.assert_awaited_once_with(mock_bizhawk_context)
        mock_goal.assert_awaited_once_with(mock_bizhawk_context, ai_state_override=300)

        mock_logger.info.reset_mock()
        await client.game_watcher(mock_bizhawk_context)
        assert not mock_logger.info.called


@pytest.mark.asyncio
async def test_runtime_gameplay_state_active_on_normal_state(mock_bizhawk_context):
    """AI state 300 should be treated as gameplay-active."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(300).to_bytes(4, 'little')]

        active, reason, ai_state = await client._runtime_gameplay_state(mock_bizhawk_context)

    assert active is True
    assert reason == "gameplay_active"
    assert ai_state == 300


@pytest.mark.asyncio
async def test_runtime_gameplay_state_non_gameplay_on_cutscene_state(mock_bizhawk_context):
    """AI state 200 should defer gameplay polling/delivery as non-gameplay."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(200).to_bytes(4, 'little')]

        active, reason, ai_state = await client._runtime_gameplay_state(mock_bizhawk_context)

    assert active is False
    assert reason == "non_gameplay_cutscene"
    assert ai_state == 200


@pytest.mark.asyncio
async def test_runtime_gameplay_state_non_gameplay_on_tutorial_or_menu_state(mock_bizhawk_context):
    """AI state below cutscene threshold should be classified as tutorial/menu non-gameplay."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(100).to_bytes(4, 'little')]

        active, reason, ai_state = await client._runtime_gameplay_state(mock_bizhawk_context)

    assert active is False
    assert reason == "non_gameplay_tutorial_or_menu"
    assert ai_state == 100


@pytest.mark.asyncio
async def test_runtime_gameplay_state_non_gameplay_on_post_normal_state(mock_bizhawk_context):
    """AI state above normal gameplay should be classified as non-gameplay post-normal."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(9999).to_bytes(4, 'little')]

        active, reason, ai_state = await client._runtime_gameplay_state(mock_bizhawk_context)

    assert active is False
    assert reason == "non_gameplay_post_normal"
    assert ai_state == 9999


@pytest.mark.asyncio
async def test_runtime_gameplay_state_fail_open_when_signal_unavailable(mock_bizhawk_context):
    """Missing ai_kirby_state_native should fail open for compatibility."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {}, clear=True), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        active, reason, ai_state = await client._runtime_gameplay_state(mock_bizhawk_context)

    assert active is True
    assert reason == "gate_signal_unavailable"
    assert ai_state is None
    mock_read.assert_not_awaited()


@pytest.mark.asyncio
async def test_game_watcher_defers_polling_and_new_writes_when_non_gameplay(mock_bizhawk_context):
    """In non-gameplay state, watcher defers location/boss polling and new mailbox writes."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.object(client, '_runtime_gameplay_state', new_callable=AsyncMock) as mock_gate, \
         patch.object(client, '_load_persistent_state', new_callable=AsyncMock) as mock_load, \
         patch.object(client, '_poll_locations', new_callable=AsyncMock) as mock_poll_locations, \
         patch.object(client, '_poll_boss_defeat_locations', new_callable=AsyncMock) as mock_poll_boss, \
         patch.object(client, '_probe_boss_defeat_candidates', new_callable=AsyncMock) as mock_probe, \
            patch.object(client, '_probe_unsafe_delivery_candidates', new_callable=AsyncMock) as mock_probe_unsafe, \
         patch.object(client, '_deliver_items', new_callable=AsyncMock) as mock_deliver, \
         patch.object(client, '_maybe_report_goal', new_callable=AsyncMock) as mock_goal:
        mock_gate.return_value = (False, "non_gameplay_cutscene", 200)

        await client.game_watcher(mock_bizhawk_context)

    mock_load.assert_awaited_once()
    mock_poll_locations.assert_not_awaited()
    mock_poll_boss.assert_not_awaited()
    mock_probe.assert_not_awaited()
    mock_probe_unsafe.assert_not_awaited()
    mock_deliver.assert_awaited_once_with(mock_bizhawk_context, allow_new_writes=False)
    mock_goal.assert_awaited_once_with(mock_bizhawk_context, ai_state_override=200)


@pytest.mark.asyncio
async def test_deliver_items_defers_new_write_when_gated(mock_bizhawk_context):
    """Delivery gating should preserve state and avoid writing a new mailbox item."""
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.items_received = [
        Mock(item=3860001, player=1),
    ]

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
            (100).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context, allow_new_writes=False)

    assert client._delivery_pending is False
    assert client._delivered_item_index == 0
    mock_write.assert_not_awaited()


@pytest.mark.asyncio
async def test_poll_boss_defeat_sends_location_checks_for_set_bits(mock_bizhawk_context):
    """Boss defeat transport register with a set bit should produce a LocationChecks send."""
    client = KirbyAmClient()
    client.initialize_client()

    boss1_loc = data.locations["BOSS_DEFEAT_1"].location_id
    mock_bizhawk_context.checked_locations = set()

    with patch.dict(data.transport_ram_addresses, {"boss_defeat_flags": 0x0202C024}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send, \
         patch('CommonClient.logger') as mock_logger:
        # Bit 0 set — Mustard Mountain boss defeated
        mock_read.return_value = [(0x01).to_bytes(4, 'little')]

        await client._poll_boss_defeat_locations(mock_bizhawk_context)

        mock_send.assert_awaited_once_with([
            {"cmd": "LocationChecks", "locations": [boss1_loc]}
        ])
        assert mock_logger.info.called
        assert "resending boss-defeat LocationChecks missing on server" in mock_logger.info.call_args.args[0]
        assert mock_logger.info.call_args.args[1] == [boss1_loc]


@pytest.mark.asyncio
async def test_poll_boss_defeat_skips_already_server_acknowledged(mock_bizhawk_context):
    """No LocationChecks sent when boss defeat bit is set but server already acknowledged it."""
    client = KirbyAmClient()
    client.initialize_client()

    boss1_loc = data.locations["BOSS_DEFEAT_1"].location_id
    mock_bizhawk_context.checked_locations = {boss1_loc}

    with patch.dict(data.transport_ram_addresses, {"boss_defeat_flags": 0x0202C024}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [(0x01).to_bytes(4, 'little')]

        await client._poll_boss_defeat_locations(mock_bizhawk_context)

        mock_send.assert_not_awaited()
        assert mock_logger.debug.called
        assert "dedupe suppressed boss-defeat LocationChecks" in mock_logger.debug.call_args.args[0]
        assert mock_logger.debug.call_args.args[1] == [boss1_loc]


@pytest.mark.asyncio
async def test_poll_boss_defeat_skips_when_address_missing(mock_bizhawk_context):
    """When boss_defeat_flags address is not in addresses.json the method should no-op."""
    client = KirbyAmClient()
    client.initialize_client()

    native_backup = dict(data.transport_ram_addresses)
    transport_without_boss = {k: v for k, v in data.transport_ram_addresses.items() if k != "boss_defeat_flags"}

    with patch.dict(data.transport_ram_addresses, transport_without_boss, clear=True), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        await client._poll_boss_defeat_locations(mock_bizhawk_context)
        mock_read.assert_not_awaited()


@pytest.mark.asyncio
async def test_shard_poll_does_not_trigger_boss_defeat_locations(mock_bizhawk_context):
    """Shard bitfield polling must not send boss-defeat location checks."""
    client = KirbyAmClient()
    client.initialize_client()

    boss1_loc = data.locations["BOSS_DEFEAT_1"].location_id
    mock_bizhawk_context.checked_locations = set()

    with patch.dict(data.native_ram_addresses, {}, clear=True), \
         patch.dict(data.transport_ram_addresses, {"shard_bitfield": 0x0202C000}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send:
        # bit 0 set in shard bitfield
        mock_read.return_value = [(0x01).to_bytes(4, 'little')]

        await client._poll_locations(mock_bizhawk_context)

        # Should only send SHARD_1, not BOSS_DEFEAT_1
        calls = mock_send.await_args_list
        assert len(calls) == 1
        sent_locations = calls[0].args[0][0]["locations"]
        assert boss1_loc not in sent_locations
