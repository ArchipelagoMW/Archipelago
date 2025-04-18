# API Guide

Archipelago has a rudimentary API that can be queried by endpoints.
The API is a work-in-progress and should be improved over time.

The following API requests are formatted as: `https://<Archipelago URL>/api/<endpoint>`

## Datapackage Endpoints
These endpoints are used by applications to acquire and validate that they have a current datapackage for game data.   
Such as item and location IDs, or name groupings.

`/datapackage`  
Fetches the current datapackage from the WebHost.  
You'll receive an dict named `games` that contain a named dict of every game and its data currently supported by Archipelago.  
Each game will have:
- A checksum `checksum`
- A dict of item groups `item_name_groups`
- Item name to AP ID dict `item_name_to_id`
- A dict of location groups `location_name_groups`
- Location name to AP ID dict `location_name_to_id`

Example:
```
{
    "games": {
        ...
        "Clique": {
            "checksum": "0271f7a80b44ba72187f92815c2bc8669cb464c7",
            "item_name_groups": {
                "Everything": [
                    "A Cool Filler Item (No Satisfaction Guaranteed)",
                    "Button Activation",
                    "Feeling of Satisfaction"
                ]
            },
            "item_name_to_id": {
                "A Cool Filler Item (No Satisfaction Guaranteed)": 69696967,
                "Button Activation": 69696968,
                "Feeling of Satisfaction": 69696969
            },
            "location_name_groups": {
                "Everywhere": [
                    "The Big Red Button",
                    "The Item on the Desk"
                ]
            },
            "location_name_to_id": {
                "The Big Red Button": 69696969,
                "The Item on the Desk": 69696968
            }
        },
        ...
    }
}
```

`/datapackage/<string:checksum>`    
Fetches datapackage by checksum.

`/datapackage_checksum`  
Fetches the checksums of the current static datapackages on the WebHost.
You'll receive a dict with `game:checksum` key-pairs for all the current officially supported games.
Example:
```
{
...
"Donkey Kong Country 3":"f90acedcd958213f483a6a4c238e2a3faf92165e",
"Factorio":"a699194a9589db3ebc0d821915864b422c782f44",
...
}
```


## Generation Endpoint
These endpoints are used internally for the WebHost to generate games and validate their generation, and also used by external applications to generate games automatically.

`(POST)` `/generate`  
Submits a game to the WebHost for generation.

`/status/<suuid:seed>`  
Retreives the status of the seed's generation.

## Room Endpoints
Endpoints to fetch information of the active WebHost room with the supplied room_ID.

`/room_status/<suuid:room_id>`  
Retrieves:
- Tracker UUID (`tracker`)
- Player list (Slot name, and Game) (`players`)
- Last known hosted port (`last_port`)
- Last activity timestamp (`last_activity`)
- Timeout counter (`timeout`)
- Downloads for files required for gameplay (`downloads`)

## User Endpoints
User endpoints can get room and seed details from the current session tokens (cookies)

`/get_rooms`  
Retreives all rooms currently owned by the session token.  
Each room will have:
- Room ID (`room_id`)
- Seed ID (`seed_id`)
- Creation timestamp (`creation_time`)
- Last activity timestamp (`last_activity`)
- Last known AP port (`last_port`)
- Room tiumeout counter (`timeout`)
- Room tracker UUID (`tracker`)

`/get_seeds`  
Retreives all seeds currently owned by the session token.  
Each seed will have:
- Seed ID (`seed_id`)
- Creation timestamp (`creation_time`)
- Player slots (`players`)

