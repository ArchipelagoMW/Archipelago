class Backpack:
    small = "Small Pack"
    large = "Large Pack"
    deluxe = "Deluxe Pack"
    premium = "Premium Pack"
    prices_per_tier = {small: 400, large: 2000, deluxe: 10000, premium: 50000}

    @staticmethod
    def get_purchasable_tiers(bigger_backpack: bool, start_without_backpack: bool = False) -> list[str]:
        tiers = [Backpack.large, Backpack.deluxe]
        if bigger_backpack:
            tiers.append(Backpack.premium)
        if start_without_backpack:
            tiers.insert(0, Backpack.small)
        return tiers
