# Shared Cache

Archipelago maintains a shared folder of information that can be persisted for a machine and reused across Libraries.
It can be found at the User Cache Directory for appname `Archipelago` in the `Cache` subfolder
(ex. `%LOCALAPPDATA%/Archipelago/Cache`).

## Common Cache

The Common Cache `common.json` can be used to store any generic data that is expected to be shared across programs
for the same User.

* `uuid`: A UUID identifier used to identify clients as from the same user/machine, to be sent in the Connect packet

## Data Package Cache

The `datapackage` folder in the shared cache folder is used to store datapackages by game and checksum to be reused
in order to save network traffic. The expected structure is `datapackage/Game Name/checksum_value.json` with the
contents of each json file being the no-whitespace datapackage contents.
