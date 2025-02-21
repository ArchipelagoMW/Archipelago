import random

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from .Civ6Client import CivVIContext

# any is also an option but should not be considered an effect
DEATH_LINK_EFFECTS = ["Gold", "Faith", "Era Score", "Unit Killed"]


async def handle_receive_deathlink(ctx: 'CivVIContext', message: str):
    """Resolves the effects of a deathlink received from the multiworld based on the options selected by the player"""
    chosen_effects: List[str] = ctx.slot_data["death_link_effect"]
    effect = random.choice(chosen_effects)

    percent = ctx.slot_data["death_link_effect_percent"]
    if effect == "Gold":
        ctx.logger.info(f"Decreasing gold by {percent}%")
        await ctx.game_interface.decrease_gold_by_percent(percent, message)
    elif effect == "Faith":
        ctx.logger.info(f"Decreasing faith by {percent}%")
        await ctx.game_interface.decrease_faith_by_percent(percent, message)
    elif effect == "Era Score":
        ctx.logger.info("Decreasing era score by 1")
        await ctx.game_interface.decrease_era_score_by_amount(1, message)
    elif effect == "Unit Killed":
        ctx.logger.info("Destroying a random unit")
        await ctx.game_interface.kill_unit(message)


async def handle_check_deathlink(ctx: 'CivVIContext'):
    """Checks if the local player should send out a deathlink to the multiworld as well as if we should respond to any pending deathlinks sent to us """
    # check if we received a death link
    if ctx.received_death_link:
        ctx.received_death_link = False
        await handle_receive_deathlink(ctx, ctx.death_link_message)

    # Check if we should send out a death link
    result = await ctx.game_interface.get_deathlink()
    if ctx.death_link_just_changed:
        ctx.death_link_just_changed = False
        return
    if result != "false":
        messages = [f"lost a unit to a {result}",
                    f"offered a sacrifice to the great {result}",
                    f"was killed by a {result}",
                    f"made a donation to the {result} fund",
                    f"made a tactical error",
                    f"picked a fight with a {result} and lost",
                    f"tried to befriend an enemy {result}",
                    f"used a {result} to reduce their military spend",
                    f"was defeated by a {result} in combat",
                    f"bravely struck a {result} and paid the price",
                    f"had a lapse in judgement against a {result}",
                    f"learned at the hands of a {result}",
                    f"attempted to non peacefully negotiate with a {result}",
                    f"was outsmarted by a {result}",
                    f"received a lesson from a {result}",
                    f"now understands the importance of not fighting a {result}",
                    f"let a {result} get the better of them",
                    f"allowed a {result} to show them the error of their ways",
                    f"heard the tragedy of Darth Plagueis the Wise from a {result}",
                    f"refused to join a {result} in their quest for power",
                    f"was tired of sitting in BK and decided to fight a {result} instead",
                    f"purposely lost to a {result} as a cry for help",
                    f"is wanting to remind everyone that they are here to have fun and not to win",
                    f"is reconsidering their pursuit of a domination victory",
                    f"had their plans toppled by a {result}",
                    ]

        if ctx.slot is not None:
            player = ctx.player_names[ctx.slot]
            message = random.choice(messages)
            await ctx.send_death(f"{player} {message}")
