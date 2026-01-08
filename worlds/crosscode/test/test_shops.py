from . import CrossCodeTestBase

class TestShopShopReceiveSlotSend(CrossCodeTestBase):
    options = {
        "shop_rando": True,
        "shop_receive_mode": "per_shop",
        "shop_send_mode": "per_slot",
    }

    def test_all_slots_available_with_shop_item(self):
        all_state = self.multiworld.get_all_state(use_cache=False)
        item_list = self.get_items_by_name(
            shop.name for shop in self.world_data.shop_unlock_by_shop.values()
        )
        for item in item_list:
            all_state.remove(item)

        for shop_name, shop_locations in self.world.world_data.per_shop_locations.items():
            shop_data = self.world_data.shops_dict[shop_name]
            # create a state with just the shop unlock for this shop.
            shop_state = all_state.copy()
            shop_state.collect(
                self.get_item_by_name(self.world_data.shop_unlock_by_shop[shop_data.internal_name].name)
            )

            self.assertTrue(shop_state.can_reach_region(shop_name, self.player))
            for location_data in shop_locations.values():
                self.assertTrue(shop_state.can_reach_location(location_data.name, self.player))

class TestSlotShopReceiveSlotSend(CrossCodeTestBase):
    options = {
        "shop_rando": True,
        "shop_receive_mode": "per_slot",
        "shop_send_mode": "per_slot",
    }

    def test_all_slots_available_with_slot_item(self):
        all_state = self.multiworld.get_all_state(use_cache=False)
        item_list = self.get_items_by_name(
            shop.name for shop in self.world_data.shop_unlock_by_shop_and_id.values()
        )
        for item in item_list:
            all_state.remove(item)

        for shop_name, shop_locations in self.world.world_data.per_shop_locations.items():
            shop_data = self.world_data.shops_dict[shop_name]

            for item_id, location_data in shop_locations.items():
                # create a state with just the slot unlock for this item.
                shop_state = all_state.copy()
                shop_state.collect(self.get_item_by_name(
                    self.world_data.shop_unlock_by_shop_and_id[shop_data.internal_name, item_id].name
                ))

                self.assertTrue(shop_state.can_reach_location(location_data.name, self.player))

class TestSlotItemReceiveSlotSend(CrossCodeTestBase):
    options = {
        "shop_rando": True,
        "shop_receive_mode": "per_item_type",
        "shop_send_mode": "per_slot",
    }

    def test_all_slots_available_with_slot_item(self):
        all_state = self.multiworld.get_all_state(use_cache=False)
        item_list = self.get_items_by_name(
            shop.name for shop in self.world_data.shop_unlock_by_id.values()
        )
        for item in item_list:
            all_state.remove(item)

        for shop_locations in self.world.world_data.per_shop_locations.values():
            for item_id, location_data in shop_locations.items():
                # create a state with just the slot unlock for this item.
                shop_state = all_state.copy()
                shop_state.collect(self.get_item_by_name(
                    self.world_data.shop_unlock_by_id[item_id].name
                ))

                self.assertTrue(shop_state.can_reach_location(location_data.name, self.player))
