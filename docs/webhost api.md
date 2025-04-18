# API Guide

Archipelago has a rudementary API that is able to be queried by endpoints.
The API is a work-in-progress and should be improved over time.

All API requests will be formatted as: `https://<Archipelago URL>/api/<endpoint>`

## Datapackage Endpoints
These endpoints are used by applications to aquire and validate they have a current datapackage for item and location IDs.

`/datapackage`  
Fetches the current datapackage from the WebHost.

`/datapackage/<string:checksum>`    
Fetches datapackage by checksum.

`/datapackage_checksum`  
Fetches checksum of current datapackage.

## Generation Endpoint
These endpoints are used internaly for the WebHost to generate games, and validate their generation.

`(POST)` `/generate`  
Submits a game to the WebHost for generation.

`/status/<suuid:seed>`  
Retreives the status of the seed's generation.

## Room Endpoints
Endpoints to fetch information of the active WebHost room with the supplied room_ID.

`/room_status/<suuid:room_id>`  
Retrieves:
- Tracker UUID (`tracker`)
- Player List (Slot name, and Game) (`players`)
- Last known hosted port (`last_port`)
- Last activity timestamp (`last_activity`)
- Timeout counter (`timeout`)
- Downloads for files required for gameplay (`downloads`)

`/room_received_items/<suuid:room_id>`  
Retreives all items received by players in the current room.  
Fetches an array of objects formatted as:
- Receiving Slot ID (`slot`)
- Items (`items`)
  - `0`: Item ID
  - `1`: Location ID
  - `2`: Sending Slot ID
  - `3`: Item Flags

## User Endpoints
User endpoints can get room and seed details from the current session tokens (cookies)

`/get_rooms`  
Retreives all rooms currently owned by the session token.  
Each room will have:
- Room ID (`room_ID`)
- Seed ID (`seed_id`)
- Creation Timestamp (`creation_time`)
- Last activity timestamp (`last_activity`)
- Last known AP Port (`last_port`)
- Room tiumeout counter (`timeout`)
- Room tracker UUID (`tracker`)

`/get_seeds`  
Retreives all seeds currently owned by the session token.  
Each seed will have:
- Seed ID (`seed_id`)
- Creation timestamp (`creation_time`)
- Player Slots (`players`)


