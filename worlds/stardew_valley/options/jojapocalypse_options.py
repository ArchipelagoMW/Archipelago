from Options import Choice, Range, Toggle


class Jojapocalypse(Choice):
    """Joja Co opens a new Archipelago branch, selling you any and all location checks you might want or need, in exchange for money.
    But are you ready to pay the price...
    Disabled: Joja does not sell location checks
    Allowed: Joja sells location checks, that you can buy if you want
    Forced: The only way to obtain location checks is through Joja
    """
    internal_name = "jojapocalypse"
    display_name = "Jojapocalypse"
    default = 0
    option_disabled = 0
    option_allowed = 1
    option_forced = 2


class JojaStartPrice(Range):
    """The price of Jojapocalypse items at the very beginning of the game. This price will increase with each Jojapocalypse purchase
    """
    internal_name = "joja_start_price"
    display_name = "Jojapocalypse Start Price"
    default = 100
    range_start = 1
    range_end = 10000


class JojaEndPrice(Range):
    """The price of the very last Jojapocalypse item you will buy. An individual location check will never go above this.
    Consider your number of checks before choosing a price, as the total amount of money you spend will highly scale with it.
    """
    internal_name = "joja_end_price"
    display_name = "Jojapocalypse End Price"
    default = 10000
    range_start = 0
    range_end = 100_000


class JojaPricingPattern(Choice):
    """Chooses the pricing strategy of Jojapocalypse sold location checks. Prices will always increase, but you can pick the increase pattern.
    """
    internal_name = "joja_pricing_pattern"
    display_name = "Jojapocalypse Pricing Pattern"
    default = 1
    option_linear = 0
    option_exponential = 1


class JojaPurchasesForMembership(Range):
    """After buying this number of location checks for Joja, you will earn your very own Joja Membership!
    The world will change accordingly.
    If you are on "Allowed", receiving your first Movie Theater before earning your membership will close down Joja permanently.
    If you obtain your membership, the movie theater will instead replace the Community Center, and some location checks will become only obtainable through Joja.
    If you are on "Forced", You will start as a Joja Member.
    """
    internal_name = "joja_purchases_for_membership"
    display_name = "Purchases For Joja Membership"
    default = 10
    range_start = 1
    range_end = 100


class JojaAreYouSure(Toggle):
    """Jojapocalypse will be an extremely unfulfilling experience.
    The main driving directive behind its Design is to make the player feel bad and guilty about picking Joja.
    Most of the things you buy will come with heavy, painful consequences, and they are explicitly done with the intent of being unfun and annoying.
    This game mode is not supposed to be fun. You will have a bad time.
    Are you really sure you want to do this?
    """
    internal_name = "joja_are_you_sure"
    display_name = "Are you sure?"
    default = Toggle.option_false
