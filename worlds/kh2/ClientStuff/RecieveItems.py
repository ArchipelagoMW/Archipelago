from CommonClient import logger
from typing import TYPE_CHECKING
from .WorldLocations import *
from ..Names import ItemName
import re
import asyncio


def to_khscii(self, item_name):
    # credit to TopazTK for this.
    out_list = []
    char_count = 0
    # Throughout the text, do:
    while char_count < len(item_name):
        char = item_name[char_count]
        # Simple character conversion through mathematics.
        if 'a' <= char <= 'z':
            out_list.append(ord(char) + 0x39)
            char_count += 1
        elif 'A' <= char <= 'Z':
            out_list.append(ord(char) - 0x13)
            char_count += 1
        elif '0' <= char <= '9':
            out_list.append(ord(char) + 0x60)
            char_count += 1
        # If it hits a "{", we will know it's a command, not a character.
        elif char == '{':
            # A command is 6 characters long, in the format of "{0xTT}",
            # with the "TT" being the 2-digit encode for that command.
            command = item_name[char_count:char_count + 6]
            if re.match(r'^{0x[a-fA-F0-9][a-fA-F0-9]}$', command):
                value = command[1:5]
                out_list.append(int(value, 16))
                char_count += 6
        # Should it be anything we do not know, we look through
        # the special dictionary.
        else:
            if char in self.special_dict:
                out_list.append(self.special_dict[char])
            else:
                out_list.append(0x01)
            char_count += 1

    # When the list ends, we add a terminator and return the string.
    out_list.append(0x00)
    return out_list


async def give_item(self, item, location):
    try:
        #sleep so we can get the datapackage and not miss any items that were sent to us while we didnt have our item id dicts
        while not self.lookup_id_to_item:
            await asyncio.sleep(0.5)
        itemname = self.lookup_id_to_item[item]
        itemdata = self.item_name_to_data[itemname]
        # itemcode = self.kh2_item_name_to_id[itemname]
        if itemdata.ability:
            if location in self.all_weapon_location_id:
                return
            if itemname in {"High Jump", "Quick Run", "Dodge Roll", "Aerial Dodge", "Glide"}:
                self.kh2_seed_save_cache["AmountInvo"]["Growth"][itemname] += 1
                return

            if itemname not in self.kh2_seed_save_cache["AmountInvo"]["Ability"]:
                self.kh2_seed_save_cache["AmountInvo"]["Ability"][itemname] = []
                #  appending the slot that the ability should be in
            #  appending the slot that the ability should be in
            # abilities have a limit amount of slots.
            # we start from the back going down to not mess with stuff.
            # Front of Invo
            # Sora:   Save+24F0+0x54 : 0x2546
            # Donald: Save+2604+0x54 : 0x2658
            # Goofy:  Save+2718+0x54 : 0x276C
            # Back of Invo. Sora has 6 ability slots that are reserved
            # Sora:   Save+24F0+0x54+0x92 : 0x25D8
            # Donald: Save+2604+0x54+0x9C : 0x26F4
            # Goofy:  Save+2718+0x54+0x9C : 0x2808
            # seed has 2 scans in sora's abilities
            # recieved second scan
            # if len(seed_save(Scan:[ability slot 52]) < (2)amount of that ability they should have from slot data
            # ability_slot = back of inventory that isnt taken
            # add ability_slot to seed_save(Scan[]) so now its Scan:[ability slot 52,50]
            # decrease back of inventory since its ability_slot is already taken
            if len(self.kh2_seed_save_cache["AmountInvo"]["Ability"][itemname]) < \
                    self.AbilityQuantityDict[itemname]:
                if itemname in self.sora_ability_set:
                    ability_slot = self.kh2_seed_save_cache["SoraInvo"][0]
                    self.kh2_seed_save_cache["AmountInvo"]["Ability"][itemname].append(ability_slot)
                    self.kh2_seed_save_cache["SoraInvo"][0] -= 2
                elif itemname in self.donald_ability_set:
                    ability_slot = self.kh2_seed_save_cache["DonaldInvo"][0]
                    self.kh2_seed_save_cache["AmountInvo"]["Ability"][itemname].append(ability_slot)
                    self.kh2_seed_save_cache["DonaldInvo"][0] -= 2
                else:
                    ability_slot = self.kh2_seed_save_cache["GoofyInvo"][0]
                    self.kh2_seed_save_cache["AmountInvo"]["Ability"][itemname].append(ability_slot)
                    self.kh2_seed_save_cache["GoofyInvo"][0] -= 2

                if ability_slot in self.front_ability_slots:
                    self.front_ability_slots.remove(ability_slot)
        # if itemdata in {bitmask} all the forms,summons and a few other things are bitmasks
        elif itemdata.memaddr in {0x36C4, 0x36C5, 0x36C6, 0x36C0, 0x36CA}:
            # if memaddr is in a bitmask location in memory
            if itemname not in self.kh2_seed_save_cache["AmountInvo"]["Bitmask"]:
                self.kh2_seed_save_cache["AmountInvo"]["Bitmask"].append(itemname)

        # if itemdata in {magic}
        elif itemdata.memaddr in {0x3594, 0x3595, 0x3596, 0x3597, 0x35CF, 0x35D0}:
            # if memaddr is in magic addresses
            self.kh2_seed_save_cache["AmountInvo"]["Magic"][itemname] += 1
        # equipment is a list instead of dict because you can only have 1 currently
        elif itemname in self.all_equipment:
            if itemname in self.kh2_seed_save_cache["AmountInvo"]["Equipment"]:
                self.kh2_seed_save_cache["AmountInvo"]["Equipment"][itemname] += 1
            else:
                self.kh2_seed_save_cache["AmountInvo"]["Equipment"][itemname] = 1
        # weapons are done differently since you can only have one and has to check it differently
        elif itemname in self.all_weapons:
            if itemname in self.keyblade_set:
                self.kh2_seed_save_cache["AmountInvo"]["Weapon"]["Sora"].append(itemname)
            elif itemname in self.staff_set:
                self.kh2_seed_save_cache["AmountInvo"]["Weapon"]["Donald"].append(itemname)
            else:
                self.kh2_seed_save_cache["AmountInvo"]["Weapon"]["Goofy"].append(itemname)

        elif itemname in self.stat_increase_set:
            self.kh2_seed_save_cache["AmountInvo"]["StatIncrease"][itemname] += 1
        else:
            # "normal" items. They have a unique byte reserved for how many they have
            if itemname in self.kh2_seed_save_cache["AmountInvo"]["Amount"]:
                self.kh2_seed_save_cache["AmountInvo"]["Amount"][itemname] += 1
            else:
                self.kh2_seed_save_cache["AmountInvo"]["Amount"][itemname] = 1

    except Exception as e:
        if self.kh2connected:
            self.kh2connected = False
        logger.info(e)
        logger.info("line 582")


async def IsInShop(self, sellable):
    # journal = 0x741230 shop = 0x741320
    # if journal=-1 and shop = 5 then in shop
    # if journal !=-1 and shop = 10 then journal

    journal = self.kh2_read_short(self.Journal)
    shop = self.kh2_read_short(self.Shop)
    if (journal == -1 and shop == 5) or (journal != -1 and shop == 10):
        # print("your in the shop")
        sellable_dict = {}
        # for item that the player has received that can be sold
        # get amount of sellable items PRE selling them
        # basically a snapshot of what the amounts of these items are pre shopping
        for itemName in sellable:
            itemdata = self.item_name_to_data[itemName]
            amount = self.kh2_read_byte(self.Save + itemdata.memaddr)
            sellable_dict[itemName] = amount
        # wait until user exits the shop
        while (journal == -1 and shop == 5) or (journal != -1 and shop == 10):
            journal = self.kh2_read_short(self.Journal)
            shop = self.kh2_read_short(self.Shop)
            await asyncio.sleep(0.5)
        # for item and amount pre shop
        for item, amount in sellable_dict.items():
            itemdata = self.item_name_to_data[item]
            afterShop = self.kh2_read_byte(self.Save + itemdata.memaddr)
            alreadySold = 0
            if item in self.kh2_seed_save["SoldEquipment"]:
                alreadySold = self.kh2_seed_save["SoldEquipment"][item]
            # if afterShop is < Amount post shop i.e if someone sold something
            if afterShop < amount:
                self.kh2_seed_save["SoldEquipment"][item] = (amount - afterShop) + alreadySold


async def verifyItems(self):
    try:
        # All these sets include items that the player has recieved
        # set of all the items that have an
        master_amount = list(self.kh2_seed_save_cache["AmountInvo"]["Amount"].keys())
        # set of all the items that have are abilities
        master_ability = list(self.kh2_seed_save_cache["AmountInvo"]["Ability"].keys())
        # set of all the items that are bitmasks
        master_bitmask = list(self.kh2_seed_save_cache["AmountInvo"]["Bitmask"])
        # sets of all the weapons. These are different because have to check inventory and equipped
        master_keyblade = list(self.kh2_seed_save_cache["AmountInvo"]["Weapon"]["Sora"])
        master_staff = list(self.kh2_seed_save_cache["AmountInvo"]["Weapon"]["Donald"])
        master_shield = list(self.kh2_seed_save_cache["AmountInvo"]["Weapon"]["Goofy"])
        # Same with weapons but a lot more slots
        master_equipment = list(self.kh2_seed_save_cache["AmountInvo"]["Equipment"].keys())
        # Set of magic, Can only be given when  the player is paused due to crashing in loadzones
        master_magic = list(self.kh2_seed_save_cache["AmountInvo"]["Magic"].keys())
        # Have to apply them to the slot that sora is in and a lot more dynamic than other amount items
        master_stat = list(self.kh2_seed_save_cache["AmountInvo"]["StatIncrease"].keys())
        # Set of all things that could be sold
        master_sell = master_equipment + master_staff + master_shield

        await asyncio.create_task(self.IsInShop(master_sell))
        # print(self.kh2_seed_save_cache["AmountInvo"]["Ability"])
        for item_name in master_amount:
            item_data = self.item_name_to_data[item_name]
            amount_of_items = 0
            amount_of_items += self.kh2_seed_save_cache["AmountInvo"]["Amount"][item_name]

            if item_name == "Torn Page":
                # Torn Pages are handled differently because they can be consumed.
                # Will check the progression in 100 acre and - the amount of visits
                # amountofitems-amount of visits done
                for location, data in tornPageLocks.items():
                    if self.kh2_read_byte(self.Save + data.addrObtained) & 0x1 << data.bitIndex > 0:
                        amount_of_items -= 1
            # 255 is the max limit for a byte
            if amount_of_items > 255:
                amount_of_items = 255
            if self.kh2_read_byte(self.Save + item_data.memaddr) != amount_of_items and amount_of_items >= 0:
                self.kh2_write_byte(self.Save + item_data.memaddr, amount_of_items)

        for item_name in master_keyblade:
            item_data = self.item_name_to_data[item_name]
            # if the inventory slot for that keyblade is less than the amount they should have,
            # and they are not in stt
            if self.kh2_read_byte(self.Save + item_data.memaddr) != 1 and self.kh2_read_byte(
                    self.Save + 0x1CFF) != 13:
                # Checking form anchors for the keyblade to remove extra keyblades
                # Checking Normal Sora,Valor Form,Master Form and Final Forms keyblades
                if self.kh2_read_short(self.Save + 0x24F0) == item_data.kh2id \
                        or self.kh2_read_short(self.Save + 0x32F4) == item_data.kh2id \
                        or self.kh2_read_short(self.Save + 0x339C) == item_data.kh2id \
                        or self.kh2_read_short(self.Save + 0x33D4) == item_data.kh2id:
                    self.kh2_write_byte(self.Save + item_data.memaddr, 0)
                else:
                    self.kh2_write_byte(self.Save + item_data.memaddr, 1)

        for item_name in master_staff:
            item_data = self.item_name_to_data[item_name]
            if self.kh2_read_byte(self.Save + item_data.memaddr) != 1 \
                    and self.kh2_read_short(self.Save + 0x2604) != item_data.kh2id \
                    and item_name not in self.kh2_seed_save["SoldEquipment"]:
                self.kh2_write_byte(self.Save + item_data.memaddr, 1)

        for item_name in master_shield:
            item_data = self.item_name_to_data[item_name]
            if self.kh2_read_byte(self.Save + item_data.memaddr) != 1 \
                    and self.kh2_read_short(self.Save + 0x2718) != item_data.kh2id \
                    and item_name not in self.kh2_seed_save["SoldEquipment"]:
                self.kh2_write_byte(self.Save + item_data.memaddr, 1)

        for item_name in master_ability:
            item_data = self.item_name_to_data[item_name]
            ability_slot = []
            ability_slot += self.kh2_seed_save_cache["AmountInvo"]["Ability"][item_name]
            for slot in ability_slot:
                current = self.kh2_read_short(self.Save + slot)
                ability = current & 0x0FFF
                if ability | 0x8000 != (0x8000 + item_data.memaddr):
                    if current - 0x8000 > 0:
                        self.kh2_write_short(self.Save + slot, 0x8000 + item_data.memaddr)
                    else:
                        self.kh2_write_short(self.Save + slot, item_data.memaddr)
        # removes the duped ability if client gave faster than the game.

        for ability in self.front_ability_slots:
            if self.kh2_read_short(self.Save + ability) != 0:
                print(f"removed {self.Save + ability} from {ability}")
                self.kh2_write_short(self.Save + ability, 0)

        # remove the dummy level 1 growths if they are in these invo slots.
        for inventorySlot in {0x25CE, 0x25D0, 0x25D2, 0x25D4, 0x25D6, 0x25D8}:
            current = self.kh2_read_short(self.Save + inventorySlot)
            ability = current & 0x0FFF
            if 0x05E <= ability <= 0x06D:
                self.kh2_write_short(self.Save + inventorySlot, 0)

        for item_name in self.master_growth:
            growthLevel = self.kh2_seed_save_cache["AmountInvo"]["Growth"][item_name]
            if growthLevel > 0:
                slot = self.growth_values_dict[item_name][2]
                min_growth = self.growth_values_dict[item_name][0]
                max_growth = self.growth_values_dict[item_name][1]
                if growthLevel > 4:
                    growthLevel = 4
                current_growth_level = self.kh2_read_short(self.Save + slot)
                ability = current_growth_level & 0x0FFF

                # if the player should be getting a growth ability
                if ability | 0x8000 != 0x8000 + min_growth - 1 + growthLevel:
                    # if it should be level one of that growth
                    if 0x8000 + min_growth - 1 + growthLevel <= 0x8000 + min_growth or ability < min_growth:
                        self.kh2_write_short(self.Save + slot, min_growth)
                    # if it is already in the inventory
                    elif ability | 0x8000 < (0x8000 + max_growth):
                        self.kh2_write_short(self.Save + slot, current_growth_level + 1)

        for item_name in master_bitmask:
            item_data = self.item_name_to_data[item_name]
            itemMemory = self.kh2_read_byte(self.Save + item_data.memaddr)
            if self.kh2_read_byte(self.Save + item_data.memaddr) & 0x1 << item_data.bitmask == 0:
                # when getting a form anti points should be reset to 0 but bit-shift doesn't trigger the game.
                if item_name in {"Valor Form", "Wisdom Form", "Limit Form", "Master Form", "Final Form"}:
                    self.kh2_write_byte(self.Save + 0x3410, 0)
                self.kh2_write_byte(self.Save + item_data.memaddr, itemMemory | 0x01 << item_data.bitmask)

        for item_name in master_equipment:
            item_data = self.item_name_to_data[item_name]
            amount_found_in_slots = 0
            if item_name in self.accessories_set:
                Equipment_Anchor_List = self.Equipment_Anchor_Dict["Accessories"]
            else:
                Equipment_Anchor_List = self.Equipment_Anchor_Dict["Armor"]
                # Checking form anchors for the equipment
            for partyMember in ["Sora", "Donald", "Goofy"]:
                for SlotOffset in Equipment_Anchor_List:
                    if self.kh2_read_short(self.Save + self.CharacterAnchors[partyMember] + SlotOffset) == item_data.kh2id:
                        amount_found_in_slots += 1
            if item_name in self.kh2_seed_save["SoldEquipment"]:
                amount_found_in_slots += self.kh2_seed_save["SoldEquipment"][item_name]
            inInventory = self.kh2_seed_save_cache["AmountInvo"]["Equipment"][item_name] - amount_found_in_slots
            if inInventory != self.kh2_read_byte(self.Save + item_data.memaddr):
                self.kh2_write_byte(self.Save + item_data.memaddr, inInventory)

        for item_name in master_magic:
            item_data = self.item_name_to_data[item_name]
            amount_of_items = 0
            amount_of_items += self.kh2_seed_save_cache["AmountInvo"]["Magic"][item_name]
            # - base address because it reads a pointer then in stead of reading what it points to its pointer+baseaddress which offsets
            if self.kh2_read_byte(self.Save + item_data.memaddr) != amount_of_items and self.kh2_read_byte(self.FadeStatus) == 0 \
                    and self.kh2_read_longlong(self.PlayerGaugePointer) != 0 \
                    and self.kh2_read_int(self.kh2_read_longlong(self.PlayerGaugePointer) + 0x88 - self.kh2_return_base_address()) != 0:
                self.kh2_write_byte(self.Save + item_data.memaddr, amount_of_items)

        for item_name in master_stat:
            amount_of_items = 0
            amount_of_items += self.kh2_seed_save_cache["AmountInvo"]["StatIncrease"][item_name]
            # checking if they talked to the computer to give them these
            if self.kh2_read_byte(self.Slot1 + 0x1B2) >= 5 and (self.kh2_read_byte(self.Save + 0x1D27) & 0x1 << 3) > 0:
                if item_name == ItemName.MaxHPUp:
                    if self.kh2_read_byte(self.Save + 0x2498) < 3:  # Non-Critical
                        Bonus = 5
                    else:  # Critical
                        Bonus = 2
                    if self.kh2_read_int(self.Slot1 + 0x004) != self.base_hp + (Bonus * amount_of_items):
                        self.kh2_write_int(self.Slot1 + 0x004, self.base_hp + (Bonus * amount_of_items))

                elif item_name == ItemName.MaxMPUp:
                    if self.kh2_read_byte(self.Save + 0x2498) < 3:  # Non-Critical
                        Bonus = 10
                    else:  # Critical
                        Bonus = 5
                    if self.kh2_read_int(self.Slot1 + 0x184) != self.base_mp + (Bonus * amount_of_items):
                        self.kh2_write_int(self.Slot1 + 0x184, self.base_mp + (Bonus * amount_of_items))

                elif item_name == ItemName.DriveGaugeUp:
                    current_max_drive = self.kh2_read_byte(self.Slot1 + 0x1B2)
                    # change when max drive is changed from 6 to 4
                    # drive is maxed at 9 and base_drive is always 5 so if amount is higher set to 4 which is the max it should be
                    amount_of_items = min(amount_of_items, 4)
                    if current_max_drive < 9 and current_max_drive != self.base_drive + amount_of_items:
                        self.kh2_write_byte(self.Slot1 + 0x1B2, self.base_drive + amount_of_items)
                # need to do these differently when the amount is dynamic
                elif item_name == ItemName.AccessorySlotUp:
                    current_accessory = self.kh2_read_byte(self.Save + 0x2501)
                    if current_accessory != self.base_accessory_slots + amount_of_items:
                        if 4 > current_accessory < self.base_accessory_slots + amount_of_items:
                            self.kh2_write_byte(self.Save + 0x2501, current_accessory + 1)
                        elif self.base_accessory_slots + amount_of_items < 4:
                            self.kh2_write_byte(self.Save + 0x2501, self.base_accessory_slots + amount_of_items)

                elif item_name == ItemName.ArmorSlotUp:
                    current_armor_slots = self.kh2_read_byte(self.Save + 0x2500)
                    if current_armor_slots != self.base_armor_slots + amount_of_items:
                        if 4 > current_armor_slots < self.base_armor_slots + amount_of_items:
                            self.kh2_write_byte(self.Save + 0x2500, current_armor_slots + 1)
                        elif self.base_armor_slots + amount_of_items < 4:
                            self.kh2_write_byte(self.Save + 0x2500, self.base_armor_slots + amount_of_items)

                elif item_name == ItemName.ItemSlotUp:
                    current_item_slots = self.kh2_read_byte(self.Save + 0x2502)
                    if current_item_slots != self.base_item_slots + amount_of_items:
                        if 8 > current_item_slots < self.base_item_slots + amount_of_items:
                            self.kh2_write_byte(self.Save + 0x2502, current_item_slots + 1)
                        elif self.base_item_slots + amount_of_items < 8:
                            self.kh2_write_byte(self.Save + 0x2502, self.base_item_slots + amount_of_items)

            # if self.kh2_read_byte(self.Save + item_data.memaddr) != amount_of_items \
            #        and self.kh2_read_byte(self.Slot1 + 0x1B2) >= 5 and \
            #        self.kh2_read_byte(self.Save + 0x23DF) & 0x1 << 3 > 0 and self.kh2_read_byte(0x741320) in {10, 8}:
            #    self.kh2_write_byte(self.Save + item_data.memaddr, amount_of_items)

        if "PoptrackerVersionCheck" in self.kh2slotdata:
            if self.kh2slotdata["PoptrackerVersionCheck"] > 4.2 and self.kh2_read_byte(
                    self.Save + 0x3607) != 1:  # telling the goa they are on version 4.3
                self.kh2_write_byte(self.Save + 0x3607, 1)

    except Exception as e:
        if self.kh2connected:
            self.kh2connected = False
        logger.info(e)
        logger.info("line 840")


async def displayInfoTextinGame(self, string_to_display):
    infoBarPointerRef = self.kh2_read_longlong(self.InfoBarPointer)
    if self.kh2_read_byte(0x800000) == 0 and infoBarPointerRef != 0 and self.kh2.read_int(infoBarPointerRef + 0x48) == 0:
        self.kh2_write_byte(0x800000, 1)  # displaying info bar popup
        displayed_string = self.to_khscii(string_to_display)
        self.kh2_write_bytes(0x800004, displayed_string)
        self.queued_info_popup.remove(string_to_display)
        await asyncio.sleep(0.5)


async def displayPuzzlePieceTextinGame(self, string_to_display):
    if self.kh2_read_byte(0x800000) == 0:
        displayed_string = self.to_khscii(string_to_display)
        self.kh2_write_bytes(0x800104, displayed_string)
        self.kh2_write_byte(0x800000, 2)  # displaying puzzle piece popup
        self.queued_puzzle_popup.remove(string_to_display)
        await asyncio.sleep(0.5)


async def displayChestTextInGame(self, string_to_display):
    if self.kh2_read_byte(0x800000) == 0:

        displayed_string = self.to_khscii(string_to_display)
        print(f"made display string {displayed_string} from {string_to_display}")
        self.kh2_write_byte(0x800150, 0)  # item picture. this will change from 0 when I can input icons from the items
        print("wrote item picture")
        self.kh2_write_bytes(0x800154, displayed_string)  # text
        print("wrote text")
        await asyncio.sleep(1)
        self.kh2_write_byte(0x800000, 3)  # displaying chest popup
        print("called chest popup")

        self.queued_chest_popup.remove(string_to_display)
        await asyncio.sleep(0.5)
