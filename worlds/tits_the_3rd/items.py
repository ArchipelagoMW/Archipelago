"""This module represents item definitions for Trails in the Sky the 3rd"""
from BaseClasses import Item, ItemClassification

class TitsThe3rdItem(Item):
    """Trails in the Sky the 3rd Item Definition"""
    game: str = "Trails in the Sky the 3rd"

    @staticmethod
    def get_item_classfication(name: str):
        """
        Returns the item classification based on the name of the item

        Args:
            name (str): The name of the item
        """
        # TODO: determine item classification (In the meantime this method will always return filler)
        return ItemClassification.filler

