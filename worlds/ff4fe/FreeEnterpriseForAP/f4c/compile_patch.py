import re
from . import compile_common
from . import consts

def process_patch_block(block, rom, env):
    params_tree = compile_common.parse(block['parameters'], 'patch', 'patch_parameters')

    patch_address = params_tree.children[0]

    # tree parsing is being slow, so for the time being instead we'll just do a dumb
    # approach that'll work until we need fancier stuff, if ever
    patch_data = []
    for piece in block['body'].split():
        if piece.startswith('#'):
            piece_size = 0
            while piece.startswith('#'):
                piece_size += 1
                piece = piece[1:]
            v = consts.get_value(piece)
            if v is None:
                raise compile_common.CompileError("Cannot compile unrecognized const {} in patch block at {:02X}".format(piece, patch_address))
            while piece_size > 0:
                piece_size -= 1
                patch_data.append(v & 0xFF)
                v = v >> 8
        else:
            patch_data.extend([int(piece[i:i+2], 16) for i in range(0, len(piece), 2)])

    rom.add_patch(patch_address, patch_data)
