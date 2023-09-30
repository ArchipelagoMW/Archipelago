# Serverside Data Storage

This document covers some of the patterns and tips and tricks used to communicate with data storage, communication with the data storage is don't through the [`Get`](network%20protocol.md#Get) \ [`Retrieved`](network%20protocol.md#Retrieved), [`Set`](network%20protocol.md#Set) \ [`SetReply`](network%20protocol.md#SetReply) and [`SetNotify`](network%20protocol.md#SetNotify) commands described inside the [Network Protocol](network%20protocol.md). The data storage is meant to preserve some date on the server that spans across the lifecycle of the server and is shared with all clients (on any team). 

### Keys
The data storage works by keys and is internally stored as a dictionary. note that the whole data storage is accessible by all clients so if you want to store data specifically for your team, game or slot you will have to make your key unique, this is often done by add the team number, game name or slot id to the key. Some examples:
| EneryLink{team} |                 |
| `EnergyLink1` | Energy for team 1 |
| `EnergyLink2` | Energy for team 2 |

| GiftBoxes;{team} |                                            |
| `GiftBoxes;0`    | Giftbox metadata for all giftbox on team 0 |
| `GiftBoxes;1`    | Giftbox metadata for all giftbox on team 1 |

| GiftBox;{team};{slot} |                                             |
| `GiftBox;0;1`         | Slot specific giftbox for slot 1 on team 0  |
| `GiftBox;5;13`        | Slot specific giftbox for slot 13 on team 5 |

### Thread Safety
Because any client can read and write to the data storage at any time you can never assume that value you read is still the same 1 second later. So a 
easy mistake to make is for example retrieving a value using a `Get` command, then processing the value, altering it, and then writing it back to the store with an `Set`-`replace` command.

There are a few given aspects to the data storage that we can use to our advantage to ensure thread safety. 
* Any additional data given to the `Set` command will be passed along to the `SetReply` response. this can be used to "tag" a certain `SetReply` by for-example adding a specific random value to your `Set` then when you receive the `SetReply` you can check that value to match it back up to your `Set` command. 
* All operations in your `Set` command are executed in order without interruption from others and the final result will only trigger one `SetRely`.

Its a lot simpler to stay thread save with basic types such a numbers as shown below in [EnergyLink](#EnergyLink), therefor it can useful to spread your data across multiple data storage keys just holding a basic value like a number, for example if you want to safely update the following data structure 
Key `Fruit`: `json { "Apple": 3, "Cherry": 7 }` it will be a lot more easy to safely update as two separated keys `FruitApple`: 3 and `FruitCherry`: 7

Lets look at a few examples:

#### EnergyLink
Energylink wants to share the current energy value across multiple clients and games, it uses a team specific key of `EneryLink{team}`. The Energy value is a numeric value and its important that games can add and take energy from it in a thread safe way.

Adding is easy, just a `Set-add` operation, for example to add 20:
```json
{
    "cmd": "Set",
    "key": "EnergyLink0",
    "default": 0,
    "operations": [
        {"operation": "add", "value": 20},
    ]
}
```
Depleting, however is more complicated, in this scenario we use both the fact that multiple operations are executed together aswel as tagging the Set.
First we subtract our value, them we set the value back to 0 if it went below 0. Lastly we will look for the corresponding `SetReply` command with the tag we specified, inside the `SetReply` we compare the `original_value` to the `value` to know how much energy we where actually able to subtract
```json
{
    "cmd": "Set",
    "key": "EnergyLink0",
    "tag": "7cc04194-b491-4cba-a89e-ef754502f3ff",
    "default": 0,
    "want_reply": true,
    "operations": [
        {"operation": "add", "value": -50},
        {"operation": "max", "value": 0},
    ]
}
```
response
```json
{
    "cmd": "Set",
    "key": "EnergyLink0",
    "tag": "7cc04194-b491-4cba-a89e-ef754502f3ff",
    "default": 0,
    "want_reply": true,
    "operations": [
        {"operation": "add", "value": -50},
        {"operation": "max", "value": 0},
    ],
    "original_value": 20,
    "value": 0

}
```
So we only where able to subtract `original_value` - `value` = 20 Energy

#### Gifting
Gifting allow players to gift items they don't need to other games, like if you get a health potion but you are at no risk of dieing someone else might have more use for it. Gifting works by slot specific giftboxes, any client can gift add a gift to the giftbox, and only the client of the slot the giftbox belongs to is supposed to remove gifts from it. Now it might seem easy with an array of gift objects however while appending to an array is thread safe, removing entries from an array cannot be done thread safe. Giftboxes are implemented as dictionaries where each gift has its own unique key. new gifts can safely be added using the `update` operation and removal of specific gifts can be done on their unique keys using the `pop` operation. 

Adding gifts
```json
{
    "cmd": "Set",
    "key": "GiftBox;0;1",
    "default": {},
    "operations": [
        {"operation": "update", "value": {
            "1a4a169f-de12-45cf-a7d9-f77c1c2ebc31": {
                "gift": "json"
            }
        }}
    ]
}
```
Removing gifts, note we are ignoring the errors here as pop-ing an non existing key will raise an error otherwise
```json
{
    "cmd": "Set",
    "key": "GiftBox;0;1",
    "default": {},
    "on_error": "ignore",
    "operations": [
        {"operation": "pop", "value": "1a4a169f-de12-45cf-a7d9-f77c1c2ebc31" },
    ]
}
```

#### Locking
This is not an actual used example but if you want an even more complex thread safety you can implement such a thing yourself using the techniques aboves. it is possible to use a `pop` operation on specific dictionary keys along with a tagging your `Set` command to see if you client can obtain a lock, for example:
```json
{
    "cmd": "Set",
    "key": "MyStoreAvailableKeys",
    "default": { "Key1": true, "Key2": true },
    "on_error": "ignore",
    "tag": "2c14b824-f274-40e2-ab88-e3ce643683c1",
    "want_reply": true,
    "operations": [
        {"operation": "pop", "value": "Key1" },
    ]
}
```
Than inside the `SetReply` check by looking in the `original_value` and 'value' if `Key1` got removed and by tag if this was done as a result to you pop-int it, if thats all true, you know you now got the lock and can do whatever you want to the key `MyStoreAvailableKeys:Key1`. and when your done with it you write back `Key1` to the `MyStoreAvailableKeys` using an update
```json
{
    "cmd": "Set",
    "key": "MyStoreAvailableKeys",
    "default": {},
    "operations": [
        {"operation": "update", "value": { "Key1": true }}
    ]
}
```
Ofcourse this is not perfect, its only safe if all clients trying to alter `MyStoreAvailableKeys:Key1` respect this locking mechanism, and if the client who obtained the lock disconnects or otherwise fails to release it you need to somehow time that out, like you could have a separated dict storing the last times for each key a lock was obtained
