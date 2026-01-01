from enum import Enum
from logging import Logger
from typing import List, Optional

from .Items import CivVIItemData
from .TunerClient import TunerClient, TunerConnectionException, TunerTimeoutException


class ConnectionState(Enum):
    DISCONNECTED = 0
    IN_GAME = 1
    IN_MENU = 2


class CivVIInterface:
    logger: Logger
    tuner: TunerClient
    last_error: Optional[str] = None

    def __init__(self, logger: Logger):
        self.logger = logger
        self.tuner = TunerClient(logger)

    async def is_in_game(self) -> ConnectionState:
        command = "IsInGame()"
        try:
            result = await self.tuner.send_game_command(command)
            if result == "false":
                return ConnectionState.IN_MENU
            self.last_error = None
            return ConnectionState.IN_GAME
        except TunerTimeoutException:
            self.print_connection_error(
                "Not connected to game, waiting for connection to be available")
            return ConnectionState.DISCONNECTED
        except TunerConnectionException as e:
            if "The remote computer refused the network connection" in str(e):
                self.print_connection_error(
                    "Unable to connect to game. Verify that the tuner is enabled. Attempting to reconnect")
            else:
                self.print_connection_error(
                    "Not connected to game, waiting for connection to be available")
            return ConnectionState.DISCONNECTED
        except Exception as e:
            if "attempt to index a nil valuestack traceback" in str(e) \
                    or ".. is not supported for string .. nilstack traceback" in str(e):
                return ConnectionState.IN_MENU
        return ConnectionState.DISCONNECTED

    def print_connection_error(self, error: str) -> None:
        if error != self.last_error:
            self.last_error = error
            self.logger.info(error)

    async def give_item_to_player(self, item: CivVIItemData, sender: str = "", amount: int = 1, game_id_override: Optional[str] = None) -> None:
        if game_id_override:
            item_id = f'"{game_id_override}"'
        else:
            item_id = item.civ_vi_id

        command = f"HandleReceiveItem({item_id}, \"{item.name}\", \"{item.item_type.value}\", \"{sender}\", {amount})"
        await self.tuner.send_game_command(command)

    async def resync(self) -> None:
        """Has the client resend all the checked locations"""
        command = "Resync()"
        await self.tuner.send_game_command(command)

    async def check_victory(self) -> bool:
        command = "ClientGetVictory()"
        result = await self.tuner.send_game_command(command)
        return result == "true"

    async def get_checked_locations(self) -> List[str]:
        command = "GetUnsentCheckedLocations()"
        result = await self.tuner.send_game_command(command, 2048 * 4)
        return result.split(",")

    async def get_deathlink(self) -> str:
        """returns either "false" or the name of the unit that killed the player's unit"""
        command = "ClientGetDeathLink()"
        result = await self.tuner.send_game_command(command)
        return result

    async def kill_unit(self, message: str) -> None:
        command = f"KillUnit(\"{message}\")"
        await self.tuner.send_game_command(command)

    async def get_last_received_index(self) -> int:
        command = "ClientGetLastReceivedIndex()"
        result = await self.tuner.send_game_command(command)
        return int(result)

    async def send_notification(self, item: CivVIItemData, sender: str = "someone") -> None:
        command = f"GameCore.NotificationManager:SendNotification(GameCore.NotificationTypes.USER_DEFINED_2, \"{item.name} Received\", \"You have received {item.name} from \" .. \"{sender}\", 0, {item.civ_vi_id})"
        await self.tuner.send_command(command)

    async def decrease_gold_by_percent(self, percent: int, message: str) -> None:
        command = f"DecreaseGoldByPercent({percent}, \"{message}\")"
        await self.tuner.send_game_command(command)

    async def decrease_faith_by_percent(self, percent: int, message: str) -> None:
        command = f"DecreaseFaithByPercent({percent}, \"{message}\")"
        await self.tuner.send_game_command(command)

    async def decrease_era_score_by_amount(self, amount: int, message: str) -> None:
        command = f"DecreaseEraScoreByAmount({amount}, \"{message}\")"
        await self.tuner.send_game_command(command)

    async def set_max_allowed_era(self, count: int) -> None:
        command = f"SetMaxAllowedEra(\"{count}\")"
        await self.tuner.send_game_command(command)

    async def get_max_allowed_era(self) -> int:
        command = "ClientGetMaxAllowedEra()"
        result = await self.tuner.send_game_command(command)
        if result == "":
            return -1
        return int(result)
