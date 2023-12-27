# How do I add a game to Archipelago?

This guide is going to try and be a broad summary of how you can do just that.  
There are two key steps to incorporating a game into Archipelago:

- Game Modification
- Archipelago Server Integration

Refer to the following documents as well:

- [network protocol.md](/docs/network%20protocol.md) for network communication between client and server.
- [world api.md](/docs/world%20api.md) for documentation on server side code and creating a world package.

# Game Modification

One half of the work required to integrate a game into Archipelago is the development of the game client. This is
typically done through a modding API or other modification process, described further down.

As an example, modifications to a game typically include (more on this later):

- Hooking into when a 'location check' is completed.
- Networking with the Archipelago server.
- Optionally, UI or HUD updates to show status of the multiworld session or Archipelago server connection.

In order to determine how to modify a game, refer to the following sections.

## Engine Identification

This is a good way to make the modding process much easier. Being able to identify what engine a game was made in is
critical. The first step is to look at a game's files. Let's go over what some game files might look like. It’s
important that you be able to see file extensions, so be sure to enable that feature in your file viewer of choice.  
Examples are provided below.

### Creepy Castle

![Creepy Castle Root Directory in Windows Explorer](/docs/img/creepy-castle-directory.png)

This is the delightful title Creepy Castle, which is a fantastic game that I highly recommend. It’s also your worst-case
scenario as a modder. All that’s present here is an executable file and some meta-information that Steam uses. You have
basically nothing here to work with. If you want to change this game, the only option you have is to do some pretty
nasty disassembly and reverse engineering work, which is outside the scope of this tutorial. Let’s look at some other
examples of game releases.

### Heavy Bullets

![Heavy Bullets Root Directory in Window's Explorer](/docs/img/heavy-bullets-directory.png)

Here’s the release files for another game, Heavy Bullets. We see a .exe file, like expected, and a few more files.
“hello.txt” is a text file, which we can quickly skim in any text editor. Many games have them in some form, usually
with a name like README.txt, and they may contain information about a game, such as a EULA, terms of service, licensing
information, credits, and general info about the game. You usually won’t find anything too helpful here, but it never
hurts to check. In this case, it contains some credits and a changelog for the game, so nothing too important.
“steam_api.dll” is a file you can safely ignore, it’s just some code used to interface with Steam.
The directory “HEAVY_BULLETS_Data”, however, has some good news.

![Heavy Bullets Data Directory in Window's Explorer](/docs/img/heavy-bullets-data-directory.png)

Jackpot! It might not be obvious what you’re looking at here, but I can instantly tell from this folder’s contents that
what we have is a game made in the Unity Engine. If you look in the sub-folders, you’ll seem some .dll files which
affirm our suspicions. Telltale signs for this are directories titled “Managed” and “Mono”, as well as the numbered,
extension-less level files and the sharedassets files. If you've identified the game as a Unity game, some useful tools
and information to help you on your journey can be found at this
[Unity Game Hacking guide.](https://github.com/imadr/Unity-game-hacking)

### Stardew Valley

![Stardew Valley Root Directory in Window's Explorer](/docs/img/stardew-valley-directory.png)

This is the game contents of Stardew Valley. A lot more to look at here, but some key takeaways.
Notice the .dll files which include “CSharp” in their name. This tells us that the game was made in C#, which is good
news. Many games made in C# can be modified using the same tools found in our Unity game hacking toolset; namely BepInEx
and MonoMod.

### Gato Roboto

![Gato Roboto Root Directory in Window's Explorer](/docs/img/gato-roboto-directory.png)

Our last example is the game Gato Roboto. This game is made in GameMaker, which is another green flag to look out for.
The giveaway is the file titled "data.win". This immediately tips us off that this game was made in GameMaker. For
modifying GameMaker games the [Undertale Mod Tool](https://github.com/krzys-h/UndertaleModTool) is incredibly helpful.

This isn't all you'll ever see looking at game files, but it's a good place to start.
As a general rule, the more files a game has out in plain sight, the more you'll be able to change.
This especially applies in the case of code or script files - always keep a lookout for anything you can use to your
advantage!

## Open or Leaked Source Games

As a side note, many games have either been made open source, or have had source files leaked at some point.
This can be a boon to any would-be modder, for obvious reasons. Always be sure to check - a quick internet search for
"(Game) Source Code" might not give results often, but when it does, you're going to have a much better time.

Be sure never to distribute source code for games that you decompile or find if you do not have express permission to do
so, or to redistribute any materials obtained through similar methods, as this is illegal and unethical.

## Modifying Release Versions of Games

However, for now we'll assume you haven't been so lucky, and have to work with only what’s sitting in your install
directory. Some developers are kind enough to deliberately leave you ways to alter their games, like modding tools,
but these are often not geared to the kind of work you'll be doing and may not help much.

As a general rule, any modding tool that lets you write actual code is something worth using.

### Research

The first step is to research your game. Even if you've been dealt the worst hand in terms of engine modification,
it's possible other motivated parties have concocted useful tools for your game already.
Always be sure to search the Internet for the efforts of other modders.

### Other helpful tools

Depending on the game’s underlying engine, there may be some tools you can use either in lieu of or in addition to
existing game tools.

#### [CheatEngine](https://cheatengine.org/)

CheatEngine is a tool with a very long and storied history.
Be warned that because it performs live modifications to the memory of other processes, it will likely be flagged as
malware (because this behavior is most commonly found in malware and rarely used by other programs).
If you use CheatEngine, you need to have a deep understanding of how computers work at the nuts and bolts level,
including binary data formats, addressing, and assembly language programming.

The tool itself is highly complex and even I have not yet charted its expanses.
However, it can also be a very powerful tool in the right hands, allowing you to query and modify gamestate without ever
modifying the actual game itself.
In theory it is compatible with any piece of software you can run on your computer, but there is no "easy way" to do
anything with it.

### What Modifications You Should Make to the Game

We talked about this briefly in [Game Modification](#game-modification) section.
The next step is to know what you need to make the game do now that you can modify it. Here are your key goals:

- Know when the player has checked a location, and react accordingly
- Be able to receive items from the server on the fly
- Keep an index for items received in order to resync from disconnections
- Add interface for connecting to the Archipelago server with passwords and sessions
- Add commands for manually rewarding, re-syncing, releasing, and other actions

Refer to the [Network Protocol documentation](/docs/network%20protocol.md) for how to communicate with Archipelago's
servers.

## But my Game is a console game. Can I still add it?

That depends – what console?

### My Game is a recent game for the PS4/Xbox-One/Nintendo Switch/etc

Most games for recent generations of console platforms are inaccessible to the typical modder. It is generally advised
that you do not attempt to work with these games as they are difficult to modify and are protected by their copyright
holders. Most modern AAA game studios will provide a modding interface or otherwise deny modifications for their console
games.

### My Game isn’t that old, it’s for the Wii/PS2/360/etc

This is very complex, but doable.
If you don't have good knowledge of stuff like Assembly programming, this is not where you want to learn it.
There exist many disassembly and debugging tools, but more recent content may have lackluster support.

### My Game is a classic for the SNES/Sega Genesis/etc

That’s a lot more feasible.
There are many good tools available for understanding and modifying games on these older consoles, and the emulation
community will have figured out the bulk of the console’s secrets.
Look for debugging tools, but be ready to learn assembly.
Old consoles usually have their own unique dialects of ASM you’ll need to get used to.

Also make sure there’s a good way to interface with a running emulator, since that’s the only way you can connect these
older consoles to the Internet.
There are also hardware mods and flash carts, which can do the same things an emulator would when connected to a
computer, but these will require the same sort of interface software to be written in order to work properly; from your
perspective the two won't really look any different.

### My Game is an exclusive for the Super Baby Magic Dream Boy. It’s this console from the Soviet Union that-

Unless you have a circuit schematic for the Super Baby Magic Dream Boy sitting on your desk, no.
Obscurity is your enemy – there will likely be little to no emulator or modding information, and you’d essentially be
working from scratch.

## How to Distribute Game Modifications

**NEVER EVER distribute anyone else's copyrighted work UNLESS THEY EXPLICITLY GIVE YOU PERMISSION TO DO SO!!!**

This is a good way to get any project you're working on sued out from under you.
The right way to distribute modified versions of a game's binaries, assuming that the licensing terms do not allow you
to copy them wholesale, is as patches.

There are many patch formats, which I'll cover in brief. The common theme is that you can’t distribute anything that
wasn't made by you. Patches are files that describe how your modified file differs from the original one, thus avoiding
the issue of distributing someone else’s original work.

Users who have a copy of the game just need to apply the patch, and those who don’t are unable to play.

### Patches

#### IPS

IPS patches are a simple list of chunks to replace in the original to generate the output. It is not possible to encode
moving of a chunk, so they may inadvertently contain copyrighted material and should be avoided unless you know it's
fine.

#### UPS, BPS, VCDIFF (xdelta), bsdiff

Other patch formats generate the difference between two streams (delta patches) with varying complexity. This way it is
possible to insert bytes or move chunks without including any original data. Bsdiff is highly optimized and includes
compression, so this format is used by APBP.

Only a bsdiff module is integrated into AP. If the final patch requires or is based on any other patch, convert them to
bsdiff or APBP before adding it to the AP source code as "basepatch.bsdiff4" or "basepatch.apbp".

#### APBP Archipelago Binary Patch

Starting with version 4 of the APBP format, this is a ZIP file containing metadata in `archipelago.json` and additional
files required by the game / patching process. For ROM-based games the ZIP will include a `delta.bsdiff4` which is the
bsdiff between the original and the randomized ROM.

To make using APBP easy, they can be generated by inheriting from `worlds.Files.APDeltaPatch`.

### Mod files

Games which support modding will usually just let you drag and drop the mod’s files into a folder somewhere.
Mod files come in many forms, but the rules about not distributing other people's content remain the same.
They can either be generic and modify the game using a seed or `slot_data` from the AP websocket, or they can be
generated per seed. If at all possible, it's generally best practice to collect your world information from `slot_data`
so that the users don't have to move files around in order to play.

If the mod is generated by AP and is installed from a ZIP file, it may be possible to include APBP metadata for easy
integration into the Webhost by inheriting from `worlds.Files.APContainer`.

## Archipelago Integration

In order for your game to communicate with the Archipelago server and generate the necessary randomized information,
you must create a world package in the main Archipelago repo. This section will cover the requisites and expectations
and show the basics of a world. More in depth documentation on the available API can be read in
the [world api doc.](/docs/world%20api.md)
For setting up your working environment with Archipelago refer
to [running from source](/docs/running%20from%20source.md) and the [style guide](/docs/style.md).

### Requirements

A world implementation requires a few key things from its implementation

- A folder within `worlds` that contains an `__init__.py`
    - This is what defines it as a Python package and how it's able to be imported
      into Archipelago's generation system. During generation time only code that is
      defined within this file will be run. It's suggested to split up your information
      into more files to improve readability, but all of that information can be
      imported at its base level within your world.
- A `World` subclass where you create your world and define all of its rules
  and the following requirements:
    - Your items and locations need a `item_name_to_id` and `location_name_to_id`,
      respectively, mapping.
    - An `option_definitions` mapping of your game options with the format
      `{name: Class}`, where `name` uses Python snake_case.
    - You must define your world's `create_item` method, because this may be called
      by the generator in certain circumstances
    - When creating your world you submit items and regions to the Multiworld.
        - These are lists of said objects which you can access at
          `self.multiworld.itempool` and `self.multiworld.regions`. Best practice for
          adding to these lists is with either `append` or `extend`, where `append` is a
          single object and `extend` is a list.
        - Do not use `=` as this will delete other worlds' items and regions.
        - Regions are containers for holding your world's Locations.
        - Locations are where players will "check" for items and must exist within
          a region. It's also important for your world's submitted items to be the same as
          its submitted locations count.
        - You must always have a "Menu" Region from which the generation algorithm
          uses to enter the game and access locations.
- Make sure to check out [world maintainer.md](/docs/world%20maintainer.md) before publishing.