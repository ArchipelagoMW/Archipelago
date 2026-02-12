import bisect
import random
from typing import TYPE_CHECKING, Iterator, Iterable

from .RecipeEngine import RecipeEngine, GameItem

if TYPE_CHECKING:
    from . import FactorioBobs

class RandomGameItems:
    def __init__(self, world: "FactorioBobs"):
        self.world = world
        self.random = random.Random(self.world.seeded_random_seed)
        self.pools: list[list[GameItem]] = []
        self.taken: dict[GameItem, int] = {} # item to pool taken from

    @property
    def recipe_engine(self) -> RecipeEngine:
        return self.world.modpack.recipe_engine

    @property
    def num_of_items(self) -> int:
        return self.world.options.percent_items_in_game * len(self.recipe_engine.get_pool_items()) // 100

    @property
    def num_of_pools(self) -> int:
        return min(self.world.options.number_of_science_packs.value, len(self.world.modpack.ordered_science_packs)) \
            + (1 if self.world.options.additional_rocket_pool.value else 0)


    def __init_pools(self) -> None:
        self.pools: list[list[GameItem]] = [[] for _ in range(self.num_of_pools)]

        first_pool = self.pools[0]
        items_with_req_tech: list[GameItem] = []

        for item in self.recipe_engine.get_pool_items():
            req_recipes = item.get_best_recipes()
            req_tech = set()
            for recipe in req_recipes:
                if recipe.is_starter:
                    continue
                req_tech.update(recipe.technologies)
            if req_tech:
                bisect.insort(items_with_req_tech, item, key=lambda itm: itm.score)
            else:
                bisect.insort(first_pool, item, key=lambda itm: itm.score)

        items_with_req_tech = items_with_req_tech[:self.num_of_items-len(first_pool)]

        items_per_pool = len(items_with_req_tech) / (self.num_of_pools - 1)

        for i in range(0, self.num_of_pools-1):
            self.pools[i+1] = items_with_req_tech[int(i*items_per_pool):int((i+1)*items_per_pool)]

        assert all(len(pool) > 0 for pool in self.pools)
        assert self.pools[-1][-1] == items_with_req_tech[-1]

        for pool in self.pools:
            self.random.shuffle(pool)

    def __pop_pool(self, index: int):
        item = self.pools[index].pop(0)
        self.taken[item] = index
        return item

    def pop_item_from_pool(self, start_index:int, end_index:int=None) -> GameItem:
        if not self.pools:
            self.__init_pools()
        if end_index is None:
            end_index = start_index

        if start_index < 0:
            start_index = len(self.pools) + start_index

        if end_index < 0:
            end_index = len(self.pools) + end_index

        num_to_pick = sum(len(pool) for pool in self.pools[start_index:end_index+1])
        if num_to_pick == 0:
            raise IndexError("Ran out of items to pick, increase number of items or decrease number of packs")
        random_num = self.random.randint(0, num_to_pick)
        for index, pool in enumerate(self.pools[start_index:end_index+1], start_index):
            if random_num <= len(pool):
                return self.__pop_pool(index)
            random_num -= len(pool)
        raise IndexError("failed to pick item from pools")

    def return_item(self, item:GameItem) -> None:
        assert item in self.taken, "tried to return item not taken in pool"
        self.pools[self.taken[item]].append(item)
        del self.taken[item]

    def return_items(self, items:Iterable[GameItem]) -> None:
        for item in items:
            self.return_item(item)