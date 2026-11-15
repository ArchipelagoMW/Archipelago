# APWorld Dev FAQ

This document is meant as a reference tool to show solutions to common problems when developing an apworld.
It is not intended to answer every question about Archipelago and it assumes you have read the other docs, 
including [Contributing](contributing.md), [Adding Games](<adding games.md>), and [World API](<world api.md>).

---

### I've never added a game to Archipelago before. Should I start with the APWorld or the game client?

Strictly speaking, this is a false dichotomy: we do *not* recommend doing 100% of client work before the APWorld,
or 100% of APWorld work before the client. It's important to iterate on both parts and test them together.
However, the early iterations tend to be very similar for most games,
so the typical recommendation for first-time AP developers is:

- Start with a proof-of-concept for [the game client](adding%20games.md#client)
  - Figure out how to interface with the game. Whether that means "modding" the game, or patching a ROM file,
    or developing a separate client program that edits the game's memory, or some other technique.
  - Figure out how to give items and detect locations in the actual game. Not every item and location,
    just one of each major type (e.g. opening a chest vs completing a sidequest) to prove all the items and locations
    you want can actually be implemented.
  - Figure out how to make a websocket connection to an AP server, possibly using a client library (see [Network Protocol](<network%20protocol.md>).
    To make absolutely sure this part works, you may want to test the connection by generating a multiworld
    with a different game, then making your client temporarily pretend to be that other game.
- Next, make a "trivial" APWorld, i.e. an APWorld that always generates the same items and locations
  - If you've never done this before, likely the fastest approach is to copy-paste [APQuest](<../worlds/apquest>), and read the many
    comments in there until you understand how to edit the items and locations.
- Then you can do your first "end-to-end test": generate a multiworld using your APWorld, [run a local server](<running%20from%20source.md>)
  to host it, connect to that local server from your game client, actually check a location in the game,
  and finally make sure the client successfully sent that location check to the AP server
  as well as received an item from it.

That's about where general recommendations end. What you should do next will depend entirely on your game
(e.g. implement more items, write down logic rules, add client features, prototype a tracker, etc).
If you're not sure, then this would be a good time to re-read [Adding Games](<adding%20games.md>), and [World API](<world%20api.md>).

There are a few assumptions in this recommendation worth stating explicitly, namely:

- If something you want to do is infeasible, you want to find out that it's infeasible as soon as possible, before
  you write a bunch of code assuming it could be done. That's why we recommend starting with the game client.
  - Getting an APWorld to generate whatever items/locations you want is always feasible, since items/locations are
    little more than id numbers and name strings during generation.
- You generally want to get to an "end-to-end playable" prototype quickly. On top of all the technical challenges these
  docs describe, it's also important to check that a randomizer is *fun to play*, and figure out what features would be
  essential for a public release.
- A first-time world developer may or may not be deeply familiar with Archipelago, but they're almost certainly familiar
  with the game they want to randomize. So judging whether your game client is working correctly might be significantly
  easier than judging if your APWorld is working.

---

### My game has a restrictive start that leads to fill errors

A "restrictive start" here means having a combination of very few sphere 1 locations and potentially requiring more
than one item to get a player to sphere 2.

One way to fix this is to hint to the Generator that an item needs to be in sphere one with local_early_items. 
Here, `1` represents the number of "Sword" items the Generator will attempt to place in sphere one.
```py
early_item_name = "Sword"
self.multiworld.local_early_items[self.player][early_item_name] = 1
```

Some alternative ways to try to fix this problem are:
* Add more locations to sphere one of your world, potentially only when there would be a restrictive start
* Pre-place items yourself, such as during `create_items`
* Put items into the player's starting inventory using `push_precollected`
* Raise an exception, such as an `OptionError` during `generate_early`, to disallow options that would lead to a
  restrictive start

---

### I have multiple options that change the item/location pool counts and need to make sure I am not submitting more/fewer items than locations

In an ideal situation your system for producing locations and items wouldn't leave any opportunity for them to be
unbalanced. But in real, complex situations, that might be unfeasible.

If that's the case, you can create extra filler based on the difference between your unfilled locations and your
itempool by comparing [get_unfilled_locations](https://github.com/ArchipelagoMW/Archipelago/blob/main/BaseClasses.py#:~:text=get_unfilled_locations)
to your list of items to submit

Note: to use self.create_filler(), self.get_filler_item_name() should be defined to only return valid filler item names
```py
total_locations = len(self.multiworld.get_unfilled_locations(self.player))
item_pool = self.create_non_filler_items()

for _ in range(total_locations - len(item_pool)):
    item_pool.append(self.create_filler())

self.multiworld.itempool += item_pool
```

A faster alternative to the `for` loop would be to use a
[list comprehension](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions):
```py
item_pool += [self.create_filler() for _ in range(total_locations - len(item_pool))]
```

---

### I learned about indirect conditions in the world API document, but I want to know more. What are they and why are they necessary?

The world API document mentions how to use `multiworld.register_indirect_condition` to register indirect conditions and
**when** you should use them, but not *how* they work and *why* they are necessary. This is because the explanation is
quite complicated.

Region sweep (the algorithm that determines which regions are reachable) is a Breadth-First Search of the region graph.
It starts from the origin region, checks entrances one by one, and adds newly reached regions and their entrances to
the queue until there is nothing more to check.

For performance reasons, AP only checks every entrance once. However, if an entrance's access_rule depends on region
access, then the following may happen:
1. The entrance is checked and determined to be nontraversable because the region in its access_rule hasn't been
   reached yet during the graph search.
2. Then, the region in its access_rule is determined to be reachable.

This entrance *would* be in logic if it were rechecked, but it won't be rechecked this cycle.
To account for this case, AP would have to recheck all entrances every time a new region is reached until no new
regions are reached.

An indirect condition is how you can manually define that a specific entrance needs to be rechecked during region sweep
if a specific region is reached during it.
This keeps most of the performance upsides. Even in a game making heavy use of indirect conditions (ex: The Witness),
using them is significantly faster than just "rechecking each entrance until nothing new is found".
The reason entrance access rules using `location.can_reach` and `entrance.can_reach` are also affected is because they
call `region.can_reach` on their respective parent/source region.

We recognize it can feel like a trap since it will not alert you when you are missing an indirect condition,
and that some games have very complex access rules.
As of [PR #3682 (Core: Region handling customization)](https://github.com/ArchipelagoMW/Archipelago/pull/3682)
being merged, it is possible for a world to opt out of indirect conditions entirely, instead using the system of
checking each entrance whenever a region has been reached, although this does come with a performance cost.
Opting out of using indirect conditions should only be used by games that *really* need it. For most games, it should
be reasonable to know all entrance &rarr; region dependencies, making indirect conditions preferred because they are
much faster.

---

### I uploaded the generated output of my world to the webhost and webhost is erroring on corrupted multidata

The error `Could not load multidata. File may be corrupted or incompatible.` occurs when uploading a locally generated
file where there is an issue with the multidata contained within it. It may come with a description like
`(No module named 'worlds.myworld')` or `(global 'worlds.myworld.names.ItemNames' is forbidden)`

Pickling is a way to compress python objects such that they can be decompressed and be used to rebuild the
python objects. This means that if one of your custom class instances ends up in the multidata, the server would not
be able to load that custom class to decompress the data, which can fail either because the custom class is unknown
(because it cannot load your world module) or the class it's attempting to import to decompress is deemed unsafe.

Common situations where this can happen include:
* Using Option instances directly in slot_data. Ex: using `options.option_name` instead of `options.option_name.value`.
  Also, consider using the `options.as_dict("option_name", "option_two")` helper.
* Using enums as Location/Item names in the datapackage. When building out `location_name_to_id` and `item_name_to_id`,
  make sure that you are not using your enum class for either the names or ids in these mappings.

---

### Some locations are technically possible to check with few or no items, but they'd be very tedious or frustrating. How do worlds deal with this?

Sometimes the game can be modded to skip these locations or make them less tedious. But when this issue is due to a fundamental aspect of the game, then the general answer is "soft logic" (and its subtypes like "combat logic", "money logic", etc.). For example: you can logically require that a player have several helpful items before fighting the final boss, even if a skilled player technically needs no items to beat it. Randomizer logic should describe what's *fun* rather than what's technically possible.

Concrete examples of soft logic include:
- Defeating a boss might logically require health upgrades, damage upgrades, certain weapons, etc. that aren't strictly necessary.
- Entering a high-level area might logically require access to enough other parts of the game that checking other locations should naturally get the player to the soft-required level.
- Buying expensive shop items might logically require access to a place where you can quickly farm money, or logically require access to enough parts of the game that checking other locations should naturally generate enough money without grinding.

Remember that all items referenced by logic (however hard or soft) must be `progression`. Since you typically don't want to turn a ton of `filler` items into `progression` just for this, it's common to e.g. write money logic using only the rare "$100" item, so the dozens of "$1" and "$10" items in your world can remain `filler`.

---

### What if my game has "missable" or "one-time-only" locations or region connections?

Archipelago logic assumes that once a region or location becomes reachable, it stays reachable forever, no matter what 
the player does in-game. Slightly more formally: Receiving an AP item must never cause a region connection or location 
to "go out of logic" (become unreachable when it was previously reachable), and receiving AP items is the only kind of 
state change that AP logic acknowledges. No other actions or events can change reachability.

So when the game itself does not follow this assumption, the options are:
- Modify the game to make that location/connection repeatable
- If there are both missable and repeatable ways to check the location/traverse the connection, then write logic for 
  only the repeatable ways
- Don't generate the missable location/connection at all
  - For connections, any logical regions will still need to be reachable through other, *repeatable* connections
  - For locations, this may require game changes to remove the vanilla item if it affects logic
- Decide that resetting the save file is part of the game's logic, and warn players about that

---

### What are "local" vs "remote" items, and what are the pros and cons of each?

First off, these terms can be misleading. Since the whole point of a multi-game multiworld randomizer is that some items
are going to be placed in other slots (unless there's only one slot), the choice isn't really "local vs remote";
it's "mixed local/remote vs all remote". You have to get "remote items" working to be an AP implementation at all, and
it's often simpler to handle every item/location the same way, so you generally shouldn't worry about "local items"
until you've finished more critical features.

Next, "local" and "remote" items confusingly refer to multiple concepts, so it's important to clearly separate them:

- Whether an item happens to get placed in the same slot it originates from, or a different slot. I'll call these
  "locally placed" and "remotely placed" items.
- Whether an AP client implements location checking for locally placed items by skipping the usual AP server roundtrip
  (i.e. sending [LocationChecks](<network%20protocol.md#locationchecks>)
  then receiving [ReceivedItems](<network%20protocol.md#receiveditems>)
  ) and directly giving the item to the player, or by doing the AP server roundtrip regardless. I'll call these
  "locally implemented" items and "remotely implemented" items.
  - Locally implementing items requires the AP client to know what the locally placed items were without asking an AP
    server (or else you'd effectively be doing remote items with extra steps). Typically, it gets that information from
    a patch file, which is one reason why games that already need a patch file are more likely to choose local items.
  - If items are remotely implemented, the AP client can use [location scouts](<network%20protocol.md#LocationScouts>)
    to learn what items are placed on what locations. Features that require this information are sometimes mistakenly
    assumed to require locally implemented items, but location scouts work just as well as patch file data.
- [The `items_handling` bitflags in the Connect packet](<network%20protocol.md#items_handling-flags>).
  AP clients with remotely implemented items will typically set all three flags, including "from your own world".
  Clients with locally implemented items might set only the "from other worlds" flag.
  - Whether a local items client sets the "starting inventory" flag likely depends on other details. For example, if a ROM
    is being patched, and starting inventory can be added to that patch, then it makes sense to leave the flag unset.

When people talk about "local vs remote items" as a choice that world devs have to make, they mean deciding whether
your client will locally or remotely implement the items which happen to be locally placed (or make both
implementations, or let the player choose an implementation).

Theoretically, the biggest benefit of "local items" is that it allows a solo (single slot) multiworld to be played
entirely offline, with no AP server, from start to finish. This is similar to a "standalone"/non-AP randomizer,
except that you still get AP's player options, generation, etc. for free.
For some games, there are also technical constraints that make certain items easier to implement locally,
or less glitchy when implemented locally, as long as you're okay with never allowing these items to be placed remotely
(or offering the player even more options).

The main downside (besides more implementation work) is that "local items" can't support "same slot co-op".
That's when two players on two different machines connect to the same slot and play together.
This only works if both players receive all the items for that slot, including ones found by the other player,
which requires those items to be implemented remotely so the AP server can send them to all of that slot's clients.

So to recap:

- (All) remote items is often the simplest choice, since you have to implement remote items anyway.
- Remote items enable same slot co-op.
- Local items enable solo offline play.
- If you want to support both solo offline play and same slot co-op,
  you might need to expose local vs remote items as an option to the player.
