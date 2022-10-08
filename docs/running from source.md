# Running From Source

If you just want to play and there is a compiled version available on the
[Archipelago releases page](https://github.com/ArchipelagoMW/Archipelago/releases),
use that version. These steps are for developers or platforms without compiled releases available.

## General

What you'll need:
 * Python 3.8.7 or newer
   * pip (Depending on platform may come included)
 * A C compiler
   * possibly optional, read OS-specific sections

Then run any of the starting point scripts, like Generate.py, and the included ModuleUpdater should prompt to install or update the
required modules and after pressing enter proceed to install everything automatically.
After this, you should be able to run the programs.

 * With yaml(s) in the `Players` folder, `Generate.py` will generate the multiworld archive.
 * `MultiServer.py`, with the filename of the generated archive as a command line parameter, will host the multiworld locally.
    * `--log_network` is a command line parameter useful for debugging.
 * `WebHost.py` will host the website on your computer.
    * You can copy `docs/webhost configuration sample.yaml` to `config.yaml`
    to change WebHost options (like the web hosting port number).
    * As a side effect, `WebHost.py` creates the template yamls for all the games in `WebHostLib/static/generated`.


## Windows

Recommended steps
 * Download and install a "Windows installer (64-bit)" from the [Python download page](https://www.python.org/downloads)
 * Download and install full Visual Studio from
   [Visual Studio Downloads](https://visualstudio.microsoft.com/downloads/)
   or an older "Build Tools for Visual Studio" from
   [Visual Studio Older Downloads](https://visualstudio.microsoft.com/vs/older-downloads/).

   * Refer to [Windows Compilers on the python wiki](https://wiki.python.org/moin/WindowsCompilers) for details
   * This step is optional. Pre-compiled modules are pinned on
     [Discord in #archipelago-dev](https://discord.com/channels/731205301247803413/731214280439103580/905154456377757808)

 * It is recommended to use [PyCharm IDE](https://www.jetbrains.com/pycharm/)
 * Run Generate.py which will prompt installation of missing modules, press enter to confirm


## macOS

Refer to [Guide to Run Archipelago from Source Code on macOS](../worlds/generic/docs/mac_en.md).


## Optional: A Link to the Past Enemizer

Only required to generate seeds that include A Link to the Past with certain options enabled. You will receive an
error if it is required.

You can get the latest Enemizer release at [Enemizer Github releases](https://github.com/Ijwu/Enemizer/releases).
It should be dropped as "EnemizerCLI" into the root folder of the project. Alternatively, you can point the Enemizer
setting in host.yaml at your Enemizer executable.


## Optional: SNI

SNI is required to use SNIClient. If not integrated into the project, it has to be started manually.

You can get the latest SNI release at [SNI Github releases](https://github.com/alttpo/sni/releases).
It should be dropped as "SNI" into the root folder of the project. Alternatively, you can point the sni setting in
host.yaml at your SNI folder.


## Running tests

Run `pip install pytest pytest-subtests`, then use your IDE to run tests or run `pytest` from the source folder.
