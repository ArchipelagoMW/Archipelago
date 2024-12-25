import os.path
import shutil
import tempfile
import zipfile
import tkinter as tk
from tkinter import filedialog

def load_external_data_archive(archive):
    if not zipfile.is_zipfile(archive):
        raise zipfile.BadZipFile
    elif not zipfile.is_zipfile(os.path.join("lib", "worlds", "ff4fe.apworld")):
        raise zipfile.BadZipFile
    else:
        sourcefile = zipfile.ZipFile(archive)
        destinationfile = zipfile.ZipFile(os.path.join("lib", "worlds", "ff4fe.apworld"), "r")
        print("Reading data...")
        newdata = tempfile.mkdtemp()
        newworld = tempfile.mkdtemp()
        sourcefile.extractall(newdata)
        sourcefile.close()
        destinationfile.extractall(newworld)
        print("Copying data...")
        shutil.copytree(os.path.join(newdata, "FEAPExternalData", "harp"),
                        os.path.join(newworld, "ff4fe", "FreeEnterpriseForAP", "FreeEnt", "compiled_songs"),
                        dirs_exist_ok=True)
        shutil.copytree(os.path.join(newdata, "FEAPExternalData", "zsprite"),
                        os.path.join(newworld, "ff4fe", "FreeEnterpriseForAP", "FreeEnt", "compiled_zeromus_pics"),
                        dirs_exist_ok=True)
        destinationfile.close()
        print("Building new APWorld...")
        shutil.make_archive(os.path.join("worlds", "ff4fe"), "zip", newworld)
        os.unlink(os.path.join("lib", "worlds", "ff4fe.apworld"))
        os.rename(os.path.join("lib", "worlds", "ff4fe.zip"), os.path.join("worlds", "ff4fe.apworld"))
        print("Done!")



root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(defaultextension="zip")
load_external_data_archive(file_path)
