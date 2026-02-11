## Required Software

- This world uses the BizHawk client, thus the usual instructions apply.
- Archipelago launcher with this world, it can't track your game otherwise.
- A Sonic The Hedgehog 16 bit (1991) ROM file.  We can't help you acquire this, please don't ask. You need one of the following:
    - Sonic The Hedgehog Revision 0 - This is the original world wide release cart.
    - Sonic The Hedgehog Revision 1 - This is the updated cart released in Japan.
    - Sega Classics SONIC_w.68K - This is actually just the rev1 ROM with an odd name.
    - Sonic The Hedgehog GameCube Edition - This is almost the same as rev1 so it's close enough.

## Setup

- You will receive a file with the extension `.aps1` that you should open using the Launcher's `Open Patch` button.
- The game state is tracked via SRAM, this includes the game seed to keep stale saves from messing up new runs.
- It is recommended, if you have save data from a previous attempt, to use the `RESET SAVE` level select option before connecting to the server.  The client will get upset if your run has data from a different seed.
- Resetting mid run will result in the client writing the progress that has been received from the AP server.  This is safe if your monitor progress has been sent to the AP server.
- The level select will currently only rerender the progress indicators when you press an input button, just press up or down after reset.
- It should be impossible to enter a level before the server sends you your session.  Make sure you connect to the server from the BizHawk Client.
- The most likely bug I've missed from patching is some oddity in how rings are reset after taking damage.  Let me know if you can get silly numbers consistently.