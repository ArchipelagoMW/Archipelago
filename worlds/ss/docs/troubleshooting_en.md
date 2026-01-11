## Skyward Sword AP World Generation and Client Troubleshooting

This is a guide with a list of errors that you can come across while playing Skyward Sword on Archipelago and possible troubleshooting options. If your issue is not in this guide, please report it to the Discord so we can investigate and help you further.
- [AP Generation Issues](#ap-generation-issues)
- [AP Client Issues](#ap-client-issues)
- [Game Patcher Issues](#game-patcher-issues)
- [Game Issues](#game-issues)

## AP Generation Issues

### Cannot remove item from pool errors
```
AssertionError: Could not remove item from pool: <item>
```
An error occured during item placement, usually regarding starting items. Try tweaking settings regarding the item mentioned and try removing that item from your starting items, if present. Please report this error in the Discord and send us your YAML file so we can locate and fix this issue.

```
ValueError: list.remove(x): x not in list
Exception in <bound method handle_itempool of <worlds.ss.SSWorld object at {address}>> for player X, named <name>.
```
Similar to the above error, however less specific. You may try tweaking settings regarding starting items, which is usually the cause of this error. Please report this error in the Discord and send us your YAML file so we can locate and fix this issue.

### Not all progressionn items reachable
```
RuntimeError: Not all progression items reachable ([Hylia's Realm - Defeat Demise]). Something went terribly wrong here.
```
If the only location unreachable is "Hylia's Realm - Defeat Demise", then try regenerating the seed. This is a rare issue where the generator cannot logically access the end of the game, which we are currently looking into the cause of. If this issue persists after attempting to generate several times, you may need to tweak your settings, as your combination of settings may increase the likelihood of this issue.

```
RuntimeError: Not all progression items reachable: ([<several locations here>]). Something went terribly wrong here.
```
If several locations are unreachable, this is larger issue than the one above. If they are all dungeon locations, try changing your key settings and starting items if you included certain keys. Please report this issue to the Discord with your YAML, even if this issue resolves itself upon trying to generate again.

## AP Client Issues

### My client won't open
See [this guide](https://github.com/Battlecats59/SS_APWorld/releases/tag/DME) to install DME for Python in your Archipelago installation.

If your issue persists after installing DME, please report your problem to the Discord so we can help you further.

### Invalid start byte
```
Connection to Dolphin failed, attempting again in 5 seconds...
Traceback (most recent call last):
  File "C:\ProgramData\Archipelago\lib\worlds\ss.apworld\ss\SSClient.py", line 643, in dolphin_sync_task
    ctx.auth = dme_read_slot()
               ^^^^^^^^^^^^^^^
  File "C:\ProgramData\Archipelago\lib\worlds\ss.apworld\ss\SSClient.py", line 289, in dme_read_slot
    return slot_bytes.decode("utf-8")
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x80 in position 1: invalid start byte
```
This error occurs upon connecting the client when it attempts to read your slot name from game memory, but cannot find it. Make sure you are using a compatible version of the patcher for the AP world version you are using. You can do this by checking the version hash in the patcher window title. If this issue persists, please report it to the Discord so we can help you further.

### My client is not sending locations or receiving items in game
This problem is likely because you are not connected to the Archipelago room or you are not playing on file 1. Make sure your client is connected and you are on file 1 in-game. If this issue persists, it is likely due to a larger issue. If this is the case, please report your issue to the Discord so we can investigate and help you further.

### I just got sent an item and I did not get it in game
There are very few edge cases where an item send you may get deleted and you won't receive it. Make sure you get to a location where Link is standing and in a state where he can receive items. If you still haven't gotten it, use the !getitem command to manually send it to yourself. Please report the issue to the Discord so it can be resolved in the future.

### My client is normally sending checks, but it didn't send one I just got
Make sure this check hasn't been collected yet (by someone finishing or using !collect). You can check if this location has been sent by opening your individual tracker in the Archipelago room and checking that location. If it is not sent, ask the host to use the /send_location command and report this issue to the Discord so it can be resolved.

## Game Patcher Issues

### Game will not generate, outputting invalid APSSR file
```
Traceback (most recent call last):
  File "gui\randogui.py", line 285, in randomize
  File "ssrando.py", line 92, in __init__
  File "archipelago.py", line 19, in __init__
Exception: Invalid APSSR file.
```
This error occurs when the patcher cannot find the file path specified, or the inputted file is not an apssr file. If this is not the case, it is likely that your apssr was corrupted. Ask the host to resend it to you, or regenerate the seed and recreate the apssr.

It is also possible that you are using an incompatible patcher version. Make sure your patcher version is compatible with the AP world version used to generate the seed.

### Other patcher errors
```
list index out of range
```
This is a rare error that usually has to do with a corrupted or incompatible version of python. If you get this error, please try downloading (or redownloading) Python 3.12. If this doesn't fix it or you cannot do this, please report it to the Discord so we can help you further.

```
charmap codec can't encode characters in position X-X: character maps to X.
```
This issue will likely come up only if you are using a patcher version that is incompatible with your current AP world version. Make sure that you are using the correct versions and that the host generated with the correct version.

```
KeyError: <key>
```
If this KeyError is spitting out the name of an option, make sure you are using a compatible version of the patcher for your AP world version. If you make sure you are on a compatible version and this issue persists, report it to the Discord so we can help you further.

## Game Issues

### Dolphin Crashes
If your Dolphin crashes, especially when going through a loading zone or getting an item, please report the crash to the Discord and tell us exactly what you were doing and where you were when the game crashed. If a black PANIC screen appears with memory addresses, please screenshot it and send it in your report. If you get an "invalid read from address" popup, please screenshot that as well.

### I think I'm out of locations
If you are out of accessible locations, you will have to wait for other players to send you items to progress further. If everyone else has no locations accessible, then there is likely a logical error in Skyward Sword or another game in the multiworld. Make sure to check the [SS AP Webtracker](https://youraveragelink.github.io/SS-Randomizer-Tracker/) to see if you can access any more locations. If you cannot, report the issue to the Discord so we can check for errors in the SS logic.

### Archipelago thinks I can reach a location, but I cannot
Check the [SSR Location Guide](https://docs.google.com/document/d/1F8AmQccCvtblnRhw_kEAVTME_xX1-O_9Ln16TVDPx6w/edit?tab=t.0#heading=h.9bzfdyr09f0y) to make sure that you actually cannot access the location. If you cannot, report the issue to the Discord with what location it is and what items you have so we can check for errors in the SS logic.

### Problems with receiving items or sending locations
Common problems with receiving items or sending locations can be troubleshooted in the [AP Client Issues Section](#ap-client-issues).