from CommonClient import ClientCommandProcessor
from typing import TYPE_CHECKING

# I don't know what is going on here, but it works.
if TYPE_CHECKING:
    from . import KH2Context
else:
    KH2Context = object


class KH2CommandProcessor(ClientCommandProcessor):
    ctx: KH2Context

    def _cmd_receive_notif(self, notification_type=""):
        """Change receive notification type.Valid Inputs:Puzzle, Info, Chest and None
        Puzzle: Puzzle Piece Popup when you receive an item.
        Info: Displays the Information notification when you receive an item.
        Chest: Displays the Chest notification when you receive an item.
        None: Toggle off any of the receiving notifications.
        """
        notification_type = notification_type.lower()
        if notification_type in {"puzzle", "info", "chest", "none"}:
            temp_client_settings = self.ctx.client_settings["receive_popup_type"]
            self.ctx.client_settings["receive_popup_type"] = notification_type
            self.output(f"Changed receive notification type from {temp_client_settings} to {self.ctx.client_settings['receive_popup_type']}")
        else:
            self.output(f"Unknown receive notification type:{notification_type}. Valid Inputs: Puzzle, Info, Chest, None")

    def _cmd_send_notif(self, notification_type=""):
        """Change send notification type.Valid Inputs:Puzzle, Info, Chest and None
        Puzzle: Puzzle Piece Popup when you send an item.
        Info: Displays the Information notification when you send an item.
        Chest: Displays the Chest notification when you send an item.
        None: Toggle off any of the receiving notifications.
        """
        notification_type = notification_type.lower()
        if notification_type in {"puzzle", "info", "chest", "none"}:
            temp_client_settings = self.ctx.client_settings["send_popup_type"]
            self.ctx.client_settings["send_popup_type"] = notification_type
            # doing it in this order to make sure it actually changes
            self.output(f"Changed send notification type from {temp_client_settings} to {self.ctx.client_settings['send_popup_type']}")
        else:
            self.output(f"Unknown send notification type:{notification_type}. Valid Inputs: Puzzle, Info, Chest, None")

    def _cmd_change_send_truncation_priority(self, priority=""):
        """Change what gets truncated first when using Chest or Puzzle piece send notification. Playername min is 5 and ItemName is 15"""
        priority = priority.lower()
        if priority in {"playername", "itemname"}:
            temp_client_settings = self.ctx.client_settings["send_truncate_first"]
            self.ctx.client_settings["send_truncate_first"] = priority
            self.output(f"Changed receive notification type truncation from {temp_client_settings} to {self.ctx.client_settings['send_truncate_first']}")
        else:
            self.output(f"Unknown priority: {priority}. Valid Inputs: PlayerName, ItemName")

    def _cmd_change_receive_truncation_priority(self, priority=""):
        """Change what gets truncated first when using Chest or Puzzle piece receive notification. Playername min is 5 and ItemName is 15"""
        priority = priority.lower()
        if priority in {"playername", "itemname"}:
            temp_client_settings = self.ctx.client_settings["receive_truncate_first"]
            self.ctx.client_settings["receive_truncate_first"] = priority
            self.output(f"Changed receive notification truncation type from {temp_client_settings} to {self.ctx.client_settings['receive_truncate_first']}")
        else:
            self.output(f"Unknown priority: {priority}. Valid Inputs: PlayerName, ItemName")

    def _cmd_deathlink(self):
        """Toggles Deathlink"""
        if self.ctx.deathlink_toggle:
            # self.ctx.tags.add("DeathLink")
            self.ctx.deathlink_toggle = False
            self.output(f"Death Link turned off")
        else:
            self.ctx.deathlink_toggle = True
            self.output(f"Death Link turned on")

    def _cmd_add_to_blacklist(self, player_name: str = ""):
        """Adds player to deathlink blacklist"""
        if player_name not in self.ctx.deathlink_blacklist:
            self.ctx.deathlink_blacklist.append(player_name)

    def _cmd_remove_from_blacklist(self, player_name: str = ""):
        """Removes player from the deathlink blacklist"""
        if player_name in self.ctx.deathlink_blacklist:
            self.ctx.deathlink_blacklist.remove(player_name)

    #def _cmd_kill(self):
    #    self.ctx.kh2_write_byte(0x810000, 1)

    #def _cmd_chest(self,itemid:int):
    #    from .RecieveItems import to_khscii
    #    from .ReadAndWrite import kh2_write_bytes,kh2_write_byte
    #    displayed_string = to_khscii(self.ctx,"Yessir")
#
    #    kh2_write_byte(self.ctx, 0x800150, int(itemid))
    #    kh2_write_bytes(self.ctx, address = 0x800154,value = displayed_string)
    #    kh2_write_byte(self.ctx,  0x800000, 3)
