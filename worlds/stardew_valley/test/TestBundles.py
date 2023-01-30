from ..bundle_data import all_bundle_items


def test_all_bundle_items_have_3_parts():
    for bundle_item in all_bundle_items:
        name = bundle_item.item.name
        assert len(name) > 0
        id = bundle_item.item.item_id
        assert (id > 0 or id == -1)
        amount = bundle_item.amount
        assert amount > 0
        quality = bundle_item.quality
        assert quality >= 0

