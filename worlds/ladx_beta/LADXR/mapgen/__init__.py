from ..romTables import ROMWithTables
from ..roomEditor import RoomEditor, ObjectWarp
from ..patches import overworld, core
from .tileset import loadTileInfo
from .map import Map, MazeGen
from .wfc import WFCMap, ContradictionException
from .roomgen import setup_room_types
from .imagegenerator import ImageGen
from .util import xyrange
from .locations.entrance import DummyEntrance
from .locationgen import LocationGenerator
from .logic import LogicGenerator
from .enemygen import generate_enemies
from ..assembler import ASM


def store_map(rom, the_map: Map):
    # Move all exceptions to room FF
    # Dig seashells
    rom.patch(0x03, 0x220F, ASM("cp $DA"), ASM("cp $FF"))
    rom.patch(0x03, 0x2213, ASM("cp $A5"), ASM("cp $FF"))
    rom.patch(0x03, 0x2217, ASM("cp $74"), ASM("cp $FF"))
    rom.patch(0x03, 0x221B, ASM("cp $3A"), ASM("cp $FF"))
    rom.patch(0x03, 0x221F, ASM("cp $A8"), ASM("cp $FF"))
    rom.patch(0x03, 0x2223, ASM("cp $B2"), ASM("cp $FF"))
    # Force tile 04 under bushes and rocks, instead of conditionally tile 3, else seashells won't spawn.
    rom.patch(0x14, 0x1655, 0x1677, "", fill_nop=True)
    # Bonk trees
    rom.patch(0x03, 0x0F03, ASM("cp $A4"), ASM("cp $FF"))
    rom.patch(0x03, 0x0F07, ASM("cp $D2"), ASM("cp $FF"))
    # Stairs under rocks
    rom.patch(0x14, 0x1638, ASM("cp $52"), ASM("cp $FF"))
    rom.patch(0x14, 0x163C, ASM("cp $04"), ASM("cp $FF"))

    # Patch D6 raft game exit, just remove the exit.
    re = RoomEditor(rom, 0x1B0)
    re.removeObject(7, 0)
    re.store(rom)
    # Patch D8 back entrance, remove the outside part
    re = RoomEditor(rom, 0x23A)
    re.objects = [obj for obj in re.objects if not isinstance(obj, ObjectWarp)] + [ObjectWarp(1, 7, 0x23D, 0x58, 0x10)]
    re.store(rom)
    re = RoomEditor(rom, 0x23D)
    re.objects = [obj for obj in re.objects if not isinstance(obj, ObjectWarp)] + [ObjectWarp(1, 7, 0x23A, 0x58, 0x10)]
    re.store(rom)

    for room in the_map:
        for location in room.locations:
            location.prepare(rom)
    for n in range(0x00, 0x100):
        sx = n & 0x0F
        sy = ((n >> 4) & 0x0F)
        if sx < the_map.w and sy < the_map.h:
            tiles = the_map.get(sx, sy).tiles
        else:
            tiles = [4] * 80
            tiles[44] = 0xC6

        re = RoomEditor(rom, n)
        # tiles = re.getTileArray()
        re.objects = []
        re.entities = []
        room = the_map.get(sx, sy) if sx < the_map.w and sy < the_map.h else None

        tileset = the_map.tilesets[room.tileset_id] if room else None
        rom.banks[0x3F][0x3F00 + n] = tileset.main_id if tileset else 0x0F
        rom.banks[0x21][0x02EF + n] = tileset.palette_id if tileset and tileset.palette_id is not None else 0x03
        rom.banks[0x1A][0x2476 + n] = tileset.attr_bank if tileset and tileset.attr_bank else 0x22
        rom.banks[0x1A][0x1E76 + n * 2] = (tileset.attr_addr & 0xFF) if tileset and tileset.attr_addr else 0x00
        rom.banks[0x1A][0x1E77 + n * 2] = (tileset.attr_addr >> 8) if tileset and tileset.attr_addr else 0x60
        re.animation_id = tileset.animation_id if tileset and tileset.animation_id is not None else 0x03

        re.buildObjectList(tiles)
        if room:
            for idx, tile_id in enumerate(tiles):
                if tile_id == 0x61:  # Fix issues with the well being used as chimney as well and causing wrong warps
                    DummyEntrance(room, idx % 10, idx // 10)
            re.entities += room.entities
            room.locations.sort(key=lambda loc: (loc.y, loc.x, id(loc)))
            for location in room.locations:
                location.update_room(rom, re)
        else:
            re.objects.append(ObjectWarp(0x01, 0x10, 0x2A3, 0x50, 0x7C))
        re.store(rom)

    rom.banks[0x21][0x00BF:0x00BF+3] = [0, 0, 0]  # Patch out the "load palette on screen transition" exception code.

    # Fix some tile attribute issues
    def change_attr(tileset, index, a, b, c, d):
        rom.banks[the_map.tilesets[tileset].attr_bank][the_map.tilesets[tileset].attr_addr - 0x4000 + index * 4 + 0] = a
        rom.banks[the_map.tilesets[tileset].attr_bank][the_map.tilesets[tileset].attr_addr - 0x4000 + index * 4 + 1] = b
        rom.banks[the_map.tilesets[tileset].attr_bank][the_map.tilesets[tileset].attr_addr - 0x4000 + index * 4 + 2] = c
        rom.banks[the_map.tilesets[tileset].attr_bank][the_map.tilesets[tileset].attr_addr - 0x4000 + index * 4 + 3] = d
    change_attr("mountains", 0x04, 6, 6, 6, 6)
    change_attr("mountains", 0x27, 6, 6, 3, 3)
    change_attr("mountains", 0x28, 6, 6, 3, 3)
    change_attr("mountains", 0x6E, 1, 1, 1, 1)
    change_attr("town", 0x59, 2, 2, 2, 2)  # Roof tile wrong color


def generate(rom_filename, w, h):
    rom = ROMWithTables(rom_filename)
    overworld.patchOverworldTilesets(rom)
    core.cleanup(rom)
    tilesets = loadTileInfo(rom)

    the_map = Map(w, h, tilesets)
    setup_room_types(the_map)

    MazeGen(the_map)
    imggen = ImageGen(tilesets, the_map, rom)
    imggen.enabled = False
    wfcmap = WFCMap(the_map, tilesets) #, step_callback=imggen.on_step)
    try:
        wfcmap.initialize()
    except ContradictionException as e:
        print(f"Failed on setup {e.x // 10} {e.y // 8} {e.x % 10} {e.y % 8}")
        imggen.on_step(wfcmap, err=(e.x, e.y))
        return
    imggen.on_step(wfcmap)
    for x, y in xyrange(w, h):
        for n in range(50):
            try:
                wfcmap.build(x * 10, y * 8, 10, 8)
                imggen.on_step(wfcmap)
                break
            except ContradictionException as e:
                print(f"Failed {x} {y} {e.x%10} {e.y%8} {n}")
                imggen.on_step(wfcmap, err=(e.x, e.y))
                wfcmap.clear()
            if n == 49:
                raise RuntimeError("Failed to fill chunk")
        print(f"Done {x} {y}")
    imggen.on_step(wfcmap)
    wfcmap.store_tile_data(the_map)

    LocationGenerator(the_map)

    for room in the_map:
        generate_enemies(room)

    if imggen.enabled:
        store_map(rom, the_map)
        from mapexport import MapExport
        MapExport(rom).export_all(w, h, dungeons=False)
        rom.save("test.gbc")
    return the_map
