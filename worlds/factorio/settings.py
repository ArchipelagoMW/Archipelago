import typing

import settings


class FactorioSettings(settings.Group):
    class Executable(settings.UserFilePath):
        is_exe = True

    class ServerSettings(settings.OptionalUserFilePath):
        """
        by default, no settings are loaded if this file does not exist. \
If this file does exist, then it will be used.
        server_settings: "factorio\\\\data\\\\server-settings.json"
        """

    class FilterItemSends(settings.Bool):
        """Whether to filter item send messages displayed in-game to only those that involve you."""

    class BridgeChatOut(settings.Bool):
        """Whether to send chat messages from players on the Factorio server to Archipelago."""

    executable: Executable = Executable("factorio/bin/x64/factorio")
    server_settings: typing.Optional[ServerSettings] = None
    filter_item_sends: typing.Union[FilterItemSends, bool] = False
    bridge_chat_out: typing.Union[BridgeChatOut, bool] = True
