# API Guide

Archipelago has a rudimentary API that can be queried by endpoints. The API is a work-in-progress and should be improved over time.

The following API requests are formatted as: `https://<Archipelago URL>/api/<endpoint>`

The returned data will be formated in a combination of JSON lists or dicts, with their keys or values being notated in `blocks` (if applicable)

Current endpoints:
- Datapackage API
    - [`/datapackage`](#datapackage)
    - [`/datapackage/<string:checksum>`](#datapackagestringchecksum)
    - [`/datapackage_checksum`](#datapackagechecksum)
- Generation API
    - [`/generate`](#generate)
    - [`/status/<suuid:seed>`](#status)
- Room API
    - [`/room_status/<suuid:room_id>`](#roomstatus)
- Tracker API
    - [`/tracker/<suuid:tracker>`](#tracker)
    - [`/static_tracker/<suuid:tracker>`](#statictracker)
    - [`/slot_data_tracker/<suuid:tracker>`](#slotdatatracker)
- User API
    - [`/get_rooms`](#getrooms)
    - [`/get_seeds`](#getseeds)


## Datapackage Endpoints
These endpoints are used by applications to acquire a room's datapackage, and validate that they have the correct datapackage for use. Datapackages normally include, item IDs, location IDs, and name groupings, for a given room, and are essential for mapping IDs received from Archipelago to their correct items or locations.

### `/datapackage`
<a name="datapackage"></a>
Fetches the current datapackage from the WebHost.  
You'll receive a dict named `games` that contains a named dict of every game and its data currently supported by Archipelago.  
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

### `/datapackage/<string:checksum>`
<a name="datapackagestringchecksum"></a>
Fetches a single datapackage by checksum.
Returns a dict of the game's data with:
- A checksum `checksum`
- A dict of item groups `item_name_groups`
- Item name to AP ID dict `item_name_to_id`
- A dict of location groups `location_name_groups`
- Location name to AP ID dict `location_name_to_id`

Its format will be identical to the whole-datapackage endpoint (`/datapackage`), except you'll only be returned the single game's data in a dict.

### `/datapackage_checksum`
<a name="datapackagechecksum"></a>
Fetches the checksums of the current static datapackages on the WebHost.
You'll receive a dict with `game:checksum` key-value pairs for all the current officially supported games.  
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
These endpoints are used internally for the WebHost to generate games and validate their generation. They are also used by external applications to generate games automatically.

### `/generate`
<a name="generate"></a>
Submits a game to the WebHost for generation.  
**This endpoint only accepts a POST HTTP request.**  

There are two ways to submit data for generation: With a file and with JSON.

#### With a file:
Have your ZIP of yaml(s) or a single yaml, and submit a POST request to the `/generate` endpoint.  
If the options are valid, you'll be returned a successful generation response. (see [Generation Response](#generation-response))

Example using the python requests library:
```
file = {'file': open('Games.zip', 'rb')}
req = requests.post("https://archipelago.gg/api/generate", files=file)
```

#### With JSON:
Compile your weights/yaml data into a dict. Then insert that into a dict with the key `"weights"`.  
Finally, submit a POST request to the `/generate` endpoint.  
If the weighted options are valid, you'll be returned a successful generation response (see [Generation Response](#generation-response))

Example using the python requests library:
```
data = {"Test":{"game": "Factorio","name": "Test","Factorio": {}},}
weights={"weights": data}
req = requests.post("https://archipelago.gg/api/generate", json=weights)
```

#### Generation Response:
##### Successful Generation:
Upon successful generation, you'll be sent a JSON dict response detailing the generation:
- The UUID of the generation `detail`
- The SUUID of the generation `encoded`
- The response text `text`
- The page that will resolve to the seed/room generation page once generation has completed `url`
- The API status page of the generation `wait_api_url` (see [Status Endpoint](#status))

Example:
```
{
    "detail": "19878f16-5a58-4b76-aab7-d6bf38be9463",
    "encoded": "GYePFlpYS3aqt9a_OL6UYw",
    "text": "Generation of seed 19878f16-5a58-4b76-aab7-d6bf38be9463 started successfully.",
    "url": "http://archipelago.gg/wait/GYePFlpYS3aqt9a_OL6UYw",
    "wait_api_url": "http://archipelago.gg/api/status/GYePFlpYS3aqt9a_OL6UYw"
}
```

##### Failed Generation:

Upon failed generation, you'll be returned a single key-value pair. The key will always be `text`  
The value will give you a hint as to what may have gone wrong.
- Options without tags, and a 400 status code
- Options in a string, and a 400 status code
- Invalid file/weight string, `No options found. Expected file attachment or json weights.` with a 400 status code
- Too many slots for the server to process, `Max size of multiworld exceeded` with a 409 status code

If the generation detects a issue in generation, you'll be sent a dict with two key-value pairs (`text` and `detail`) and a 400 status code. The values will be:
- Summary of issue in `text`
- Detailed issue in `detail`

In the event of an unhandled server exception, you'll be provided a dict with a single key `text`:
- Exception, `Uncought Exception: <error>` with a 500 status code

### `/status/<suuid:seed>`
<a name="status"></a>
Retrieves the status of the seed's generation.  
This endpoint will return a dict with a single key-vlaue pair. The key will always be `text`  
The value will tell you the status of the generation:
- Generation was completed: `Generation done` with a 201 status code
- Generation request was not found: `Generation not found` with a 404 status code
- Generation of the seed failed: `Generation failed` with a 500 status code
- Generation is in progress still: `Generation running` with a 202 status code

## Room Endpoints
Endpoints to fetch information of the active WebHost room with the supplied room_ID.

### `/room_status/<suuid:room_id>`  
<a name="roomstatus"></a>
Will provide a dict of room data with the following keys:
- Tracker SUUID (`tracker`)
- A list of players (`players`)
    - Each item containing a list with the Slot name and Game
- Last known hosted port (`last_port`)
- Last activity timestamp (`last_activity`)
- The room timeout counter (`timeout`)
- A list of downloads for files required for gameplay (`downloads`)
    - Each item is a dict containings the download URL and slot (`slot`, `download`)

Example:
```
{
    "downloads": [
        {
            "download": "/slot_file/kK5fmxd8TfisU5Yp_eg/1",
            "slot": 1
        },
        {
            "download": "/slot_file/kK5fmxd8TfisU5Yp_eg/2",
            "slot": 2
        },
        {
            "download": "/slot_file/kK5fmxd8TfisU5Yp_eg/3",
            "slot": 3
        },
        {
            "download": "/slot_file/kK5fmxd8TfisU5Yp_eg/4",
            "slot": 4
        },
        {
            "download": "/slot_file/kK5fmxd8TfisU5Yp_eg/5",
            "slot": 5
        }
    ],
    "last_activity": "Fri, 18 Apr 2025 20:35:45 GMT",
    "last_port": 52122,
    "players": [
        [
            "Slot_Name_1",
            "Ocarina of Time"
        ],
        [
            "Slot_Name_2",
            "Ocarina of Time"
        ],
        [
            "Slot_Name_3",
            "Ocarina of Time"
        ],
        [
            "Slot_Name_4",
            "Ocarina of Time"
        ],
        [
            "Slot_Name_5",
            "Ocarina of Time"
        ]
    ],
    "timeout": 7200,
    "tracker": "cf6989c0-4703-45d7-a317-2e5158431171"
}
```

## Tracker Endpoints
Endpoints to fetch information regarding players of an active WebHost room with the supplied tracker_ID. The tracker ID
can either be viewed while on a room tracker page, or from the [room's endpoint](#room-endpoints).

### `/tracker/<suuid:tracker>`
<a name=tracker></a>
Will provide a dict of tracker data with the following keys:

- Each player's current alias (`aliases`)
  - Will return the name if there is none
- A list of items each player has received as a NetworkItem (`player_items_received`)
- A list of checks done by each player as a list of the location id's (`player_checks_done`)
- The total number of checks done by all players (`total_checks_done`)
- Hints that players have used or received (`hints`)
- The time of last activity of each player in RFC 1123 format (`activity_timers`)
- The time of last active connection of each player in RFC 1123 format (`connection_timers`)
- The current client status of each player (`player_status`)

Example:
```json
{
  "aliases": [
    {
      "team": 0,
      "player": 1,
      "alias": "Incompetence"
    },
    {
      "team": 0,
      "player": 2,
      "alias": "Slot_Name_2"
    }
  ],
  "player_items_received": [
    {
      "team": 0,
      "player": 1,
      "items": [
        [1, 1, 1, 0],
        [2, 2, 2, 1]
      ]
    },
    {
      "team": 0,
      "player": 2,
      "items": [
        [1, 1, 1, 2],
        [2, 2, 2, 0]
      ]
    }
  ],
  "player_checks_done": [
    {
      "team": 0,
      "player": 1,
      "locations": [
        1,
        2
      ]
    },
    {
      "team": 0,
      "player": 2,
      "locations": [
        1,
        2
      ]
    }
  ],
  "total_checks_done": [
    {
      "team": 0,
      "checks_done": 4
    }
  ],
  "hints": [
    {
      "team": 0,
      "player": 1,
      "hints": [
        [1, 2, 4, 6, 0, "", 4, 0]
      ]
    },
    {
      "team": 0,
      "player": 2,
      "hints": []
    }
  ],
  "activity_timers": [
    {
      "team": 0,
      "player": 1,
      "time": "Fri, 18 Apr 2025 20:35:45 GMT"
    },
    {
      "team": 0,
      "player": 2,
      "time": "Fri, 18 Apr 2025 20:42:46 GMT"
    }
  ],
  "connection_timers": [
    {
      "team": 0,
      "player": 1,
      "time": "Fri, 18 Apr 2025 20:38:25 GMT"
    },
    {
      "team": 0,
      "player": 2,
      "time": "Fri, 18 Apr 2025 21:03:00 GMT"
    }
  ],
  "player_status": [
    {
      "team": 0,
      "player": 1,
      "status": 0
    },
    {
      "team": 0,
      "player": 2,
      "status": 0
    }
  ]
}
```

### `/static_tracker/<suuid:tracker>`
<a name=statictracker></a>
Will provide a dict of static tracker data with the following keys:

- item_link groups and their players (`groups`)
- The datapackage hash for each game (`datapackage`)
  - This hash can then be sent to the datapackage API to receive the appropriate datapackage as necessary
- The number of checks found vs. total checks available per player (`player_locations_total`)
  - Same logic as the multitracker template: found = len(player_checks_done.locations) / total = player_locations_total.total_locations (all available checks).

Example:
```json
{
  "groups": [
    {
      "slot": 5,
      "name": "testGroup",
      "members": [
        1,
        2
      ]
    },
    {
      "slot": 6,
      "name": "myCoolLink",
      "members": [
        3,
        4
      ]
    }
  ],
  "datapackage": {
    "Archipelago": {
      "checksum": "ac9141e9ad0318df2fa27da5f20c50a842afeecb",
    },
    "The Messenger": {
      "checksum": "6991cbcda7316b65bcb072667f3ee4c4cae71c0b",
    }
  },
  "player_locations_total": [
    {
      "player": 1,
      "team" : 0,
      "total_locations": 10
    },
    {
      "player": 2,
      "team" : 0,
      "total_locations": 20
    }
  ],
}
```

### `/slot_data_tracker/<suuid:tracker>`
<a name=slotdatatracker></a>
Will provide a list of each player's slot_data.

Example:
```json
[
  {
    "player": 1,
    "slot_data": {
      "example_option": 1,
      "other_option": 3
    }
  },
  {
    "player": 2,
    "slot_data": {
      "example_option": 1,
      "other_option": 2
    }
  }
]
```

## User Endpoints
User endpoints can get room and seed details from the current session tokens (cookies)

### `/get_rooms`  
<a name="getrooms"></a>
Retreives a list of all rooms currently owned by the session token.  
Each list item will contain a dict with the room's details:
- Room SUUID (`room_id`)
- Seed SUUID (`seed_id`)
- Creation timestamp (`creation_time`)
- Last activity timestamp (`last_activity`)
- Last known AP port (`last_port`)
- Room timeout counter in seconds (`timeout`)
- Room tracker SUUID (`tracker`)

Example:
```
[
    {
        "creation_time": "Fri, 18 Apr 2025 19:46:53 GMT",
        "last_activity": "Fri, 18 Apr 2025 21:16:02 GMT",
        "last_port": 52122,
        "room_id": "90ae5f9b-177c-4df8-ac53-9629fc3bff7a",
        "seed_id": "efbd62c2-aaeb-4dda-88c3-f461c029cef6",
        "timeout": 7200,
        "tracker": "cf6989c0-4703-45d7-a317-2e5158431171"
    },
    {
        "creation_time": "Fri, 18 Apr 2025 20:36:42 GMT",
        "last_activity": "Fri, 18 Apr 2025 20:36:46 GMT",
        "last_port": 56884,
        "room_id": "14465c05-d08e-4d28-96bd-916f994609d8",
        "seed_id": "a528e34c-3b4f-42a9-9f8f-00a4fd40bacb",
        "timeout": 7200,
        "tracker": "4e624bd8-32b6-42e4-9178-aa407f72751c"
    }
]
```

### `/get_seeds`  
<a name="getseeds"></a>
Retreives a list of all seeds currently owned by the session token.  
Each item in the list will contain a dict with the seed's details:
- Seed SUUID (`seed_id`)
- Creation timestamp (`creation_time`)
- A list of player slots (`players`)
    - Each item in the list will contain a list of the slot name and game

Example:
```
[
    {
        "creation_time": "Fri, 18 Apr 2025 19:46:52 GMT",
        "players": [
            [
                "Slot_Name_1",
                "Ocarina of Time"
            ],
            [
                "Slot_Name_2",
                "Ocarina of Time"
            ],
            [
                "Slot_Name_3",
                "Ocarina of Time"
            ],
            [
                "Slot_Name_4",
                "Ocarina of Time"
            ],
            [
                "Slot_Name_5",
                "Ocarina of Time"
            ]
        ],
        "seed_id": "efbd62c2-aaeb-4dda-88c3-f461c029cef6"
    },
    {
        "creation_time": "Fri, 18 Apr 2025 20:36:39 GMT",
        "players": [
            [
                "Slot_Name_1",
                "Clique"
            ],
            [
                "Slot_Name_2",
                "Clique"
            ],
            [
                "Slot_Name_3",
                "Clique"
            ],
            [
                "Slot_Name_4",
                "Archipelago"
            ]
        ],
        "seed_id": "a528e34c-3b4f-42a9-9f8f-00a4fd40bacb"
    }
]
```