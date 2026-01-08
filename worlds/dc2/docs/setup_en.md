# Dark Cloud 2 Setup Guide

## Required Software

- [pcsx2 version 1.6.0](https://www.pcsx2.net/downloads)
- [DC2AP Client](https://github.com/ArsonAssassin/DC2AP/releases)
- [Dark Cloud 2 APWorld] (https://github.com/ArsonAssassin/DC2AP/releases)
- Dark Cloud 2 ROM. The Archipelago community cannot provide this.

## General Concept

The DC2AP Client is a C# client which reads memory addresses from ePSXe and communicates with Archipelago. Location Checks are sent when specific memory addresses update, and items are given by editing the memory addresses.

## Joining a MultiWorld Game

1. Run pcsx2 1.6.0. It MUST be this version.
2. Load the Dark Cloud  rom
3. Open the DC2AP Client
4. Enter your host (including port), slot name and password (if set)
5. Press Connect. This will fail if the above steps were not completed properly.

## Where do I get a config file?

If you are using the Archipelago website to generate, you can create one in the Game Options page. If you are generating locally, you can Generate Templates from the Archipelago launcher to create a default template, and edit it manually.
