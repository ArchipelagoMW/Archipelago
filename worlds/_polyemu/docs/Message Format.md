# Message Format

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Message Size|2|The length of the rest of the message.|
|`0x02`|Request/Response Chain|1+|Either a request chain or response chain|

## Request Chain Format

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Device ID|8|The ID of the device this message is intended for. If this ID does not match the device's understanding of its own ID, it will send back an error. If set to `0x0000000000000000`, the device processing the request will not perform this check. Ideally, this ID is unique per running game. This value is used by connection brokers to route requests.|
|`0x08`|Requests|1+|A sequence of requests.|

### Request Format

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Request Type|1|The type of request.|
|`0x01`|Request Body|0+|The body as defined by the request type.|

### Request Types

|Value|Type|Description|
|--|--|--|
|`0x00`|No-op|Does nothing; refreshes connection timeout.|
|`0x01`|Supported Operations|Lists request types that the device is capable of fulfilling.|
|`0x02`|Platform|Returns the platform id.|
|`0x03`|Memory Size|Returns the size of each memory domain supported by the device. Unsupported domains are omitted.|
|`0x04`|List Devices|Lists devices by ID.|
|`0x10`|Read|Reads data from a specified address and memory domain.|
|`0x11`|Write|Writes data to a specified address and memory domain.|
|`0x12`|Guard|Skips all following requests in the chain if some piece of memory does not match expected value.|
|`0x20`|Lock|Halts emulation and processes requests until unlocked.|
|`0x21`|Unlock|Resumes emulation (requests in the same chain will still be processed on this frame).|

#### [`0x00`] No-op

No body

#### [`0x01`] Supported Operations

No body

#### [`0x02`] Platform

No Body

#### [`0x04`] List Devices

No Body

#### [`0x10`] Read

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Domain ID|1|The domain the address corresponds to.|
|`0x01`|Address|8|The address to read.|
|`0x09`|Size|2|The number of bytes to read.|

#### [`0x11`] Write

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Domain ID|1|The domain the address corresponds to.|
|`0x01`|Address|8|The address to write to.|
|`0x09`|Data Size|2|The length of the data to be written.|
|`0x0B`|Data|1+|The data to write.|

#### [`0x12`] Guard

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Domain ID|1|The domain the address corresponds to.|
|`0x01`|Address|8|The address to check.|
|`0x09`|Data Size|2|The length of the data to be written.|
|`0x0B`|Expected Data|1+|The expected value of the memory at the address.|

#### [`0x20`] Lock

No Body

#### [`0x21`] Unlock

No Body

#### [`0x22`] Display Message

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Text Size|2|The length of the text to be displayed.|
|`0x02`|Text|0+|The text (utf-8 encoded).|

## Response Chain Format

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x02`|Responses|1+|A sequence of responses.|

### Response Types

|Value|Type|Description|
|--|--|--|
|`0x80`|No-op|Acknowledges a no-op request.|
|`0x81`|Supported Operations|The list of supported request types.|
|`0x82`|Platform|Contains the platform id.|
|`0x83`|Memory Size|Contains a sequence of domains and their sizes.|
|`0x84`|List Devices|Contains a list of device ids.|
|`0x90`|Read|Contains data read from memory.|
|`0x91`|Write|Acknowledges a write request|
|`0x92`|Guard|Indicates the success of a guard request. Requests whose responses follow a failed guard will receive this response type to indicate that they were not fulfilled as a result of that guard's failure.|
|`0xA0`|Lock|Acknowledges a lock request.|
|`0xA1`|Unlock|Acknowledges an unlock request.|
|`0xFF`|Error|Something bad happened.|

#### [`0x80`] No-op

No body

#### [`0x81`] Supported Operations

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Number of Entries|1|The number of operations in the following list.|
|`0x01`|Operation List|1+|A list of request types the device is capable of fulfilling (1-byte each).|

#### [`0x82`] Platform

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Platform ID|1|The ID of the platform the emulator is emulating.|

#### [`0x83`] Memory Size

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Number of Entries|1|The number of memory domains listed in the response.|
|`0x01`|Sizes|*|A list of memory size entries.|

##### Memory Size Entry

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Domain ID|1|Which domain this entry refers to.|
|`0x01`|Size|8|The size of the memory domain.|

#### [`0x84`] List Devices

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Number of Devices|1|The number of device ids in the following list.|
|`0x01`|Device IDs|*|A list of device ids (8-bytes each).|

#### [`0x90`] Read

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Data Size|2|The size of the data.|
|`0x02`|Data|1+|The data requested in the read.|

#### [`0x91`] Write

No body

#### [`0x92`] Guard

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Validated|1|Whether the data validated. 0 if validation failed.|

#### [`0xA0`] Lock

No Body

#### [`0xA1`] Unlock

No Body

#### [`0xA2`] Display Message

No Body

#### [`0xFF`] Error

|Offset|Field Name|Size|Description|
|--|--|--|--|
|`0x00`|Code|1|The type of error.|
|`0x01`|Body Size|2|The size of the body.|
|`0x03`|Body|0+|Contextual information based on the error.|

##### Error Types

|Value|Type|Description|
|--|--|--|
|`0x00`|Device Error|Device returned a device-specific or unknown error.|
|`0x01`|Unsupported Operation|The device does not support the request.|
|`0x02`|Mismatched Device|The device received the request chain, but the specified device ID did not match what the device believes its ID to be.|
|`0x80`|No Such Device|Specified device does not exist.|
|`0x81`|Device Closed Connection|The connection to the device was lost before any response was received.|
