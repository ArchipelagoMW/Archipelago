# Archipelago Network Protocol v2.0
The v2.0 protocol is an almost carbon copy of the v1.0 protocol with the exception of a new handshake and one new packet. The v1.0 protocol can be found as [network protocol.md](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/network%20protocol.md) in the same directory.

## WebSocket Connection Handshake
The handshake is slightly extended to accomodate multiple protocols by requiring the client to set `Sec-WebSocket-Protocol` to include `v2.0`. The server should not reply with a `RoomInfo` packet until the client sends a `Join` packet. If the `Join` packet is valid, the Server is expected to reply with a `RoomInfo` packet. If the `Join` packet is invalid, the server is expected to close the connection with no further information provided.

## Packets

### Join
Sent by the client to signal that they wish to join a room. This packet becomes [illegal](#Terminology) once the client has joined a Room.

#### Arguments
| Name | Type | Notes |
|------|------|-------|
| id   | str  | The rooms identifier which the client wishes to join. |

#### Handling
The server should verify that `id` matches an existing running room or optionally a room that needs to be loaded. If it does match a room the server must reply with a `RoomInfo` packet after which the v1.0 protocol takes over entirely.

- *Recommendation:* The room identifiers should be case-insensitive and avoid easily confusable symbols. A short identifier system similar to what is seen in party games (4-8 letters and numbers) may be ideal.
- *Note:* The server implementation is free to either refuse the connection if the room is currently "closed"/"stopped" or to "open"/"start" the room with this request by a client. 
- *Note:* The server implementation is free to assign new room identifiers in the case the recommended short identifier system is implemented. 

## Terminology
- `illegal` (packet): An illegal packet should result in the connection being closed in strict compliance mode or simply ignored if this protocol compliance is not requested.
