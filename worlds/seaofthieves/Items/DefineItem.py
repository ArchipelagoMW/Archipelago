from ..Items.ItemDetail import ItemDetail
from BaseClasses import Item, ItemClassification

class Define:

    class Money:

        @staticmethod
        def gold(value: int):
            itm = ItemDetail("{} Gold".format(value), ItemClassification.filler)
            itm.numeric_value = value
            return itm

        @staticmethod
        def dabloon(value: int):
            itm = ItemDetail("{} Dabloons".format(value), ItemClassification.filler)
            itm.numeric_value = value
            return itm

        @staticmethod
        def ancient_coin(value: int):
            itm = ItemDetail("{} Ancient Coins".format(value), ItemClassification.filler)
            itm.numeric_value = value
            return itm

    class Trap:
        @staticmethod
        def kraken():
            itm = ItemDetail("Kraken", ItemClassification.trap)
            return itm

    class Item:

        class Ship:

            @staticmethod
            def sail():
                itm = ItemDetail("Sail", ItemClassification.progression)
                return itm

            @staticmethod
            def sail_inferno():
                itm = ItemDetail("Ashen Sail", ItemClassification.progression)
                return itm

            @staticmethod
            def stove():
                itm = ItemDetail("Stove", ItemClassification.progression)
                return itm

            @staticmethod
            def food_barrel():
                itm = ItemDetail("Food Barrel", ItemClassification.progression)
                return itm

            @staticmethod
            def wood_barrel():
                itm = ItemDetail("Wood Barrel", ItemClassification.progression)
                return itm

            @staticmethod
            def cannon_barrel():
                itm = ItemDetail("Cannon Barrel", ItemClassification.progression)
                return itm

        class Voyage:

            @staticmethod
            def fortress():
                itm = ItemDetail("Voyages of Sea Forts", ItemClassification.progression)
                return itm

            @staticmethod
            def gh():
                itm = ItemDetail("Voyages of Gold Hoarders", ItemClassification.progression)
                return itm

            @staticmethod
            def ma():
                itm = ItemDetail("Voyages of Merchants", ItemClassification.progression)
                return itm

            @staticmethod
            def oos():
                itm = ItemDetail("Voyages of Souls", ItemClassification.progression)
                return itm

            @staticmethod
            def af():
                itm = ItemDetail("Voyages of Athena", ItemClassification.progression)
                return itm

            @staticmethod
            def rb():
                itm = ItemDetail("Voyages of Reaper", ItemClassification.progression)
                return itm

            @staticmethod
            def tt():
                itm = ItemDetail("Voyages of Tall Tales", ItemClassification.progression)
                return itm

            @staticmethod
            def destiny():
                itm = ItemDetail("Voyages of Destiny", ItemClassification.progression)
                return itm

        class Emissary:

            @staticmethod
            def gh():
                itm = ItemDetail("Emissary of Gold Hoarders", ItemClassification.progression)
                return itm

            @staticmethod
            def ma():
                itm = ItemDetail("Emissary of Merchants", ItemClassification.progression)
                return itm

            @staticmethod
            def oos():
                itm = ItemDetail("Emissary of Souls", ItemClassification.progression)
                return itm

            @staticmethod
            def af():
                itm = ItemDetail("Emissary of Athena", ItemClassification.progression)
                return itm

            @staticmethod
            def rb():
                itm = ItemDetail("Emissary of Reaper", ItemClassification.progression)
                return itm

        class Seal:
            @staticmethod
            def gh():
                itm = ItemDetail("Hoarder's Seal", ItemClassification.progression)
                return itm

            @staticmethod
            def ma():
                itm = ItemDetail("Merchant's Seal", ItemClassification.progression)
                return itm

            @staticmethod
            def oos():
                itm = ItemDetail("Soul's Seal", ItemClassification.progression)
                return itm

            @staticmethod
            def af():
                itm = ItemDetail("Athena's Seal", ItemClassification.progression)
                return itm

            @staticmethod
            def rb():
                itm = ItemDetail("Reaper's Seal", ItemClassification.progression)
                return itm

        class Weapon:
            @staticmethod
            def personal():
                itm = ItemDetail("Personal Weapons", ItemClassification.progression)
                return itm

            @staticmethod
            def ship():
                itm = ItemDetail("Ship Weapons", ItemClassification.progression)
                return itm

        class Equipment:
            @staticmethod
            def fishing_rod():
                itm = ItemDetail("Fishing Rod", ItemClassification.progression)
                return itm

            @staticmethod
            def shovel():
                itm = ItemDetail("Shovel", ItemClassification.progression)
                return itm

            @staticmethod
            def wallet():
                itm = ItemDetail("Progressive Wallet", ItemClassification.progression, 0, 2)
                return itm


    class Shop:
        @staticmethod
        def ancient_spire():
            itm = ItemDetail("Catalog of Ancient Spire", ItemClassification.progression)
            return itm

        @staticmethod
        def dagger_tooth():
            itm = ItemDetail("Catalog of Dagger Tooth", ItemClassification.progression)
            return itm

        @staticmethod
        def galleons_grave():
            itm = ItemDetail("Catalog of Galleon's Grave", ItemClassification.progression)
            return itm

        @staticmethod
        def morrows_peak():
            itm = ItemDetail("Catalog of Morrow's Peak", ItemClassification.progression)
            return itm

        @staticmethod
        def plunder():
            itm = ItemDetail("Catalog of Plunder", ItemClassification.progression)
            return itm

        @staticmethod
        def sanctuary():
            itm = ItemDetail("Catalog of Sanctuary", ItemClassification.progression)
            return itm


    class Victory:

        @staticmethod
        def pirate_legend():
            itm = ItemDetail("Pirate Legend", ItemClassification.progression)
            return itm