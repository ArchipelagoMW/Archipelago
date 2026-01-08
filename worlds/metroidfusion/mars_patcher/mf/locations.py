from __future__ import annotations

import json
import os
import pkgutil
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from ..frozendict import frozendict

from .constants.items import (
    ITEM_ENUMS,
    ITEM_SPRITE_ENUMS,
    JINGLE_ENUMS,
    KEY_AREA,
    KEY_BLOCK_X,
    KEY_BLOCK_Y,
    KEY_CENTERED,
    KEY_HIDDEN,
    KEY_ITEM,
    KEY_ITEM_JINGLE,
    KEY_ITEM_MESSAGES,
    KEY_ITEM_MESSAGES_KIND,
    KEY_ITEM_SPRITE,
    KEY_LANGUAGES,
    KEY_MAJOR_LOCS,
    KEY_MESSAGE_ID,
    KEY_MINOR_LOCS,
    KEY_ORIGINAL,
    KEY_ROOM,
    KEY_SOURCE,
    SOURCE_ENUMS,
    ItemJingle,
    ItemMessagesKind,
    ItemSprite,
    ItemType,
    MajorSource,
)

from ..text import Language

if TYPE_CHECKING:
    from .auto_generated_types import Itemmessages, MarsschemamfLocations


class Location:
    def __init__(
        self, area: int, room: int, orig_item: ItemType, new_item: ItemType = ItemType.UNDEFINED
    ):
        if type(self) is Location:
            raise TypeError()
        self.area = area
        self.room = room
        self.orig_item = orig_item
        self.new_item = new_item

    def __str__(self) -> str:
        item_str = self.orig_item.name
        if self.new_item != ItemType.UNDEFINED:
            item_str += "/" + self.new_item.name
        return f"{self.area},0x{self.room:02X}: {item_str}"


class MajorLocation(Location):
    def __init__(
        self,
        area: int,
        room: int,
        major_src: MajorSource,
        orig_item: ItemType,
        new_item: ItemType = ItemType.UNDEFINED,
        item_messages: ItemMessages | None = None,
        item_jingle: ItemJingle = ItemJingle.MAJOR,
    ):
        super().__init__(area, room, orig_item, new_item)
        self.major_src = major_src
        self.item_messages = item_messages
        self.item_jingle = item_jingle


class MinorLocation(Location):
    def __init__(
        self,
        area: int,
        room: int,
        block_x: int,
        block_y: int,
        hidden: bool,
        orig_item: ItemType,
        new_item: ItemType = ItemType.UNDEFINED,
        item_sprite: ItemSprite = ItemSprite.UNCHANGED,
        item_messages: ItemMessages | None = None,
        item_jingle: ItemJingle = ItemJingle.MINOR,
    ):
        super().__init__(area, room, orig_item, new_item)
        self.block_x = block_x
        self.block_y = block_y
        self.hidden = hidden
        self.item_sprite = item_sprite
        self.item_messages = item_messages
        self.item_jingle = item_jingle


@dataclass(frozen=True)
class ItemMessages:
    kind: ItemMessagesKind
    item_messages: frozendict[Language, str]
    centered: bool
    message_id: int

    LANG_ENUMS: ClassVar[dict[str, Language]] = {
        "JapaneseKanji": Language.JAPANESE_KANJI,
        "JapaneseHiragana": Language.JAPANESE_HIRAGANA,
        "English": Language.ENGLISH,
        "German": Language.GERMAN,
        "French": Language.FRENCH,
        "Italian": Language.ITALIAN,
        "Spanish": Language.SPANISH,
    }

    KIND_ENUMS: ClassVar[dict[str, ItemMessagesKind]] = {
        "CustomMessage": ItemMessagesKind.CUSTOM_MESSAGE,
        "MessageID": ItemMessagesKind.MESSAGE_ID,
    }

    @classmethod
    def from_json(cls, data: Itemmessages) -> ItemMessages:
        item_messages: dict[Language, str] = {}
        centered = True
        kind: ItemMessagesKind = cls.KIND_ENUMS[data[KEY_ITEM_MESSAGES_KIND]]
        message_id = 0
        if kind == ItemMessagesKind.CUSTOM_MESSAGE:
            for lang_name, message in data[KEY_LANGUAGES].items():
                lang = cls.LANG_ENUMS[lang_name]
                item_messages[lang] = message
            centered = data.get(KEY_CENTERED, True)
        else:
            message_id = data[KEY_MESSAGE_ID]

        return cls(kind, frozendict(item_messages), centered, message_id)


class LocationSettings:
    def __init__(self, major_locs: list[MajorLocation], minor_locs: list[MinorLocation]):
        self.major_locs = major_locs
        self.minor_locs = minor_locs

    @classmethod
    def initialize(cls) -> LocationSettings:
        path = os.path.join("data", "locations.json")
        data = json.loads(pkgutil.get_data(__name__, path).decode())

        major_locs = []
        for entry in data[KEY_MAJOR_LOCS]:
            major_loc = MajorLocation(
                entry[KEY_AREA],
                entry[KEY_ROOM],
                SOURCE_ENUMS[entry[KEY_SOURCE]],
                ITEM_ENUMS[entry[KEY_ORIGINAL]],
            )
            major_locs.append(major_loc)

        minor_locs = []
        for entry in data[KEY_MINOR_LOCS]:
            minor_loc = MinorLocation(
                entry[KEY_AREA],
                entry[KEY_ROOM],
                entry[KEY_BLOCK_X],
                entry[KEY_BLOCK_Y],
                entry[KEY_HIDDEN],
                ITEM_ENUMS[entry[KEY_ORIGINAL]],
            )
            minor_locs.append(minor_loc)

        return LocationSettings(major_locs, minor_locs)

    def set_assignments(self, data: MarsschemamfLocations) -> None:
        for maj_loc_entry in data[KEY_MAJOR_LOCS]:
            # Get source and item
            source = SOURCE_ENUMS[maj_loc_entry[KEY_SOURCE]]
            item = ITEM_ENUMS[maj_loc_entry[KEY_ITEM]]
            # Find location with this source
            maj_loc = next(m for m in self.major_locs if m.major_src == source)
            maj_loc.new_item = item
            if KEY_ITEM_MESSAGES in maj_loc_entry:
                maj_loc.item_messages = ItemMessages.from_json(maj_loc_entry[KEY_ITEM_MESSAGES])
            maj_loc.item_jingle = JINGLE_ENUMS[maj_loc_entry[KEY_ITEM_JINGLE]]
        for min_loc_entry in data[KEY_MINOR_LOCS]:
            # Get area, room, block X, block Y
            area = min_loc_entry[KEY_AREA]
            room = min_loc_entry[KEY_ROOM]
            block_x = min_loc_entry[KEY_BLOCK_X]
            block_y = min_loc_entry[KEY_BLOCK_Y]
            # Find location with this source
            try:
                min_loc = next(
                    m
                    for m in self.minor_locs
                    if m.area == area
                    and m.room == room
                    and m.block_x == block_x
                    and m.block_y == block_y
                )
            except StopIteration:
                raise ValueError(
                    f"Invalid minor location: Area {area}, Room {room}, X {block_x}, Y {block_y}"
                )
            # Set item and item sprite
            item = ITEM_ENUMS[min_loc_entry[KEY_ITEM]]
            min_loc.new_item = item
            if KEY_ITEM_SPRITE in min_loc_entry:
                min_loc.item_sprite = ITEM_SPRITE_ENUMS[min_loc_entry[KEY_ITEM_SPRITE]]
            if KEY_ITEM_MESSAGES in min_loc_entry:
                min_loc.item_messages = ItemMessages.from_json(min_loc_entry[KEY_ITEM_MESSAGES])
            min_loc.item_jingle = JINGLE_ENUMS[min_loc_entry[KEY_ITEM_JINGLE]]
