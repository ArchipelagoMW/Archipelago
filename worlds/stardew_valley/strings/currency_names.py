class Currency:
    qi_coin = "Qi Coin"
    golden_walnut = "Golden Walnut"
    qi_gem = "Qi Gem"
    star_token = "Star Token"
    money = "Money"
    cinder_shard = "Cinder Shard"

    @staticmethod
    def is_currency(item: str) -> bool:
        return item in [Currency.qi_coin, Currency.golden_walnut, Currency.qi_gem, Currency.star_token, Currency.money]


