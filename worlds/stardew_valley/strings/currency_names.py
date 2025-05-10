class Currency:
    qi_coin = "Qi Coin"
    golden_walnut = "Golden Walnut"
    qi_gem = "Qi Gem"
    star_token = "Star Token"
    money = "Money"
    cinder_shard = "Cinder Shard"
    prize_ticket = "Prize Ticket"
    calico_egg = "Calico Egg"
    golden_tag = "Golden Tag"

    @staticmethod
    def is_currency(item: str) -> bool:
        return item in [Currency.qi_coin, Currency.golden_walnut, Currency.qi_gem, Currency.star_token, Currency.money,
                        MemeCurrency.code, MemeCurrency.clic, MemeCurrency.steps, MemeCurrency.time, MemeCurrency.energy, MemeCurrency.blood,
                        MemeCurrency.cookies, MemeCurrency.child]


class MemeCurrency:
    dead_pumpkins = "Dead Pumpkins"
    child = "Child"
    code = "Code"
    clic = "Clic"
    steps = "Steps"
    time = "Time"
    energy = "Energy"
    blood = "Blood"
    cookies = "CookieClics"
