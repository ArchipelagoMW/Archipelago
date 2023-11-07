from typing import Dict, List

from .Technologies import factorio_base_id
from .Options import MaxSciencePack


def make_pools() -> Dict[str, List[str]]:
    pools: Dict[str, List[str]] = {}
    for i, pack in enumerate(MaxSciencePack.get_ordered_science_packs(), start=1):
        max_needed: int = 999
        prefix: str = f"AP-{i}-"
        pools[pack] = [prefix + str(x).upper().zfill(3) for x in range(1, max_needed + 1)]
    return pools


location_pools: Dict[str, List[str]] = make_pools()

location_table: Dict[str, int] = {}
end_id: int = factorio_base_id
for pool in location_pools.values():
    location_table.update({name: ap_id for ap_id, name in enumerate(pool, start=end_id)})
    end_id += len(pool)

assert end_id - len(location_table) == factorio_base_id
del pool
