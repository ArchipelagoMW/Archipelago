""" Module which adds client commands to a given Archipelago Client. """
import Utils

try:
    from worlds.tracker.TrackerClient import (TrackerCommandProcessor as
        ClientCommandProcessor, TrackerGameContext as CommonContext)
except ImportError:
    from CommonClient import ClientCommandProcessor, CommonContext

from CommonClient import logger
from .energy_link_processor import EnergyLinkProcessor

class EnergyLinkCommandProcessor(ClientCommandProcessor):
    """ EnergyLink client commands. """
    energy_link: EnergyLinkProcessor

    def __init__(self, ctx: CommonContext, server_address: str = None):
        if server_address:
            ctx.server_address = server_address
        super().__init__(ctx)

        self.energy_link = EnergyLinkProcessor(ctx)

    def _cmd_send_energy(self, arg: str):
        """ Sends an amount of energy to the server, which is pulled from Luigi's wallet.
        Each point of energy is worth a single coin (rank worth 5000)"""
        if not _validate_processor_context(self.ctx):
            return

        Utils.async_start(self.energy_link.send_energy_async(arg))

    def _cmd_display_energy(self):
        """ Displays the current amount of energy available from the server. """
        if not _validate_processor_context(self.ctx):
            return

        Utils.async_start(self.energy_link.get_energy_async())

    def _cmd_request_energy(self, arg: str):
        """
        Requests energy from the server, which each point has the worth of a single coin (rank worth 5000).
        Will return up to the requested amount based upon the team's energy pool.
        """
        if not _validate_processor_context(self.ctx):
            return

        Utils.async_start(self.energy_link.request_energy_async(arg))

def _validate_processor_context(ctx: CommonContext):
    has_energy_link: bool = ctx.energy_link is not None
    is_connected_to_server: bool = ctx.server is not None
    if isinstance(ctx, CommonContext) and has_energy_link and is_connected_to_server:
        return True
    logger.warning("Please connect the client to the AP server before continuing.")
    return False
