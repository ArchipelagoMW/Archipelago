# Digimon World Randomizer Setup Guide

## Required Software

- [Duckstation](https://github.com/stenzek/duckstation/releases/tag/latest)
- [DWAP Client](https://github.com/ArsonAssassin/DWAP/releases)
- [Digimon World APWorld] (https://github.com/ArsonAssassin/DWAP/releases)
- Digimon World US ROM. The Archipelago community cannot provide this.

## Optional Software

- [Digimon World Poptracker Pack](https://github.com/seto10987/Digimon-World-AP-PopTracker-Pack), for use with [Poptracker](https://github.com/black-sliver/PopTracker/releases)

## General Concept

The DWAP Client is a C# client which reads memory addresses from ePSXe and communicates with Archipelago. Location Checks are sent when specific memory addresses update, and items are given by editing the memory addresses.

## Joining a MultiWorld Game

1. Run Duckstation.
2. Load the Digimon World (USA) rom
3. Open the DWAP Client
4. Enter your host (including port), slot name and password (if set)
5. Press Connect. This will fail if the above steps were not completed properly.

## Where do I get a config file?

If you are using the Archipelago website to generate, you can create one in the Game Options page. If you are generating locally, you can Generate Templates from the Archipelago launcher to create a default template, and edit it manually.
