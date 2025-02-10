## Message Format

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Message Size|2|The length of the rest of the message.|
|`0x02`|Device ID|8|The ID of the device this message is intended for.|
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
|`0x01`|Supported Operations|Lists requests that the device is capable of fulfilling.|
|`0x02`|Platform|Returns the platform id.|
|`0x03`|Memory Size|Returns the sizes of each memory domain.|
|`0x04`|List Devices|TODO fix Returns some identifier for the device based on the running game. This remains consistent until the game is swapped for another, and is only used to track that the same game is loaded as was during previous requests. It could be a hash of the ROM, but may also be a timestamp representing when the game was first loaded, or any other arbitrary data.|
|`0x10`|Read|Reads data from a specified address and memory domain.|
|`0x11`|Write|Writes data to a specified address and memory domain.|
|`0x12`|Guard|Skips all following requests if some piece of memory does not match expected value.|
|`0x20`|Lock|Halts emulation and processes requests until unlocked.|
|`0x21`|Unlock|Resumes emulation (requests in the same chain will still be processed on this frame).|

### [`0x00`] No-op

No body

### [`0x01`] Supported Operations

No body

### [`0x02`] Platform

No Body

### [`0x04`] List Devices

No Body

### [`0x10`] Read

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Domain ID|1|The domain the address corresponds to.|
|`0x01`|Address|8|The address to read.|
|`0x09`|Size|2|The number of bytes to read.|

### [`0x11`] Write

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Domain ID|1|The domain the address corresponds to.|
|`0x01`|Address|8|The address to write to.|
|`0x09`|Data Size|2|The length of the data to be written.|
|`0x0B`|Data|1+|The data to write.|

### [`0x12`] Guard

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Domain ID|1|The domain the address corresponds to.|
|`0x01`|Address|8|The address to check.|
|`0x09`|Data Size|2|The length of the data to be written.|
|`0x0B`|Expected Data|1+|The expected value of the memory at the address.|

### [`0x20`] Lock

No Body

### [`0x21`] Unlock

No Body

### [`0x22`] Display Message

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Message Size|2|The length of the text to be displayed.|
|`0x02`|Text|0+|The text (utf-8 encoded).|

## Response Types

|Value|Type|Description|
|--|--|--|
|`0x80`|Acknowledge|No-op request was received.|
|`0x82`|Platform|Returns the platform id.|
|`0x83`|Memory Size|Returns the platform id.|
|`0x84`|List Devices|Contains the List Devices.|
|`0x90`|Read|Contai.|
|`0x91`|Write|Writes data to a specified address and memory domain.|
|`0x92`|Guard|Skips all following requests if some piece of memory does not match expected value.|
|`0xA0`|Lock|Halts emulation and processes requests until unlocked.|
|`0xA1`|Unlock|Resumes emulation (requests in the same chain will still be processed on this frame).|
|`0xFF`|Error|Something bad happened.|

### [`0x80`] Acknowledge

No body

### [`0x81`] Supported Operations

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Number of Entries|1|The number of operations in the following list.|
|`0x01`|Operation List|1+|A list of request types the device is capable of fulfilling (1-byte each).|

### [`0x82`] Platform

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Platform ID|1|The ID of the platform the emulator is emulating.|

### [`0x83`] Memory Size

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Number of Entries|1|The number of memory domains listed in the response.|
|`0x01`|Sizes|*|A list of memory size entries.|

#### Memory Size Entry

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Domain ID|1|Which domain this entry refers to.|
|`0x01`|Size|8|The size of the memory domain.|

### [`0x84`] List Devices

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Number of Devices|1|The number of device ids in the following list.|
|`0x01`|Device IDs|*|An 8-byte device id per device.|

### [`0x90`] Read

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Data Size|2|The size of the data.|
|`0x02`|Data|1+|The data requested in the read.|

### [`0x91`] Write

No body

### [`0x92`] Guard

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Validated|1|Whether the data validated. 0 if validation failed.|

### [`0xA0`] Lock

No Body

### [`0xA1`] Unlock

No Body

### [`0xA2`] Display Message

No Body

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
