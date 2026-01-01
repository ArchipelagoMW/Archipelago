from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional, Tuple, ClassVar

from ...data.villagers_data import Villager
from ...strings.villager_names import NPC

suffix = " <3"
location_prefix = "Friendsanity: "


def to_item_name(npc_name: str) -> str:
    return npc_name + suffix


def to_location_name(npc_name: str, heart: int) -> str:
    return location_prefix + npc_name + " " + str(heart) + suffix


pet_heart_item_name = to_item_name(NPC.pet)


def extract_npc_from_item_name(item_name: str) -> Optional[str]:
    if not item_name.endswith(suffix):
        return None

    return item_name[:-len(suffix)]


def extract_npc_from_location_name(location_name: str) -> Tuple[Optional[str], int]:
    if not location_name.endswith(suffix):
        return None, 0

    trimmed = location_name[len(location_prefix):-len(suffix)]
    last_space = trimmed.rindex(" ")
    return trimmed[:last_space], int(trimmed[last_space + 1:])


@lru_cache(maxsize=32)  # Should not go pass 32 values if every friendsanity options are in the multi world
def get_heart_steps(max_heart: int, heart_size: int) -> Tuple[int, ...]:
    return tuple(range(heart_size, max_heart + 1, heart_size)) + ((max_heart,) if max_heart % heart_size else ())


@dataclass(frozen=True)
class FriendsanityFeature(ABC):
    is_enabled: ClassVar[bool]

    heart_size: int

    to_item_name = staticmethod(to_item_name)
    to_location_name = staticmethod(to_location_name)
    pet_heart_item_name = pet_heart_item_name
    extract_npc_from_item_name = staticmethod(extract_npc_from_item_name)
    extract_npc_from_location_name = staticmethod(extract_npc_from_location_name)

    @abstractmethod
    def get_randomized_hearts(self, villager: Villager) -> Tuple[int, ...]:
        ...

    @property
    def is_pet_randomized(self):
        return bool(self.get_pet_randomized_hearts())

    @abstractmethod
    def get_pet_randomized_hearts(self) -> Tuple[int, ...]:
        ...


class FriendsanityNone(FriendsanityFeature):
    is_enabled = False

    def __init__(self):
        super().__init__(1)

    def get_randomized_hearts(self, villager: Villager) -> Tuple[int, ...]:
        return ()

    def get_pet_randomized_hearts(self) -> Tuple[int, ...]:
        return ()


@dataclass(frozen=True)
class FriendsanityBachelors(FriendsanityFeature):
    is_enabled = True

    def get_randomized_hearts(self, villager: Villager) -> Tuple[int, ...]:
        if not villager.bachelor:
            return ()

        return get_heart_steps(8, self.heart_size)

    def get_pet_randomized_hearts(self) -> Tuple[int, ...]:
        return ()


@dataclass(frozen=True)
class FriendsanityStartingNpc(FriendsanityFeature):
    is_enabled = True

    def get_randomized_hearts(self, villager: Villager) -> Tuple[int, ...]:
        if not villager.available:
            return ()

        if villager.bachelor:
            return get_heart_steps(8, self.heart_size)

        return get_heart_steps(10, self.heart_size)

    def get_pet_randomized_hearts(self) -> Tuple[int, ...]:
        return get_heart_steps(5, self.heart_size)


@dataclass(frozen=True)
class FriendsanityAll(FriendsanityFeature):
    is_enabled = True

    def get_randomized_hearts(self, villager: Villager) -> Tuple[int, ...]:
        if villager.bachelor:
            return get_heart_steps(8, self.heart_size)

        return get_heart_steps(10, self.heart_size)

    def get_pet_randomized_hearts(self) -> Tuple[int, ...]:
        return get_heart_steps(5, self.heart_size)


@dataclass(frozen=True)
class FriendsanityAllWithMarriage(FriendsanityFeature):
    is_enabled = True

    def get_randomized_hearts(self, villager: Villager) -> Tuple[int, ...]:
        if villager.bachelor:
            return get_heart_steps(14, self.heart_size)

        return get_heart_steps(10, self.heart_size)

    def get_pet_randomized_hearts(self) -> Tuple[int, ...]:
        return get_heart_steps(5, self.heart_size)
