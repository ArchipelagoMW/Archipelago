from . import compile_common

def process_shop_block(block, rom, env):
    params_tree = compile_common.parse(block['parameters'], 'shop', 'shop_block_params')
    tree = compile_common.parse(block['body'], 'shop', 'shop_block_body')

    item_list = (list(tree.children) + ([0xFF] * 8))[:8]

    rom.shops[params_tree.children[0]] = item_list
