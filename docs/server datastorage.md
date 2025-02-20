# Serverside Data Storage

This document covers some of the patterns and tips and tricks used to communicate with data storage, communication with the data storage is done through the [`Get`](network%20protocol.md#Get) \ [`Retrieved`](network%20protocol.md#Retrieved), [`Set`](network%20protocol.md#Set) \ [`SetReply`](network%20protocol.md#SetReply) and [`SetNotify`](network%20protocol.md#SetNotify) commands described inside the [Network Protocol](network%20protocol.md). The data storage is meant to preserve some data on the server that spans across the lifecycle of the server and is shared with all clients (on any team). 

## Keys
The data storage works by keys and is internally stored as a dictionary. note that the whole data storage is accessible by all clients so if you want to store data specifically for your team, game or slot you will have to make your key unique, this is often done by add the team number, game name or slot id to the key. Some examples:
| EneryLink{team} |                   |
| ---             | ---               |
| `EnergyLink1`   | Energy for team 1 |
| `EnergyLink2`   | Energy for team 2 |

| GiftBoxes;{team} |                                            |
| ---              | ---                                        |
| `GiftBoxes;0`    | Giftbox metadata for all giftbox on team 0 |
| `GiftBoxes;1`    | Giftbox metadata for all giftbox on team 1 |

| GiftBox;{team};{slot} |                                             |
| ---                   | ---                                         |
| `GiftBox;0;1`         | Slot specific giftbox for slot 1 on team 0  |
| `GiftBox;5;13`        | Slot specific giftbox for slot 13 on team 5 |

## Thread Safety
Because any client can read and write to the data storage at any time you can never assume that value you read is still the same 1 second later. So an 
easy mistake is for example retrieving a value using a `Get` command, then processing the value, altering it, and then writing it back to the store with an `Set`-`replace` command. The `Set`-`replace` command will simply override the value discarding any possible changes by any other clients.

There are a few aspects to the data storage that we can use to our advantage to ensure thread safety:
* Any additional data given to the `Set` command will be passed along to the `SetReply` response. this can be used to "tag" a certain `SetReply` by for-example adding a specific random value to your `Set` then when you receive the `SetReply` you can check that value to match it back up to your `Set` command. 
* All operations in your `Set` command are executed in order without interruption from others and the final result will only trigger one `SetRely`.

Its a lot simpler to stay thread safe with basic types such a numbers as shown below in [EnergyLink](#EnergyLink), therefor it can useful to spread your data across multiple data storage keys just holding a basic value like a number in each, for example if you want to safely update the following data structure 
Key `Fruit`: `{ "Apple": 3, "Cherry": 7 }` it will be a lot more easy to safely update as two separated keys `FruitApple`: `3` and `FruitCherry`: `7`.

Lets look at a few examples:

### EnergyLink
Energylink lets you share you excess energy with across multiple clients and games, it uses a team specific key of `EneryLink{team}`. The Energy value is a numeric value and its important that games can add and take energy from it in a thread safe way. We will also provide our current `slot` number, this allows other clients to distinguish which client added or drained what. A little side note, over the course of a long game, many clients can contribute to the energy value making it larger then an int64, while python and json have no issues with this, some programming languages might need to take extra care.

Adding is easy, just a `Set`-`add` operation, for example to add 20:
```json
{
    "cmd": "Set",
    "key": "EnergyLink0",
    "default": 0,
    "slot": 5,
    "operations": [
        {"operation": "add", "value": 20},
    ]
}
```
Depleting, however is more complicated, in this scenario we use both the fact that multiple operations are executed together aswel as tagging the Set.
First we subtract our value 50, then we set the value back to 0 if it went below 0. Lastly we will look for the corresponding `SetReply` command with the tag we specified, inside the `SetReply` we compare the `original_value` to the `value` to know how much energy we where actually able to subtract.
```json
{
    "cmd": "Set",
    "key": "EnergyLink0",
    "tag": "7cc04194-b491-4cba-a89e-ef754502f3ff",
    "default": 0,
    "slot": 5,
    "want_reply": true,
    "operations": [
        {"operation": "add", "value": -50},
        {"operation": "max", "value": 0},
    ]
}
```
Response:
```json
{
    "cmd": "Set",
    "key": "EnergyLink0",
    "tag": "7cc04194-b491-4cba-a89e-ef754502f3ff",
    "default": 0,
    "slot": 5,
    "want_reply": true,
    "operations": [
        {"operation": "add", "value": -50},
        {"operation": "max", "value": 0},
    ],
    "original_value": 20,
    "value": 0

}
```
So we only where able to subtract `original_value` - `value` = 20 Energy.

### Gifting
Gifting allows players to gift items they don't need to other games, like if you get a health potion but you are at no risk of dieing someone else might have more use for it. Gifting works by slot specific giftboxes, any client can add a gift to the giftbox, and only the client of the slot the giftbox belongs to is supposed to remove gifts from it. Now it might seem easy with an array of gift objects however while appending to an array is thread safe, removing entries from an array cannot be done thread safe. Therefor giftboxes are implemented as dictionaries where each gift has its own unique key. new gifts can safely be added using the `update` operation and removal of specific gifts can be done using their unique keys with the `pop` operation. (for more imformation visit the [gifting api documentation](https://github.com/agilbert1412/Archipelago.Gifting.Net/blob/main/Documentation/Gifting%20API.md)).

Adding gifts:
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
Removing gifts, note we are ignoring the errors here as pop-ing an non existing key will raise an error otherwise.
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

### Queue (FIFO) \ Stack (FILO) 
Queues can be implemented using lists and this will still be safe aslong as all producers only append to the end of the list and consumers only remove the first or last element in the list. To append to a list we would use the `add` operation with an array value, this will append all elements in the provided array to the list. In order to `peek` any elemment in the list, you would unfortunately have to retrieve the full list by its key. To remove the first or last element of a list we can use the `pop` opperation.

Adding elements to the list is easy, just a `Set`-`add` operation with an array as value:
```json
{
    "cmd": "Set",
    "key": "SomeQueueName",
    "default": [],
    "operations": [
        {"operation": "add", "value": ["whatever value"] },
    ]
}
```
To pop an element in the queue we would use a `Set`-`pop` operation, with a value of `0` for queues and `1` for stacks
```json
{
    "cmd": "Set",
    "key": "SomeQueueName",
    "default": [],
    "on_error": "ignore",
    "tag": "4CDF4226-C7D2-4242-8636-D16FA9EA2016",
    "want_reply": true,
    "operations": [
        {"operation": "pop", "value": 0 },
    ]
}
```
Than inside the `SetReply` check by tag if this was done as a result to you pop-ing it, if thats the case you find the pop-ed element in the `original_value`. 

### Locking
This is not an actual used example but if you want an even more complex thread safe way you can implement using the techniques aboves. it is possible to use a `pop` operation on specific dictionary keys along with a tagging your `Set` command to see if you client can obtain a lock, for example:
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
Than inside the `SetReply` check by looking in the `original_value` and 'value' if `Key1` got removed and by tag if this was done as a result to you pop-ing it, if thats all true, you know you now got the lock and can do whatever you want to the key `MyStoreAvailableKeys:Key1`. and when your done with it, you write back `Key1` to the `MyStoreAvailableKeys` using an update.
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
Ofcourse this is not perfect, its only safe if all clients trying to alter `MyStoreAvailableKeys:Key1` respect this locking mechanism, and if the client who obtained the lock disconnects or otherwise fails to release it you need to somehow timeout that lock, like you could have a separated dict storing the last timestamps for each key a lock was obtained.
