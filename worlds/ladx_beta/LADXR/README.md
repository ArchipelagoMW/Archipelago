# Legend Of Zelda: Link's Awakening DX: Randomizer
Or, LADXR for short.

## What is this?

See https://daid.github.io/LADXR/

## Usage

The only requirements are: to use python3, and the English v1.0 ROM for Links Awakening DX.

The proper SHA-1 for the rom is `d90ac17e9bf17b6c61624ad9f05447bdb5efc01a`.

Basic usage:
`python3 main.py zelda.gbc`

The script will generate a new rom with item locations shuffled. There are many options, see `-h` on the script for details.

## Development

This is still in the early stage of development. Important bits are:
* `randomizer.py`: Contains the actual logic to randomize the rom, and checks to make sure it can be solved.
* `logic/*.py`: Contains the logic definitions of what connects to what in the world and what it requires to access that part.
* `locations/*.py`: Contains definitions of location types, and what items can be there. As well as the code on how to place an item there. For example the Chest class has a list of all items that can be in a chest. And the needed rom patch to put that an item in a specific chest.
* `patches/*.py`: Various patches on the code that are not directly related to a specific location. But more general fixes 
