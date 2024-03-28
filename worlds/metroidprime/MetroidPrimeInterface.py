from logging import Logger
from worlds.metroidprime.DolphinClient import GC_GAME_ID_ADDRESS, DolphinClient, DolphinException

METROID_PRIME_ID = b"GM8E01"

class MetroidPrimeInterface:
  _dolphin_client: DolphinClient
  connection_status: str
  logger: Logger

  def __init__(self, logger) -> None:
    self.logger = logger
    self._dolphin_client = DolphinClient(logger)

  def connect_to_game(self):
    self._dolphin_client.connect()
    self.logger.info("Connected to Dolphin Emulator")
    if self._dolphin_client.read_address(GC_GAME_ID_ADDRESS, 6) != METROID_PRIME_ID:
      self.logger.error(f"Connected to the wrong game, please connect to Metroid Prime V1 English ({METROID_PRIME_ID})")
      self.disconnect_from_game()

  def disconnect_from_game(self):
    self._dolphin_client.disconnect()
    self.logger.info("Disconnected from Dolphin Emulator")

  def is_connected(self):
    return self._dolphin_client.is_connected()

  def is_in_playable_game(self) -> bool:
    """ Check if the player is in the actual game rather than the main menu """
    return False

  def get_current_region(self):
    pass

  def give_item_to_player(self, item_id):
    pass

  def check_for_new_locations(self):
    pass
