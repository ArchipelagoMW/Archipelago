# APContainer

An APContainer is a zip file holding data or code that somehow extends Archipelago.  
The main use currently is for patch files to be read by game clients.  
In the future, [apworlds](apworld%20specification.md) may become a type of APContainer as well.

## Specification

An APContainer must be a zip archive.  
This zip file can (and usually will) have a custom extension linking it to one specific purpose.

An APContainer must contain a manifest file called `archipelago.json`.  
This file must either in the root, or in the only subfolder of the root.  

## Examples

### Valid Containers

```
AP_69139584124759499357_P1_Player1.mygamepatch
├── archipelago.json  # A flat zipfile structure with the manifest file next to the other files is ok.
├── patch_data_1.json
└── patch_data_2.json
```


```
AP_69139584124759499357_P1_Player1.mygamepatch
├── archipelago.json  # As long as the manifest is in the root, any amount of subfolders are allowed.
└── patch_data
    ├── patch_data_1.json
    └── patch_data_2.json
```

```
AP_69139584124759499357_P1_Player1.mygamepatch
└── patch_data
    ├── archipelago.json  # If the only thing in the root is a single directory, the manifest is allowed to be in it.
    ├── patch_data_1.json
    └── patch_data_2.json
```

### Invalid APContainers

```
AP_69139584124759499357_P1_Player1.mygamepatch
├── manifest
│   └── archipelago.json  # If there are multiple files/directories in the root, the manifest cannot be in a subdirectory.
└── patch_data
    ├── patch_data_1.json
    └── patch_data_2.json
```