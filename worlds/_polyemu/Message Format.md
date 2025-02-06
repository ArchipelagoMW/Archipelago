## Message Format

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Message Size|2|The length of the rest of the message.|
|`0x02`|Device ID|1|The ID of the device this message is intended for. Use 0 to indicate the connection broker.|
|`0x03`|Requests|1+|A sequence of requests.|

## Request Format

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Request Type|1|The type of request.|
|`0x01`|Request Body|0+|The body as defined by the request type.|

## Request Types

|Value|Type|Description|
|--|--|--|
|`0x00`|No-op|Does nothing; refreshes connection timeout.|
|`0x01`|Read|Reads data from a specified address and memory domain.|
|`0x02`|Write|Writes data to a specified address and memory domain.|
|`0x03`|Guard|Skips all following requests if some piece of memory does not match expected value.|
|`0x04`|Lock|Halts emulation and processes requests until unlocked.|
|`0x05`|Unock|Resumes emulation (requests in the same chain will still be processed on this frame).|
|`0x06`|Platform|Returns the platform id.|
|`0x07`|Game ID|Returns some identifier for the game. This remains consistent until the game is swapped for another, and is only used to track that the same game is loaded as was during previous requests. It could be a hash of the ROM, but may also be a timestamp representing when the game was first loaded, or any other arbitrary data.|

### [`0x00`] No-op

No body

### [`0x01`] Read

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Domain ID|1|The domain the address corresponds to.|
|`0x01`|Address|8|The address to read.|
|`0x09`|Size|2|The number of bytes to read.|

### [`0x02`] Write

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Domain ID|1|The domain the address corresponds to.|
|`0x01`|Address|8|The address to write to.|
|`0x09`|Data Size|2|The length of the data to be written.|
|`0x0B`|Data|1+|The data to write.|

### [`0x03`] Guard

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Domain ID|1|The domain the address corresponds to.|
|`0x01`|Address|8|The address to check.|
|`0x09`|Data Size|2|The length of the data to be written.|
|`0x0B`|Expected Data|1+|The expected value of the memory at the address.|


## Response Types

|Value|Type|Description|
|--|--|--|
|`0x80`|Acknowledge|No-op request was received.|
|`0x81`|Read|Contai.|
|`0x82`|Write|Writes data to a specified address and memory domain.|
|`0x83`|Guard|Skips all following requests if some piece of memory does not match expected value.|
|`0x84`|Lock|Halts emulation and processes requests until unlocked.|
|`0x85`|Unock|Resumes emulation (requests in the same chain will still be processed on this frame).|
|`0x86`|Platform|Returns the platform id.|
|`0x87`|Game ID|Returns the game id.|
|`0xFF`|Error|Something bad happened.|

### [`0x80`] Acknowledge

No body

### [`0x81`] Read

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Data|1+|The data requested in the read.|

### [`0x82`] Write

No body

### [`0x83`] Guard

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Validated|1|Whether the data validated. 0 if validation failed.|


### [`0xFF`] Error

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Code|1|The type of error.|
|`0x01`|Body Size|2|The size of the body.|
|`0x03`|Body|0+|Contextual information based on the error.|

#### Error Types

|Value|Type|Description|
|--|--|--|
|`0x00`|Device Error|Device returned an error.|
|`0x01`|Invalid Device|Specified device does not exist.|
