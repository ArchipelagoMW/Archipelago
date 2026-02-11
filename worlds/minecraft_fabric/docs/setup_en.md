# Minecraft Fabric Setup Guide

## There are a few steps that players need to do in order to get this mod working properly:

* Follow the Archipelago Setup Guide to install the launcher needed to generate the files for the Randomizer
* Download the latest AP World for this mod
* Place the minecraft_fabric.apworld into the worlds folder in the Archipelago Application
* Open the Archipelago Application, and use the Options Creator to generate your YAML config
* Using your YAML (and the YAMLs of other people's games), create a server for playing by following this Guide

The Next Instructions will differ Slightly depending on whether you want to play the Minecraft Randomizer in a Single Player world, or a Multiplayer world.

## Single Player

* Install Prism Launcher (or your preferred MC launcher if you haven't already)
* Create a new instance of 1.20.1 running the latest version of Fabric (0.18.4 at the time of writing this)
* Install the Archipelago Mod, along with its dependencies Koala Lib and Fabric API
* Boot up Minecraft and Create a new world, filling in Archipelago server address, port, and password (if needed)

Whenever the Single Player world created via this method is opened, it will automatically rejoin the server it was connected to.

In the event that an incorrect AP Server, Slot Name, or Password is entered, or your single player game fails to connect to an Archipelago Server, you can either generate a new world, or you can follow the instructions for Multiplayer.

## Multiplayer

The instructions for playing on a Server are the same as normal Minecraft up until you join the server. Once you're in the world, you can run the command /connect or /archipelago connect, and fill in the necessary information.
Screenshot of the /connect command

If the world was generated in Single Player and the Archipelago Server information supplied is valid, the Server should connect automatically when the world starts.

Whenever the server starts, it will also automatically reconnect to the Archipelago Server the same way as a Single Player World. 
