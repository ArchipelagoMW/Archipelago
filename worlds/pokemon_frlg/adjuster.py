import os

def frlgFetchPatch(_opts, _isPatchValid):
    # Asks for a ROM or patch file then validates it
    # Replaces the function fetchPatch from the Pokemon Emerald world's adjuster.py file
    from tkinter import filedialog, messagebox
    oldPatchFolder = os.path.dirname(_opts.patch.get()) if _isPatchValid else None
    oldPatchFile = _opts.patch.get() if _isPatchValid else None
    patch = filedialog.askopenfilename(initialdir=oldPatchFolder, initialfile=oldPatchFile, title='Choose a Gen 3 Pokemon ROM or a .apemerald/.apfirered/.apleafgreen patch file.', filetypes=[('Rom & Patch Files', ['.gba', '.apemerald', '.apfirered', '.apleafgreen'])])

    if patch and os.path.exists(patch):
        if os.path.splitext(patch)[-1] == '.gba':
            # If .gba, verify ROM integrity by checking for its internal name at addresses #0000A0-#0000AB (must be POKEMON EMER/FIRE/LEAF)
            with open(patch, 'rb') as stream:
                romData = bytearray(stream.read())
                return patch, frlgGetRomVersion(patch, romData)
        elif os.path.splitext(patch)[-1] == '.apemerald':
            return patch, 'Emerald'
        elif os.path.splitext(patch)[-1] in ['.apfirered', '.apleafgreen']:
            # If .apfirered or .apleafgreen, patch the ROM to fetch its revision number
            romData = frlgBuildApRom(patch)
            return patch, frlgGetRomVersion(patch, romData)
    messagebox.showerror(title='Error while loading a ROM', message=f'The ROM at path {patch} isn\'t a valid Gen 3 Pokemon ROM!')
    return patch, 'Unknown'

def frlgBuildApRom(_patch):
    # Builds the AP ROM if a patch file was given
    # Extends the function buildApRom from the Pokemon Emerald world's adjuster.py file
    from tkinter import messagebox
    if os.path.splitext(_patch)[-1] in ['.apfirered', '.apleafgreen']:
        # Patch the registered ROM as an AP ROM
        import Patch
        _, apRomPath = Patch.create_rom_file(_patch)
        with open(apRomPath, 'rb') as stream:
            return bytearray(stream.read())
    else:
        messagebox.showerror(title='Failure', message=f'Cannot build the AP ROM: invalid file extension: requires .gba, .apemerald, .apfirered or .apleafgreen')
        return

def frlgGetRomVersion(_patch, _romData):
    # Retrieves and returns the version of the ROM given
    # Extends the function buildApRom from the Pokemon Emerald world's adjuster.py file
    from tkinter import messagebox
    allowedInternalNames = {'POKEMON EMER': 'Emerald', 'POKEMON FIRE': 'Firered', 'POKEMON LEAF': 'Leafgreen'}
    internalName = _romData[0xA0:0xAC].decode('utf-8')
    internalRevision = int(_romData[0xBC])
    versionName = allowedInternalNames.get(internalName, '')
    if not versionName:
        messagebox.showerror(title='Error while loading a ROM', message=f'The ROM at path {_patch} isn\'t a valid Gen 3 Pokemon ROM!')
        return 'Unknown'
    return f'{versionName}{'_rev1' if internalRevision == 1 else ''}'