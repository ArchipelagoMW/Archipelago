# Archipelago General Client
## Archipelago Connection Handshake
These steps should be followed in order to establish a gameplay connection with an Archipelago session.

1. Client establishes WebSocket connection to Archipelago server.
2. Server accepts connection and responds with a [RoomInfo](#RoomInfo) packet.
3. Client may send a [GetDataPackage](#GetDataPackage) packet.
4. Server sends a [DataPackage](#DataPackage) packet in return. (If the client sent GetDataPackage.)
5. Client sends [Connect](#Connect) packet in order to authenticate with the server.
6. Server validates the client's packet and responds with [Connected](#Connected) or [ConnectionRefused](#ConnectionRefused).
7. Server may send [ReceivedItems](#ReceivedItems) to the client, in the case that the client is missing items that are queued up for it.
8. Server sends [PrintJSON](#PrintJSON) to all players to notify them of the new client connection.

In the case that the client does not authenticate properly and receives a [ConnectionRefused](#ConnectionRefused) then the server will maintain the connection and allow for follow-up [Connect](#Connect) packet.

There are also a number of community-supported libraries available that implement this network protocol to make integrating with Archipelago easier.

| Language/Runtime              | Project                                                                                            | Remarks                                                                         |
|-------------------------------|----------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| Python                        | [Archipelago CommonClient](https://github.com/ArchipelagoMW/Archipelago/blob/main/CommonClient.py) |                                                                                 |
|                               | [Archipelago SNIClient](https://github.com/ArchipelagoMW/Archipelago/blob/main/SNIClient.py)       | For Super Nintendo Game Support; Utilizes [SNI](https://github.com/alttpo/sni). |
| JVM (Java / Kotlin)           | [Archipelago.MultiClient.Java](https://github.com/ArchipelagoMW/Archipelago.MultiClient.Java)      |                                                                                 |
| .NET (C# / C++ / F# / VB.NET) | [Archipelago.MultiClient.Net](https://www.nuget.org/packages/Archipelago.MultiClient.Net)          |                                                                                 |
| C++                           | [apclientpp](https://github.com/black-sliver/apclientpp)                                           | header-only                                                                     |
|                               | [APCpp](https://github.com/N00byKing/APCpp)                                                        | CMake                                                                           |
| JavaScript / TypeScript       | [archipelago.js](https://www.npmjs.com/package/archipelago.js)                                     | Browser and Node.js Supported                                                   |
| Haxe                          | [hxArchipelago](https://lib.haxe.org/p/hxArchipelago)                                              |                                                                                 |
| Rust                          | [ArchipelagoRS](https://github.com/ryanisaacg/archipelago_rs)                                      |                                                                                 |

## Synchronizing Items
When the client receives a [ReceivedItems](#ReceivedItems) packet, if the `index` argument does not match the next index that the client expects then it is expected that the client will re-sync items with the server. This can be accomplished by sending the server a [Sync](#Sync) packet and then a [LocationChecks](#LocationChecks) packet.

Even if the client detects a desync, it can still accept the items provided in this packet to prevent gameplay interruption.

When the client receives a [ReceivedItems](#ReceivedItems) packet and the `index` arg is `0` (zero) then the client should accept the provided `items` list as its full inventory. (Abandon previous inventory.)

# Archipelago Protocol Packets
Packets are sent between the multiworld server and client in order to sync information between them. Below is a directory of each packet.

Packets are simple JSON lists in which any number of ordered network commands can be sent, which are objects. Each command has a "cmd" key, indicating its purpose. All packet argument types documented here refer to JSON types, unless otherwise specified.

An object can contain the "class" key, which will tell the content data type, such as "Version" in the following example.

Example:
```javascript
[{"cmd": "RoomInfo", "version": {"major": 0, "minor": 1, "build": 3, "class": "Version"}, "tags": ["WebHost"], ... }]
```

## (Server -> Client)
These packets are are sent from the multiworld server to the client. They are not messages which the server accepts.
* [RoomInfo](#RoomInfo)
* [ConnectionRefused](#ConnectionRefused)
* [Connected](#Connected)
* [ReceivedItems](#ReceivedItems)
* [LocationInfo](#LocationInfo)
* [RoomUpdate](#RoomUpdate)
* [PrintJSON](#PrintJSON)
* [DataPackage](#DataPackage)
* [Bounced](#Bounced)
* [InvalidPacket](#InvalidPacket)
* [Retrieved](#Retrieved)
* [SetReply](#SetReply)

### RoomInfo
Sent to clients when they connect to an Archipelago server.
#### Arguments
| Name | Type | Notes |
| ---- | ---- | ----- |
| version | [NetworkVersion](#NetworkVersion) | Object denoting the version of Archipelago which the server is running. |
| tags | list\[str\] | Denotes special features or capabilities that the sender is capable of. Example: `WebHost` |
| password | bool | Denoted whether a password is required to join this room.|
| permissions | dict\[str, [Permission](#Permission)\[int\]\] | Mapping of permission name to [Permission](#Permission), keys are: "release", "collect" and "remaining". |
| hint_cost | int | The amount of points it costs to receive a hint from the server. |
| location_check_points | int | The amount of hint points you receive per item/location check completed. ||
| games | list\[str\] | List of games present in this multiworld. |
| datapackage_versions | dict\[str, int\] | Data versions of the individual games' data packages the server will send. Used to decide which games' caches are outdated. See [Data Package Contents](#Data-Package-Contents). |
| seed_name | str | uniquely identifying name of this generation |
| time | float | Unix time stamp of "now". Send for time synchronization if wanted for things like the DeathLink Bounce. |

#### release
Dictates what is allowed when it comes to a player releasing their run. A release is an action which distributes the rest of the items in a player's run to those other players awaiting them.

* `auto`: Distributes a player's items to other players when they complete their goal.
* `enabled`: Denotes that players may release at any time in the game.
* `auto-enabled`: Both of the above options together.
* `disabled`: All release modes disabled.
* `goal`: Allows for manual use of release command once a player completes their goal. (Disabled until goal completion)

#### collect
Dictates what is allowed when it comes to a player collecting their run. A collect is an action which sends the rest of the items in a player's run.

* `auto`: Automatically when they complete their goal.
* `enabled`: Denotes that players may !collect at any time in the game.
* `auto-enabled`: Both of the above options together.
* `disabled`: All collect modes disabled.
* `goal`: Allows for manual use of collect command once a player completes their goal. (Disabled until goal completion)


#### remaining
Dictates what is allowed when it comes to a player querying the items remaining in their run.

* `goal`: Allows a player to query for items remaining in their run but only after they completed their own goal.
* `enabled`: Denotes that players may query for any items remaining in their run (even those belonging to other players).
* `disabled`: All remaining item query modes disabled.

### ConnectionRefused
Sent to clients when the server refuses connection. This is sent during the initial connection handshake.
#### Arguments
| Name | Type | Notes |
| ---- | ---- | ----- |
| errors | list\[str\] | Optional. When provided, should contain any one of: `InvalidSlot`, `InvalidGame`, `IncompatibleVersion`, `InvalidPassword`, or `InvalidItemsHandling`. |

InvalidSlot indicates that the sent 'name' field did not match any auth entry on the server.
InvalidGame indicates that a correctly named slot was found, but the game for it mismatched.
IncompatibleVersion indicates a version mismatch.
InvalidPassword indicates the wrong, or no password when it was required, was sent.
InvalidItemsHandling indicates a wrong value type or flag combination was sent.

### Connected
Sent to clients when the connection handshake is successfully completed.
#### Arguments
| Name              | Type                                     | Notes                                                                                                                                               |
|-------------------|------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| team              | int                                      | Your team number. See [NetworkPlayer](#NetworkPlayer) for more info on team number.                                                                 |
| slot              | int                                      | Your slot number on your team. See [NetworkPlayer](#NetworkPlayer) for more info on the slot number.                                                |
| players           | list\[[NetworkPlayer](#NetworkPlayer)\]  | List denoting other players in the multiworld, whether connected or not.                                                                            |
| missing_locations | list\[int\]                              | Contains ids of remaining locations that need to be checked. Useful for trackers, among other things.                                               |
| checked_locations | list\[int\]                              | Contains ids of all locations that have been checked. Useful for trackers, among other things. Location ids are in the range of ± 2<sup>53</sup>-1. |
| slot_data         | dict\[str, any\]                         | Contains a json object for slot related data, differs per game. Empty if not required. Not present if slot_data in [Connect](#Connect) is false.    |
| slot_info         | dict\[int, [NetworkSlot](#NetworkSlot)\] | maps each slot to a [NetworkSlot](#NetworkSlot) information                                                                                         |

### ReceivedItems
Sent to clients when they receive an item.
#### Arguments
| Name | Type | Notes |
| ---- | ---- | ----- |
| index | int | The next empty slot in the list of items for the receiving client. |
| items | list\[[NetworkItem](#NetworkItem)\] | The items which the client is receiving. |

### LocationInfo
Sent to clients to acknowledge a received [LocationScouts](#LocationScouts) packet and responds with the item in the location(s) being scouted.
#### Arguments
| Name | Type | Notes |
| ---- | ---- | ----- |
| locations | list\[[NetworkItem](#NetworkItem)\] | Contains list of item(s) in the location(s) scouted. |

### RoomUpdate
Sent when there is a need to update information about the present game session. Generally useful for async games.
Once authenticated (received Connected), this may also contain data from Connected.
#### Arguments
The arguments for RoomUpdate are identical to [RoomInfo](#RoomInfo) barring:

| Name | Type | Notes |
| ---- | ---- | ----- |
| hint_points | int | New argument. The client's current hint points. |
| players | list\[[NetworkPlayer](#NetworkPlayer)\] | Send in the event of an alias rename. Always sends all players, whether connected or not. |
| checked_locations | list\[int\] | May be a partial update, containing new locations that were checked, especially from a coop partner in the same slot. |
| missing_locations | list\[int\] | Should never be sent as an update, if needed is the inverse of checked_locations. |

All arguments for this packet are optional, only changes are sent.

### PrintJSON
Sent to clients purely to display a message to the player. While various message types provide additional arguments, clients only need to evaluate the `data` argument to construct the human-readable message text. All other arguments may be ignored safely.
#### Arguments
| Name | Type | Message Types | Contents |
| ---- | ---- | ------------- | -------- |
| data | list\[[JSONMessagePart](#JSONMessagePart)\] | (all) | Textual content of this message |
| type | str | (any) | [PrintJsonType](#PrintJsonType) of this message (optional) |
| receiving | int | ItemSend, ItemCheat, Hint | Destination player's ID |
| item | [NetworkItem](#NetworkItem) | ItemSend, ItemCheat, Hint | Source player's ID, location ID, item ID and item flags |
| found | bool | Hint | Whether the location hinted for was checked |
| team | int | Join, Part, Chat, TagsChanged, Goal, Release, Collect, ItemCheat | Team of the triggering player |
| slot | int | Join, Part, Chat, TagsChanged, Goal, Release, Collect | Slot of the triggering player |
| message | str | Chat, ServerChat | Original chat message without sender prefix |
| tags | list\[str\] | Join, TagsChanged | Tags of the triggering player |
| countdown | int | Countdown | Amount of seconds remaining on the countdown |

#### PrintJsonType
PrintJsonType indicates the type of a [PrintJSON](#PrintJSON) packet. Different types can be handled differently by the client and can also contain additional arguments. When receiving an unknown or missing type, the `data`'s list\[[JSONMessagePart](#JSONMessagePart)\] should still be displayed to the player as normal text.

Currently defined types are:

| Type | Subject |
| ---- | ------- |
| ItemSend | A player received an item. |
| ItemCheat | A player used the `!getitem` command. |
| Hint | A player hinted. |
| Join | A player connected. |
| Part | A player disconnected. |
| Chat | A player sent a chat message. |
| ServerChat | The server broadcasted a message. |
| Tutorial | The client has triggered a tutorial message, such as when first connecting. |
| TagsChanged | A player changed their tags. |
| CommandResult | Someone (usually the client) entered an `!` command. |
| AdminCommandResult | The client entered an `!admin` command. |
| Goal | A player reached their goal. |
| Release | A player released the remaining items in their world. |
| Collect | A player collected the remaining items for their world. |
| Countdown | The current server countdown has progressed. |

### DataPackage
Sent to clients to provide what is known as a 'data package' which contains information to enable a client to most easily communicate with the Archipelago server. Contents include things like location id to name mappings, among others; see [Data Package Contents](#Data-Package-Contents) for more info.

#### Arguments
| Name | Type | Notes |
| ---- | ---- | ----- |
| data | [DataPackageObject](#Data-Package-Contents) | The data package as a JSON object. |

### Bounced
Sent to clients after a client requested this message be sent to them, more info in the [Bounce](#Bounce) package.

#### Arguments
| Name | Type | Notes |
| ---- | ---- | ----- |
| games | list\[str\] | Optional. Game names this message is targeting |
| slots | list\[int\] | Optional. Player slot IDs that this message is targeting |
| tags | list\[str\] | Optional. Client [Tags](#Tags) this message is targeting |
| data | dict | The data in the [Bounce](#Bounce) package copied |

### InvalidPacket
Sent to clients if the server caught a problem with a packet. This only occurs for errors that are explicitly checked for.

#### Arguments
| Name | Type | Notes |
| ---- | ---- | ----- |
| type | str | The [PacketProblemType](#PacketProblemType) that was detected in the packet. |
| original_cmd | Optional[str] | The `cmd` argument of the faulty packet, will be `None` if the `cmd` failed to be parsed. |
| text | str | A descriptive message of the problem at hand. |

##### PacketProblemType
`PacketProblemType` indicates the type of problem that was detected in the faulty packet, the known problem types are below but others may be added in the future.

| Type | Notes |
| ---- | ----- |
| cmd | `cmd` argument of the faulty packet that could not be parsed correctly. |
| arguments | Arguments of the faulty packet which were not correct. |

### Retrieved
Sent to clients as a response the a [Get](#Get) package.
#### Arguments
| Name | Type | Notes |
| ---- | ---- | ----- |
| keys | dict\[str\, any] | A key-value collection containing all the values for the keys requested in the [Get](#Get) package. |

If a requested key was not present in the server's data, the associated value will be `null`.

Additional arguments added to the [Get](#Get) package that triggered this [Retrieved](#Retrieved) will also be passed along.

### SetReply
Sent to clients in response to a [Set](#Set) package if want_reply was set to true, or if the client has registered to receive updates for a certain key using the [SetNotify](#SetNotify) package. SetReply packages are sent even if a [Set](#Set) package did not alter the value for the key.
#### Arguments
| Name           | Type | Notes                                                                                      |
|----------------|------|--------------------------------------------------------------------------------------------|
| key            | str  | The key that was updated.                                                                  |
| value          | any  | The new value for the key.                                                                 |
| original_value | any  | The value the key had before it was updated. Not present on "_read" prefixed special keys. |

Additional arguments added to the [Set](#Set) package that triggered this [SetReply](#SetReply) will also be passed along.

## (Client -> Server)
These packets are sent purely from client to server. They are not accepted by clients.

* [Connect](#Connect)
* [Sync](#Sync)
* [LocationChecks](#LocationChecks)
* [LocationScouts](#LocationScouts)
* [StatusUpdate](#StatusUpdate)
* [Say](#Say)
* [GetDataPackage](#GetDataPackage)
* [Bounce](#Bounce)
* [Get](#Get)
* [Set](#Set)
* [SetNotify](#SetNotify)

### Connect
Sent by the client to initiate a connection to an Archipelago game session.

#### Arguments
| Name           | Type                              | Notes                                                                                        |
|----------------|-----------------------------------|----------------------------------------------------------------------------------------------|
| password       | str                               | If the game session requires a password, it should be passed here.                           |
| game           | str                               | The name of the game the client is playing. Example: `A Link to the Past`                    |
| name           | str                               | The player name for this client.                                                             |
| uuid           | str                               | Unique identifier for player client.                                                         |
| version        | [NetworkVersion](#NetworkVersion) | An object representing the Archipelago version this client supports.                         |
| items_handling | int                               | Flags configuring which items should be sent by the server. Read below for individual flags. |
| tags           | list\[str\]                       | Denotes special features or capabilities that the sender is capable of. [Tags](#Tags)        |
| slot_data      | bool                              | If true, the Connect answer will contain slot_data                                           |

#### items_handling flags
| Value | Meaning |
| ----- | ------- |
| 0b000 | No ReceivedItems is sent to you, ever. |
| 0b001 | Indicates you get items sent from other worlds. |
| 0b010 | Indicates you get items sent from your own world. Requires 0b001 to be set. |
| 0b100 | Indicates you get your starting inventory sent. Requires 0b001 to be set. |
| null  | Null or undefined loads settings from world definition for backwards compatibility. This is deprecated. |

#### Authentication
Many, if not all, other packets require a successfully authenticated client. This is described in more detail in [Archipelago Connection Handshake](#Archipelago-Connection-Handshake).

### ConnectUpdate
Update arguments from the Connect package, currently only updating tags and items_handling is supported.

#### Arguments
| Name | Type | Notes |
| ---- | ---- | ----- |
| items_handling | int | Flags configuring which items should be sent by the server. |
| tags | list\[str\] | Denotes special features or capabilities that the sender is capable of. [Tags](#Tags) |

### Sync
Sent to server to request a [ReceivedItems](#ReceivedItems) packet to synchronize items.
#### Arguments
No arguments necessary.

### LocationChecks
Sent to server to inform it of locations that the client has checked. Used to inform the server of new checks that are made, as well as to sync state.

#### Arguments
| Name | Type | Notes |
| ---- | ---- | ----- |
| locations | list\[int\] | The ids of the locations checked by the client. May contain any number of checks, even ones sent before; duplicates do not cause issues with the Archipelago server. |

### LocationScouts
Sent to the server to inform it of locations the client has seen, but not checked. Useful in cases in which the item may appear in the game world, such as 'ledge items' in A Link to the Past. The server will always respond with a [LocationInfo](#LocationInfo) packet with the items located in the scouted location.

#### Arguments
| Name | Type | Notes |
| ---- | ---- | ----- |
| locations | list\[int\] | The ids of the locations seen by the client. May contain any number of locations, even ones sent before; duplicates do not cause issues with the Archipelago server. |
| create_as_hint | int | If non-zero, the scouted locations get created and broadcasted as a player-visible hint. <br/>If 2 only new hints are broadcast, however this does not remove them from the LocationInfo reply. |

### StatusUpdate
Sent to the server to update on the sender's status. Examples include readiness or goal completion. (Example: defeated Ganon in A Link to the Past)

#### Arguments
| Name | Type | Notes |
| ---- | ---- | ----- |
| status | ClientStatus\[int\] | One of [Client States](#Client-States). Send as int. Follow the link for more information. |

### Say
Basic chat command which sends text to the server to be distributed to other clients.

#### Arguments
| Name | Type | Notes |
| ------ | ----- | ------ |
| text | str  | Text to send to others. |

### GetDataPackage
Requests the data package from the server. Does not require client authentication.

#### Arguments
| Name  | Type | Notes                                                                                                                           |
|-------| ----- |---------------------------------------------------------------------------------------------------------------------------------|
| games | list\[str\]  | Optional. If specified, will only send back the specified data. Such as, \["Factorio"\] -> Datapackage with only Factorio data. |

### Bounce
Send this message to the server, tell it which clients should receive the message and 
the server will forward the message to all those targets to which any one requirement applies.

#### Arguments
| Name | Type | Notes |
| ------ | ----- | ------ |
| games | list\[str\] | Optional. Game names that should receive this message |
| slots | list\[int\] | Optional. Player IDs that should receive this message |
| tags | list\[str\] | Optional. Client tags that should receive this message |
| data | dict | Any data you want to send |

### Get
Used to request a single or multiple values from the server's data storage, see the [Set](#Set) package for how to write values to the data storage. A Get package will be answered with a [Retrieved](#Retrieved) package.
#### Arguments
| Name | Type | Notes |
| ------ | ----- | ------ |
| keys | list\[str\] | Keys to retrieve the values for. |

Additional arguments sent in this package will also be added to the [Retrieved](#Retrieved) package it triggers.

Some special keys exist with specific return data, all of them have the prefix `_read_`, so `hints_{team}_{slot}` is `_read_hints_{team}_{slot}`.

| Name                          | Type                     | Notes                                             |
|-------------------------------|--------------------------|---------------------------------------------------|
| hints_{team}_{slot}           | list\[[Hint](#Hint)\]    | All Hints belonging to the requested Player.      |
| slot_data_{slot}              | dict\[str, any\]         | slot_data belonging to the requested slot.        |
| item_name_groups_{game_name}  | dict\[str, list\[str\]\] | item_name_groups belonging to the requested game. |

### Set
Used to write data to the server's data storage, that data can then be shared across worlds or just saved for later. Values for keys in the data storage can be retrieved with a [Get](#Get) package, or monitored with a [SetNotify](#SetNotify) package.
Keys that start with `_read_` cannot be set.
#### Arguments
| Name       | Type                                                  | Notes                                                                                                                  |
|------------|-------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| key        | str                                                   | The key to manipulate. Can never start with "_read".                                                                   |
| default    | any                                                   | The default value to use in case the key has no value on the server.                                                   |
| want_reply | bool                                                  | If true, the server will send a [SetReply](#SetReply) response back to the client.                                     |
| operations | list\[[DataStorageOperation](#DataStorageOperation)\] | Operations to apply to the value, multiple operations can be present and they will be executed in order of appearance. |

Additional arguments sent in this package will also be added to the [SetReply](#SetReply) package it triggers.

#### DataStorageOperation
A DataStorageOperation manipulates or alters the value of a key in the data storage. If the operation transforms the value from one state to another then the current value of the key is used as the starting point otherwise the [Set](#Set)'s package `default` is used if the key does not exist on the server already.
DataStorageOperations consist of an object containing both the operation to be applied, provided in the form of a string, as well as the value to be used for that operation, Example:
```json
{"operation": "add", "value": 12}
```

The following operations can be applied to a datastorage key
| Operation | Effect |
| ------ | ----- |
| replace | Sets the current value of the key to `value`. |
| default | If the key has no value yet, sets the current value of the key to `default` of the [Set](#Set)'s package (`value` is ignored). |
| add | Adds `value` to the current value of the key, if both the current value and `value` are arrays then `value` will be appended to the current value. |
| mul | Multiplies the current value of the key by `value`. |
| pow | Multiplies the current value of the key to the power of `value`. |
| mod | Sets the current value of the key to the remainder after division by `value`. |
| max | Sets the current value of the key to `value` if `value` is bigger. |
| min | Sets the current value of the key to `value` if `value` is lower. |
| and | Applies a bitwise AND to the current value of the key with `value`. |
| or | Applies a bitwise OR to the current value of the key with `value`. |
| xor | Applies a bitwise Exclusive OR to the current value of the key with `value`. |
| left_shift | Applies a bitwise left-shift to the current value of the key by `value`. |
| right_shift | Applies a bitwise right-shift to the current value of the key by `value`. |
| remove | List only: removes the first instance of `value` found in the list. |
| pop | List or Dict: for lists it will remove the index of the `value` given. for dicts it removes the element with the specified key of `value`. |
| update | Dict only: Updates the dictionary with the specified elements given in `value` creating new keys, or updating old ones if they previously existed. |

### SetNotify
Used to register your current session for receiving all [SetReply](#SetReply) packages of certain keys to allow your client to keep track of changes.
#### Arguments
| Name | Type | Notes |
| ------ | ----- | ------ |
| keys | list\[str\] | Keys to receive all [SetReply](#SetReply) packages for. |

## Appendix

### Coop
Coop in Archipelago is automatically facilitated by the server, however some of the default behaviour may not be what you desire.

If the game in question is a remote-items game (attribute on AutoWorld), then all items will always be sent and received.
If the game in question is not a remote-items game, then any items that are placed within the same world will not be send by the server.

To manually react to others in the same player slot doing checks, listen to [RoomUpdate](#RoomUpdate) -> checked_locations.

### NetworkPlayer
A list of objects. Each object denotes one player. Each object has four fields about the player, in this order: `team`, `slot`, `alias`, and `name`. `team` and `slot` are ints, `alias` and `name` are strs.

Each player belongs to a `team` and has a `slot`. Team numbers start at `0`. Slot numbers are unique per team and start at `1`. Slot number `0` refers to the Archipelago server; this may appear in instances where the server grants the player an item.

`alias` represents the player's name in current time. `name` is the original name used when the session was generated. This is typically distinct in games which require baking names into ROMs or for async games.

```python
from typing import NamedTuple
class NetworkPlayer(NamedTuple):
    team: int
    slot: int
    alias: str
    name: str
```

Example:
```json
[
    {"team": 0, "slot": 1, "alias": "Lord MeowsiePuss", "name": "Meow"}, 
    {"team": 0, "slot": 2, "alias": "Doggo", "name": "Bork"},
    {"team": 1, "slot": 1, "alias": "Angry Duck", "name": "Angry Quack"},
    {"team": 1, "slot": 2, "alias": "Mountain Duck", "name": "Honk"}
]
```

### NetworkItem
Items that are sent over the net (in packets) use the following data structure and are sent as objects:
```python
from typing import NamedTuple
class NetworkItem(NamedTuple):
    item: int
    location: int
    player: int
    flags: int
```
In JSON this may look like:
```json
[
    {"item": 1, "location": 1, "player": 1, "flags": 1},
    {"item": 2, "location": 2, "player": 2, "flags": 2},
    {"item": 3, "location": 3, "player": 3, "flags": 0}
]
```
`item` is the item id of the item. Item ids are in the range of ± 2<sup>53</sup>-1.

`location` is the location id of the item inside the world. Location ids are in the range of ± 2<sup>53</sup>-1.

`player` is the player slot of the world the item is located in, except when inside an [LocationInfo](#LocationInfo) Packet then it will be the slot of the player to receive the item

`flags` are bit flags:
| Flag | Meaning |
| ----- | ----- |
| 0 | Nothing special about this item |
| 0b001 | If set, indicates the item can unlock logical advancement |
| 0b010 | If set, indicates the item is important but not in a way that unlocks advancement |
| 0b100 | If set, indicates the item is a trap |

### JSONMessagePart
Message nodes sent along with [PrintJSON](#PrintJSON) packet to be reconstructed into a legible message. The nodes are intended to be read in the order they are listed in the packet.

```python
from typing import TypedDict, Optional
class JSONMessagePart(TypedDict):
    type: Optional[str]
    text: Optional[str]
    color: Optional[str] # only available if type is a color
    flags: Optional[int] # only available if type is an item_id or item_name
    player: Optional[int] # only available if type is either item or location
```

`type` is used to denote the intent of the message part. This can be used to indicate special information which may be rendered differently depending on client. How these types are displayed in Archipelago's ALttP client is not the end-all be-all. Other clients may choose to interpret and display these messages differently.
Possible values for `type` include:

| Name | Notes |
| ---- | ----- |
| text | Regular text content. Is the default type and as such may be omitted. |
| player_id | player ID of someone on your team, should be resolved to Player Name |
| player_name | Player Name, could be a player within a multiplayer game or from another team, not ID resolvable |
| item_id | Item ID, should be resolved to Item Name |
| item_name | Item Name, not currently used over network, but supported by reference Clients. |
| location_id | Location ID, should be resolved to Location Name |
| location_name | Location Name, not currently used over network, but supported by reference Clients. |
| entrance_name | Entrance Name. No ID mapping exists. |
| color | Regular text that should be colored. Only `type` that will contain `color` data. |


`color` is used to denote a console color to display the message part with and is only send if the `type` is `color`. This is limited to console colors due to backwards compatibility needs with games such as ALttP. Although background colors as well as foreground colors are listed, only one may be applied to a [JSONMessagePart](#JSONMessagePart) at a time.

Color options:
* bold
* underline
* black
* red
* green
* yellow
* blue
* magenta
* cyan
* white
* black_bg
* red_bg
* green_bg
* yellow_bg
* blue_bg
* magenta_bg
* cyan_bg
* white_bg

`text` is the content of the message part to be displayed.
`player` marks owning player id for location/item, 
`flags` contains the [NetworkItem](#NetworkItem) flags that belong to the item

### Client States
An enumeration containing the possible client states that may be used to inform the server in [StatusUpdate](#StatusUpdate).

```python
import enum
class ClientStatus(enum.IntEnum):
    CLIENT_UNKNOWN = 0
    CLIENT_READY = 10
    CLIENT_PLAYING = 20
    CLIENT_GOAL = 30
```

### NetworkVersion
An object representing software versioning. Used in the [Connect](#Connect) packet to allow the client to inform the server of the Archipelago version it supports.
```python
from typing import NamedTuple
class Version(NamedTuple):
    major: int
    minor: int
    build: int
```

### SlotType
An enum representing the nature of a slot.

```python
import enum
class SlotType(enum.IntFlag):
    spectator = 0b00
    player = 0b01
    group = 0b10
```

### NetworkSlot
An object representing static information about a slot.

```python
import typing
from NetUtils import SlotType
class NetworkSlot(typing.NamedTuple):
   name: str
   game: str
   type: SlotType
   group_members: typing.List[int] = []  # only populated if type == group
```

### Permission
An enumeration containing the possible command permission, for commands that may be restricted. 
```python
import enum
class Permission(enum.IntEnum):
    disabled = 0b000  # 0, completely disables access
    enabled = 0b001  # 1, allows manual use
    goal = 0b010  # 2, allows manual use after goal completion
    auto = 0b110  # 6, forces use after goal completion, only works for release and collect
    auto_enabled = 0b111  # 7, forces use after goal completion, allows manual use any time
```

### Hint
An object representing a Hint.
```python
import typing
class Hint(typing.NamedTuple):
    receiving_player: int
    finding_player: int
    location: int
    item: int
    found: bool
    entrance: str = ""
    item_flags: int = 0
```

### Data Package Contents
A data package is a JSON object which may contain arbitrary metadata to enable a client to interact with the Archipelago server most easily. Currently, this package is used to send ID to name mappings so that clients need not maintain their own mappings.

We encourage clients to cache the data package they receive on disk, or otherwise not tied to a session. You will know when your cache is outdated if the [RoomInfo](#RoomInfo) packet or the datapackage itself denote a different version. A special case is datapackage version 0, where it is expected the package is custom and should not be cached.

Note: 
 * Any ID is unique to its type across AP: Item 56 only exists once and Location 56 only exists once.
 * Any Name is unique to its type across its own Game only: Single Arrow can exist in two games.
 * The IDs from the game "Archipelago" may be used in any other game. 
   Especially Location ID -1: Cheat Console and -2: Server (typically Remote Start Inventory)

#### Contents
| Name | Type | Notes |
| ------ | ----- | ------ |
| games | dict[str, GameData] | Mapping of all Games and their respective data |

#### GameData
GameData is a **dict** but contains these keys and values. It's broken out into another "type" for ease of documentation.

| Name | Type | Notes |
| ---- | ---- | ----- |
| item_name_to_id | dict[str, int] | Mapping of all item names to their respective ID. |
| location_name_to_id | dict[str, int] | Mapping of all location names to their respective ID. |
| version | int | Version number of this game's data |

### Tags
Tags are represented as a list of strings, the common Client tags follow:

| Name       | Notes                                                                                                                                                                                                              |
|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| AP         | Signifies that this client is a reference client, its usefulness is mostly in debugging to compare client behaviours more easily.                                                                                  |
| DeathLink  | Client participates in the DeathLink mechanic, therefore will send and receive DeathLink bounce packets                                                                                                            |
| Tracker    | Tells the server that this client will not send locations and is actually a Tracker. When specified and used with empty or null `game` in [Connect](#connect), game and game's version validation will be skipped. |
| TextOnly   | Tells the server that this client will not send locations and is intended for chat. When specified and used with empty or null `game` in [Connect](#connect), game and game's version validation will be skipped.  |

### DeathLink
A special kind of Bounce packet that can be supported by any AP game. It targets the tag "DeathLink" and carries the following data:

| Name | Type | Notes |
| ---- | ---- | ---- |
| time | float | Unix Time Stamp of time of death. |
| cause | str | Optional. Text to explain the cause of death, ex. "Berserker was run over by a train." |
| source | str | Name of the player who first died. Can be a slot name, but can also be a name from within a multiplayer game. |
