# DELTARUNE Archipelago Setup Guide

## Required Software

- DELTARUNE from the [Steam page](https://store.steampowered.com/app/1671210/)
  - If you want to use a Steam depot instead of a Steam install, use (`download_depot 1671210 1671212 2054633419585385858`)
- Archipelago from the [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases)
  - Require minimum 0.6.7
- DELTARUNE APWorld from the [Releases Page](https://github.com/theemeraldsword85/DELTARUNEAP/releases)
- DELTARUNE Archipelago mod from [GameBanana Page](https://gamebanana.com/mods/699556) or [Releases Page](https://github.com/Tenebrosful/DeltaruneAP-mod/releases)
  
## HIGHLY Recommended Software

- Universal Tracker APWorld from the [UT Releases Page](https://github.com/FarisTheAncient/Archipelago/releases)
- [Archipelago Visual Tracker for DELTARUNE](https://github.com/SylvieSpark/Deltarune-AVT-Tracker) made by SylvieSpark and hotelPneumario (Sadly this only supports up to Chapter 5's Garden as of right now.)

## Create your YAML

Your YAML file is the settings of your Archipelago world.

Using `Generate Template Options` you can find the default YAML and other presets in `<Archipelago folder Path>\Players\Templates` which you can edit to your liking. You can also use the `Option Creator` in the Archipelago Launcher but be warned that using `Options Generator` will make it harder to read some of the option descriptions. Otherwise, it works great.

After setting your options to your liking, you can generate a Multiworld by following the [Archipelago Setup](https://archipelago.gg/tutorial/Archipelago/setup_en).

## Installation

**Remember that DELTARUNEAP will not affect your base DELTARUNE saves. DELTARUNEAP has a separate save folder for each slot you play as, meaning you can play multiple multiworld at once or even multiple slots in the same multiworld.**

The game mod can either be installed through a Mod Loader or by using the Archipelago client.

You can also patch your game with DeltaPatcher if you would like, though we recommend the other options since they are easier.

### Patching the game with a Mod Loader

Download the mod from [GameBanana](https://gamebanana.com/mods/699556) with either G3M or DeltaMod (We recommend using the xdelta version as it patches in 6 seconds versus csx that patches in like 2 minutes.)

### OR Patching the game with the Archipelago DELTARUNE Client

1. Download the APWorld and place it into archipelago/custom_worlds (Double clicking the APWorld will also work!)

<img width="670" height="222" alt="image" src="https://github.com/user-attachments/assets/b2686ca9-68d3-4f78-806a-7d1fcf1f887d" />

2. Download the bsdiff files from the mod [Releases Page](https://github.com/Tenebrosful/DeltaruneAP-mod/releases) (it's the .zip that says "bsdiff" at the end).

<img width="1190" height="253" alt="Screenshot 2026-08-30 170645" src="https://github.com/user-attachments/assets/c8af3a7d-0b74-4117-87ba-6d991edb0537" />

3. Unzip the folder and rename it to `DELTARUNE_PATCH`

<img width="540" height="176" alt="image" src="https://github.com/user-attachments/assets/dd9dd1b3-bc21-4640-9581-dc1b42d4cd53" />

<img width="606" height="132" alt="image" src="https://github.com/user-attachments/assets/8e88940b-5656-4299-a5ad-0b7a71a6b44f" />

<img width="631" height="69" alt="image" src="https://github.com/user-attachments/assets/4117efbb-1259-4b6a-81e1-c0cfa8f350a5" />

4. Move the `DELTARUNE_PATCH` folder to the root of Archipelago folder.

<img width="693" height="680" alt="image" src="https://github.com/user-attachments/assets/e41b1fb9-2ddf-4de4-96fa-77066625e58c" />

If you don't know where that is, you can find your Archipelago folder by clicking `Browse Files` in your Archipelago launcher.

<img width="795" height="287" alt="image" src="https://github.com/user-attachments/assets/fda6c8de-be13-4066-8be0-b0fc64b99fcc" />

5. **Restart the Archipelago Launcher** (Or start the launcher if it's not open yet)

<img width="815" height="108" alt="image" src="https://github.com/user-attachments/assets/efced590-006a-4439-8f77-a60f06889ae3" />

6. Start the DELTARUNE client from your Archipelago folder or the Archipelago app.
   
<img width="801" height="244" alt="image" src="https://github.com/user-attachments/assets/f44823ed-4dae-4361-a2e2-d29e21c9c519" />

<img width="802" height="631" alt="image" src="https://github.com/user-attachments/assets/d01efa7b-8340-4e31-b1a3-3ac37fda9b99" />


7. If your game is installed on your `C:` drive through Steam, you can type `/auto_patch steaminstall` word for word or if it's a downloaded depot `/auto_patch steamdepot` (`/auto_patch linux` or `/auto_patch linuxdepot` for linux) at the bottom of the client. **If this works, you can skip straight to step 8.**

<img width="799" height="115" alt="image" src="https://github.com/user-attachments/assets/adc8e601-4aa9-461f-9a2d-e424db0fb0c8" />

Usually, Steam automatically attempts to download games to you `C:` drive, so it will likely be there unless you know you told Steam to use a `D:` drive, for example. Though, if you're not sure, you can easily find the directory by opening the DELTARUNE directory through Steam by right-clicking DELTARUNE in your library and selecting `Manage > Browse local files`. Then, on Windows you can see the directory you need at the top of the window.

<img width="490" height="215" alt="image" src="https://github.com/user-attachments/assets/69383d3a-9b69-4df8-a5b1-45021a8e6e65" />

<img width="720" height="382" alt="image" src="https://github.com/user-attachments/assets/69557b6c-38fe-4ec6-a380-8367fe9c60e4" />

If your game isn't installed on your `C:` drive, or if it's not working for some reason, input the directory as explained in the previous instruction, like `/auto_patch [directory]`. Obviously don't put the square brackets `[]` inside the command.

<img width="802" height="122" alt="Screenshot 2026-08-24 021609" src="https://github.com/user-attachments/assets/71b12631-a79f-4633-9bad-7f4a6e5ed871" />

8. Enter the command and wait for it to patch. **This process is resource intensive, so don't freak out if it stops responding. Just be patient!**

<img width="802" height="632" alt="image" src="https://github.com/user-attachments/assets/263f0f1e-b12c-4a59-934b-d09ed2d3e101" />

<img width="802" height="629" alt="image" src="https://github.com/user-attachments/assets/c99eadea-d26e-4613-9a70-2324e5cac9f1" />

9. Next, go to your Archipelago folder. If everything goes according to plan, you will see a folder called `DELTARUNE`.

<img width="604" height="96" alt="image" src="https://github.com/user-attachments/assets/aebde2aa-86f0-4761-8768-aee1c2690f96" />

Inside this folder, run the DELTARUNE application.

<img width="613" height="260" alt="image" src="https://github.com/user-attachments/assets/ff6d72c0-4cc1-4d98-96dc-ae2bf930f6e7" />

You'll know you patched the game correctly if you get this screen.

<img width="638" height="493.5" alt="image" src="https://github.com/user-attachments/assets/93b00107-9e57-483c-8edc-e831ee761fb6" />

### Linux users

The Linux installation is mostly similar, however, DELTARUNE will be installed on Steam as the Linux variant.

Since this randomizer only supports the Windows version, we must fix this, by right-click the game in Steam, going to `Properties -> Compatibility`, and checking `Force the use of a specific Steam Play compatibility tool`.

This downloads the Windows version of DELTARUNE to use instead of the Linux version. If the play button is greyed out in Steam, be sure to go to `Settings -> Compatibility` and toggle `Enable Steam Play for all other titles`.

## Hosting

If you are the host, once you have all of the players YAML, use the Generator provided by the Archipelago Launcher.

Once the output zip is generated, if you are playing a solo player multiworld you can host it yourself with the Host option in the Archipelago Client and connect to `localhost:38281`.

If you're not doing a solo multiworld you must upload it to the [Archipelago upload page](https://archipelago.gg/uploads) to generate your room.

## Connect to the Multiworld

Open your patched DELTARUNE version and choose `Change connection info` to input your host, port, slot and (if applicable) password.

You can also copy/paste `host:port` directly into the host slot.

<img width="639" height="494" alt="image" src="https://github.com/user-attachments/assets/2f06bf7c-f3e5-44df-9acc-17e9b4a8b1c1" />

If you want to change the preview items color, it's configurable by switching menu with left/right arrow key.

Not required, but you can also open the DELTARUNE Client in the Archipelago Launcher to use Text commands. You can also use Universal Tracker features if you have the tracker APWorld installed.

### Linux Proxy

Linux users require the usage of a proxy, though **it can be used by anyone who's having difficulties connecting in-game**. Start the Archipelago Deltarune Client, then connect to the room and use the command `/linux_proxy`. You should now be able to connect with the window method with `localhost` for host and `1225` as port.

<img width="638" height="477" alt="image" src="https://github.com/user-attachments/assets/8f99a79d-be22-4abb-afc2-ca64a628e189" />

**On Steam (via Proton)**: This assumes the game is in a Steam Library folder.  Right-click DELTARUNE, go to `Manage -> Browse Local Files`. Go up the directories to the `steamapps` folder, open `compatdata/1671210` (1671210 is the "magic number" for
DELTARUNE in Steam). Save data from here is at `/pfx/drive_c/users/steamuser/AppData/Local/DELTARUNE`.

**Through WINE directly**: This depends on the prefix used. If it is default, then the save data is located at
`/home/USERNAME/.wine/drive_c/users/USERNAME/AppData/Local/DELTARUNE`.
