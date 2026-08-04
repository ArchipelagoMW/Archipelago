# Mega Man X5 Setup Guide

## Required software

- **Archipelago** 0.6.7 or later
  ([releases](https://github.com/ArchipelagoMW/Archipelago/releases)), and the
  `mmx5.apworld` file.
- **BizHawk 2.7 or newer**
  ([releases](https://github.com/TASEmulators/BizHawk/releases)) — 2.7.0 is
  the minimum Archipelago's connector script accepts. This world was tested
  on **2.10**; versions newer than that print an untested-version warning
  from the connector but are expected to work. On first install, run
  BizHawk's prerequisites installer if EmuHawk won't start. The PSX core is
  **NymaShock** (BizHawk's default for PS1).
- A **US-region PS1 BIOS** (e.g. SCPH-5501), dumped from your own console. In
  EmuHawk: **Config → Firmware**, find the PSX (U) entry and point it at your
  BIOS file — or drop the file into BizHawk's `Firmware` folder and let it
  auto-detect.
- A **Mega Man X5 NTSC-U (SLUS-01334) disc image**, dumped from your own copy:
  a raw **2352-byte/sector `.bin`**, single data track.

### Accepted disc images

The patcher checks the MD5 of your `.bin`:

| MD5 | Notes |
|---|---|
| `98c0d278dc4a795a0a7562d950d37cc9` | Redump — the standard dump |
| `09e670f6e666211b7fcdbb7d48b716e1` | Same disc with one extra trailing zero sector |

Both work and produce an identical patched game. To check yours on Windows:

```
certutil -hashfile "Megaman X5.bin" MD5
```

If it matches neither hash, your dump is a different format (2048-byte
sectors, a `.iso`, or multi-track) — re-dump as raw 2352-byte mode.

## Installing the apworld

Put `mmx5.apworld` in your Archipelago install's `custom_worlds` folder, then
restart the Archipelago Launcher. "Mega Man X5" should appear in the games list.

**Everyone in a multiworld must use the same `mmx5.apworld` version** — the
game edits live in the apworld, not in the seed, so a version mismatch between
the generator and a player produces a disc that does not match the seed's
expectations.

## Generating and patching

1. Generate a game with a Mega Man X5 YAML (produce a template from the
   Launcher's **Generate Template Options**).
2. From the finished seed you will receive a **`.apmmx5`** file.
3. Open it via the Launcher's **Open Patch** (double-clicking the file also
   works if your system associates `.apmmx5` with Archipelago). The first
   time, Archipelago will ask you to locate your Mega Man X5 `.bin` — point it
   at the file you verified above.
4. This produces a patched `.cue` + `.bin` beside the patch file.

## Playing

1. Open **BizHawk** and load the patched **`.cue`** (not the original, and
   not the `.bin` directly).
2. Open **Tools → Lua Console**, then **Script → Open Script**, and load
   `data/lua/connector_bizhawk_generic.lua` from your Archipelago install.
3. From the Archipelago Launcher, start the **BizHawk Client**, and connect it
   to the room's address with your slot name.

The client will report the disc mode and confirm it can see the game. Once
connected, play normally — checks send themselves and items arrive as you go.

## Things worth knowing

- **Armor capsules play Dr. Light's dialogue but grant no armor.** That is
  correct: the capsule is the check, and the armor part itself comes from the
  multiworld. **You must walk fully into the capsule** — standing next to it
  makes it open but the sequence will not continue.
- **Boss checks land a few seconds after the kill**, once the results screen
  commits it. Nothing is wrong if they do not appear instantly. One boss kill
  sends **three** checks at once (boss, DNA reward, DNA Part) — that is
  intended.
- **Received items appear at the next stage load, not instantly.** Items are
  written into your save data, and the game builds its live weapon/armor state
  when a stage or character loads. If a weapon arrives while you are in a
  stage, expect it once you next enter one — it is not lost.
- **If a tank or an armor part is briefly missing from your menu, that is
  deliberate.** The original game hides a pickup — or the route to it — once
  you already own what it gives. Since Archipelago can hand you that item
  early, the client temporarily withholds it while you are in the stage
  holding its check, so the check stays collectable. You get the item back as
  soon as you collect that check or leave the stage. This affects tanks (on
  discs patched before the fix — re-patching removes it) and Falcon Armor Head
  while you are in Squid Adler's stage, whose energy balls the game hides once
  you own the part its capsule grants. **Armor you have equipped keeps
  working** — the game decides which armor to wear when the stage loads, and
  the client only withholds afterwards — so this costs you nothing beyond the
  pause menu showing one fewer part until you collect that check.
- **"Small Energy" filler items currently do nothing in-game.** They exist to
  pad the item pool; receiving one is not a bug.
- **Save often, and be aware of BizHawk's memory-card handling.** BizHawk only
  writes the card to disk on a clean close, or when you press its
  **Flush SaveRAM** hotkey (`Ctrl+S` by default), unless you enable autosave
  under `Config → Customize → Advanced`. An unclean exit loses everything since
  the last flush.
- **Savestates include the memory card.** Loading an old savestate rolls back
  in-game saves made after it was created.
- **Prefer playing while connected.** Boss and DNA checks are recovered from
  the save whenever you reconnect, but item-pickup checks (capsules, tanks)
  buffer only 16 deep while the client is disconnected — a long offline
  session can overflow the buffer and lose checks.
- **Memory cards are keyed by the disc's filename.** If you re-patch and the
  output name changes, BizHawk will start you on a fresh card; copy the old
  `.SaveRAM` file to the new name to keep your save.

## Troubleshooting

**The client connects to the room but never sees the game.** The connector Lua
is not running in BizHawk, or your BizHawk is older than 2.7.

**The patcher rejects my disc image.** Check its MD5 against the table above.
The usual cause is a 2048-byte-per-sector dump rather than raw 2352.

**I loaded a save from a different seed.** The client refuses to touch a save
stamped for another seed, to avoid corrupting it. Start a new game for a new
seed.
