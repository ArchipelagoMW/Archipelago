"""Tests for item notification formatting and location name resolution."""
from unittest.mock import Mock, patch

import pytest

from ..data import data
from ..client import KirbyAmClient


def test_item_name_resolves_from_data_items():
    """_item_name should resolve item labels from data.items when available."""
    client = KirbyAmClient()
    ctx = Mock()
    ctx.item_names = None  # No AP context item names

    # Pick a real item from data.items to test
    if data.items:
        item_id, item_data = next(iter(data.items.items()))
        name = client._item_name(ctx, item_id, 1)
        assert name == item_data.label, f"Expected {item_data.label}, got {name}"
    else:
        pytest.skip("No items in data.items available for test")


def test_item_name_fallback_unknown_item():
    """_item_name should provide Item ID fallback for unknown items."""
    client = KirbyAmClient()
    ctx = Mock()
    ctx.item_names = None

    # Use an item ID that doesn't exist
    name = client._item_name(ctx, 999999999, 1)
    assert name == "Item 999999999", f"Expected fallback format, got {name}"


def test_item_name_prefers_context_item_names():
    """_item_name should prefer AP context item_names over data.items."""
    client = KirbyAmClient()
    ctx = Mock()

    # Mock the context item_names lookup
    mock_lookup = Mock()
    mock_lookup.lookup_in_slot = Mock(return_value="ContextResolvedName")
    ctx.item_names = mock_lookup

    name = client._item_name(ctx, 123456, 1)
    assert name == "ContextResolvedName"
    mock_lookup.lookup_in_slot.assert_called_once_with(123456, 1)


def test_location_name_resolves_from_data():
    """_location_name should resolve location labels from data.locations."""
    client = KirbyAmClient()

    # Pick a real location from data.locations
    location_data = next(
        (loc for loc in data.locations.values() if loc.location_id is not None),
        None,
    )
    if location_data is None:
        pytest.skip("No locations with non-None location_id available for test")

    name = client._location_name(location_data.location_id)
    assert name == location_data.label, \
        f"Expected {location_data.label} for location_id {location_data.location_id}, got {name}"


def test_location_name_fallback_unknown_location():
    """_location_name should provide Location ID fallback for unknown locations."""
    client = KirbyAmClient()

    # Use a location ID that doesn't exist
    name = client._location_name(999999999)
    assert name == "Location 999999999", f"Expected fallback format, got {name}"


def test_location_name_handles_none():
    """_location_name should handle None gracefully."""
    client = KirbyAmClient()
    name = client._location_name(None)
    assert name == "", f"Expected empty string for None, got {name}"


def test_send_notification_omits_sender_includes_receiver_and_location():
    """_maybe_emit_send_notification should omit sender, include receiver and location in message."""
    client = KirbyAmClient()
    client.initialize_client()
    ctx = Mock()
    ctx.slot = 1
    ctx.bizhawk_ctx = Mock()
    ctx.item_names = None
    ctx.player_names = {2: "OtherPlayer"}

    # Find a real item and location to use
    test_item_id = None
    test_item_data = None
    test_location_id = None

    if data.items:
        test_item_id, test_item_data = next(iter(data.items.items()))
    if data.locations:
        test_location_id = next(
            (loc.location_id for loc in data.locations.values() if loc.location_id is not None),
            None
        )

    if test_item_id is None or test_location_id is None:
        pytest.skip("Not enough test data to run this test")

    args = {
        "type": "ItemSend",
        "item": Mock(item=test_item_id, player=1, location=test_location_id),
        "receiving": 2,
    }

    with patch('worlds.kirbyam.client.bizhawk.display_message') as mock_display:
        with patch('worlds.kirbyam.client.Utils.async_start'):
            client._maybe_emit_send_notification(ctx, args)

        # Verify display_message was called with proper formatting
        assert mock_display.called, "display_message should be called"
        message = mock_display.call_args[0][1]

        # Format: "You sent <item> to <receiver> at <location>".
        assert "You sent" in message
        assert " at " in message
        expected_location = client._location_name(test_location_id)
        assert expected_location in message
        assert "OtherPlayer" in message or "Player 2" in message
        assert test_item_data is not None and test_item_data.label in message, \
            f"Expected resolved item label {test_item_data.label!r} in message: {message}"


def test_send_notification_deduplicates_by_key():
    """_maybe_emit_send_notification should deduplicate by (item, sender, receiver, location)."""
    client = KirbyAmClient()
    client.initialize_client()
    ctx = Mock()
    ctx.slot = 1
    ctx.bizhawk_ctx = Mock()
    ctx.item_names = None
    ctx.player_names = {}

    args = {
        "type": "ItemSend",
        "item": Mock(item=12345, player=1, location=67890),
        "receiving": 2,
    }

    with patch('worlds.kirbyam.client.bizhawk.display_message') as mock_display:
        with patch('worlds.kirbyam.client.Utils.async_start'):
            # First call should go through
            client._maybe_emit_send_notification(ctx, args)
            first_call_count = mock_display.call_count

            # Second identical call should be deduplicated
            client._maybe_emit_send_notification(ctx, args)
            second_call_count = mock_display.call_count

            assert first_call_count >= 1, "First call should trigger display"
            assert second_call_count == first_call_count, "Duplicate should be suppressed"


def test_send_notification_only_emits_own_items():
    """_maybe_emit_send_notification should only emit when sender_id matches ctx.slot."""
    client = KirbyAmClient()
    client.initialize_client()
    ctx = Mock()
    ctx.slot = 1
    ctx.bizhawk_ctx = Mock()
    ctx.item_names = None
    ctx.player_names = {}

    # Item from different sender
    args = {
        "type": "ItemSend",
        "item": Mock(item=12345, player=3, location=67890),  # player 3, but ctx.slot is 1
        "receiving": 2,
    }

    with patch('worlds.kirbyam.client.bizhawk.display_message') as mock_display:
        with patch('worlds.kirbyam.client.Utils.async_start'):
            client._maybe_emit_send_notification(ctx, args)

        # Should not emit for items from other players
        assert mock_display.call_count == 0, "Should not emit notifications for other players' items"


def test_send_notification_ignores_non_itemsend_events():
    """_maybe_emit_send_notification should ignore non-ItemSend event types."""
    client = KirbyAmClient()
    client.initialize_client()
    ctx = Mock()
    ctx.slot = 1

    args = {
        "type": "SomeOtherEventType",
        "item": Mock(item=12345, player=1, location=67890),
        "receiving": 2,
    }

    with patch('worlds.kirbyam.client.bizhawk.display_message') as mock_display:
        with patch('worlds.kirbyam.client.Utils.async_start'):
            client._maybe_emit_send_notification(ctx, args)

        # Should not emit for non-ItemSend types
        assert mock_display.call_count == 0, "Should not emit for non-ItemSend events"


def test_player_name_handles_archipelago_id():
    """_player_name should return 'Archipelago' for player_id 0."""
    client = KirbyAmClient()
    ctx = Mock()
    ctx.player_names = {}

    name = client._player_name(ctx, 0)
    assert name == "Archipelago"


def test_player_name_resolves_from_context():
    """_player_name should resolve from ctx.player_names when available."""
    client = KirbyAmClient()
    ctx = Mock()
    ctx.player_names = {1: "Alice", 2: "Bob"}

    name = client._player_name(ctx, 1)
    assert name == "Alice"


def test_player_name_fallback_player_id():
    """_player_name should provide Player ID fallback."""
    client = KirbyAmClient()
    ctx = Mock()
    ctx.player_names = {}

    name = client._player_name(ctx, 5)
    assert name == "Player 5"
