# MSU-1 Setup Guide

## What is MSU-1?

MSU-1 allows for the use of custom in-game music. It works on original hardware, the SuperNT, and certain emulators.
This guide will explain how to find custom music packages, often called MSU packs, and how to configure them for use
with original hardware, the SuperNT, and the snes9x emulator.

## Where to find MSU Packs

MSU packs are constantly in development. We won't link to any packs as most include ripped music from other media.

## What an MSU pack should look like

MSU packs contain many files, most of which are the music files which will be used when playing the game. These files
should be named similarly, with a hyphenated number at the end, and with a `.pcm` extension. It does not matter what
each music file is named, so long as they all follow the same pattern. The most popular filename you will find
is `alttp_msu-X.pcm`, where X is replaced by a number.

There is one other type of file you should find inside an MSU pack's folder. This file indicates to the hardware or to
the emulator that MSU should be enabled for this game. This file should be named similarly to the other files in the
folder, but will have a `.msu` extension and be 0 KB in size.

A short example of the contents of an MSU pack folder are as follows:

```
List of files inside an MSU pack folder:
alttp_msu.msu
alttp_msu-1.pcm
alttp_msu-2.pcm
...
alttp_msu-34.pcm
```

## How to use an MSU Pack

In all cases, you must rename your ROM file to match the pattern of names inside your MSU pack's folder, then place your
ROM file inside that folder.

This will cause the folder contents to look like the following:

```
List of files inside an MSU pack folder:
alttp_msu.msu
alttp_msu.sfc    <-- Add your ROM file
alttp_msu-1.pcm
alttp_msu-2.pcm
...
alttp_msu-34.pcm
```

### With snes9x

1. Load the ROM file from snes9x.

### With SD2SNES / FXPak on original hardware

1. Load the MSU pack folder onto your SD2SNES / FXPak.
2. Navigate into the MSU pack folder and load your ROM.

### With SD2SNES / FXPak on SuperNT

1. Load the MSU pack folder onto your SD2SNES / FXPak.
2. Power on your SuperNT and navigate to the `Settings` menu.
3. Enter the `Audio` settings.
4. Check the box marked `Cartridge Audio Enable.`
5. Navigate back to the previous menu.
6. Choose `Save/Clear Settings`.
7. Choose `Save Settings`.
8. Choose `Run Cartridge` from the main menu.
9. Navigate into your MSU pack folder and load your ROM.

## A word of caution to streamers

Many MSU packs use copyrighted music which is not permitted for use on platforms like Twitch and YouTube. If you choose
to stream music from an MSU pack, please ensure you have permission to do so. If you stream music which has not been
licensed to you, or licensed for use in a stream in general, your VOD may be muted. In the worst case, you may receive a
DMCA take-down notice. Please be careful to only stream music for which you have the rights to do so.