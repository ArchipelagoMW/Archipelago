from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import ClassVar

from .base import FeatureBase
from ...data.game_item import GameItem, ItemTag
from ...strings.book_names import ordered_lost_books

item_prefix = "Power: "
location_prefix = "Read "


def to_item_name(book: str) -> str:
    return item_prefix + book


def to_location_name(book: str) -> str:
    return location_prefix + book


def extract_book_from_location_name(location_name: str) -> str | None:
    if not location_name.startswith(location_prefix):
        return None

    return location_name[len(location_prefix):]


class BooksanityFeature(FeatureBase, ABC):
    is_enabled: ClassVar[bool]

    to_item_name = staticmethod(to_item_name)
    progressive_lost_book = "Progressive Lost Book"
    to_location_name = staticmethod(to_location_name)
    extract_book_from_location_name = staticmethod(extract_book_from_location_name)

    @abstractmethod
    def is_included(self, book: GameItem) -> bool:
        ...

    @staticmethod
    def get_randomized_lost_books() -> Iterable[str]:
        return []


class BooksanityDisabled(BooksanityFeature):
    is_enabled = False

    def is_included(self, book: GameItem) -> bool:
        return False


class BooksanityPower(BooksanityFeature):
    is_enabled = True

    def is_included(self, book: GameItem) -> bool:
        return ItemTag.BOOK_POWER in book.tags


class BooksanityPowerSkill(BooksanityFeature):
    is_enabled = True

    def is_included(self, book: GameItem) -> bool:
        return ItemTag.BOOK_POWER in book.tags or ItemTag.BOOK_SKILL in book.tags


class BooksanityAll(BooksanityFeature):
    is_enabled = True

    def is_included(self, book: GameItem) -> bool:
        return ItemTag.BOOK_POWER in book.tags or ItemTag.BOOK_SKILL in book.tags

    @staticmethod
    def get_randomized_lost_books() -> Iterable[str]:
        return ordered_lost_books
