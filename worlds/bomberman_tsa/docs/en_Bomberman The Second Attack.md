# Bomberman 64 The Second Attack Setup Guide

## What you need
- Bizhawk https://tasvideos.org/BizHawk/ReleaseHistory#Bizhawk210
- The latest bomberman_tsa.apworld provided in the latest release post


## Installation
Same as every other unsupported N64 apworld, 
- simply move bomberman_tsa.apworld into the custom_worlds directory in your Archipelago install server
(default path: C:\ProgramData\Archipelago\custom_worlds)
- or simply double click the apworld and it should install itself (Archipelago version 0.5.0 and later)

## Running
1. In the Archipelago launcher push the 'Generate Template Options' button to generate a yaml for your options
2. Like every other apworld, fill out your yaml options and have the host generate the multiworld, the produced zip file should contain a .apbombtsa patch file. Receive this .apbombtsa patch from the multiworld host.
3. Push the 'Open Patch' button in the launcher and it should ask for a 'Bomberman 64 The Second Attack (US)' legal ROM dump (MD5 Hash: aec1fdb0f1caad86c9f457989a4ce482), then select the generated  .apbombtsa patch file to produce a .z64 ROM which should auto launch in a bizhawk instance. You should be set otherwise from here just follow the same instructions as any other supported N64 apworld.

## Troubleshooting
- The windows 7 version of archipelago uses python 3.8 which will not work with this apworld.