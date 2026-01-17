# The Legend of Zelda: Oracle of Ages Setup Guide

## Required Software

- [Oracle of Ages .apworld](https://github.com/SenPierre/ArchipelagoOoA/releases/latest)
- [Bizhawk 2.9.1 (x64)](https://tasvideos.org/BizHawk/ReleaseHistory)
- Your legally obtained Oracle of Agess US ROM file

## Installation Instructions

1. Put your **Oracle of Ages US ROM** inside your Archipelago install folder (named "Legend of Zelda, The - Oracle of Ages (USA).gbc")
2. Download the **Oracle of Ages .apworld file** and double-click it to install it the "custom_worlds/" subdirectory of your Archipelago install directory
3. Generate a seed using your .yaml settings file (see below if you don't know how to get the template)
4. Download the .apooa patch file that was built by the server while generating, this will be used to generate your modified ROM
5. Open this patch file using the Archipelago Launcher
6. If everything went fine, the patched ROM was built in the same directory as the .apoos file, and both Bizhawk and the client launched
7. Connect the Client to the AP Server of your choice, and you can start playing!

## Create a Config (.yaml) File

To get the template YAML file:
1. install the .apworld file as instructed above
2. if Archipelago Launcher was running on your computer, close it 
3. run the Archipelago launcher
4. click on "Generate Template Settings"
5. it should open a directory in file explorer, pick the file named `The Legend of Zelda - Oracle of Ages.yaml`

From there, you can edit it and place it directly inside the "Players" subdirectory of your Archipelago install.
Once you have files in there, you can run ArchipelagoGenerate and play your generated multiworld!
