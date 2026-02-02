# Schedule I

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

 - Sends checks from all missions.
 - Sends and receives all customer checks and items.
 - Customers can be unlocked by receiving them through archipelago when randomize_customers is true in the YAML.
 - checks for samples will be sent no matter the settings and are functional.
 - Dealers will send checks when recruiting regardless of settings.
 - Dealer AP unlock will allow user to then recruit them in game. Check is still possible when having them as a possible contact.
 - Suppliers will not be unlockable if suppliers are randomized and only unlocked through ap items
 - Suppliers give checks for unlocking them when suppliers are not randomized
 - Every Action that would cause cartel influence in a region to drop is a check (x7 per region)
 - Unable to reduce cartel influence naturally and cartel influence items added to pool when randomize_cartel_influence is true
 - Level up rewards are suppressed when randomize_level_up_rewards is true
 - Level up rewards are added to the item pool when randomize_level_up_rewards is true
 - Whenever you'd nomrally get unlocks for leveling up, you get a check regardless of the option
 - Deathlink is sent when a player dies or when they arrested. Recieved deathlink causes player to get arrested
 - Property and busniesses give checks when purchased
 - Randomized properties or businesses will not be unlocked when purchased if randomization on, properties and/or businesses will be added to the item pool
 - Recipe checks are sent when recipes are learned
 - Cash for trash are sent every 10 trash burned
 - Filler items will be sent as deaddrop quests

## Once I'm inside Schedule1, how do I play Schedule1AP

Use In-Game UI to connect to server. Once connected, Create a new world and skip the prologue.
Make sure to save as often as you can, and you are able to rejoin. Restart your game if you need to rejoin the world!
If you want to play with friends (Untested): Invite them to your lobby. All of you connect as same archipelago Info, Load into world.

## A statement on the ownership over Schedule1AP

Schedule I apworld is MIT license. Created by MacH8s