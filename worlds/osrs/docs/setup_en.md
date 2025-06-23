# Setup Guide for Old School Runescape

## Required Software

- [RuneLite](https://runelite.net/)
- If the account being used has been migrated to a Jagex Account, the [Jagex Launcher](https://www.jagex.com/en-GB/launcher)
will also be necessary to run RuneLite

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

You can customize your settings by visiting the 
[Old School Runescape Player Options Page](/games/Old%20School%20Runescape/player-options).

## Joining a MultiWorld Game

### Install the RuneLite Plugins
Open RuneLite and click on the wrench icon on the right side. From there, click on the plug icon to access the
Plugin Hub. You will need to install the [Archipelago Plugin](https://github.com/digiholic/osrs-archipelago) 
and [Region Locker Plugin](https://github.com/slaytostay/region-locker). The Region Locker plugin
will include three plugins; only the `Region Locker` plugin itself is required. The `Region Locker GPU` plugin can be
used to display locked chunks in gray, but is incompatible with other GPU plugins such as 117's HD OSRS and can be
disabled.

### Create a new OSRS Account
The OSRS Randomizer assumes you are playing on a newly created f2p Ironman account. As such, you will need to [create a
new Runescape account](https://secure.runescape.com/m=account-creation/create_account?theme=oldschool). 

If you already have a [Jagex Account](https://www.jagex.com/en-GB/accounts) you can add up to 20 characters on
one account through the Jagex Launcher. Note that there is currently no way to _remove_ characters
from a Jagex Account, as such, you might want to create a separate account to hold your Archipelago
characters if you intend to use your main Jagex account for more characters in the future.

**Protip**: In order to avoid having to remember random email addresses for many accounts, take advantage of an email
alias, a feature supported by most email providers. Any text after a `+` in your email address will redirect to your
normal address, but the email will be recognized by the Jagex login as a new email address. For example, if your email
were `Archipelago@gmail.com`, entering `Archipelago+OSRSRandomizer@gmail.com` would cause the confirmation email to
be sent to your primary address, but the alias can be used to create a new account. One recommendation would be to
include the date of generation in the account, such as `Archipelago+APYYMMDD@gmail.com` for easy memorability.

After creating an account, you may run through Tutorial Island without connecting; the randomizer has no 
effect on the Tutorial.

### Connect to the Multiserver
In the Archipelago Plugin, enter your server information. The `Auto Reconnect on Login For` field should remain blank;
it will be populated by the character name you first connect with, and it will reconnect to the AP server whenever that
character logs in. Open the Archipelago panel on the right-hand side to connect to the multiworld while logged in to
a game world to associate this character to the randomizer.

For further information about how to connect to the server in the RuneLite plugin,
please see the [Archipelago Plugin](https://github.com/digiholic/osrs-archipelago) instructions.