"""Logic holder class that maintains the state of all logic conditions for MN64."""

from typing import Any, Dict


class MN64LogicHolder:
    """
    Logic holder class that retains the state of all logic conditions used in lambda functions.

    This class is passed to all lambda functions defined in the logic files (e.g., for medal_of_flames).    It maintains the current state of all items, abilities, flags, and conditions that determine
    accessibility in the game logic.

    Key Management:
    - Keys are tracked by count (silver_key_count, gold_key_count, diamond_key_count)
    - has_*_key() methods automatically track accessible doors and require sufficient keys
    - can_open_mixed_doors() supports checking multiple key types at once

    Usage examples:
    - l.has_silver_key()          # Check for silver keys (accounts for accessible doors)
    - l.has_silver_key(2)         # Check for at least 2 silver keys minimum
    - l.can_open_mixed_doors(silver_doors=1, gold_doors=1)  # 1 silver + 1 gold
    """

    def __init__(self) -> None:
        """Initialize all logic properties to False by default."""
        # Items and Keys (now using counts instead of booleans)
        self.silver_key_count: int = 0
        self.gold_key_count: int = 0
        self.diamond_key_count: int = 0
        self.jump_gym_key: bool = False  # This one stays boolean as it's a special key

        # Context tracking for key consumption logic
        self._current_location_context: str = ""

        # Track accessible key-consuming locations (shared across evaluations)
        self._accessible_silver_doors: set = set()
        self._accessible_gold_doors: set = set()
        self._accessible_diamond_doors: set = set()

        # Equipment and Tools
        self.windup_camera: bool = False
        self.chain_pipe: bool = False
        self.ice_kunai: bool = False
        self.medal_of_flames: bool = False
        self.bazooka: bool = False
        self.bombs: bool = False
        self.flute: bool = False
        self.meat_hammer: bool = False

        # Characters and Abilities
        self.mermaid: bool = False
        self.mini_ebisumaru: bool = False
        self.sudden_impact: bool = False
        self.jetpack: bool = False

        self.goemon: bool = False
        self.yae: bool = False
        self.ebisumaru: bool = False
        self.sasuke: bool = False

        # Game Progression Flags
        self.beat_tsurami: bool = False
        self.congo_defeated: bool = False
        self.ghost_toys_defeated: bool = False
        self.beat_thaisambda: bool = False

        # Crane Game Related
        self.power_on_crane_game: bool = False

        # Character Specific Items/Batteries
        self.sasuke_battery_1: bool = False
        self.sasuke_battery_2: bool = False
        self.sasuke_dead: bool = False

        # Transportation and Access
        self.superpass: bool = False

        # Quest and Event States
        self.event_cucumber_quest_need_key: bool = False
        self.requires_visiting_ghost_toys_entrance_ebisumaru: bool = False
        self.moving_boulder_in_forest: bool = False
        self.visited_witch: bool = False
        self.kyushu_fly: bool = False
        # self.fish_quest: bool = False
        self.cucumber: bool = False
        self.triton_horn: bool = False
        self.event_cucumber_quest_find_priest: bool = False
        self.mokubei_brother: bool = False

        # Character Interactions and Story Flags
        self.omitsu_talked: bool = False
        self.strength_count: int = 0
        self.all_miracle_items: bool = False
        self.achilles_heel: bool = False

        # Item Counters
        self.silver_fortune_doll_count: int = 0
        self.gold_fortune_doll_count: int = 0
        self.golden_health_count: int = 0
        self.normal_health_count: int = 0

    # Key management methods
    def has_silver_key(self, min_keys: int = 1, location_name: str = None) -> bool:
        """Check if we have enough silver keys for all accessible silver key doors."""
        context = location_name or self._current_location_context

        # If this is a silver key-consuming transition, add it to the set
        if context and "silver key" in context.lower():
            self._accessible_silver_doors.add(context)

        # We need enough keys for all accessible doors plus any additional minimum
        required_keys = max(min_keys, len(self._accessible_silver_doors))
        return self.silver_key_count >= required_keys

    def has_gold_key(self, min_keys: int = 1, location_name: str = None) -> bool:
        """Check if we have enough gold keys for all accessible gold key doors."""
        context = location_name or self._current_location_context

        # If this is a gold key-consuming transition, add it to the set
        if context and "gold key" in context.lower():
            self._accessible_gold_doors.add(context)

        # We need enough keys for all accessible doors plus any additional minimum
        required_keys = max(min_keys, len(self._accessible_gold_doors))
        return self.gold_key_count >= required_keys

    def has_diamond_key(self, min_keys: int = 1, location_name: str = None) -> bool:
        """Check if we have enough diamond keys for all accessible diamond key doors."""
        context = location_name or self._current_location_context

        # If this is a diamond key-consuming transition, add it to the set
        if context and "diamond key" in context.lower():
            self._accessible_diamond_doors.add(context)

        # We need enough keys for all accessible doors plus any additional minimum
        required_keys = max(min_keys, len(self._accessible_diamond_doors))
        return self.diamond_key_count >= required_keys

    def can_open_mixed_doors(self, silver_doors: int = 0, gold_doors: int = 0, diamond_doors: int = 0) -> bool:
        """Check if we have enough keys to open multiple doors of different types in the same area."""
        return self.silver_key_count >= silver_doors and self.gold_key_count >= gold_doors and self.diamond_key_count >= diamond_doors

    def reset_lock_tracking(self) -> None:
        """Reset the context tracking but keep door tracking across evaluations."""
        self._current_location_context = ""
        # NOTE: We don't clear the door sets here as they represent cumulative accessibility

    def clear_all_door_tracking(self) -> None:
        """Clear all door tracking. Use this for fresh logic evaluation sessions."""
        self._accessible_silver_doors.clear()
        self._accessible_gold_doors.clear()
        self._accessible_diamond_doors.clear()
        self._current_location_context = ""

    def get_accessible_doors_count(self, key_type: str) -> int:
        """Get the current count of accessible key-consuming doors for a key type."""
        if key_type == "silver":
            return len(self._accessible_silver_doors)
        elif key_type == "gold":
            return len(self._accessible_gold_doors)
        elif key_type == "diamond":
            return len(self._accessible_diamond_doors)
        return 0

    def get_available_keys(self, key_type: str) -> int:
        """Get the current count of available keys for a key type."""
        if key_type == "silver":
            return self.silver_key_count
        elif key_type == "gold":
            return self.gold_key_count
        elif key_type == "diamond":
            return self.diamond_key_count
        return 0

    def set_state(self, property_name: str, value: bool) -> None:
        """
        Set the state of a specific property.

        Args:
            property_name: The name of the property to set
            value: The boolean value to set
        """
        if hasattr(self, property_name):
            setattr(self, property_name, value)
        else:
            raise ValueError(f"Property '{property_name}' does not exist in MN64LogicHolder")

    def get_state(self, property_name: str) -> bool:
        """
        Get the state of a specific property.

        Args:
            property_name: The name of the property to get

        Returns:
            The boolean value of the property
        """
        if hasattr(self, property_name):
            return getattr(self, property_name)
        else:
            raise ValueError(f"Property '{property_name}' does not exist in MN64LogicHolder")

    def get_all_states(self) -> Dict[str, bool]:
        """
        Get all property states as a dictionary.

        Returns:
            Dictionary mapping property names to their boolean values
        """
        return {attr: getattr(self, attr) for attr in dir(self) if not attr.startswith("_") and not callable(getattr(self, attr))}

    def set_multiple_states(self, states: Dict[str, bool]) -> None:
        """
        Set multiple property states at once.

        Args:
            states: Dictionary mapping property names to boolean values
        """
        for property_name, value in states.items():
            self.set_state(property_name, value)

    def reset_all(self) -> None:
        """Reset all properties to False."""
        for attr in dir(self):
            if not attr.startswith("_") and not callable(getattr(self, attr)):
                setattr(self, attr, False)

    def __repr__(self) -> str:
        """String representation showing current state of all properties."""
        states = self.get_all_states()
        true_states = [name for name, value in states.items() if value]
        return f"MN64LogicHolder(active_states={true_states})"
