""" Module which stores the async operations used by the EnergyLinkCommandProcessor. """

import inspect
import Utils

from CommonClient import CommonContext, logger
from ...Wallet import Wallet
from .energy_link import EnergyLink

class EnergyLinkProcessor:
    """
    Service to be used with the EnergyLinkCommandProcessor.
    """
    _ctx: CommonContext
    energy_link: EnergyLink
    wallet: Wallet

    def __init__(self, ctx: CommonContext):
        self._ctx = ctx
        self.energy_link = EnergyLink(ctx)

        if not hasattr(ctx, 'wallet'):
            raise AttributeError("Could not resolve wallet from the provided client context.")
        self.wallet = ctx.wallet

    async def send_energy_async(self, arg: str):
        """
        Withdrawls currency from Luigi's Mansion and store it as energy in the team's Energy pool.

        :param arg: The amount of energy to be stored. This amount is multiplied by the lowest currency amount
        in Luigi's Mansion.
        """
        is_valid, amount = _validate_processor_arg(arg)
        if not is_valid:
            return

        if not _check_if_in_game(self._ctx):
            logger.error("Make sure that Luigi's Mansion is running before sending energy.")
            return

        wallet_amount = self.wallet.get_wallet_worth()
        calculated_amount = self.wallet.get_calculated_amount_worth(amount)
        if calculated_amount >  wallet_amount:
            logger.error("Cannot withdrawl the requested amount (%s) / calculated amount (%s) from Luigi's wallet.", amount, calculated_amount)
            return

        self.wallet.remove_amount_from_wallet(amount)

        logger.info("Sending %s to team %s's energy pool.", amount, self._ctx.team)
        await self.energy_link.send_energy_async(amount)

    async def request_energy_async(self, arg: str):
        """
        Requests currency from the team's Energy pool to be converted into currency for Luigi's Mansion.

        :param arg: The amount of energy to be withdrawn. This amount is multiplied by the lowest currency amount
        in Luigi's Mansion.
        """
        is_valid, amount = _validate_processor_arg(arg)
        if not is_valid:
            return

        if not _check_if_in_game(self._ctx):
            logger.error("Make sure that Luigi's Mansion is running before requesting energy.")
            return

        await self.energy_link.request_energy_async(amount)
        logger.info("Requested %s energy.", amount)

    async def get_energy_async(self):
        """
        Gets the amount of energy available in the team's pool.
        """
        await self.energy_link.get_energy_async()

        retries:int  = 0
        energy_amount: int = None
        while retries < 5:
            try:
                energy_amount = self._ctx.stored_data[self.energy_link.get_ap_key()]
                break
            except KeyError:
                retries += 1
                await Utils.asyncio.sleep(1)

        if energy_amount is None:
            logger.error("Timed out getting energy information from server, please try again later.")

        logger.info("Team %s's energy: %s.", self._ctx.team, energy_amount)

def _validate_processor_arg(amount: str):
    try:
        amount_as_int = int(amount)
    except ValueError:
        logger.info("The amount must be a number value.")
        return False, 0
    if amount_as_int <= 0:
        logger.info("The amount requested needs to be greater than zero.")
        return False, 0
    return True, amount_as_int

def _check_if_in_game(ctx):
    if not hasattr(ctx, 'check_ingame') and inspect.isfunction(ctx.check_ingame()):
        return False
    if not ctx.check_ingame():
        return False
    return True
