> Research notes mirrored from the mmx5-ap-research workspace (2026-08-03).
> Working copies live there and are updated as addresses are confirmed;
> re-sync this mirror when they change. No game data included.

# MMX5 community cheat archive (gamehacking.org game 89275, NTSC-U)

Pasted by Ivor 2026-07-31 (the site blocks automated fetch). Same DB the god
mode research started from. Kept verbatim below; annotations first.

## Cross-validation against our RAM map (high value)

| Code | Confirms |
|---|---|
| `800D1CA0 FFFF` Have All Armor Parts | armor-parts u16 = 0x1CA0 (client TODO map ✓) |
| `800D1C84 FFFF / 800D1C86 000F` All Power-Up Parts | parts words 0x1C84/86 (ramwatch give_all_parts ✓) |
| `300D1C7F 00FF` All Sub/W/EX tanks | tank byte 0x1C7F (client grant byte ✓) |
| `300D1C47 0040` Max Energy X | max-HP byte 0x1C47 ✓ |
| `300D1C49 00??` Character & Armor Modifier | 0x1C49 = character/armor selector |
| `800D1CB4 ????` Mavericks Defeated modifier | 0x1CB4 = kill counter (seen ticking in diff log) |
| `300D1C0C 00??` Level Modifier | stage id 0x1C0C ✓ (spawner input) |
| `300D4F56..67 0001` "Enable ..." family | the 0x0D4F5x block = PAUSE-MENU row enable flags (X-Buster/weapons/EX/exit-level...) — explains why they were 00 during Izzy gameplay; they are not a gameplay gate ✓ |
| `800D1C76 A0A0 / 800D1C78 0920` (sub-tank fill) | 0x1C76/77 = sub-tank fill bytes, 0x1C78 = W-tank fill ✓ |
| `8009A0FC 2020` Infinite Health | live HP 0x9A0FC ✓ |
| `800920EC 0000` (kill boss, conditional) | boss HP 0x920EC ✓ |
| `8009A0C4/C6` moon-jump/fly writes | player x/y VELOCITY words at +0x24/+0x26 |
| `800D1CAE 0040` Infinite Hours To Collision | countdown u16 0x1CAE (notes said 0x1CAC region — recheck which) |

## Tooling adopted into mmx5_ramwatch.lua

* **Get Items From Anywhere** `80054066 2400` -> `magnet_on()`/`magnet_off()`.
  NOPs the touch-test beqz at 0x80054064 in the collect routine (our
  disassembly region) — on-screen items self-collect. Perfect for stub/ring
  testing without navigation deaths.
* **Float Jump** `D00C931C 0040 / 8009A0C6 0001` -> `float_on()` (hold X).
* Walk Through Walls / Fly / Moon Jump variants below if ever needed —
  note "Press Select For Suicide" exists (`D00C931E 0100 / 8009A0FC 0000`),
  which is what a mislabeled web copy sold us as "air walk". Never trust
  unverified mirrors; this file is the authority now.

## Verbatim archive

```
00'00"00 Clear Time (PAR/GS): 800D1CB0 0000
All Bosses Defeated: 800D1C4A 00FF
All Eight Bosses Defeated In Rematch: 50000402 0000 / 800D1C2E 0202
All Mega Man X Armor: 800D1C4A 000F
All Subtanks (Press L2 To Fill): 800D1C7E F000 / D00C931E 0001 / 800D1C76 A0A0 / D00C931E 0001 / 800D1C78 0920
Allow You To Walk On Spikes: D0074634 72E8 / 80074634 5F90 / D0038B9C 0012 / 80038B9E 1000 / D0038BF0 0018 / 80038BF2 1000
Always Drop Item Modifier: 8005452A 2400 / 80053688 000B / 8005368A 1000 / 800536B8 00?? / 800536BA 3402
Always Have Shadows: 8009A12C 0001
Character & Armor Modifier: 300D1C49 00??
Completely Immune To Any Virus: 3009A19B 0000
Damage Taken Is 0 In Level: 800D1CB8 0000
Debug Fly Mode (L2 on, Select off): D00C931E 0001 / 800350A4 800F / 800350A6 3C02 / D00C931E 0100 / 800350A4 800D / 800350A6 3C02
Destroy Metal "V" Blocks With Any Weapon: 80032FBE 2400 / 80032FD2 2400
Enable C-Shot: 300D4F58 0001
Enable Change Button Configuration: 300D4F64 0001
Enable Change Screen Configuration: 300D4F66 0001
Enable Dark Hold: 300D4F5B 0001
Enable EX: 300D4F67 0001
Enable Exit A Level: 300D4F63 0001
Enable F-Laser: 300D4F5C 0001
Enable Giga Attack: 300D4F5F 0001
Enable Goo Shaver: 300D4F5E 0001
Enable Ground Fire: 300D4F5D 0001
Enable Life Gauge: 300D4F61 0001
Enable Powerup Modifier 1-4: 300D4F68..6B 00??
Enable Restore Life Gauge: 300D4F60 0001
Enable Restore Weapon Energy Gauge: 300D4F62 0001
Enable Return To The Game: 300D4F65 0001
Enable Spike Ball: 300D4F59 0001
Enable Tri-Thunder: 300D4F5A 0001
Enable Wing Spiral: 300D4F57 0001
Enable X-Buster: 300D4F56 0001
Float Jump (hold X): D00C931C 0040 / 8009A0C6 0001
Diagonal Movement pack (xMrNx): D00C931C 9000 / 8009A0C4 8600 / ... (velocity writes keyed on d-pad combos)
Get Items From Anywhere: 80054066 2400
Have All Armor (X): 300D1C49 0004
Have All Armor Parts: 800D1CA0 FFFF
Have All Energy Orbs In Ride Chaser Level: D00D51A2 7FFF / 800D1C26 0008
Have All Power-Up Parts: 800D1C84 FFFF / 800D1C86 000F
Have All Special Parts: 800D1C84 FFFC / 800D1C86 0003
Have All Sub/W/EX tanks: 300D1C7F 00FF
Have All Weapons: 3009A169 00FF
Hit Anywhere: D00C931C 0010 / 80031ED6 2400 / D00C931C 0080 / 80031ED6 1040
Hyper: 8009A0E4 0001
Hyper Mode (Circle+L2 on / Circle+R2 off): D00C931C 0021 / 80062EA0 0000 / D00C931C 0022 / 80062EA0 0005
Immune To Lava: 800F2AB0 2400 / 800F6C3C 2400
Infinite All Ammo: D003F82C 1823 / 8003F832 2400
Infinite All Ammo (Zero): D0041D8C 00AC / 80041D8E 2400 / D0043C44 00AE / 80043C46 2400 / D0046E84 2023 / 80046E8A 2400
Infinite <weapon> family: 8009A14A..8009A158 = 0120 (ammo slots)
Infinite Health: 8009A0FC 2020
Infinite Health (X): 8009A0CF 4040 / 800D1C46 4000
Infinite Hours To Collision: 800D1CAE 0040
Infinite In-Air Moves: 8009A126 0000
Infinite Leg Jets Power: 8009A188 0000 (also 00FF variant)
Infinite Lives: 300D1C45 0004
Jump in Midair (nolberto82, code-injection at 0x80008300): 80008300 0080 / ... / 8002DF20 20C0 / 8002DF22 0800 / 8003F192 2400
Kill Bosses in 1 Hit: D10920EC 0000 / 800920EC 0000
Level Clear Time 0:00:00: 8009A1F0 0000
Level Modifier: D00D1C0C 0016 / 300D1C0C 00??
Mavericks Defeated In Level Modifier: 800D1CB4 ????
Max Energy X / Zero: 300D1C47 0040 / 300D1C48 0040
Max Mavericks Defeated: 800D1CB4 03E7
Max Weapon Energy: 50000A02 0000 / 8009A148 0168 / 800D1C52 3C00
Moon Jump (X+L2): D00C931C 0041 / 8009A0C4 DFFF
One Hit Kills: 80032178 005C / 8003217A 90E4
Overall Game Clear Time 0:00:00: 800D1DB4 0000 / 800D1DB6 0000
Press Select For Suicide: D00C931E 0100 / 8009A0FC 0000 / D00C931E 0100 / 8009A0A4 0002
Quick Charge: 8003EB98 0005 / 8003EB9A 2444 / 8003FDAC 0005 / 8003FDAE 2463
Rank Modifier In Level X / Zero: 300D1CAA 000? / 300D1CAB 000?
Stage Modifier: D00C931C 0100 / 800D1C0C ????
Ultra Buster Shot: 8009A13C FFFF
Unarmored X and Gaea Armor X Can Air Dash: 800388E2 2400
Walk Through Walls: 8002FDD0 2400 / 8002FE04 2400 / 8002FE80 2400 / 800305D4 2400 / 80030ECC 2400 / 80038A50 2400 / 80038EEC 0011 / 80038EEE 2402
X/All Armors And Zero Can Push Metal "V" Blocks: 800F9DA2 2400
X/All Armors And Zero Stick To Walls: 8003AEAA 2400 / 8003AEB6 2400
X/Zero Can Fly (xMrNx): D00C931C 0000 / 8009A0C4 FFFF / D00C931C 0000 / 8009A0C6 FFFF / D00C931C 1000 / 8009A0C4 8600 / D00C931C 1000 / 8009A0C6 0002 / D00C931C 4000 / 8009A0C4 B200 / D00C931C 4000 / 8009A0C6 FFFD
Recolor Zero (Black Armor) to Viral Armor Zero: (palette writes 801051A2+ / 80105B82+, cosmetic - see gamehacking.org)
```
