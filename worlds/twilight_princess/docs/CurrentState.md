# Current state of the World

Here is a file that lays out the basics for the current state of the randomizer

## Settings

All settings are functional in generation, some are not functionally changed in-game. For example Hyrule Castle Requirments can be set to "all dungeons". The world will generate and take that into account in logic. When you then play the game currently Hyrule Castle will be open, so you can self enfoce the requirement and not enter Hyrule Castle until all dungeons are defeated.

Note:
Known generation errors when generating with faron woods logic to closed or palace of twilight on non open. The errors are rare so regenerating with a new seed is likely to fix the errors.

## Client

The client has a command `/name` to allow you to change your in-game name upto 16 characters. (This is to be done before connecting to the server and after loading a save)

The client checks for version numbers of the generate seed and will log a message if the versions do not match. (I have not and do not plan to keep backwards compatiblity for a while as this apworld is still in Alpha)

With custom randomizer gci, defeating ganon will trigger the compleation of the world.

Non US Region support (EU, JP) currently under devlopment.

## Locations

The location settings will label locations as excluded which will means that they will prevent progession and usefull items from being placed at that location.
\*In some cases this will place the items in their vanilla location

With there being 475 locations in the game there are bound to be mistakes in the data. If you notice a location not triggering please leave a comment on the [Issue thread for it](https://github.com/WritingHusky/Twilight_Princess_apworld/issues/2)

## Generation

When generating the world, all possible locations will be created and given an item. Logic is based off the world data from the base randomizer web generator. (If you find logic weridness please make an issue for it)

## Dungeons

Dungeon Items: Small keys, Big keys, Maps and Compasses, can be shuffled into the world according to some settings. See the Yaml for info about the settings.
\*Some settings will alter the way these items are shuffled, more info in setting description.

# Message

Thank you all for spending the time to enjoy this. I would also like to thank every one who has been reporting things for me to fix.

If you could star this repo that would mean a lot to me, I like numbers to go up.

If you feel something is wrong with this file let me know so I can fix it. If it is wrong here then its is highly likely that I don't know about it.
