# Wonder Trades

Pokemon Emerald uses Archipelago's data storage to emulate wonder trading. Wonder trading is meant as a sort of gacha game surprise trade where you give up one of your pokemon and at some point in the future you'll receive one in return from another player who decided to participate. In practice, small groups will be able to use it as a means of simple trading as well by coordinating when they participate.

The goal of the implementation used by Pokemon Emerald is to allow players to interact with an NPC in-game to deposit and withdraw pokemon without having to touch their client. The client will automatically detect their state, look for available trades, and notify the player when they've received something.

It's also intended to work for Pokemon games other than Emerald, should any other games decide to opt in and implement the feature into their clients.

## Data Storage Key

There is one wonder trade entry per team at `pokemon_wonder_trades_{team number}`.

It should be a dict that looks something like this:

```json
{
  "_lock": 0,
  "0": "{some json data}",
  "3": "{some json data}"
}
```

`_lock` tells you whether you're allowed to try to modify the key. Its value should be either `0` to represent an unlocked state, or a timestamp represented by time since Epoch in ms (`int(time.time_ns() / 1000000)`). More below.

All other keys are just non-negative integers as strings, and they should hold JSON data representing a pokemon that can be taken from the server and given to your player. You can think of them as wonder trade slots. Pidgeon holes with a label. For consistency and ease of use, keep these keys between 0 and 255, and prefer the lowest number you can use. But you can't rely on those numbers being contiguous or starting at 0.

The values of non-`_lock` entries are strings of JSON matching the schema currently located at `data/trade_pokemon_schema.json`. These entries should be universally understandable by anything trying to interact with wonder trades. Of course, some Pokemon games include more data than others for a given Pokemon, some games don't have species introduced in later generations, and some data is of a different format, has different values, or is even spelled differently. The hope is that translating to and from JSON is reasonable for any game (or at least any game likely to be integrated into AP), and you can easily tell from the JSON whether your game is capable of giving the pokemon to the player in-game.

WIP
