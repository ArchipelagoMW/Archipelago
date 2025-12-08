# BK Simulator

## What is BK Simulator?
You have to walk to BK, in various weather conditions. Each time you reach BK is a check. Collect every check (and return home!) to goal.

<iframe frameborder="0" src="https://itch.io/embed/4088465?linkback=true" width="552" height="167"><a href="https://emilyv99.itch.io/bk-simulator">BK Simulator by Emily</a></iframe>

## Settings
[Options Page](../player-options)
- You choose how many locations are in the game. Collecting ALL of them is required as the goal.
- You can adjust the distance to the nearest BK at the start. This will heavily control the speed / length of the game.
- You can also adjust the speed gained for each speed upgrade.
- You can set a percentage of your Shoe/Boot upgrades to be replaced with filler. (Higher values will be fulfilled as much as is possible without breaking logic requirements)

## Items / Logic
Items:
- Shoe upgrades allow you to walk faster
- Snow Boots allow you to walk in snow (and walk faster in snow)
- Opening a new BK location cuts the distance you need to walk in half

Logic:
- Sunny weather is the standard, and where you should start
- Rainy weather is slower to walk in, and expects that you have more upgrades than sunny weather expects
- Snowy weather requires snow boots to walk in
- Higher-numbered checks will expect gradually more items to become in-logic.
- "Sphere 1" includes the first 2 Sunny checks only.

