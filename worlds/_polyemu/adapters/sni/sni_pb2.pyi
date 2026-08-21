from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AddressSpace(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FxPakPro: _ClassVar[AddressSpace]
    SnesABus: _ClassVar[AddressSpace]
    Raw: _ClassVar[AddressSpace]

class MemoryMapping(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Unknown: _ClassVar[MemoryMapping]
    HiROM: _ClassVar[MemoryMapping]
    LoROM: _ClassVar[MemoryMapping]
    ExHiROM: _ClassVar[MemoryMapping]
    SA1: _ClassVar[MemoryMapping]

class DeviceCapability(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    None: _ClassVar[DeviceCapability]
    ReadMemory: _ClassVar[DeviceCapability]
    WriteMemory: _ClassVar[DeviceCapability]
    ExecuteASM: _ClassVar[DeviceCapability]
    ResetSystem: _ClassVar[DeviceCapability]
    PauseUnpauseEmulation: _ClassVar[DeviceCapability]
    PauseToggleEmulation: _ClassVar[DeviceCapability]
    ResetToMenu: _ClassVar[DeviceCapability]
    FetchFields: _ClassVar[DeviceCapability]
    ReadDirectory: _ClassVar[DeviceCapability]
    MakeDirectory: _ClassVar[DeviceCapability]
    RemoveFile: _ClassVar[DeviceCapability]
    RenameFile: _ClassVar[DeviceCapability]
    PutFile: _ClassVar[DeviceCapability]
    GetFile: _ClassVar[DeviceCapability]
    BootFile: _ClassVar[DeviceCapability]
    NWACommand: _ClassVar[DeviceCapability]

class Field(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DeviceName: _ClassVar[Field]
    DeviceVersion: _ClassVar[Field]
    DeviceStatus: _ClassVar[Field]
    CoreName: _ClassVar[Field]
    CoreVersion: _ClassVar[Field]
    CorePlatform: _ClassVar[Field]
    RomFileName: _ClassVar[Field]
    RomHashType: _ClassVar[Field]
    RomHashValue: _ClassVar[Field]

class DirEntryType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Directory: _ClassVar[DirEntryType]
    File: _ClassVar[DirEntryType]
FxPakPro: AddressSpace
SnesABus: AddressSpace
Raw: AddressSpace
Unknown: MemoryMapping
HiROM: MemoryMapping
LoROM: MemoryMapping
ExHiROM: MemoryMapping
SA1: MemoryMapping
None: DeviceCapability
ReadMemory: DeviceCapability
WriteMemory: DeviceCapability
ExecuteASM: DeviceCapability
ResetSystem: DeviceCapability
PauseUnpauseEmulation: DeviceCapability
PauseToggleEmulation: DeviceCapability
ResetToMenu: DeviceCapability
FetchFields: DeviceCapability
ReadDirectory: DeviceCapability
MakeDirectory: DeviceCapability
RemoveFile: DeviceCapability
RenameFile: DeviceCapability
PutFile: DeviceCapability
GetFile: DeviceCapability
BootFile: DeviceCapability
NWACommand: DeviceCapability
DeviceName: Field
DeviceVersion: Field
DeviceStatus: Field
CoreName: Field
CoreVersion: Field
CorePlatform: Field
RomFileName: Field
RomHashType: Field
RomHashValue: Field
Directory: DirEntryType
File: DirEntryType

class DevicesRequest(_message.Message):
    __slots__ = ("kinds",)
    KINDS_FIELD_NUMBER: _ClassVar[int]
    kinds: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, kinds: _Optional[_Iterable[str]] = ...) -> None: ...

class DevicesResponse(_message.Message):
    __slots__ = ("devices",)
    class Device(_message.Message):
        __slots__ = ("uri", "displayName", "kind", "capabilities", "defaultAddressSpace", "system")
        URI_FIELD_NUMBER: _ClassVar[int]
        DISPLAYNAME_FIELD_NUMBER: _ClassVar[int]
        KIND_FIELD_NUMBER: _ClassVar[int]
        CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
        DEFAULTADDRESSSPACE_FIELD_NUMBER: _ClassVar[int]
        SYSTEM_FIELD_NUMBER: _ClassVar[int]
        uri: str
        displayName: str
        kind: str
        capabilities: _containers.RepeatedScalarFieldContainer[DeviceCapability]
        defaultAddressSpace: AddressSpace
        system: str
        def __init__(self, uri: _Optional[str] = ..., displayName: _Optional[str] = ..., kind: _Optional[str] = ..., capabilities: _Optional[_Iterable[_Union[DeviceCapability, str]]] = ..., defaultAddressSpace: _Optional[_Union[AddressSpace, str]] = ..., system: _Optional[str] = ...) -> None: ...
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    devices: _containers.RepeatedCompositeFieldContainer[DevicesResponse.Device]
    def __init__(self, devices: _Optional[_Iterable[_Union[DevicesResponse.Device, _Mapping]]] = ...) -> None: ...

class ResetSystemRequest(_message.Message):
    __slots__ = ("uri",)
    URI_FIELD_NUMBER: _ClassVar[int]
    uri: str
    def __init__(self, uri: _Optional[str] = ...) -> None: ...

class ResetSystemResponse(_message.Message):
    __slots__ = ("uri",)
    URI_FIELD_NUMBER: _ClassVar[int]
    uri: str
    def __init__(self, uri: _Optional[str] = ...) -> None: ...

class ResetToMenuRequest(_message.Message):
    __slots__ = ("uri",)
    URI_FIELD_NUMBER: _ClassVar[int]
    uri: str
    def __init__(self, uri: _Optional[str] = ...) -> None: ...

class ResetToMenuResponse(_message.Message):
    __slots__ = ("uri",)
    URI_FIELD_NUMBER: _ClassVar[int]
    uri: str
    def __init__(self, uri: _Optional[str] = ...) -> None: ...

class PauseEmulationRequest(_message.Message):
    __slots__ = ("uri", "paused")
    URI_FIELD_NUMBER: _ClassVar[int]
    PAUSED_FIELD_NUMBER: _ClassVar[int]
    uri: str
    paused: bool
    def __init__(self, uri: _Optional[str] = ..., paused: bool = ...) -> None: ...

class PauseEmulationResponse(_message.Message):
    __slots__ = ("uri", "paused")
    URI_FIELD_NUMBER: _ClassVar[int]
    PAUSED_FIELD_NUMBER: _ClassVar[int]
    uri: str
    paused: bool
    def __init__(self, uri: _Optional[str] = ..., paused: bool = ...) -> None: ...

class PauseToggleEmulationRequest(_message.Message):
    __slots__ = ("uri",)
    URI_FIELD_NUMBER: _ClassVar[int]
    uri: str
    def __init__(self, uri: _Optional[str] = ...) -> None: ...

class PauseToggleEmulationResponse(_message.Message):
    __slots__ = ("uri",)
    URI_FIELD_NUMBER: _ClassVar[int]
    uri: str
    def __init__(self, uri: _Optional[str] = ...) -> None: ...

class DetectMemoryMappingRequest(_message.Message):
    __slots__ = ("uri", "fallbackMemoryMapping", "romHeader00FFB0")
    URI_FIELD_NUMBER: _ClassVar[int]
    FALLBACKMEMORYMAPPING_FIELD_NUMBER: _ClassVar[int]
    ROMHEADER00FFB0_FIELD_NUMBER: _ClassVar[int]
    uri: str
    fallbackMemoryMapping: MemoryMapping
    romHeader00FFB0: bytes
    def __init__(self, uri: _Optional[str] = ..., fallbackMemoryMapping: _Optional[_Union[MemoryMapping, str]] = ..., romHeader00FFB0: _Optional[bytes] = ...) -> None: ...

class DetectMemoryMappingResponse(_message.Message):
    __slots__ = ("uri", "memoryMapping", "confidence", "romHeader00FFB0")
    URI_FIELD_NUMBER: _ClassVar[int]
    MEMORYMAPPING_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    ROMHEADER00FFB0_FIELD_NUMBER: _ClassVar[int]
    uri: str
    memoryMapping: MemoryMapping
    confidence: bool
    romHeader00FFB0: bytes
    def __init__(self, uri: _Optional[str] = ..., memoryMapping: _Optional[_Union[MemoryMapping, str]] = ..., confidence: bool = ..., romHeader00FFB0: _Optional[bytes] = ...) -> None: ...

class ReadMemoryRequest(_message.Message):
    __slots__ = ("requestAddress", "requestAddressSpace", "requestMemoryMapping", "size")
    REQUESTADDRESS_FIELD_NUMBER: _ClassVar[int]
    REQUESTADDRESSSPACE_FIELD_NUMBER: _ClassVar[int]
    REQUESTMEMORYMAPPING_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    requestAddress: int
    requestAddressSpace: AddressSpace
    requestMemoryMapping: MemoryMapping
    size: int
    def __init__(self, requestAddress: _Optional[int] = ..., requestAddressSpace: _Optional[_Union[AddressSpace, str]] = ..., requestMemoryMapping: _Optional[_Union[MemoryMapping, str]] = ..., size: _Optional[int] = ...) -> None: ...

class ReadMemoryResponse(_message.Message):
    __slots__ = ("requestAddress", "requestAddressSpace", "requestMemoryMapping", "deviceAddress", "deviceAddressSpace", "data")
    REQUESTADDRESS_FIELD_NUMBER: _ClassVar[int]
    REQUESTADDRESSSPACE_FIELD_NUMBER: _ClassVar[int]
    REQUESTMEMORYMAPPING_FIELD_NUMBER: _ClassVar[int]
    DEVICEADDRESS_FIELD_NUMBER: _ClassVar[int]
    DEVICEADDRESSSPACE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    requestAddress: int
    requestAddressSpace: AddressSpace
    requestMemoryMapping: MemoryMapping
    deviceAddress: int
    deviceAddressSpace: AddressSpace
    data: bytes
    def __init__(self, requestAddress: _Optional[int] = ..., requestAddressSpace: _Optional[_Union[AddressSpace, str]] = ..., requestMemoryMapping: _Optional[_Union[MemoryMapping, str]] = ..., deviceAddress: _Optional[int] = ..., deviceAddressSpace: _Optional[_Union[AddressSpace, str]] = ..., data: _Optional[bytes] = ...) -> None: ...

class WriteMemoryRequest(_message.Message):
    __slots__ = ("requestAddress", "requestAddressSpace", "requestMemoryMapping", "data")
    REQUESTADDRESS_FIELD_NUMBER: _ClassVar[int]
    REQUESTADDRESSSPACE_FIELD_NUMBER: _ClassVar[int]
    REQUESTMEMORYMAPPING_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    requestAddress: int
    requestAddressSpace: AddressSpace
    requestMemoryMapping: MemoryMapping
    data: bytes
    def __init__(self, requestAddress: _Optional[int] = ..., requestAddressSpace: _Optional[_Union[AddressSpace, str]] = ..., requestMemoryMapping: _Optional[_Union[MemoryMapping, str]] = ..., data: _Optional[bytes] = ...) -> None: ...

class WriteMemoryResponse(_message.Message):
    __slots__ = ("requestAddress", "requestAddressSpace", "requestMemoryMapping", "deviceAddress", "deviceAddressSpace", "size")
    REQUESTADDRESS_FIELD_NUMBER: _ClassVar[int]
    REQUESTADDRESSSPACE_FIELD_NUMBER: _ClassVar[int]
    REQUESTMEMORYMAPPING_FIELD_NUMBER: _ClassVar[int]
    DEVICEADDRESS_FIELD_NUMBER: _ClassVar[int]
    DEVICEADDRESSSPACE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    requestAddress: int
    requestAddressSpace: AddressSpace
    requestMemoryMapping: MemoryMapping
    deviceAddress: int
    deviceAddressSpace: AddressSpace
    size: int
    def __init__(self, requestAddress: _Optional[int] = ..., requestAddressSpace: _Optional[_Union[AddressSpace, str]] = ..., requestMemoryMapping: _Optional[_Union[MemoryMapping, str]] = ..., deviceAddress: _Optional[int] = ..., deviceAddressSpace: _Optional[_Union[AddressSpace, str]] = ..., size: _Optional[int] = ...) -> None: ...

class SingleReadMemoryRequest(_message.Message):
    __slots__ = ("uri", "request")
    URI_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    uri: str
    request: ReadMemoryRequest
    def __init__(self, uri: _Optional[str] = ..., request: _Optional[_Union[ReadMemoryRequest, _Mapping]] = ...) -> None: ...

class SingleReadMemoryResponse(_message.Message):
    __slots__ = ("uri", "response")
    URI_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    uri: str
    response: ReadMemoryResponse
    def __init__(self, uri: _Optional[str] = ..., response: _Optional[_Union[ReadMemoryResponse, _Mapping]] = ...) -> None: ...

class SingleWriteMemoryRequest(_message.Message):
    __slots__ = ("uri", "request")
    URI_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    uri: str
    request: WriteMemoryRequest
    def __init__(self, uri: _Optional[str] = ..., request: _Optional[_Union[WriteMemoryRequest, _Mapping]] = ...) -> None: ...

class SingleWriteMemoryResponse(_message.Message):
    __slots__ = ("uri", "response")
    URI_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    uri: str
    response: WriteMemoryResponse
    def __init__(self, uri: _Optional[str] = ..., response: _Optional[_Union[WriteMemoryResponse, _Mapping]] = ...) -> None: ...

class MultiReadMemoryRequest(_message.Message):
    __slots__ = ("uri", "requests")
    URI_FIELD_NUMBER: _ClassVar[int]
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    uri: str
    requests: _containers.RepeatedCompositeFieldContainer[ReadMemoryRequest]
    def __init__(self, uri: _Optional[str] = ..., requests: _Optional[_Iterable[_Union[ReadMemoryRequest, _Mapping]]] = ...) -> None: ...

class MultiReadMemoryResponse(_message.Message):
    __slots__ = ("uri", "responses")
    URI_FIELD_NUMBER: _ClassVar[int]
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    uri: str
    responses: _containers.RepeatedCompositeFieldContainer[ReadMemoryResponse]
    def __init__(self, uri: _Optional[str] = ..., responses: _Optional[_Iterable[_Union[ReadMemoryResponse, _Mapping]]] = ...) -> None: ...

class MultiWriteMemoryRequest(_message.Message):
    __slots__ = ("uri", "requests")
    URI_FIELD_NUMBER: _ClassVar[int]
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    uri: str
    requests: _containers.RepeatedCompositeFieldContainer[WriteMemoryRequest]
    def __init__(self, uri: _Optional[str] = ..., requests: _Optional[_Iterable[_Union[WriteMemoryRequest, _Mapping]]] = ...) -> None: ...

class MultiWriteMemoryResponse(_message.Message):
    __slots__ = ("uri", "responses")
    URI_FIELD_NUMBER: _ClassVar[int]
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    uri: str
    responses: _containers.RepeatedCompositeFieldContainer[WriteMemoryResponse]
    def __init__(self, uri: _Optional[str] = ..., responses: _Optional[_Iterable[_Union[WriteMemoryResponse, _Mapping]]] = ...) -> None: ...

class ReadDirectoryRequest(_message.Message):
    __slots__ = ("uri", "path")
    URI_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    uri: str
    path: str
    def __init__(self, uri: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class DirEntry(_message.Message):
    __slots__ = ("name", "type")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: DirEntryType
    def __init__(self, name: _Optional[str] = ..., type: _Optional[_Union[DirEntryType, str]] = ...) -> None: ...

class ReadDirectoryResponse(_message.Message):
    __slots__ = ("uri", "path", "entries")
    URI_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    uri: str
    path: str
    entries: _containers.RepeatedCompositeFieldContainer[DirEntry]
    def __init__(self, uri: _Optional[str] = ..., path: _Optional[str] = ..., entries: _Optional[_Iterable[_Union[DirEntry, _Mapping]]] = ...) -> None: ...

class MakeDirectoryRequest(_message.Message):
    __slots__ = ("uri", "path")
    URI_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    uri: str
    path: str
    def __init__(self, uri: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class MakeDirectoryResponse(_message.Message):
    __slots__ = ("uri", "path")
    URI_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    uri: str
    path: str
    def __init__(self, uri: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class RemoveFileRequest(_message.Message):
    __slots__ = ("uri", "path")
    URI_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    uri: str
    path: str
    def __init__(self, uri: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class RemoveFileResponse(_message.Message):
    __slots__ = ("uri", "path")
    URI_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    uri: str
    path: str
    def __init__(self, uri: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class RenameFileRequest(_message.Message):
    __slots__ = ("uri", "path", "newFilename")
    URI_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    NEWFILENAME_FIELD_NUMBER: _ClassVar[int]
    uri: str
    path: str
    newFilename: str
    def __init__(self, uri: _Optional[str] = ..., path: _Optional[str] = ..., newFilename: _Optional[str] = ...) -> None: ...

class RenameFileResponse(_message.Message):
    __slots__ = ("uri", "path", "newFilename")
    URI_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    NEWFILENAME_FIELD_NUMBER: _ClassVar[int]
    uri: str
    path: str
    newFilename: str
    def __init__(self, uri: _Optional[str] = ..., path: _Optional[str] = ..., newFilename: _Optional[str] = ...) -> None: ...

class PutFileRequest(_message.Message):
    __slots__ = ("uri", "path", "data")
    URI_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    uri: str
    path: str
    data: bytes
    def __init__(self, uri: _Optional[str] = ..., path: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class PutFileResponse(_message.Message):
    __slots__ = ("uri", "path", "size")
    URI_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    uri: str
    path: str
    size: int
    def __init__(self, uri: _Optional[str] = ..., path: _Optional[str] = ..., size: _Optional[int] = ...) -> None: ...

class GetFileRequest(_message.Message):
    __slots__ = ("uri", "path")
    URI_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    uri: str
    path: str
    def __init__(self, uri: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class GetFileResponse(_message.Message):
    __slots__ = ("uri", "path", "size", "data")
    URI_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    uri: str
    path: str
    size: int
    data: bytes
    def __init__(self, uri: _Optional[str] = ..., path: _Optional[str] = ..., size: _Optional[int] = ..., data: _Optional[bytes] = ...) -> None: ...

class BootFileRequest(_message.Message):
    __slots__ = ("uri", "path")
    URI_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    uri: str
    path: str
    def __init__(self, uri: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class BootFileResponse(_message.Message):
    __slots__ = ("uri", "path")
    URI_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    uri: str
    path: str
    def __init__(self, uri: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class FieldsRequest(_message.Message):
    __slots__ = ("uri", "fields")
    URI_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    uri: str
    fields: _containers.RepeatedScalarFieldContainer[Field]
    def __init__(self, uri: _Optional[str] = ..., fields: _Optional[_Iterable[_Union[Field, str]]] = ...) -> None: ...

class FieldsResponse(_message.Message):
    __slots__ = ("uri", "fields", "values")
    URI_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    uri: str
    fields: _containers.RepeatedScalarFieldContainer[Field]
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, uri: _Optional[str] = ..., fields: _Optional[_Iterable[_Union[Field, str]]] = ..., values: _Optional[_Iterable[str]] = ...) -> None: ...

class NWACommandRequest(_message.Message):
    __slots__ = ("uri", "command", "args", "binaryArg")
    URI_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    BINARYARG_FIELD_NUMBER: _ClassVar[int]
    uri: str
    command: str
    args: str
    binaryArg: bytes
    def __init__(self, uri: _Optional[str] = ..., command: _Optional[str] = ..., args: _Optional[str] = ..., binaryArg: _Optional[bytes] = ...) -> None: ...

class NWACommandResponse(_message.Message):
    __slots__ = ("uri", "asciiReply", "binaryReplay")
    class NWAASCIIItem(_message.Message):
        __slots__ = ("item",)
        class ItemEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
        ITEM_FIELD_NUMBER: _ClassVar[int]
        item: _containers.ScalarMap[str, str]
        def __init__(self, item: _Optional[_Mapping[str, str]] = ...) -> None: ...
    URI_FIELD_NUMBER: _ClassVar[int]
    ASCIIREPLY_FIELD_NUMBER: _ClassVar[int]
    BINARYREPLAY_FIELD_NUMBER: _ClassVar[int]
    uri: str
    asciiReply: _containers.RepeatedCompositeFieldContainer[NWACommandResponse.NWAASCIIItem]
    binaryReplay: bytes
    def __init__(self, uri: _Optional[str] = ..., asciiReply: _Optional[_Iterable[_Union[NWACommandResponse.NWAASCIIItem, _Mapping]]] = ..., binaryReplay: _Optional[bytes] = ...) -> None: ...
