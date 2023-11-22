class Quality:
    basic = "Basic"
    silver = "Silver"
    gold = "Gold"
    iridium = "Iridium"

    @staticmethod
    def get_highest(quality1: str, quality2: str) -> str:
        for quality in qualities_in_desc_order:
            if quality1 == quality or quality2 == quality:
                return quality
        return Quality.basic


qualities_in_desc_order = [Quality.iridium, Quality.gold, Quality.silver, Quality.basic]
