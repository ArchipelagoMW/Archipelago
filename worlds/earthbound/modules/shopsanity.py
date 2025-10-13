from ..game_data.local_data import psi_item_table, character_item_table, special_name_table, item_id_table, money_item_table
from ..game_data.text_data import calc_pixel_width, text_encoder
from ..game_data.static_location_data import location_ids
from ..Options import ShopRandomizer, MagicantMode, MonkeyCavesMode
from BaseClasses import ItemClassification, Location
import struct
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import EarthBoundWorld
    from .Rom import LocalRom

high_purchase_areas = {
    "Twoson",
    "Fourside",
    "Scaraba",
    "Andonuts Lab Area"  # long walk with no atm
}

shop_locations = {
    "Onett Drugstore - Right Counter Slot 1",
    "Onett Drugstore - Right Counter Slot 2",
    "Onett Drugstore - Right Counter Slot 3",
    "Onett Drugstore - Right Counter Slot 4",
    "Onett Drugstore - Right Counter Slot 5",
    "Onett Drugstore - Left Counter",
    "Summers - Beach Cart",
    "Onett Burger Shop - Slot 1",
    "Onett Burger Shop - Slot 2",
    "Onett Burger Shop - Slot 3",
    "Onett Burger Shop - Slot 4",
    "Onett Bakery - Slot 1",
    "Onett Bakery - Slot 2",
    "Onett Bakery - Slot 3",
    "Onett Bakery - Slot 4",
    "Twoson Department Store Burger Shop - Slot 1",
    "Twoson Department Store Burger Shop - Slot 2",
    "Twoson Department Store Burger Shop - Slot 3",
    "Twoson Department Store Burger Shop - Slot 4",
    "Twoson Department Store Bakery - Slot 1",
    "Twoson Department Store Bakery - Slot 2",
    "Twoson Department Store Bakery - Slot 3",
    "Twoson Department Store Bakery - Slot 4",
    "Twoson Department Store Top Floor - Right Counter Slot 1",
    "Twoson Department Store Top Floor - Right Counter Slot 2",
    "Twoson Department Store Top Floor - Right Counter Slot 3",
    "Twoson Department Store Top Floor - Right Counter Slot 4",
    "Twoson Department Store Top Floor - Right Counter Slot 5",
    "Twoson Department Store Top Floor - Right Counter Slot 6",
    "Twoson Department Store Top Floor - Left Counter Slot 1",
    "Summers - Magic Cake Cart Shop Slot",
    "Burglin Park Junk Shop - Slot 1",
    "Burglin Park Junk Shop - Slot 2",
    "Burglin Park Junk Shop - Slot 3",
    "Burglin Park Junk Shop - Slot 4",
    "Burglin Park Junk Shop - Slot 5",
    "Burglin Park Junk Shop - Slot 6",
    "Burglin Park Bread Stand - Slot 1",
    "Burglin Park Bread Stand - Slot 2",
    "Burglin Park Bread Stand - Slot 3",
    "Burglin Park Bread Stand - Slot 4",
    "Burglin Park Bread Stand - Slot 5",
    "Burglin Park Bread Stand - Slot 6",
    "Burglin Park - Banana Stand",
    "Happy-Happy Village Drugstore - Right Counter Slot 1",
    "Happy-Happy Village Drugstore - Right Counter Slot 2",
    "Happy-Happy Village Drugstore - Right Counter Slot 3",
    "Happy-Happy Village Drugstore - Right Counter Slot 4",
    "Happy-Happy Village Drugstore - Right Counter Slot 5",
    "Threed Drugstore - Right Counter Slot 1",
    "Threed Drugstore - Right Counter Slot 2",
    "Threed Drugstore - Right Counter Slot 3",
    "Threed Drugstore - Right Counter Slot 4",
    "Threed Drugstore - Right Counter Slot 5",
    "Threed Drugstore - Left Counter Slot 1",
    "Threed Drugstore - Left Counter Slot 2",
    "Threed Drugstore - Left Counter Slot 3",
    "Threed Drugstore - Left Counter Slot 4",
    "Threed Drugstore - Left Counter Slot 5",
    "Threed - Arms Dealer Slot 1",
    "Threed - Arms Dealer Slot 2",
    "Threed - Arms Dealer Slot 3",
    "Threed - Arms Dealer Slot 4",
    "Threed Bakery - Slot 1",
    "Threed Bakery - Slot 2",
    "Threed Bakery - Slot 3",
    "Threed Bakery - Slot 4",
    "Threed Bakery - Slot 5",
    "Threed Bakery - Slot 6",
    "Threed Bakery - Slot 7",
    "Scaraba - Expensive Water Guy",
    "Winters Drugstore - Slot 1",
    "Winters Drugstore - Slot 2",
    "Winters Drugstore - Slot 3",
    "Winters Drugstore - Slot 4",
    "Winters Drugstore - Slot 5",
    "Winters Drugstore - Slot 6",
    "Winters Drugstore - Slot 7",
    "Saturn Valley Shop - Center Saturn Slot 1",
    "Saturn Valley Shop - Center Saturn Slot 2",
    "Saturn Valley Shop - Center Saturn Slot 3",
    "Saturn Valley Shop - Center Saturn Slot 4",
    "Saturn Valley Shop - Center Saturn Slot 5",
    "Dusty Dunes Drugstore - Counter Slot 1",
    "Dusty Dunes Drugstore - Counter Slot 2",
    "Dusty Dunes Drugstore - Counter Slot 3",
    "Dusty Dunes Drugstore - Counter Slot 4",
    "Dusty Dunes Drugstore - Counter Slot 5",
    "Dusty Dunes - Arms Dealer Slot 1",
    "Dusty Dunes - Arms Dealer Slot 2",
    "Dusty Dunes - Arms Dealer Slot 3",
    "Dusty Dunes - Arms Dealer Slot 4",
    "Fourside Bakery - Slot 1",
    "Fourside Bakery - Slot 2",
    "Fourside Bakery - Slot 3",
    "Fourside Bakery - Slot 4",
    "Fourside Bakery - Slot 5",
    "Fourside Bakery - Slot 6",
    "Fourside Department Store - Tool Shop Slot 1",
    "Fourside Department Store - Tool Shop Slot 2",
    "Fourside Department Store - Tool Shop Slot 3",
    "Fourside Department Store - Tool Shop Slot 4",
    "Fourside Department Store - Tool Shop Slot 5",
    "Fourside Department Store - Tool Shop Slot 6",
    "Fourside Department Store - Tool Shop Slot 7",
    "Fourside Department Store - Shop Shop Slot 1",
    "Fourside Department Store - Shop Shop Slot 2",
    "Fourside Department Store - Shop Shop Slot 3",
    "Fourside Department Store - Shop Shop Slot 4",
    "Fourside Department Store - Food Shop Slot 1",
    "Fourside Department Store - Food Shop Slot 2",
    "Fourside Department Store - Food Shop Slot 3",
    "Fourside Department Store - Food Shop Slot 4",
    "Fourside Department Store - Food Shop Slot 5",
    "Fourside Department Store - 2F Cart Slot 1",
    "Fourside Department Store - 2F Cart Slot 2",
    "Fourside Department Store - 2F Cart Slot 3",
    "Fourside Department Store - 2F Cart Slot 4",
    "Fourside Department Store - 2F Cart Slot 5",
    "Fourside Department Store - 2F Cart Slot 6",
    "Fourside Department Store - 2F Cart Slot 7",
    "Fourside Department Store - Toys Shop Slot 1",
    "Fourside Department Store - Toys Shop Slot 2",
    "Fourside Department Store - Toys Shop Slot 3",
    "Fourside Department Store - Toys Shop Slot 4",
    "Fourside Department Store - Toys Shop Slot 5",
    "Fourside Department Store - Toys Shop Slot 6",
    "Fourside Department Store - Sports Shop Slot 1",
    "Fourside Department Store - Sports Shop Slot 2",
    "Fourside Department Store - Sports Shop Slot 3",
    "Fourside Department Store - Sports Shop Slot 4",
    "Fourside Department Store - Burger Shop Slot 1",
    "Fourside Department Store - Burger Shop Slot 2",
    "Fourside Department Store - Burger Shop Slot 3",
    "Fourside Department Store - Burger Shop Slot 4",
    "Fourside Department Store - Burger Shop Slot 5",
    "Fourside Department Store - Arms Dealer Slot 1",
    "Fourside Department Store - Arms Dealer Slot 2",
    "Fourside Department Store - Arms Dealer Slot 3",
    "Fourside Department Store - Arms Dealer Slot 4",
    "Fourside Department Store - Arms Dealer Slot 5",
    "Fourside - Northeast Alley Junk Shop Slot 1",
    "Fourside - Northeast Alley Junk Shop Slot 2",
    "Fourside - Northeast Alley Junk Shop Slot 3",
    "Fourside - Northeast Alley Junk Shop Slot 4",
    "Magicant - Shop Slot 1",
    "Magicant - Shop Slot 2",
    "Summers - Scam Shop Slot 1",
    "Summers - Scam Shop Slot 2",
    "Summers - Scam Shop Slot 3",
    "Summers - Scam Shop Slot 4",
    "Summers - Scam Shop Slot 5",
    "Summers - Scam Shop Slot 6",
    "Summers - Scam Shop Slot 7",
    "Summers Harbor - Shop Slot 1",
    "Summers Harbor - Shop Slot 2",
    "Summers Harbor - Shop Slot 3",
    "Summers Harbor - Shop Slot 4",
    "Summers Harbor - Shop Slot 5",
    "Summers Harbor - Shop Slot 6",
    "Summers Harbor - Shop Slot 7",
    "Summers Restaurant - Slot 1",
    "Summers Restaurant - Slot 2",
    "Summers Restaurant - Slot 3",
    "Summers Restaurant - Slot 4",
    "Summers Restaurant - Slot 5",
    "Summers Restaurant - Slot 6",
    "Scaraba - Indoors Shop Slot 1",
    "Scaraba - Indoors Shop Slot 2",
    "Scaraba - Indoors Shop Slot 3",
    "Scaraba - Indoors Shop Slot 4",
    "Scaraba - Indoors Shop Slot 5",
    "Scaraba - Indoors Shop Slot 6",
    "Scaraba Bazaar - Red Snake Carpet Slot 1",
    "Scaraba Bazaar - Red Snake Carpet Slot 2",
    "Scaraba Bazaar - Red Snake Carpet Slot 3",
    "Scaraba Bazaar - Bottom Left Carpet Slot 1",
    "Scaraba Bazaar - Bottom Left Carpet Slot 2",
    "Scaraba Bazaar - Bottom Left Carpet Slot 3",
    "Scaraba Bazaar - Bottom Left Carpet Slot 4",
    "Scaraba Bazaar - Bottom Left Carpet Slot 5",
    "Scaraba Bazaar - Bottom Left Carpet Slot 6",
    "Scaraba Hotel - Arms Dealer Slot 1",
    "Scaraba Hotel - Arms Dealer Slot 2",
    "Scaraba Hotel - Arms Dealer Slot 3",
    "Scaraba Hotel - Arms Dealer Slot 4",
    "Deep Darkness - Businessman Slot 1",
    "Deep Darkness - Businessman Slot 2",
    "Deep Darkness - Businessman Slot 3",
    "Deep Darkness - Businessman Slot 4",
    "Deep Darkness - Businessman Slot 5",
    "Deep Darkness - Businessman Slot 6",
    "Deep Darkness - Businessman Slot 7",
    "Happy-Happy Village - Trust Shop Slot 1",
    "Happy-Happy Village - Trust Shop Slot 2",
    "Saturn Valley Shop - Post-Belch Saturn Slot 1",
    "Saturn Valley Shop - Post-Belch Saturn Slot 2",
    "Saturn Valley Shop - Post-Belch Saturn Slot 3",
    "Saturn Valley Shop - Post-Belch Saturn Slot 4",
    "Scaraba - Southern Camel Shop Slot 1",
    "Scaraba - Southern Camel Shop Slot 2",
    "Scaraba - Southern Camel Shop Slot 3",
    "Scaraba - Southern Camel Shop Slot 4",
    "Scaraba - Southern Camel Shop Slot 5",
    "Scaraba - Southern Camel Shop Slot 6",
    "Scaraba - Southern Camel Shop Slot 7",
    "Deep Darkness - Arms Dealer Slot 1",
    "Deep Darkness - Arms Dealer Slot 2",
    "Deep Darkness - Arms Dealer Slot 3",
    "Deep Darkness - Arms Dealer Slot 4",
    "Lost Underworld - Tenda Camp Shop Slot 1",
    "Lost Underworld - Tenda Camp Shop Slot 2",
    "Lost Underworld - Tenda Camp Shop Slot 3",
    "Lost Underworld - Tenda Camp Shop Slot 4",
    "Lost Underworld - Tenda Camp Shop Slot 5",
    "Lost Underworld - Tenda Camp Shop Slot 6",
    "Lost Underworld - Tenda Camp Shop Slot 7",
    "Happy-Happy Village Drugstore - Left Counter Slot 1",
    "Happy-Happy Village Drugstore - Left Counter Slot 2",
    "Happy-Happy Village Drugstore - Left Counter Slot 3",
    "Happy-Happy Village Drugstore - Left Counter Slot 4",
    "Happy-Happy Village Drugstore - Left Counter Slot 5",
    "Happy-Happy Village Drugstore - Left Counter Slot 6",
    "Happy-Happy Village Drugstore - Left Counter Slot 7",
    "Grapefruit Falls - Hiker Shop Slot 1",
    "Grapefruit Falls - Hiker Shop Slot 2",
    "Grapefruit Falls - Hiker Shop Slot 3",
    "Saturn Valley Shop - Top Saturn Slot 1",
    "Saturn Valley Shop - Top Saturn Slot 2",
    "Saturn Valley Shop - Top Saturn Slot 3",
    "Saturn Valley Shop - Top Saturn Slot 4",
    "Saturn Valley Shop - Top Saturn Slot 5",
    "Saturn Valley Shop - Top Saturn Slot 6",
    "Saturn Valley Shop - Top Saturn Slot 7",
    "Dusty Dunes Drugstore - Left Shop Slot 1",
    "Dusty Dunes Drugstore - Left Shop Slot 2",
    "Dusty Dunes Drugstore - Left Shop Slot 3",
    "Dusty Dunes Drugstore - Left Shop Slot 4",
    "Dusty Dunes Drugstore - Left Shop Slot 5",
    "Dusty Dunes Drugstore - Left Shop Slot 6",
    "Dusty Dunes Drugstore - Left Shop Slot 7",
    "Dusty Dunes - Mine Food Cart Slot 1",
    "Dusty Dunes - Mine Food Cart Slot 2",
    "Dusty Dunes - Mine Food Cart Slot 3",
    "Dusty Dunes - Mine Food Cart Slot 4",
    "Dusty Dunes - Mine Food Cart Slot 5",
    "Dusty Dunes - Mine Food Cart Slot 6",
    "Dusty Dunes - Mine Food Cart Slot 7",
    "Moonside Hotel - Shop Slot 1",
    "Moonside Hotel - Shop Slot 2",
    "Moonside Hotel - Shop Slot 3",
    "Moonside Hotel - Shop Slot 4",
    "Moonside Hotel - Shop Slot 5",
    "Dalaam Restaurant - Slot 1",
    "Dalaam Restaurant - Slot 2",
    "Dalaam Restaurant - Slot 3",
    "Dalaam Restaurant - Slot 4",
    "Scaraba Bazaar - Delicacy Shop Slot 1",
    "Scaraba Bazaar - Delicacy Shop Slot 2",
    "Scaraba Bazaar - Delicacy Shop Slot 3",
    "Scaraba Bazaar - Delicacy Shop Slot 4",
    "Scaraba Bazaar - Delicacy Shop Slot 5",
    "Scaraba Bazaar - Delicacy Shop Slot 6",
    "Scaraba Bazaar - Delicacy Shop Slot 7",
    "Twoson/Scaraba - Shared Condiment Shop Slot 1",
    "Twoson/Scaraba - Shared Condiment Shop Slot 2",
    "Twoson/Scaraba - Shared Condiment Shop Slot 3",
    "Twoson/Scaraba - Shared Condiment Shop Slot 4",
    "Twoson/Scaraba - Shared Condiment Shop Slot 5",
    "Twoson/Scaraba - Shared Condiment Shop Slot 6",
    "Twoson/Scaraba - Shared Condiment Shop Slot 7",
    "Andonuts Lab - Caveman Shop Slot 1",
    "Andonuts Lab - Caveman Shop Slot 2",
    "Andonuts Lab - Caveman Shop Slot 3",
    "Andonuts Lab - Caveman Shop Slot 4",
    "Andonuts Lab - Caveman Shop Slot 5"
}


def write_shop_checks(world: "EarthBoundWorld", rom: "LocalRom", shop_checks: list[Location]) -> None:
    unsellable_filler_prices = {
        "Broken Machine": 150,
        "Broken Air Gun": 110,
        "Broken Laser": 250,
        "Broken Pipe": 250,
        "Broken Tube": 800,
        "Broken Bazooka": 900,
        "Broken Trumpet": 500,
        "Broken Harmonica": 1500,
        "Counter-PSI Unit": 300,
        "Shield Killer": 500,
        "Heavy Bazooka": 1800,
        "Hungry HP-Sucker": 1600,
        "Defense Shower": 1000,
        "Neutralizer": 5000,
        "Brain Stone": 2,
        "Monkey's Love": 2
    }
    # Unique non-progression items that have no price by default. If they're on a shop,
    # give them a base price. (prog items are handled by the "price" variable)
    # Equipamizer already assigns prices to Equipment with no price, so they can be exempt.
    if not world.options.armorizer:
        unsellable_filler_prices["Cloak of Kings"] = 2000
        unsellable_filler_prices["Diadem of Kings"] = 1500
        unsellable_filler_prices["Bracer of Kings"] = 3500

    if not world.options.weaponizer:
        unsellable_filler_prices["Magicant Bat"] = 3000
        unsellable_filler_prices["Legendary Bat"] = 5000
        unsellable_filler_prices["Magnum Air Gun"] = 220
        unsellable_filler_prices["Laser Gun"] = 500
        unsellable_filler_prices["Baddest Beam"] = 3000

    if world.options.shop_randomizer == ShopRandomizer.option_shopsanity:
        rom.write_bytes(0x04FD77, bytearray([world.options.scout_shop_checks]))
        for location in shop_checks:

            flag = location.address - 0xEB1000
            if location.item.player == world.player:
                if world.options.remote_items:
                    if location.item.name in special_name_table or location.item.name in money_item_table:
                        item_type = 0x04
                        item_id = 0xAD
                    else:
                        item_type = 0x05
                        item_id = item_id_table[location.item.name]
                else:
                    if location.item.name in psi_item_table:
                        item_type = 0x01
                        item_id = psi_item_table[location.item.name]
                    elif location.item.name == "Photograph" and location.item.player == world.player:
                        item_type = 0x06
                        item_id = 0xAD
                    elif location.item.name in character_item_table:
                        item_type = 0x02
                        item_id = character_item_table[location.item.name][0]
                    elif location.item.name in money_item_table:
                        item_type = 0x07
                        item_id = list(money_item_table).index(location.item.name) + 1
                    else:
                        item_type = 0x00
                        item_id = item_id_table[location.item.name] 

                if location.item.name in unsellable_filler_prices and location.item.player == world.player:
                    rom.write_bytes(0x15501A + (item_id_table[location.item.name] * 39),
                                    struct.pack("H", unsellable_filler_prices[location.item.name]))

            else:
                item_type = 0x04
                item_id = 0xAD
        
            if ItemClassification.trap in location.item.classification:
                price = 0
            else:
                price = world.random.randint(1, (75 * world.area_levels[location.parent_region.name]))

            if location.parent_region.name in high_purchase_areas:
                price = int(price / 1.5)
            
            item_struct = struct.pack('<BHBH', item_id, price, item_type, flag)
            rom.write_bytes(0x34002A + (0x06 * flag), item_struct)
            menu_long_name = text_encoder(location.item.name, 127)
            menu_item_name = location.item.name[:0x30]
            menu_item_name = menu_item_name.replace(" ", " ")
            pixel_length = calc_pixel_width(menu_item_name)
            while pixel_length > 78:
                menu_item_name = menu_item_name[:-1]
                pixel_length = calc_pixel_width(menu_item_name)
            menu_item_name = text_encoder(menu_item_name, 0x30)
            player_name = text_encoder(world.multiworld.get_player_name(location.item.player), 16)
            player_name.append(0x00)
            rom.write_bytes(0x341190 + (flag * 0x30), menu_item_name)
            rom.write_bytes(0x3466D0 + (flag * 0x11), player_name)
            rom.write_bytes(0x351100 + (flag * 127), menu_long_name)

        rom.write_bytes(0x019DE5, struct.pack("I", 0xF007805C))  # Build the shop menus
        rom.write_bytes(0x019E23, struct.pack("I", 0xF008465C))  # Display the item name
        rom.write_bytes(0x019E8F, struct.pack("I", 0xF0094E5C))  # Display the item price
        rom.write_bytes(0x011AC6, struct.pack("I", 0xF009985C))  # display the player name
        rom.write_bytes(0x019EDD, struct.pack("I", 0xF00AA45C))  # Transfer the used data and player selection into a script for processing
        rom.write_bytes(0x019ED3, struct.pack("I", 0xF00ADD5C))  # Display SOLD OUT
        rom.write_bytes(0x019B66, struct.pack("I", 0xF00B0B5C))  # Prevent items for other players flashing the "you can equip this"
        rom.write_bytes(0x019DA0, struct.pack("I", 0xF00B275C))  # Preserve the greyed out HP/PP palette

        rom.write_bytes(0x05E0A9, struct.pack("I", 0xF4900008))  # Compare the price of the item with money on hand
        rom.write_bytes(0x05E0B6, struct.pack("I", 0xF4905808))  # Display the item we bought and ask to confirm
        # The player bought the item; set a flag and give it to them
        rom.write_bytes(0x05E0CE, struct.pack("I", 0xF493C30A))
        rom.write_bytes(0x05E0C8, struct.pack("I", 0xF493C3))
        rom.write_bytes(0x05DF1E, struct.pack("I", 0xF496140A))
        # Prevent the game from checking inventory space if not needed
        rom.write_bytes(0x05E029, struct.pack("I", 0xF496340A))
        rom.write_bytes(0x05E04C, struct.pack("I", 0xF496590A))
        rom.write_bytes(0x05E1AE, struct.pack("I", 0xF00EB8))  # Post-shop cleanup

        rom.write_bytes(0x05E1A5, struct.pack("I", 0xF00EAA))
        rom.write_bytes(0x05E119, struct.pack("I", 0xF00EB1))
        rom.write_bytes(0x05E0F2, struct.pack("I", 0xF00EC0))

        rom.write_bytes(0x3407E0, bytearray([item_id_table[world.filler_shop[0]], 0x00, 0x00, 0x00, 0x49, 0x01]))
        rom.write_bytes(0x3407E6, bytearray([item_id_table[world.filler_shop[1]], 0x00, 0x00, 0x00, 0x4A, 0x01]))

        rom.write_bytes(0x3408DC, bytearray([0xE0, 0x00, 0x00, 0x00, 0xFF, 0xFF]))
        rom.write_bytes(0x3408E2, bytearray([0x5D, 0x00, 0x00, 0x00, 0xFF, 0xFF]))
        rom.write_bytes(0x3408E8, bytearray([0x5A, 0x00, 0x00, 0x00, 0xFF, 0xFF]))
        rom.write_bytes(0x3408EE, bytearray([0x7F, 0x00, 0x00, 0x00, 0xFF, 0xFF]))
        rom.write_bytes(0x3408F4, bytearray([0x5F, 0x00, 0x00, 0x00, 0xFF, 0xFF]))
        rom.write_bytes(0x3408FA, bytearray([0x6C, 0x00, 0x00, 0x00, 0xFF, 0xFF]))
        rom.write_bytes(0x340900, bytearray([0x8C, 0x00, 0x00, 0x00, 0xFF, 0xFF]))

        if world.options.magicant_mode >= MagicantMode.option_alternate_goal:  # 2
            rom.write_bytes(0x3405E8, bytearray([item_id_table[world.magicant_junk[6]], 0x00, 0x00, 0x00, 0xF5, 0x00]))
            rom.write_bytes(0x3405EE, bytearray([item_id_table[world.magicant_junk[7]], 0x00, 0x00, 0x00, 0xF6, 0x00]))
    else:
        filler_shop_items = world.filler_drops.copy()
        filler_shop_items = [x for x in filler_shop_items if x not in [227, 228, 229, 230, 231, 0]]
        for location in location_ids:
            if location_ids[location] >= 0xEB1000:
                slot = location_ids[location] - 0xEB1000
                rom.write_bytes(0x1576B9 + slot, bytearray([world.random.choice(filler_shop_items)]))
                rom.write_bytes(0x1576e3, bytearray([0xEF]))
                rom.write_bytes(0x15779c, bytearray([0x5A]))
                if world.options.monkey_caves_mode < MonkeyCavesMode.option_shop:  # 2
                    rom.write_bytes(0x15776b, bytearray([0xE0]))
                    rom.write_bytes(0x157775, bytearray([0x8C]))
                    rom.write_bytes(0x157778, bytearray([0x6C]))
                    rom.write_bytes(0x157781, bytearray([0x5D]))
                    rom.write_bytes(0x157848, bytearray([0x7F]))  # DD Drugstore left counter 1
        rom.write_bytes(0x157802, bytearray([world.random.choice(filler_shop_items)]))
        rom.write_bytes(0x157803, bytearray([world.random.choice(filler_shop_items)]))
