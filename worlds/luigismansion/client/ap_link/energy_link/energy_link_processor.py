""" Module which stores the async operations used by the EnergyLinkCommandProcessor. """

import inspect
import Utils

from CommonClient import CommonContext, logger
from ...Wallet import Wallet
from .energy_link import EnergyLink, EnergyLinkConstants

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
        Withdraws currency from Luigi's Mansion and store it as energy in the team's Energy pool.

        :param arg: The amount of energy to be stored.
        in Luigi's Mansion.
        """
        is_valid, amount = _validate_processor_arg(arg)
        if not is_valid:
            return
        if not _has_energy_link_tag(self._ctx):
            return
        if not _check_if_in_game(self._ctx):
            logger.error("Make sure that Luigi's Mansion is running before sending energy.")
            return

        wallet_amount = self.wallet.get_wallet_worth()
        if wallet_amount == 0:
            logger.error("Luigi's wallet is empty, cannot send energy at this time.")
            return

        minimum_amount = self.wallet.get_calculated_amount_worth(1)
        if amount < minimum_amount:
            logger.info("Minimum energy request amount is %s, cannot send the amount %s.", minimum_amount, amount)
            return

        logger.info("Attempting to withdraw %sG to be sent as energy to team %s.", amount, self._ctx.team)
        remainder = _remove_amount_from_wallet(self.wallet, amount)

        amount -= remainder
        logger.info("Sending %s energy to team %s's pool.", int(amount), self._ctx.team)
        await self.energy_link.send_energy_async(int(amount))

    async def request_energy_async(self, arg: str):
        """
        Requests currency from the team's Energy pool to be converted into currency for Luigi's Mansion.

        :param arg: The amount of energy to be withdrawn.
        in Luigi's Mansion.
        """
        is_valid, amount = _validate_processor_arg(arg)
        if not is_valid:
            return

        if not _check_if_in_game(self._ctx):
            logger.error("Make sure that Luigi's Mansion is running before requesting energy.")
            return

        if not _has_energy_link_tag(self._ctx):
            return

        minimum_worth = self.wallet.get_calculated_amount_worth(1)
        result, remainder = divmod(amount, minimum_worth)
        if result <= 0:
            logger.info("Minimum energy request amount is %s, cannot request the amount %s.", minimum_worth, amount)
            return

        if remainder > 0:
            logger.info("Energy requests must be divisble by %s. %s energy wasn't requested.", minimum_worth, remainder)

        usable_amount = int(result * minimum_worth)
        await self.energy_link.request_energy_async(usable_amount)
        logger.info("Requested %s energy from team %s's pool.", usable_amount, self._ctx.team)

    async def get_energy_async(self):
        """
        Gets the amount of energy available in the team's pool.
        """
        if not _has_energy_link_tag(self._ctx):
            return

        await self.energy_link.get_energy_async()

        retries:int  = 0
        energy_amount: int = None
        while retries < 5:
            try:
                # We pop the amount to prevent it from caching on future requests.
                energy_amount = self._ctx.stored_data.pop(self.energy_link.get_ap_key())
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

def _has_energy_link_tag(ctx: CommonContext) -> bool:
    if EnergyLinkConstants.FRIENDLY_NAME not in ctx.tags:
        logger.info("Energy Link is not enabled for Luigi's Mansion.")
        return False
    return True

def _remove_amount_from_wallet(wallet: Wallet, amount_to_send: int) -> int:
    wallet_worth: int = wallet.get_wallet_worth()
    minimum_energy_worth = wallet.get_calculated_amount_worth(1)

    if amount_to_send > wallet_worth:
        logger.error("Luigi's has %sG and cannot afford the requested energy amount (%s), a partial amount will be sent instead.", wallet_worth,  amount_to_send)

    return _remove_currencies_recursive(wallet, amount_to_send, minimum_energy_worth)

def _remove_currencies(wallet: Wallet, amount_to_send: int) -> dict[str, int]:
    new_amount = amount_to_send
    currencies_to_remove: dict[str, int] = {}

    for currency_name, currency_type in wallet.get_currencies().items():
        if new_amount == 0:
            break

        currency_to_remove, remainder = divmod(new_amount, currency_type.calc_value)
        new_amount = remainder
        if currency_to_remove <= 0:
            continue

        remove_amount = currency_type.get() - currency_to_remove
        if remove_amount < 0:
            currency_to_remove += remove_amount
            new_amount += ((remove_amount * -1) * currency_type.calc_value)

        currencies_to_remove.update({ currency_name: int(currency_to_remove) })

    return currencies_to_remove, int(new_amount)

def _remove_currencies_recursive(wallet: Wallet, amount_to_send: int, minimum_energy_worth: int) -> dict[str, int]:
    new_amount = amount_to_send

    while new_amount > 0:
        # Try to remove currency from energy link amount.
        temp_currencies, remaining = _remove_currencies(wallet, new_amount)
        new_amount = remaining
        wallet.remove_from_wallet(temp_currencies)

        # If the remaining amount of energy is less than the minimum possible amount we break out of the loop.
        if remaining < minimum_energy_worth:
            break

        # If the remaining amount isn't 0 and we run out of currency we will try to convert
        # some higher valued currencies to close the gap.
        if remaining > 0:
            for currency_name in wallet.get_currencies(has_amount=True):
                if wallet.try_convert_currency(currency_name):
                    break

        if len(wallet.get_currencies(has_amount=True)) == 0:
            break

    return int(new_amount)
