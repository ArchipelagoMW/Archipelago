# The Messenger Plando Guide

This guide details the usage of the game-specific plando options that The Messenger has. The Messenger also supports the
generic item plando. For more information on what plando is and for information covering item plando, refer to the
[generic Archipelago plando guide](/tutorial/Archipelago/plando/en). The Messenger also uses the generic connection
plando system, but with specific behaviors that will be covered in this guide along with the other options.

## Shop Price Plando

This option allows you to specify prices for items in both shops. This also supports weighting, allowing you to choose
from multiple different prices for any given item.

### Example

```yaml
The Messenger:
  shop_price_plan:
    Karuta Plates: 50
    Devil's Due: 1
    Barmath'azel Figurine:
      # left side is price, right side is weight
      500: 10
      700: 5
      1000: 20
```

This block will make the item at the `Karuta Plates` node cost 50 shards, `Devil's Due` will cost 1 shard, and
`Barmath'azel Figurine` will cost either 500, 700, or 1000, with 1000 being the most likely with a 20/35 chance.

## Portal Plando

This option allows you to specify certain outputs for the portals. This option will only be checked if portal shuffle
and the `connections` plando host setting are enabled.

A portal connection is plandoed by specifying an `entrance` and an `exit`. This option also supports `percentage`, which
is the percent chance that that connection occurs. The `entrance` is which portal is going to be entered, whereas the
`exit` is where the portal will lead and can include a shop location, a checkpoint, or any portal. However, the
portal exit must also be in the available pool for the selected portal shuffle option. For example, if portal shuffle is
set to `shops`, then the valid exits will only be portals and shops; any exit that is a checkpoint will not be valid. If
portal shuffle is set to `checkpoints`, you may not have multiple portals lead to the same area, e.g. `Seashell` and
`Spike Wave` may not both be used since they are both in Quillshroom Marsh. If the option is set to `anywhere`, then all
exits are valid.

All valid connections for portal shuffle can be found by scrolling through the [portals module](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/messenger/portals.py#L12).
The entrance and exit should be written exactly as they appear within that file, except for when the **exit** point is a
portal. In that case, it should have "Portal" included.

### Example

```yaml
The Messenger:
  portal_plando:
    - entrance: Riviere Turquoise
      exit: Wingsuit
    - entrance: Sunken Shrine
      exit: Sunny Day
    - entrance: Searing Crags
      exit: Glacial Peak Portal
```

This block will make it so that the Riviere Turquoise Portal will exit to the Wingsuit Shop, the Sunken Shrine Portal
will exit to the Sunny Day checkpoint, and the Searing Crags Portal will exit to the Glacial Peak Portal.

## Transition Plando

This option allows you to specify certain connections when using transition shuffle. This will only work if
transition shuffle and the `connections` plando host setting are enabled. 

Each transition connection is plandoed by specifying its attributes:

* `entrance` is where you will enter this transition from.
* `exit` is where the transition will lead.
* `percentage` is the chance this connection will happen at all.
* `direction` is used to specify whether this connection will also go in reverse. This entry will be ignored if the
  transition shuffle is set to `coupled` or if the specified connection can only occur in one direction, such as exiting
  to Riviere Turquoise. The default direction is "both", which will make it so that returning through the exit
  transition will return you to where you entered it from. "entrance" and "exit" are treated the same, with them both
  making this transition only one-way.

Valid connections can be found in the [`RANDOMIZED_CONNECTIONS` dictionary](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/messenger/connections.py#L640).
The keys (left) are entrances, and values (right) are exits. Whether you want the connection to go both ways or not,
both sides must either be two-way or one-way; E.g. connecting Artificer (Corrupted Future Portal) to one of the
Quillshroom Marsh entrances is not a valid pairing. A pairing can be determined to be two-way if both the entrance and
exit of that pair are an exit and entrance of another pairing, respectively.

### Example

```yaml
The Messenger:
  plando_connections:
    - entrance: Searing Crags - Top
      exit: Dark Cave - Right
    - entrance: Glacial Peak - Left
      exit: Corrupted Future
```

This block will create the following connections:
1. Leaving Searing Crags towards Glacial Peak will take you to the beginning of Dark Cave, and leaving the Dark Cave
   door will return you to the top of Searing Crags.
2. Taking Manfred to leave Glacial Peak, will take you to Corrupted Future. There is no reverse connection here so it
   will always be one-way.
