# Jak And Daxter (ArchipelaGOAL) Setup Guide

## Required Software

- A legally purchased copy of *Jak And Daxter: The Precursor Legacy.*
- Python version 3.10 or higher. Make sure this is added to your PATH environment variable.
- [Task](https://taskfile.dev/installation/) (This makes it easier to run commands.)

## Installation

### Installation via OpenGOAL Mod Launcher

At this time, the only supported method of setup is through Manual Compilation. Aside from the legal copy of the game, all tools required to do this are free.

***Windows Preparations***

***Linux Preparations***

***Using the Launcher***

### Manual Compilation (Linux/Windows)

***Windows Preparations***

- Dump your copy of the game as an ISO file to your PC.
- Download a zipped up copy of the Archipelago Server and Client [here.](https://github.com/ArchipelaGOAL/Archipelago)
- Download a zipped up copy of the modded OpenGOAL game [here.](https://github.com/ArchipelaGOAL/ArchipelaGOAL)
- Unzip the two projects into easily accessible directories.


***Linux Preparations***

***Compiling***

## Starting a Game

- Open 3 Powershell windows. If you have VSCode, you can run 3 terminals to consolidate this process.
    - In the first window, navigate to the Archipelago folder using `cd` and run `python ./Launcher.py --update_settings`. Then run it again without the `--update_settings` flag.
    - In the second window, navigate to the ArchipelaGOAL folder and run `task extract`. This will prompt you to tell the mod where to find your ISO file to dump its contents. When that is done, run `task repl`.
    - In the third window, navigate to the ArchipelaGOAL folder and run `task boot-game`. At this point, Jak should be standing outside Samos's hut.
    - Once you confirm all those tasks succeeded, you can now close all these windows.
- Edit your host.yaml file and ensure these lines exist. And don't forget to specify your ACTUAL install path. If you're on Windows, no backslashes!
```
jakanddaxter_options:
  # Path to folder containing the ArchipelaGOAL mod.
  root_directory: "D:/Files/Repositories/ArchipelaGOAL"
```  
- In the Launcher, click Generate to create a new random seed. Save the resulting zip file.
- In the Launcher, click Host to host the Archipelago server. It will prompt you for the location of that zip file.
- Once the server is running, in the Launcher, find the Jak and Daxter Client and click it. You should see the command window begin to compile the game. 
- When it completes, you should hear the menu closing sound effect, and you should see the text client indicate that the two agents are ready to communicate with the game.
- Connect the client to the Archipelago server and enter your slot name. Once this is done, the game should be ready to play. Talk to Samos to trigger the cutscene where he sends you to Geyser Rock, and off you go!

Once you complete the setup steps, you should only need to run the Launcher again to generate a game, host a server, or run the client and connect to a server.
- You never need to download the zip copies of the projects again (unless there are updates).
- You never need to dump your ISO again.
- You never need to extract the ISO assets again.

### Joining a MultiWorld Game

MultiWorld games are untested at this time.

### Playing Offline

Offline play is untested at this time.

## Installation and Setup Troubleshooting

### Compilation Failures

### Runtime Failures

- If the client window appears but no sound plays, you will need to enter the following commands into the client to connect it to the game.
    - `/repl connect`
    - `/memr connect`
- Once these are done, you can enter `/repl status` and `/memr status` to check that everything is connected and ready.

## Gameplay Troubleshooting

### Known Issues

- I've streamlined the process of connecting the client's agents to the game, but it comes at the cost of more granular commands useful for troubleshooting.
- The game needs to run in debug mode in order to allow the repl to connect to it. At some point I want to make sure it can run in retail mode, or at least hide the debug text on screen and play the game's introductory cutscenes properly.
- The client is currently not very robust and doesn't handle failures gracefully. This may result in items not being delivered to the game, or location checks not being delivered to the server.
- The game relates tasks and power cells closely but separately. Some issues may result from having to tell the game to check for the power cells you own, rather than the tasks you completed.