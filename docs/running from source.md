# Running From Source

If you just want to play and there is a compiled version available on the
[Archipelago releases page](https://github.com/ArchipelagoMW/Archipelago/releases),
use that version. These steps are for developers or platforms without compiled releases available.

## General

What you'll need:
 * [Python 3.11.9 or newer](https://www.python.org/downloads/), not the Windows Store version
   * On Windows, please consider only using the latest supported version in production environments since security
     updates for older versions are not easily available.
   * Python 3.12.x is currently the newest supported version
 * pip: included in downloads from python.org, separate in many Linux distributions
 * Matching C compiler
   * possibly optional, read operating system specific sections

Then run any of the starting point scripts, like Generate.py, and the included ModuleUpdater should prompt to install or update the
required modules and after pressing enter proceed to install everything automatically.
After this, you should be able to run the programs.

 * `Launcher.py` gives access to many components, including clients registered in `worlds/LauncherComponents.py`.
    * The Launcher button "Generate Template Options" will generate default yamls for all worlds.
 * With yaml(s) in the `Players` folder, `Generate.py` will generate the multiworld archive.
 * `MultiServer.py`, with the filename of the generated archive as a command line parameter, will host the multiworld locally.
    * `--log_network` is a command line parameter useful for debugging.
 * `WebHost.py` will host the website on your computer.
    * You can copy `docs/webhost configuration sample.yaml` to `config.yaml`
    to change WebHost options (like the web hosting port number).


## Windows

Recommended steps
 * Download and install a "Windows installer (64-bit)" from the [Python download page](https://www.python.org/downloads)
   * [read above](#General) which versions are supported

 * **Optional**: Download and install Visual Studio Build Tools from
   [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
   * Refer to [Windows Compilers on the python wiki](https://wiki.python.org/moin/WindowsCompilers) for details. 
     Generally, selecting the box for "Desktop Development with C++" will provide what you need.
   * Build tools are not required if all modules are installed pre-compiled. Pre-compiled modules are pinned on
     [Discord in #ap-core-dev](https://discord.com/channels/731205301247803413/731214280439103580/905154456377757808)

 * It is recommended to use [PyCharm IDE](https://www.jetbrains.com/pycharm/)
 * Run ModuleUpdate.py which will prompt installation of missing modules, press enter to confirm
   * In PyCharm: right-click ModuleUpdate.py and select `Run 'ModuleUpdate'`
   * Without PyCharm: open a command prompt in the source folder and type `py ModuleUpdate.py`


## macOS

Refer to [Guide to Run Archipelago from Source Code on macOS](../worlds/generic/docs/mac_en.md).


## Optional: A Link to the Past Enemizer

Only required to generate seeds that include A Link to the Past with certain options enabled. You will receive an
error if it is required.

You can get the latest Enemizer release at [Enemizer Github releases](https://github.com/Ijwu/Enemizer/releases).
It should be dropped as "EnemizerCLI" into the root folder of the project. Alternatively, you can point the Enemizer
setting in host.yaml at your Enemizer executable.


## Optional: SNI

[SNI](https://github.com/alttpo/sni/blob/main/README.md) is required to use SNIClient. If not integrated into the project, it has to be started manually.

You can get the latest SNI release at [SNI Github releases](https://github.com/alttpo/sni/releases).
It should be dropped as "SNI" into the root folder of the project. Alternatively, you can point the sni setting in
host.yaml at your SNI folder.


## Optional: Git

[Git](https://git-scm.com) is required to install some of the packages that Archipelago depends on.
It may be possible to run Archipelago from source without it, at your own risk.

It is also generally recommended to have Git installed and understand how to use it, especially if you're thinking about contributing.

You can download the latest release of Git at [The downloads page on the Git website](https://git-scm.com/downloads).

Beyond that, there are also graphical interfaces for Git that make it more accessible.
For repositories on Github (such as this one), [Github Desktop](https://desktop.github.com) is one such option.
PyCharm has a built-in version control integration that supports Git.

## Running tests

Information about running tests can be found in [tests.md](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/tests.md#running-tests)
