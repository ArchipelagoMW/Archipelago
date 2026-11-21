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
                        MemeCurrency.cookies, MemeCurrency.child, MemeCurrency.dead_crops, MemeCurrency.dead_pumpkins, MemeCurrency.missed_fish,
                        MemeCurrency.time_elapsed, MemeCurrency.honeywell, MemeCurrency.sleep_days, MemeCurrency.bank_money, MemeCurrency.deathlinks,
                        MemeCurrency.goat]


class MemeCurrency:
    goat = "Goat"
    deathlinks = "DeathLinks"
    bank_money = "Bank Money"
    sleep_days = "Sleep Days"
    blood = "Blood"
    child = "Child"
    clic = "Clic"
    code = "Code"
    cookies = "CookieClics"
    dead_crops = "Dead Crop"
    dead_pumpkins = "Dead Pumpkin"
    energy = "Energy"
    steps = "Steps"
    time = "Time"
    time_elapsed = "Time Elapsed"
    honeywell = "Honeywell"
    missed_fish = "Missed Fish"
