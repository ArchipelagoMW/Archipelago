# Dark Souls III Randomizer Setup Guide

[Game Page] | Setup | [Items] | [Locations] | [Enemy Randomization]

[Game Page]: /games/Dark%20Souls%20III/info/en
[Items]: /tutorial/Dark%20Souls%20III/items/en
[Locations]: /tutorial/Dark%20Souls%20III/locations/en
[Enemy Randomization]: /tutorial/Dark%20Souls%20III/enemy-randomization/en

## Required Software

- [Dark Souls III](https://store.steampowered.com/app/374320/DARK_SOULS_III/)
- [Dark Souls III AP Client]

[Dark Souls III AP Client]: https://github.com/fswap/ds3-archipelago/releases/latest

## Optional Software

- [Map tracker](https://github.com/TVV1GK/DS3_AP_Maptracker)

## Setting Up

First, download the client from the link above (`DS3.Archipelago.*.zip`). It doesn't need to go
into any particular directory; it'll automatically locate _Dark Souls III_ in your Steam
installation folder.

Version 4.0.0 of the randomizer _only_ supports the latest version of _Dark Souls III_, 1.15.2. This
is the latest version, so you don't need to do any downpatching!

### Running the Static Randomizer

Before you first connect to a multiworld, you need to generate the local data files for your world's
randomized item and (optionally) enemy locations. You only need to do this once per multiworld.

1. Before you first connect to a multiworld, run `randomizer\DS3Randomizer.exe`.

2. Put in your Archipelago room address (usually something like `archipelago.gg:12345`), your player
   name (also known as your "slot name"), and your password if you have one.

3. Click "Load" and wait a minute or two.

### Running and Connecting the Game

To run _Dark Souls III_ in Archipelago mode:

1. Start Steam. **Do not run Steam in offline mode.** Running Steam in offline mode will make
   certain scripted invaders fail to spawn. ModEngine3 will automatically make sure that _Dark Souls
   III_ doesn't connect to the Steam servers, so you won't get penalized for playing a modded game.

2. Run `launch-ds3.bat`. This will start _Dark Souls III_ with your mod injected. It will also start
   a terminal window, but you can ignore this. All your interactions with Archipelago will be in the
   game itself.

3. As soon as the game starts, you'll see an overlay in the top right corner. This is the
   Archipelago client: it will tell you when you're connected to the server, it will show any server
   messages, and it will allow you to send messages to the server.

4. In most cases, the overlay will connect without any issue. If the connection fails, that's
   probably because the server went to sleep or the URL changed. Go to your room page on
   archipelago.gg to wake it up and then click "Reconnect". If the URL changed, click "Change URL"
   instead and tell it the new one.

## Frequently Asked Questions

### Where do I get a config file?

The [AP client archive] also includes a YAML template that documents all the options. You can
customize this to suit your needs.

[AP client archive]: https://github.com/fswap/ds3-archipelago/releases/latest

### Does this work with Proton?

The *Dark Souls III* Archipelago randomizer supports running on Linux under Proton. There are a few
things to keep in mind:

* Make sure you download the `*-linux.tar.gz` file from the releases page.

* Because `DS3Randomizer.exe` relies on the .NET runtime, you'll need to install the [.NET Runtime]
  under **plain [WINE]**, then run `DS3Randomizer.exe` under plain WINE as well. It won't work as a
  Proton app!

* To run the game itself, just run the `launch-ds3.sh` script. No need to run this under Proton;
  ModEngine3 takes care of that for you.

[.NET Runtime]: https://dotnet.microsoft.com/en-us/download/dotnet/6.0
[WINE]: https://www.winehq.org/

## Troubleshooting

### Enemy randomizer issues

The DS3 Archipelago randomizer uses [thefifthmatt's DS3 enemy randomizer], essentially unchanged.
Unfortunately, this randomizer has a few known issues, including enemy AI not working, enemies
spawning in places they can't be killed, and, in a few rare cases, enemies spawning in ways that
crash the game when they load. These bugs should be [reported upstream], but unfortunately the
Archipelago devs can't help much with them.

[thefifthmatt's DS3 enemy randomizer]: https://www.nexusmods.com/darksouls3/mods/484
[reported upstream]: https://github.com/thefifthmatt/SoulsRandomizers/issues

If you're running into an enemy randomizer bug that's severely affecting your run, you can re-run
`randomizer\DS3Randomizer.exe` and check the "Disable Enemy Randomizer" option. This will preserve
all your item randomization but put the enemies back into their vanilla locations. Once you're past
the buggy part, you can re-run it again with randomization enabled.

### The game crashes when I go to a specific location

This is almost certainly caused by enemy randomization issues. As above, re-run
`randomizer\DS3Randomizer.exe` and check the "Disable Enemy Randomizer" option.

### `launch-ds3.bat` isn't working

Sometimes `launch-ds3.bat` will briefly flash a terminal on your screen and then terminate without
actually starting the game. This is usually caused by some issue communicating with Steam either to
find `DarkSoulsIII.exe` or to launch it properly. If this is happening to you, make sure:

* You have DS3 1.15.2 installed. This is the latest patch as of January 2025. (Note that older
  versions of Archipelago required an older patch, but that _will not work_ with the current
  version.)

* You own the DS3 DLC if your randomizer config has DLC enabled. (It's possible, but unconfirmed,
  that you need the DLC even when it's disabled in your config.)

* Steam is not running in administrator mode. To fix this, right-click `steam.exe` (by default this
  is in `C:\Program Files\Steam`), select "Properties", open the "Compatiblity" tab, and uncheck
  "Run this program as an administrator".

* There is no `dinput8.dll` file in your DS3 game directory. This is the old way of installing mods,
  and it can interfere with the new ModEngine2 workflow.

* You're not using any other mods for DS3. While it's possible to use the Archipelago mod along with
  other mods, support isn't guaranteed, and mod conflicts are a likely source of problems when
  loading the game.

If you've checked all of these, you can also try:

* Running `launch-ds3.bat` as an administrator.

* Reinstalling DS3 or even reinstalling Steam itself.

* Making sure DS3 is installed on the same drive as Steam and as the randomizer. (A number of users
  are able to run these on different drives, but this has helped some users.)

If none of this works, open `me3-config.me3` in a text editor and replace the last two sections
with:

```toml
# [[natives]]
# path = "archipelago.dll"
# 
# [[packages]]
# path = "randomizer"
```

This tells it not to even try loading the Archipelago mod. If `launch-ds3.bat` still doesn't work,
[report the bug to ModEngine3].

[report the bug to ModEngine3]: https://github.com/garyttierney/me3/discussions/categories/bug-reports

### `DS3Randomizer.exe` isn't working

This is usually caused by using a version of the randomizer client that's not compatible with the
version used to generate the multiworld. If you're generating your multiworld on archipelago.gg, you
*must* use the latest [Dark Souls III AP Client]. If you want to use a different client version, you
*must* generate the multiworld locally using the apworld bundled with the client.

Other things to check include that your room is running and the URL is what you expect it to be, and
that Windows is configured to allow `DS3Randomizer.exe` to communicate on your network (usually this
is a private network).

## Reporting a Bug or Requesting Help

If you're having an issue and the troubleshooting guide isn't enough to help, reach out to the
[Archipelago DS3 Discord] for assistance. When you do so, you'll find people will be much more
helpful if you provide the following information:

[Archipelago DS3 Discord]: https://discord.com/channels/731205301247803413/1005246392329052220

* The version of the client you're using. **Just saying "the latest version" isn't enough**, please
  provide an actual version number!

* A screenshot of the error you're seeing, if there's an error message of any kind.

* Information about what you were doing when the error ocurred. Were you trying to generate a
  multiworld? Were you running DS3Randomizer.exe? Were you running `launch-ds3.bat`? Were you doing
  something in the game?

* Your room URL (the one that starts with `https://archipelago.gg/room/`, *not* the one that starts
  with `archipelago.gg:`) and your slot name. Often times the best way for someone to help you is to
  have direct access to your slot.

* If you can, provide your spoiler log as well. If you don't have access to it, ask the person
  running your multiworld.

When in doubt, provide more information than you think we'll need!
