from typing import Iterable, Dict


def repeated_item_names_gen(item_names: Iterable[str], item_counts: Dict[str, int]):
    """
    Generator that repeatedly yields the items names in `item_names` as many times as the count of that item name in
    `item_counts`.
    """
    for item_name in item_names:
        item_count = item_counts[item_name]
        for _ in range(item_count):
            yield item_name
