# probably I should generate this from the list file

static_item_data_location = 0xe9d
static_item_element_size = 9
static_first_dragon_index = 6
item_position_table = 0x402
items_ram_start = 0xa1
connector_port_offset = 0xff9
# dragon speeds are hardcoded directly in their respective movement subroutines, not in their item table or state data
# so this is the second byte of an LDA immediate instruction
yorgle_speed_data_location = 0x724
grundle_speed_data_location = 0x73f
rhindle_speed_data_location = 0x709


# in case I need to place a rom address in the rom
rom_address_space_start = 0xf000

start_castle_offset = 0x39c
start_castle_values = [0x11, 0x10, 0x0F]
"""yellow, black, white castle gate rooms"""

# indexed by static item table index.  0x00 indicates the position data is in ROM and is irrelevant to the randomizer
item_ram_addresses = [
    0xD9,  # lamp
    0x00,  # portcullis 1
    0x00,  # portcullis 2
    0x00,  # portcullis 3
    0x00,  # author name
    0x00,  # GO object
    0xA4,  # Rhindle
    0xA9,  # Yorgle
    0xAE,  # Grundle
    0xB6,  # Sword
    0xBC,  # Bridge
    0xBF,  # Yellow Key
    0xC2,  # White key
    0xC5,  # Black key
    0xCB,  # Bat
    0xA1,  # Dot
    0xB9,  # Chalice
    0xB3,  # Magnet
    0xE7,  # AP object 1
    0xEA,  # AP bat object
    0xBC,  # NULL object (end of table)
]
