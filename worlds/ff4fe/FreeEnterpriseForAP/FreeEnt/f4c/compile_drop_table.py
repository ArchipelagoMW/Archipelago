from . import ff4struct
from . import compile_common

def process_droptable_block(block, rom, env):
    params_tree = compile_common.parse(block['parameters'], 'drop_table', 'droptable_block_params')
    droptable_id = params_tree.children[0]

    droptable = ff4struct.drop_table.decode(rom.drop_tables[droptable_id])

    tree = compile_common.parse(block['body'], 'drop_table', 'droptable_block_body')
    for entry in tree.children:
        item = None
        if len(entry.children) > 1:
            item = entry.children[1]
        rarity = str(entry.children[0].children[0])
        if rarity not in ['common', 'uncommon', 'rare', 'mythic']:
            raise compile_common.CompileError(f"Unsupported drop table rarity {rarity} in drop table ${droptable_id:02X}")
        setattr(droptable, rarity, item)

    rom.drop_tables[droptable_id] = droptable.encode()
