REM Add registry entries to enable the build_apworld context menu action, which will become immediately available
REG ADD HKCU\Software\Classes\directory\shell\MenuItemNamePanel /t REG_SZ /ve /d "Build APWorld"
REG ADD HKCU\Software\Classes\directory\shell\MenuItemNamePanel /t REG_SZ /v icon /d "%CD%\data\icon.ico"
REG ADD HKCU\Software\Classes\directory\shell\MenuItemNamePanel\command /t REG_SZ /ve /d "cmd /c python \"%CD%\build_apworld.py\" \"%%V\" || pause"
