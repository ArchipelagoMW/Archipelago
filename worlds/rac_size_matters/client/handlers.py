from __future__ import annotations

from NetUtils import ClientStatus

from ..core import ARMOUR_SET_CHECKS

# Challenge handler

class ChallengeHandlerMixin:
    def _on_challenge_armour_earned(self, loc_name: str) -> None:
        """Fired when a new armour piece is detected after a challenge completes."""
        self._pending_challenge_checks.append(loc_name)


# Cutscene handler

class CutsceneHandlerMixin:
    async def _send_goal_status(self) -> None:
        if not self.finished_game:
            await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            self.finished_game = True


# Events handler

class EventsHandlerMixin:
    async def _send_playing_status(self) -> None:
        """Tell the server we're actually in-game, not sitting at the main
        menu. Matches RAC3's pcsx2_sync_task, which sends CLIENT_PLAYING the
        moment its main_menu flag flips False -> True (i.e. a save was just
        loaded) — fired here from GameOrchestrator's on_initial_load hook,
        our equivalent edge."""
        await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_PLAYING}])

    def _on_armour_pickup_update(self, key: str, new_value: int) -> None:
        del key, new_value

    def _on_menu_close_for_armour_sets(self) -> None:
        if not self._armour_set_checks_enabled:
            return
        self._armour_slot_state.update(self.pine)
        slot_values = self._armour_slot_state.memory_values
        for name, check in ARMOUR_SET_CHECKS.items():
            if check.matches(slot_values):
                self._append_location_by_name(name)
