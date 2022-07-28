# Archipelago Setup Guide

This guide provides an overview of how to install, set up, and run the Archipelago multiworld software.

## Installing the Archipelago software

The most recent public release of Archipelago can be found on the
[GitHub releases page](https://github.com/ArchipelagoMW/Archipelago/releases).

Run the .exe file. After accepting the license agreement, you will be asked which components you would like to install.
Read below for more information.

1. The first component is the `Generator`. It is not needed to play games with Archipelago -- our website also has a
generator that does not need to be installed. If you install the generator, it allows you to create a multiworld using
only your own computer.
   - If you want to use this generator with certain games, you will need to enable their "ROM Setup" options
     now, and you will need a legally-obtained ROM for each of those games.


2. The second component is the `Server`. It is also not needed to play games with Archipelago -- our website can host
multiworlds using its own server. If you install the server, it allows you to host multiworlds on your own computer.
   - Unless you will be the only player, hosting on your own computer is for advanced users only. It requires forwarding
     the port you are hosting on. We do not provide a guide for how to do this. The default port for Archipelago is
     `38281`.


3. The last components are the `Clients`. They __are__ needed to play games with Archipelago. If you see a game that you
don't intend to play with Archipelago, you may uncheck it now. 
   - You will need a legally-obtained ROM for each game that uses ROMS.

If you change your mind and would like to install more components later, simply run the .exe again and check the boxes
for each new component.

Once the installer finishes, you're done installing the basics for Archipelago! However, each individual game needs
additional setup to work properly. Check out the [Supported Games](https://archipelago.gg/games) page to see what each
randomizer is like and how to set them up.

## Generating a multiworld

### Overview

Archipelago needs to know which worlds it's working with, and what those worlds' rules are, before it can start 
shuffling items around. Once the players have decided which games they want to play, they need to spend some time
creating config files for their own games. Then, once they have those config files, __one person__ collects all of them
and plugs them into a generator (either on the website or their own computer).

The generator figures out how many items there are and shuffles them between all of the worlds. It spits out a new .zip
file that contains everything Archipelago needs to work (where each item is, and any patch file or Minecraft server that
the players might need to play). Then it's time to host the game!

- Example: Alice and Bob want to generate a multiworld together. Alice wants to play A Link To The Past, Bob wants to
  play Super Metroid, and they want to share a Minecraft world, so they need three config files total. Alice puts those
  files into a .zip, then uploads the .zip to the website, which generates a multiworld with all three games.
- Example: Charlie wants to generate their own multiworld with two Slay the Spire worlds and two StarCraft II worlds.
  They need four config files total. They put them into a .zip, upload the .zip to the website, and generate their
  multiworld.

### What is a config file?

A config file tells Archipelago what the rules are for your world. For example, some games allow the player to stop
certain items from being randomized, or allow them to change the end goal of the game; the config file controls it all.

### Creating a config file

Each game has a "Settings Page" on our website that allows you to control the most common options for that
game. You can mouse over the name of any option to see a tooltip with more details. Once you're happy with your choices,
click `Export Settings` to download a config file with all of your choices.
- Remember the `Player Name` you typed; that's the "slot name" you might need for some games!
- You can find the settings page for your game on the [Supported Games](https://archipelago.gg/games) page.

Advanced players can create their own config file using a text editor. Read the
[Advanced YAML Guide](https://archipelago.gg/tutorial/Archipelago/advanced_settings/en) to find out how.

### Generating with the website

Once all players have their config files, one person must collect them and put them in a .zip file. Then that person
goes to the [Generate Game](https://archipelago.gg/generate) page and clicks `Upload File`. Once they select the .zip,
that's it! Go to [Hosting an Archipelago server] below to see more about hosting the multiworld now that it's been
generated.
- There are several options on the Generate Game page, like adding a password. Most of these control what players can do
  outside of their game. Mouse over the question marks to learn more about each option.

### Generating with a local generator

Follow these steps only if you installed the Generator and want to avoid using the website to generate your game.

Once all players have their config files, one person must collect them and put them directly inside the folder
`[Archipelago directory]/Players`. 

- Do not create a .zip. This is different from generating with the website.
- Create the `Players` folder if it does not exist.

After filling the `Players` folder, run `ArchipelagoGenerate.exe`. This process creates a .zip representing your
multiworld in `[Archipelago directory]/output`. Go to [Hosting an Archipelago Server] below to see more about hosting
the multiworld now that it's been generated.
- All of the settings described on the Generate Game page, plus other options, are controlled by the `host.yaml` file
  in the Archipelago installation folder. If you want to edit those settings, do so *before* generating the multiworld.

## Hosting an Archipelago server

### Overview

Games do not know how to communicate with other games by default. We sidestep that issue by having those games
communicate with a "server", which is designed to keep track of what's going on in the multiworld and tell
every game what's up at all times. So whenever someone wants to play a game through Archipelago, they always
need a server running, even if they're playing alone.

Our website can "host" servers, or you can host them on your own machine. Either way, someone has to do it.

### Hosting with the website

If you generated your multiworld with the website, simply click `Create New Room` on the page that appeared when you
generated the multiworld. The website will immediately host a server on your behalf.

If you generated your multiworld locally, instead go to the
[Host Game](https://archipelago.gg/uploads) page, click `Upload File`, and select the .zip you generated. The website
will host a server for you.

You should see a table. Each row represents one world, and has information like the "slot name", game name, and links to
any files a player might need to download. Now just follow your game's guide on joining a multiworld, and you're all
set.
- Make sure you forward those download links to the players who need them, or else they won't be able to join the
  multiworld!
- Many games need you to type in an IP address and a port number in the format `ip.address:#####`. Those are properties
  of the server. For servers hosted on the website, the IP address is `archipelago.gg`. To find the port number, read
  the first few lines of text in your server carefully. The lines that say `Hosting game at` both contain the 5-digit
  port number, but *not* the IP address.

### Hosting locally

If you generated your multiworld locally, you might also want to host a server locally. Just run `ArchipelagoServer.exe`
and select the .zip file you generated in your `output` folder when it prompts you to. The server will start running.
Just like when working with the website, follow your game's guide on joining a multiworld to start playing.
- Some players might still need additional files to play. Sometimes, these files can be found inside the .zip you
  generated. Simply extract the files and distribute them to the players that need them.
- Many games need you to type in an IP address and a port number in the format `ip.address:#####`. Those are properties
  of the server. For servers hosted locally, read the first few lines of text in your server carefully. The line
  that says `Hosting game at` contains both the IP address and the port number for your server.
  - Exception: if you are playing a game on the same computer that hosts your server, you may type `localhost` instead
    of the server's IP address.