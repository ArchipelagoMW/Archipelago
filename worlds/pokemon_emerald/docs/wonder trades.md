# Wonder Trades

Pokemon Emerald uses Archipelago's data storage to reproduce what the Pokemon series calls wonder trading. Wonder
trading is meant as a sort of gacha game surprise trade where you give up one of your pokemon and at some point in the
future you'll receive one in return from another player who decided to participate. In practice, small groups will be
able to use it as a means of simple trading as well by coordinating when they participate.

The goal of the implementation used by Pokemon Emerald is to allow players to interact with an NPC in-game to deposit
and withdraw pokemon without having to touch their client. The client will automatically detect their state, look for
available trades, and notify the player when they've received something.

It's also intended to work for Pokemon games other than Emerald, should any other games decide to opt in and implement
the feature into their clients.

## Data Storage Format

There is one wonder trade entry per team at `pokemon_wonder_trades_{team number}`.

It should be a dict that looks something like this:

```json
{
  "_lock": 0,
  "0": [3, "{some json data}"],
  "3": [2, "{some json data}"]
}
```

### Lock

`_lock` tells you whether you're allowed to try to modify the key. Its value should be either `0` to represent an
unlocked state, or a timestamp represented by time since Epoch in ms (`int(time.time_ns() / 1000000)`).
[See below](#preventing-race-conditions) for more info.

### Non-lock Keys

All other keys are just non-negative integers as strings. You can think of them as wonder trade slots. Pidgeon holes
with a label. For consistency and ease of use, keep the keys between 0 and 255, and prefer the lowest number you can
use. They ONLY act as names that can be easily written to and removed from.
- You SHOULD NOT rely on those numbers being contiguous or starting at 0.
- You SHOULD NOT rely on a "trade" residing at a single slot until it is removed.
- You SHOULD NOT assume that the number has any significance to a player's slot, or trade order, or anything really.

### Values

The first entry in the tuple represents which slot put the pokemon up for trade. You could use this to display in your
game or client who the trade came from, but its primary purpose is to discriminate entries you can take from those you
can't. You don't want to send something to the server, see that the server has something to take, and then take your own
pokemon right back.

The JSON data should match the schema currently located at `data/trade_pokemon_schema.json`. It should be universally
understandable by anything trying to interact with wonder trades. Of course, some Pokemon games include more data than
others for a given pokemon, some games don't have species introduced in later generations, and some data is of a
different format, has different values, or is even spelled differently. The hope is that translating to and from JSON is
reasonable for any game (or at least any game likely to be integrated into AP), and you can easily tell from the JSON
whether your game is capable of giving the pokemon to the player in-game.

## Preventing Race Conditions

This caused by far the most headache of implementing wonder trades. You should be very thorough in trying to prevent
issues here.

If you prefer more technical explanations, the Pokemon Emerald client has documented wonder trade functions. The rest of
this section explains what problems are being solved and why the solutions work.

The problem that needs solving is that your client needs to know what the value of the trade data is before it commits
some sort of action. By design, multiple clients are writing to and removing from the same key in data storage, so if
two clients try to interact and there's ambiguity in what the data looks like, it will cause issues of duplication and
loss of data.

For example, client 1 and client 2 both see a pokemon that they can take, so they copy the pokemon to their respective
games, and both send a command to remove that pokemon from the data store. The first command works and removes the
entry, which sends an update to both clients that there no longer exists a pokemon at that slot. And then the second
command, which was already sent, tries to remove the same entry. At best, the data was duplicated, and at worst the
server raises an exception or crashes.

Thankfully, when you receive an update from the server that a storage value changed, it will tell you both the previous
and current value. That's where the lock comes in. At a basic level, your client attempts to claim ownership of the key
temporarily while it makes its modifications, and all other clients respect that claim by not interacting until the lock
is released. You know you locked the key because the `SetReply` you receive for modifying the lock is the one that set
it from an unlocked state to a locked state. When two clients try to lock at the same time, one will see an unlocked
state move to a locked state, and the other will see an already locked state move to a locked state. You can identify
whether a `SetReply` was triggered by your client's `Set` by attaching a uuid to the `Set` command, which will also be
attached to the `SetReply`. See the Emerald client for an example.

Which brings us to problem 2, which is the scenario where a client crashes or closes before unlocking the key. One rogue
client might prevent all other clients from ever interacting with wonder trading again.

So for this reason, the lock is a timestamp, and the key is considered "locked" if that timestamp is less than 5 seconds
in the past. If a client dies after locking, its lock will expire, and other clients will be able to make modifications.
Setting the lock to 0 is the canonical way of marking it as unlocked, but it's not a special case really. It's
equivalent to marking the key as last locked in 1970.

Which brings us to problem 3. Multiple clients which want to obtain the lock can only check whether the lock is
obtainable by refreshing the current lock's timestamp. So two clients trying to secure a lock made by a dead client may
trade back and forth, updating the lock to see if it is expired yet, seeing that it is not, and then waiting 5 seconds
while the other client does the same thing, which causes the lock to again be less than 5 seconds old.

Using a cooldown period longer than the time to expire only increases the minimum number of clients that can trigger
this cycle. Instead, the solution is to double your cooldown every time you bounce off an expired lock (and reset it
once you acquire it). Eventually the amount of time every client is waiting will be enough to create a gap large enough
for one client to consider the lock expired, and it will acquire the lock, make its changes, and set the lock state to
definitively unlocked, which will let the next client claim it, and so on.
