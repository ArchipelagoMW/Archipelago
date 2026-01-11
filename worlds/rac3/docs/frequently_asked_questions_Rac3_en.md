# Ratchet & Clank 3 AP Frequently Asked Questions

## I have my client connected, but I can't send out/receive checks, what can I do?

It is probably caused by one of these:
1. Make sure you have PINE enabled in the PCSX2 settings
2. Make sure you have only **one instance** of PCSX2 open
3. Try out these commands in the Rac3 client: `/force_update`, `/rac3_info`
4. Try closing and reopening the client
5. You connected to AP without verifying that it the client successfully connected to the emulator. 
   It will say "Connected to RaC3" if it sucessfully connected

## My RaC3 client never loads! It is always a black window no matter how long I wait, what can I do?

Try installing [Universal Tracker](https://github.com/FarisTheAncient/Archipelago/releases) and see if it works, 
sometimes it just refuses to load the client without it installed even though it should work without it. 
Installing Universal Tracker appears to solve this problem for those reporting this issue.

## In the vendors I can purchase a weapon multiple times, but I get nothing, why?

Until you don't have a weapon it's vendor slot will be active, because the game tries to put it back to the shop 
because you don't have it, don't purchase weapons or Armor in the current versions.

## When I receive a weapon/gadget it sends out multiple checks, why is it happening?

Currently weapon vendors and some gadget checks are being sent out when you receive them, best action is to put **Gadgets** 
and **Weapons** into the exclusion list, this makes them always be junk checks (eg. jackpot mode, bolts).

## X check is in logic, but when I go there I don't receive it, why?

Currently there are some checks that doesn't work with sequence breaking (Example Obani Gemini: Infobot: Blackwater City)
these are collected into a location group called  `Unstable`. If you generate the yaml for yourself make sure it is in 
the **excluded locations** section (it should be there by default along with some ones).

## I'm missing Holostar Studios and/or Qwark's hideout in my ship, but I got their infobots, what should I do?

These 2 specific planets have softlock preventions in place. In order to visit Holostar you need to have the hypershot
and the hacker. For Hideout you need to have the refractor to avoid being softlocked on Phoenix Rescue.

## Ok, but how do I know which locations are getting excluded with each option?
Please refer to these: 
- [Unstable](https://github.com/Taoshix/Archipelago-RaC3/blob/main/worlds/rac3/Locations.py#L581-L596)
- [Weapons](https://github.com/Taoshix/Archipelago-RaC3/blob/main/worlds/rac3/Locations.py#L509-L527)
- [Gadgets](https://github.com/Taoshix/Archipelago-RaC3/blob/main/worlds/rac3/Locations.py#L529-L538)




