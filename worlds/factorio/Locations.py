from typing import Dict, List

from .Technologies import factorio_base_id, factorio_id
from .Options import MaxSciencePack

boundary: int = 0xff
total_locations: int = 0xff

assert total_locations <= boundary
assert factorio_base_id != factorio_id


def make_pools() -> Dict[str, List[str]]:
    pools: Dict[str, List[str]] = {}
    for i, pack in enumerate(MaxSciencePack.get_ordered_science_packs(), start=1):
        max_needed: int = sum(divmod(boundary, i))
        scale: float = boundary / max_needed
        prefix: str = f"AP-{i}-"
        pools[pack] = [prefix + hex(int(x * scale))[2:].upper().zfill(2) for x in range(1, max_needed + 1)]
    return pools


location_pools: Dict[str, List[str]] = make_pools()

location_table: Dict[str, int] = {}
end_id: int = factorio_id
for pool in location_pools.values():
    location_table.update({name: ap_id for ap_id, name in enumerate(pool, start=end_id)})
    end_id += len(pool)

assert end_id - len(location_table) == factorio_id
del pool
