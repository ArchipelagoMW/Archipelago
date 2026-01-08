# The Minish Cap

## Where is the options page?

This is currently a custom world so there is no options page yet. In order to
create your options you'll need to download one of the starter YAMLs on the GitHub releases page. Alternatively you can create the default yaml by following the Archipelago `&template` guide:

How to generate a template yaml:  For Core-Verified apworlds, your \Players\Templates folder will already have template yamls by default.  For Custom apworlds, install the apworld first by double clicking on it, then open ArchipelagoLauncher.exe to start the Launcher, and click on Generate Template Options to create template yamls for all of the apworlds in your \custom_worlds folder as well as your \lib\worlds folder.  After you click on this button, a File Explorer window will open (on Windows) pointing directly to your \Players\Templates folder, with all of the new template files.  Use these to create player options for any of the apworlds you have installed, Core-Verified or Custom.

## What does randomization do to this game?

This randomizer handles item randomization only. Inventory items, Quest items, Elements, Heart Pieces/Containers,
Scrolls and rupees can all be randomized.

Kinstones & Fusions are not *yet* included. The game will act as if every fusion has already occurred and no kinstones
will drop from grass/enemies.

## What items and locations get randomized?

Locations:
- Big/Small Chests
- Heart Pieces/Containers
- Shops
- Dojo Items
- Dig Spots
- Rupees

Items:
- All inventory items
- Quest Items
- Heart Pieces/Containers
- Dungeon Keys, Maps & Compasses
- Elements
- Scrolls
- Rupees
- Refills (hearts, bombs & arrows)

## What other changes are made to the game?

The game has been modified to open the world up much more than vanilla. You will start with Ezlo, and all the opening
cutscenes along with many other story events will be skipped. Hyrule Town has also been modified to make nearly every
location accessible at any point.

There are also a small handful of QoL changes made for convenience. Here are some of the more important ones:

- The ability to quickwarp in the save menu (effectively save, quitting and loading in one option)
- Showing the amount of dungeon small/big keys, the compass and map while hovering over the region of any particular
  dungeon on the world map.
- Recording various stats such as when specific items were acquired for display at the credits
- Making multiple items be given progressively.
- And of course removing as much of Ezlo's dialog as possible. Seriously, who thought a talking hat was a good idea?

## What does another world's item look like in The Minish Cap?

Items from worlds other than your own will show up as a clock icon, however, this is a temporary sprite until an ap
item sprite is made. The following item types will show up as different colors:
- Progression: Green
- Useful: Blue
- Normal/Filler: Red
- Trap: A random appearance of Green/Blue/Red

## When the player receives an item, what happens?

Most items will trigger the short "Get Item" cutscene where Link holds up the item. Others such as bottles, rupees,
dungeon items and refills won't trigger the cutscene. They'll simply be placed directly into your inventory menu,
viewable on one of the three pause screens.

## Can I play offline?

Yes, the client and connector are only necessary for sending and receiving items. If you're playing a solo game, you
don't need to play online unless you want the rest of Archipelago's functionality (like hints and auto-tracking). If
you're playing a multiworld game, the client will sync your game with the server the next time you connect.
