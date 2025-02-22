# Dark Souls III Randomizer Setup Guide

## Required Software

- [Dark Souls III](https://store.steampowered.com/app/374320/DARK_SOULS_III/)
- [Dark Souls III AP Client]

[Dark Souls III AP Client]: https://github.com/nex3/Dark-Souls-III-Archipelago-client/releases/latest

## Optional Software

- [Map tracker](https://github.com/TVV1GK/DS3_AP_Maptracker)

## Setting Up

First, download the client from the link above (`DS3.Archipelago.*.zip`). It doesn't need to go
into any particular directory; it'll automatically locate _Dark Souls III_ in your Steam
installation folder.

Version 3.0.0 of the randomizer _only_ supports the latest version of _Dark Souls III_, 1.15.2. This
is the latest version, so you don't need to do any downpatching! However, if you've already
downpatched your game to use an older version of the randomizer, you'll need to reinstall the latest
version before using this version. You should also delete the `dinput8.dll` file if you still have
one from an older randomizer version.

### One-Time Setup

Before you first connect to a multiworld, you need to generate the local data files for your world's
randomized item and (optionally) enemy locations. You only need to do this once per multiworld.

1. Before you first connect to a multiworld, run `randomizer\DS3Randomizer.exe`.

2. Put in your Archipelago room address (usually something like `archipelago.gg:12345`), your player
   name (also known as your "slot name"), and your password if you have one.

3. Click "Load" and wait a minute or two.

### Running and Connecting the Game

To run _Dark Souls III_ in Archipelago mode:

1. Start Steam. **Do not run in offline mode.** Running Steam in offline mode will make certain
   scripted invaders fail to spawn. Instead, change the game itself to offline mode on the menu
   screen.

2. Run `launchmod_darksouls3.bat`. This will start _Dark Souls III_ as well as a command prompt that
   you can use to interact with the Archipelago server.

3. Type `/connect {SERVER_IP}:{SERVER_PORT} {SLOT_NAME}` into the command prompt, with the
   appropriate values filled in. For example: `/connect archipelago.gg:24242 PlayerName`.

4. Start playing as normal. An "Archipelago connected" message will appear onscreen once you have
   control of your character and the connection is established.

## Frequently Asked Questions

### Where do I get a config file?

The [Player Options](/games/Dark%20Souls%20III/player-options) page on the website allows you to
configure your personal options and export them into a config file. The [AP client archive] also
includes an options template.

[AP client archive]: https://github.com/nex3/Dark-Souls-III-Archipelago-client/releases/latest

### Does this work with Proton?

The *Dark Souls III* Archipelago randomizer supports running on Linux under Proton. There are a few
things to keep in mind:

* Because `DS3Randomizer.exe` relies on the .NET runtime, you'll need to install
  the [.NET Runtime] under **plain [WINE]**, then run `DS3Randomizer.exe` under
  plain WINE as well. It won't work as a Proton app!

* To run the game itself, just run `launchmod_darksouls3.bat` under Proton.

[.NET Runtime]: https://dotnet.microsoft.com/en-us/download/dotnet/8.0
[WINE]: https://www.winehq.org/

## Troubleshooting

### Enemy randomizer issues

The DS3 Archipelago randomizer uses [thefifthmatt's DS3 enemy randomizer],
essentially unchanged. Unfortunately, this randomizer has a few known issues,
including enemy AI not working, enemies spawning in places they can't be killed,
and, in a few rare cases, enemies spawning in ways that crash the game when they
load. These bugs should be [reported upstream], but unfortunately the
Archipelago devs can't help much with them.

[thefifthmatt's DS3 enemy randomizer]: https://www.nexusmods.com/darksouls3/mods/484
[reported upstream]: https://github.com/thefifthmatt/SoulsRandomizers/issues

Because in rare cases the enemy randomizer can cause seeds to be impossible to
complete, we recommend disabling it for large async multiworlds for safety
purposes.

### `launchmod_darksouls3.bat` isn't working

Sometimes `launchmod_darksouls3.bat` will briefly flash a terminal on your
screen and then terminate without actually starting the game. This is usually
caused by some issue communicating with Steam either to find `DarkSoulsIII.exe`
or to launch it properly. If this is happening to you, make sure:

* You have DS3 1.15.2 installed. This is the latest patch as of January 2025.
  (Note that older versions of Archipelago required an older patch, but that
  _will not work_ with the current version.)

* You own the DS3 DLC if your randomizer config has DLC enabled. (It's possible,
  but unconfirmed, that you need the DLC even when it's disabled in your config).

* Steam is not running in administrator mode. To fix this, right-click
  `steam.exe` (by default this is in `C:\Program Files\Steam`), select
  "Properties", open the "Compatiblity" tab, and uncheck "Run this program as an
  administrator".

* There is no `dinput8.dll` file in your DS3 game directory. This is the old way
  of installing mods, and it can interfere with the new ModEngine2 workflow.

If you've checked all of these, you can also try:

* Running `launchmod_darksouls3.bat` as an administrator.

* Reinstalling DS3 or even reinstalling Steam itself.

* Making sure DS3 is installed on the same drive as Steam and as the randomizer.
  (A number of users are able to run these on different drives, but this has
  helped some users.)

If none of this works, unfortunately there's not much we can do. We use
ModEngine2 to launch DS3 with the Archipelago mod enabled, but unfortunately
it's no longer maintained and its successor, ModEngine3, isn't usable yet.

### `DS3Randomizer.exe` isn't working

This is almost always caused by using a version of the randomizer client that's
not compatible with the version used to generate the multiworld. If you're
generating your multiworld on archipelago.gg, you *must* use the latest [Dark
Souls III AP Client]. If you want to use a different client version, you *must*
generate the multiworld locally using the apworld bundled with the client.
