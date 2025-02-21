# About dev_util
This directory contains a collection of scripts to help with modding Trails in the Sky the 3rd for Archipelago.

## Setup
Before running these scripts, please modify `dev_config.json` in this directory to point to the correct paths.
- gameDirectory: This should point to your TitS the 3rd installation root. This root should contain the unmodified `ED6_DTXX` files from your game download.
- lbARKDirectory: This should point to your [LB-ARK installation](https://github.com/Aureole-Suite/LB-ARK). This is by default `"C:\\Program Files (x86)\\Steam\\steamapps\\common\\Trails in the Sky the 3rd\\data"`

Afterwards, please download both [calmare.exe](https://github.com/Kyuuhachi/Aureole/releases/tag/factoria-v1.1.0) and [factoria.exe](https://github.com/Kyuuhachi/Aureole/releases/tag/factoria-v1.1.0) and place them within the `worlds/tits_the_third/external_tools` directory.

## patch.py

This script is used to create, apply, and diff patches to and from your LB-ARK directory. It expects the following directory structure:
```
├───data
│   ├───ED6_DT21
│   ├───ED6_DT21_CLM
│   └───ED6_DT22
```

If you wish to add any new archives to the patch, please update the `MODIFIED_ARCHIVES` constant at the top of `worlds/tits_the_third/patch/patch.py`.

# Usage:
- `./patch.py create` will create a new patch based off the contents in your LB-ARK directory.
- `./patch.py apply` will use the files in your base Trails in the Sky the Third installation folder. It will automatically put them through Factoria and store them in your LB-ARK folder. Additionally, it will put any `._sn` files through Calmare and store them in `ED6_DT21_CLM` within your LB-ARK folder. Before applying, it will show you a rudementary diff between the patch and your current LB-ARK directory, and if there are files in your LB-ARK directory, it will prompt you to back them up if you wish through a y/n prompt before replacing your LB-ARK directory.
- `./patch.py diff` will only diff the differences between the patch output and your current LB-ARK directory. This is useful for finding out what changed after pulling the latest changes from the repo. **Note that your console text should support the JP character set, or this might print some garbage if it tries to render any of that.**

### About `ED6_DT21`
`ED6_DT21` is split into two parts after applying the patch:
- `ED6_DT21` contains the `._sn` files
- `ED6_DT21_CLM` contains the decompiled `.clm` files.

Note that the `ED6_DT21_CLM` is ignored when creating a patch! When applying a patch, it will generate this folder from the `._sn` files in `ED6_DT21`.

## update_dt21.py
You can run `./update_dt21.py` to:
1. wipe your `ED6_DT21`
2. put all files within `ED6_DT21_CLM` through calmare and
3. move them to `ED6_DT21`.

## hot_refresh_clm_changes.py
You can run `./hot_refresh_clm_changes.py` while developing to automatically detect changes to `.clm` files in `ED6_DT21_CLM`, compile them through calmare, and replace the existing file in `ED6_DT21`.

## diff_against_main.py
You can run `./diff_against_main.py` to compare your current branch against the main branch, including patch contents.
It will use the latest from main / your current branch on remote, but ignore your local, uncommited changes.

Usage (while on the branch you want to compare against main):
```
python diff_against_main.py
```



