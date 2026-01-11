# Logic module for Bowser Door randomization.

import inspect
import random

from ...randomizer import data
from ...randomizer.logic import flags
from ...randomizer.logic.patch import Patch


def patch_bowser_doors(world):
    """

    Args:
        world (randomizer.logic.main.GameWorld):

    Returns:
        randomizer.logic.patch.Patch: Patch data.

    """
    patch = Patch()

    if world.settings.is_flag_enabled(flags.ShuffleBowsersKeep):
        def find_subclasses(module, clazz):
            return [
                cls
                for name, cls in inspect.getmembers(module)
                if inspect.isclass(cls) and issubclass(cls, clazz) and cls != clazz
            ]

        all_rooms = find_subclasses(data.locations, data.locations.BowserRoom)
        doors = [[], [], [], [], [], []]
        assigned_rooms = []

        # remove backward exits
        for i in all_rooms:
            if i.backward_exit_byte > 0:
                patch.add_data(i.backward_exit_byte, 15)
            if i.backward_event_byte > 0:
                patch.add_data(i.backward_event_byte, 15)
            if i.is_final:
                patch.add_data(i.change_event_byte, [0x4C, 0x81])

        for i in range(0, len(doors)):
            for j in range(0, 3):
                room = random.choice([r for r in all_rooms if r not in assigned_rooms])
                doors[i].append(room)
                assigned_rooms.append(room)

        # exits and event exits need to go to room 240, patch room 240 to run event 332 on load and music
        patch.add_data(0x1D40D5, [0xF0, 0xA0, 0x93, 0x1C, 0x05, 0x02, 0x39, 0xE0, 0x81, 0xF0, 0xA0])
        patch.add_data(0x1D4307, [0xF0, 0xA0])
        patch.add_data(0x1D46E4, [0xF0, 0xA0, 0x92, 0x1B, 0x03, 0x06, 0x2F, 0xE1, 0x81, 0x42, 0xA1, 0x87, 0x76, 0x02,
                                  0x1A, 0x58, 0x62, 0x81, 0xF0, 0xA0, 0x95, 0x56, 0x02, 0x16, 0x7B, 0xE0, 0x81, 0xF0,
                                  0xA0, 0x96, 0x19, 0x00, 0x02, 0x3F, 0xE0, 0x81, 0xF0, 0xA0, 0x96, 0x19, 0x00, 0x02,
                                  0x3F, 0xE0, 0x81, 0xF0, 0xA0])
        patch.add_data(0x204E8D, [0xF0, 0x80, 0x02, 0x37, 0xE0, 0xFE, 0x68, 0xF0, 0x80])
        patch.add_data(0x20502A, [0xF0, 0x80])
        patch.add_data(0x205285, [0xF0, 0x80])
        patch.add_data(0x20F217, [0x42, 0x4C, 0x01])
        # battle rooms should load BK2 music
        patch.add_data(0x20F6CD, [0x42])
        patch.add_data(0x20F6E8, [0x42])
        patch.add_data(0x20FB8D, [0x42])
        patch.add_data(0x20FBA8, [0x42])
        patch.add_data(0x20FBC3, [0x42])
        patch.add_data(0x20FBE4, [0x42])
        # patch final rooms so that they always run event 332 on exit
        patch.add_data(0x20F703, [0x4C, 0x81])
        patch.add_data(0x20FB6C, [0x4C, 0x81])
        patch.add_data(0x20FB75, [0x4C, 0x81])
        patch.add_data(0x20FBDE, [0x4C, 0x81])
        patch.add_data(0x20FC11, [0x4C, 0x81])
        patch.add_data(0x20FC1D, [0x4C, 0x81])

        # modify event 2121 to set tries counter to 10 at the start of each of the 6 starter rooms and then load
        # their original entrance event, and initiate counter
        # start of event checks to see if it's a retry on a platforming room - specifically for Z-platform room
        event_patch_data = [0xE0, 0x2B, 0x00, 0xBA, 0x7A, 0xE4, 0x2D, 0x01, 0x00, 0xBD, 0x7A, 0xE4, 0x2D, 0x05, 0x00,
                            0xBD, 0x7A, 0xE4, 0x2D, 0x09, 0x00, 0xBD, 0x7A, 0xE4, 0x2D, 0x0D, 0x00, 0xBD, 0x7A, 0xE4,
                            0x2D, 0x11, 0x00, 0xBD, 0x7A, 0xE4, 0x2D, 0x15, 0x00, 0xBD, 0x7A, 0xA8, 0x2B, 0x0A, 0xC3,
                            0xE2, 0xCF, 0x01, 0xDC, 0x7A, 0xE2, 0xD3, 0x01, 0xE4, 0x7A, 0xE2, 0xC8, 0x01, 0xEC, 0x7A,
                            0xE2, 0xD1, 0x01, 0xF4, 0x7A, 0xE2, 0xD2, 0x01, 0xFC, 0x7A, 0xE2, 0xC9, 0x01, 0x04, 0x7B,
                            0xB0, 0x2D, 0x01, 0x00, 0xD0, 0x1A, 0x0D, 0xFE, 0xB0, 0x2D, 0x05, 0x00, 0xD0, 0x0F, 0x00,
                            0xFE, 0xB0, 0x2D, 0x09, 0x00, 0xD0, 0x2C, 0x07, 0xFE, 0xB0, 0x2D, 0x0D, 0x00, 0xD0, 0x1E,
                            0x0D, 0xFE, 0xB0, 0x2D, 0x11, 0x00, 0xD0, 0x24, 0x0D, 0xFE, 0xB0, 0x2D, 0x15, 0x00, 0xD0,
                            0x2B, 0x07, 0xFE]
        patch.add_data(0x1F7A91, event_patch_data)
        i = 0x1F7A91 + len(event_patch_data)
        while i <= 0x1F7B0C:
            patch.add_data(i, 0x9B)
            i += 1

        # fix Z-platform room failing to reload on failure - force it to run entrance event on reload at original coords
        # this only affects this one room for some reason
        # this means that if you fail at any point in this room, you will go back to the beginning of it
        # oh well. git gud
        patch.add_data(0x1F5666, [0x81, 0x04, 0x3A, 0xE5])

        # 6 entrance doors
        initial_door_room_addresses = [0x205CCD, 0x205CD4, 0x205CDB, 0x205CE2, 0x205CE9, 0x205CF0]
        initial_door_coord_addresses = [0x205CCF, 0x205CD6, 0x205CDD, 0x205CE4, 0x205CEB, 0x205CF2]

        # remove any 10-try set events from rooms so that they dont reset if in the middle of a chain
        patch.add_data(0x1F5462, [0xA6, 0xAC, 0xD0, 0x25, 0x07, 0xFE, 0x9B, 0xFE])
        patch.add_data(0x1F5531,
                       [0xA6, 0xAC, 0x9C, 0x0B, 0x15, 0xF2, 0x36, 0x03, 0x16, 0xF2, 0x36, 0x03, 0x17, 0xF2, 0x36, 0x03,
                        0xD0, 0x25, 0x07, 0xFE, 0x9B, 0xFE])

        # DYNAMIC WRITING OF EVENT 332 #
        # man, this is some shit #
        # dont ask me what the hell i did here but it apparently works #
        # this code completely replaces event 332 and calculates where jump pointers need to go, as some rooms have
        # special conditions on how the entrance event should run, meaning varying byte size #
        original_address = 0x1E2291
        ram_jump_data = []
        room_counters = [1, 2, 5, 6, 9, 10, 13, 14, 17, 18, 21, 22]
        for counter in room_counters:
            ram_jump_data.append([0xE4, 0x2D, counter, 0x00, 0, 0])
        treasure_room_ram_jump = [0xD2, 0x00, 0x00]
        room_increments = [2, 3, 6, 7, 10, 11, 14, 15, 18, 19, 22, 23]
        ram_load_event_data = []

        for index, door in enumerate(doors):
            # set bowser door # to this room
            patch.add_data(initial_door_room_addresses[index], [door[0].relative_room_id])
            patch.add_data(initial_door_coord_addresses[index],
                           [door[0].start_x, door[0].start_y, door[0].start_z + 0xE0])
            # set tries to 10 and load original room event
            patch.add_data(0x1f7ABF + (index * 5), door[0].relative_room_id)
            patch.add_data(0x1f7AE1 + (index * 8), door[0].original_event)
            patch.add_data(door[0].original_event_location, [0x49, 0x08])
            for j in range(0, len(door)):
                if j + 1 < len(door):
                    current_condition_address = original_address + 6 * len(ram_jump_data) + len(
                        treasure_room_ram_jump)
                    for l in range(0, index * 2 + j):
                        current_condition_address += len(ram_load_event_data[l])
                    addr = format(current_condition_address, 'x').zfill(6)
                    ram_jump_data[index * 2 + j][4] = int(addr[4:6], 16)
                    ram_jump_data[index * 2 + j][5] = int(addr[2:4], 16)
                    patchdata = []
                    patchdata.extend((0xB0, 0x2D, room_increments[index * 2 + j], 0x00))
                    if door[j + 1].relative_room_id == 0xD1:
                        patchdata.extend((0xB0, 0x1F, 0x00, 0x00))
                    patchdata.extend((0xF0, 0x00))
                    if not door[j].needs_manual_run_on_exit:
                        patchdata.extend((0x68, door[j + 1].relative_room_id, 0x81, door[j + 1].start_x,
                                          door[j + 1].start_y, door[j + 1].start_z + 0xE0))
                        patchdata.append(0x71)
                    else:
                        patchdata.extend((0x68, door[j + 1].relative_room_id, 0x01, door[j + 1].start_x,
                                          door[j + 1].start_y, door[j + 1].start_z + 0xE0))
                        patchdata.append(0x71)
                        patchdata.extend((0xD0, door[j + 1].original_event[0], door[j + 1].original_event[1]))
                    patchdata.append(0xFE)
                    ram_load_event_data.append(patchdata)

        treasure_room_jump_address = original_address
        for l in ram_jump_data:
            treasure_room_jump_address += len(l)
        treasure_room_jump_address += len(treasure_room_ram_jump)
        for l in ram_load_event_data:
            treasure_room_jump_address += len(l)
        addr = format(treasure_room_jump_address, 'x').zfill(6)
        treasure_room_ram_jump[1] = int(addr[4:6], 16)
        treasure_room_ram_jump[2] = int(addr[2:4], 16)

        combined_data = []
        for i in ram_jump_data:
            for j in i:
                combined_data.append(j)
        for j in treasure_room_ram_jump:
            combined_data.append(j)
        for i in ram_load_event_data:
            for j in i:
                combined_data.append(j)

        combined_data.extend((0xF0, 0x00))
        combined_data.extend((0xF3, 0x90, 0xA8))
        combined_data.extend((0xF3, 0xBE, 0xA9))
        combined_data.extend((0xB4, 0x17))
        combined_data.extend((0xFD, 0xB0, 0x70, 0x00))
        addr = treasure_room_jump_address
        jumpaddr = format(addr + 0x32, 'x').zfill(6)
        combined_data.extend((0xE2, 0x20, 0x00, int(jumpaddr[4:6], 16), int(jumpaddr[2:4], 16)))
        jumpaddr = format(addr + 0x32 + 0x0B, 'x').zfill(6)
        combined_data.extend((0xE2, 0x30, 0x00, int(jumpaddr[4:6], 16), int(jumpaddr[2:4], 16)))
        jumpaddr = format(addr + 0x32 + 0x0B + 0x0B, 'x').zfill(6)
        combined_data.extend((0xE2, 0x40, 0x00, int(jumpaddr[4:6], 16), int(jumpaddr[2:4], 16)))
        jumpaddr = format(addr + 0x32 + 0x0B + 0x0B + 0x0B, 'x').zfill(6)
        combined_data.extend((0xE2, 0x50, 0x00, int(jumpaddr[4:6], 16), int(jumpaddr[2:4], 16)))
        jumpaddr = format(addr + 0x32 + 0x0B + 0x0B + 0x0B + 0x0B, 'x').zfill(6)
        combined_data.extend((0xE2, 0x60, 0x00, int(jumpaddr[4:6], 16), int(jumpaddr[2:4], 16)))
        combined_data.extend((0xB4, 0x47))
        combined_data.extend((0xFD, 0xB1, 0x80, 0x00))
        combined_data.extend((0xB5, 0x47))
        jump1 = int(format(addr + 0x66, 'x').zfill(6)[4:6], 16)
        jump2 = int(format(addr + 0x66, 'x').zfill(6)[2:4], 16)
        combined_data.extend((0xD2, jump1, jump2))
        combined_data.extend((0xB4, 0x47))
        combined_data.extend((0xFD, 0xB1, 0x08, 0x00))
        combined_data.extend((0xB5, 0x47))
        combined_data.extend((0xD2, jump1, jump2))
        combined_data.extend((0xB4, 0x48))
        combined_data.extend((0xFD, 0xB1, 0x80, 0x00))
        combined_data.extend((0xB5, 0x48))
        combined_data.extend((0xD2, jump1, jump2))
        combined_data.extend((0xB4, 0x48))
        combined_data.extend((0xFD, 0xB1, 0x08, 0x00))
        combined_data.extend((0xB5, 0x48))
        combined_data.extend((0xD2, jump1, jump2))
        combined_data.extend((0xB4, 0x49))
        combined_data.extend((0xFD, 0xB1, 0x80, 0x00))
        combined_data.extend((0xB5, 0x49))
        combined_data.extend((0xD2, jump1, jump2))
        combined_data.extend((0xB4, 0x49))
        combined_data.extend((0xFD, 0xB1, 0x08, 0x00))
        combined_data.extend((0xB5, 0x49))
        combined_data.extend((0xB4, 0x17))
        combined_data.extend((0xFD, 0xB0, 0x07, 0x00))
        combined_data.extend((0xAD, 0x00, 0x02))
        combined_data.append(0xAF)
        clearaddr1 = int(format(addr + 0x66 + 0x13, 'x').zfill(6)[4:6], 16)
        clearaddr2 = int(format(addr + 0x66 + 0x13, 'x').zfill(6)[2:4], 16)
        combined_data.extend((0xDF, clearaddr1, clearaddr2))
        combined_data.extend((0xF3, 0x90, 0x28))
        combined_data.extend((0xF3, 0xBE, 0x29))
        finaladdr1 = int(format(addr + 0x8A, 'x').zfill(6)[4:6], 16)
        finaladdr2 = int(format(addr + 0x8A, 'x').zfill(6)[2:4], 16)
        combined_data.extend((0xAA, 0x16))
        if world.settings.is_flag_enabled(flags.BowsersKeep1):
            combined_data.extend((0xE0, 0x16, 0x01, finaladdr1, finaladdr2))
        elif world.settings.is_flag_enabled(flags.BowsersKeep2):
            combined_data.extend((0xE0, 0x16, 0x02, finaladdr1, finaladdr2))
        elif world.settings.is_flag_enabled(flags.BowsersKeep3):
            combined_data.extend((0xE0, 0x16, 0x03, finaladdr1, finaladdr2))
        elif world.settings.is_flag_enabled(flags.BowsersKeep5):
            combined_data.extend((0xE0, 0x16, 0x05, finaladdr1, finaladdr2))
        elif world.settings.is_flag_enabled(flags.BowsersKeep6):
            combined_data.extend((0xE0, 0x16, 0x06, finaladdr1, finaladdr2))
        else:
            combined_data.extend((0xE0, 0x16, 0x04, finaladdr1, finaladdr2))
        combined_data.extend((0xF0, 0x00))
        combined_data.extend((0x68, 0x90, 0x80, 0x04, 0x4F, 0xE0))
        combined_data.append(0x71)
        combined_data.append(0xFE)
        combined_data.extend((0xF0, 0x00))
        combined_data.extend((0x68, 0xBE, 0x81, 0x10, 0x4F, 0xE0))
        combined_data.append(0x71)

        c2 = []
        for i in combined_data:
            c2.append(format(i, 'x').zfill(2))

        patch.add_data(original_address, combined_data)
        i = original_address + len(combined_data)
        while i <= 0x1E24C6:
            patch.add_data(i, 0x9B)
            i += 1

    # Also need to patch the original event!!! In case Ds flag isn't enabled
    if world.settings.is_flag_enabled(flags.BowsersKeep1):
        patch.add_data(0x204CAD, 1)
    elif world.settings.is_flag_enabled(flags.BowsersKeep2):
        patch.add_data(0x204CAD, 2)
    elif world.settings.is_flag_enabled(flags.BowsersKeep3):
        patch.add_data(0x204CAD, 3)
    elif world.settings.is_flag_enabled(flags.BowsersKeep4):
        patch.add_data(0x204CAD, 4)
    elif world.settings.is_flag_enabled(flags.BowsersKeep5):
        patch.add_data(0x204CAD, 5)
    elif world.settings.is_flag_enabled(flags.BowsersKeep6):
        patch.add_data(0x204CAD, 6)

    return patch
