If you just want to play and there is a [compiled version](https://github.com/Berserker66/MultiWorld-Utilities/releases) available, use that version. These steps are for developers or platforms without compiled releases available.

# General
What you'll need:
 * Python 3.8+
   * with pip, which depending on platform may have to be installed separately
 * A C compiler

Then run any of the starting points, like Generate and the included ModuleUpdater should prompt to install or update the required modules and after pressing enter proceed to install everything automatically. After this, you should be able to run the programs.

## Windows
Recommended steps
 * Download and install [Python](https://www.python.org/ftp/python/3.9.10/python-3.9.10-amd64.exe), make sure to install it with pip included
 * Download and install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019)
   * Or go to [unoffical python packages](https://www.lfd.uci.edu/~gohlke/pythonlibs/) to download and install a precompiled bsdiff4 for your python.
 * run Generate.py which will prompt installation of missing modules, press enter to confirm

## Optional A Link to the Past Enemizer
At https://github.com/Ijwu/Enemizer/releases you can get the latest Enemizer release, it should be dropped as "EnemizerCLI" into the root folder of the project. Alternatively, you can point the Enemizer setting in host.yaml at your Enemizer.
