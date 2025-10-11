# Trackmania

## Where is the options page?

The player options page for this game can be found [here](../player-options) and contains all the options you need to configure and export a config .yaml file.

## How on Earth does a randomizer work for Trackmania?

That's a good question! This mode is similar to Flink's [Random Map Challenge](https://flinkblog.de/RMC/), but loosely in the structure of the official campaigns. At the start of the game, you will have access to a random number of maps from [Trackmania Exchange](https://trackmania.exchange/). Your goal is to beat your target time on each of these tracks. You can choose any medal, or any time between any two medals, as your target time. The quickest medal that is still slower than or equal to your target time is considered your progression medal. When you have the progression medals from 80% tracks in a series (by default), you can move on to the next series, which has an additional set of tracks. Once you have completed 5 series (by default), you have won the randomizer! Of course, the number of maps in a series, the number of series, your target time, and much more are all configurable on the [options page](../player-options).

The catch here is that all of your medals have been randomized! When you drive a run that beats a medal time, say the gold medal time for example, you will (probably) not get a gold medal. You will get a different medal, or an item from another player's game. Other players in your server will have to find your medals in their worlds in order for you to progress to the next series. Every medal time below your target time, as well as the target time itself, all count as "locations" that items from any world in the server can be in (by default).

## Are there any additional items?

Some of the maps on Trackmania Exchange are incredibly difficult. If another player's important progression item has taken the place of the author medal on a track you cannot beat, there is still hope! There are a few map skip items that have been added to the item pool. When you use one, it will complete the currently loaded track and collect all the items that were on the map. Use them wisely, there aren't that many! There is also a PB discount item, which instead will lower your PB time used by the plugin by 1.5% (by default). This is useful for maps where you are close but not quite able to reach your target time! These items are a bit more common (by default).

## Why did I just get an item called Yep Tree?

Archipelago requires all worlds to generate the same number of items and locations. To satisfy this without giving 
way too many Map Skips to the players, this randomizer generates some filler items. These have been given fun names 
that reference the Trackmania community. If you get an item with a crazy name, that is what is happening! Medals 
below your progression medal currently have no real value in the randomizer. You can disable them in the options if 
you prefer.

## How do I setup up my game to work with Archipelago?

The setup guide for this game can be found [here](../../../tutorial/Trackmania/setup/en)

## Which items can be in another player's world?

Any medal from any track, the Map Skip item, the PB Discount item, and anny filler items!

## What does another world's item look like in Trackmania?

Items belonging to other worlds are represented by a medal with the Archipelago logo on it in the normal race UI.

## When the player receives an item, what happens?

When you receive an item, it will show up in your inventory shown in the Archipelago Plugin.

## Is club access required to play Trackmania (2020) in Archipelago?

Yes, this randomizer works by picking random user created maps, and unfortunately you must have club access to play user created maps.

## What Trackmania 2 titlepacks are supported?

TM Canyon, TM Stadium, TM Valley, TM Lagoon, and TM All are all supported. Other titlepacks have not been specifically excluded, but are also not supported. They may or may not work, try at your own risk! 
