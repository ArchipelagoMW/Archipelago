from typing import List


class CropQuality:
    basic = "Basic Crop"
    silver = "Silver Crop"
    gold = "Gold Crop"
    iridium = "Iridium Crop"

    @staticmethod
    def get_highest(qualities: List[str]) -> str:
        for quality in crop_qualities_in_desc_order:
            if quality in qualities:
                return quality
        return CropQuality.basic


class FishQuality:
    basic = "Basic Fish"
    silver = "Silver Fish"
    gold = "Gold Fish"
    iridium = "Iridium Fish"

    @staticmethod
    def get_highest(qualities: List[str]) -> str:
        for quality in fish_qualities_in_desc_order:
            if quality in qualities:
                return quality
        return FishQuality.basic


class ForageQuality:
    basic = "Basic Forage"
    silver = "Silver Forage"
    gold = "Gold Forage"
    iridium = "Iridium Forage"

    @staticmethod
    def get_highest(qualities: List[str]) -> str:
        for quality in forage_qualities_in_desc_order:
            if quality in qualities:
                return quality
        return ForageQuality.basic


class ArtisanQuality:
    basic = "Basic Artisan"
    silver = "Silver Artisan"
    gold = "Gold Artisan"
    iridium = "Iridium Artisan"

    @staticmethod
    def get_highest(qualities: List[str]) -> str:
        for quality in artisan_qualities_in_desc_order:
            if quality in qualities:
                return quality
        return ArtisanQuality.basic


crop_qualities_in_desc_order = [CropQuality.iridium, CropQuality.gold, CropQuality.silver, CropQuality.basic]
fish_qualities_in_desc_order = [FishQuality.iridium, FishQuality.gold, FishQuality.silver, FishQuality.basic]
forage_qualities_in_desc_order = [ForageQuality.iridium, ForageQuality.gold, ForageQuality.silver, ForageQuality.basic]
artisan_qualities_in_desc_order = [ArtisanQuality.iridium, ArtisanQuality.gold, ArtisanQuality.silver, ArtisanQuality.basic]
