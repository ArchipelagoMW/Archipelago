"""
This module is used for creating patches for the AP mod / development, as well
as applying the patch given the unmodified directory of the game.

Please see readme.md for instructions on how to setup and run this script.
"""

import difflib
import filecmp
import inspect
import os
import shutil
import subprocess
import tempfile
import sys
import zipfile

import bsdiff4

if sys.path[-1].endswith("worlds"):
    # running script from worlds/tits_the_3rd/dev_util
    # pylint: disable=import-error
    from tits_the_3rd.util import (
        copy_contents,
        delete_contents,
        get_tooling_path,
        move_contents_with_file_ending,
        prompt_and_create_backup,
        read_dev_config_and_assert_contents
    )
else:
    # running from archipelago root
    from worlds.tits_the_3rd.util import (
        copy_contents,
        delete_contents,
        get_tooling_path,
        move_contents_with_file_ending,
        prompt_and_create_backup,
        read_dev_config_and_assert_contents
    )

MODIFIED_ARCHIVES = [
    "ED6_DT21",
    "ED6_DT22"
]

def _move_calmare_contents(source: str, destination: str):
    """
    Move the .clm files in the source directory to the destination directory

    :str source: the source directory
    :str destination: the destination directory
    """
    move_contents_with_file_ending(source, destination, ".clm")

def _copy_to_lb_ark_dir(temp_dir: str, lb_ark_dir: str):
    """
    Copy the contents from the temp_dir into the lbARK directory

    :str temp_dir: The temporary directory created in the patch script
    :str lb_ark_dir: The lbARK directory installation
    """
    if not os.path.exists(lb_ark_dir):
        os.makedirs(lb_ark_dir)
    elif os.listdir(lb_ark_dir):
        # For now, assume we're running this as a script from the dev_util directory, and we always want to prompt for backup.
        # When we actually bake this into the AP client, we will create a unique lbARK directory for each AP game.
        frame = inspect.stack()[-1]
        entrypoint_file = frame.filename
        backup_dir = os.path.dirname(os.path.abspath(entrypoint_file))
        print("***************************************")
        print("          PATCH / LB-ARK DIFF          ")
        print("***************************************")
        _print_diff(temp_dir, lb_ark_dir)
        print("***************************************")
        print("              END OF DIFF              ")
        print("***************************************")
        prompt_and_create_backup(backup_dir, lb_ark_dir)
        delete_contents(lb_ark_dir)
    copy_contents(temp_dir, lb_ark_dir)

def _copy_from_lb_ark_dir(temp_dir: str, lb_ark_dir: str):
    """
    Copy the contents from the  lb_ark_dir into the temp_dir

    :str temp_dir: The temporary directory created in the patch script
    :str lb_ark_dir: The lbARK directory installation
    """
    if not os.path.exists(lb_ark_dir):
        raise FileNotFoundError(f"Directory {lb_ark_dir} does not exist. Please see readme.md for setup.")
    for directory_name in MODIFIED_ARCHIVES:
        dt_path = os.path.join(lb_ark_dir, directory_name)
        if not os.path.exists(dt_path):
            print(f"Directory {dt_path} not found and will be created.")
            os.makedirs(dt_path, exist_ok=True)
        dest_path = os.path.join(temp_dir, directory_name)
        shutil.copytree(dt_path, dest_path)

def _decompress_with_factoria(temp_dir: str, source_dir: str):
    """
    Decompress the ED6_DTXX files with factoria.

    :str temp_dir: The temporary directory created in the patch script.
    :str source_dir: The game directory where the original files are.
    """
    factoria_path = get_tooling_path("factoria.exe")
    for filename in MODIFIED_ARCHIVES:
        base_file_path = os.path.join(source_dir, filename)
        for extention in [".dir", ".dat"]:
            file_path = f"{base_file_path}{extention}"
            if not os.path.exists(file_path):
                raise ValueError(f"Path {file_path} does not exist.")
        try:
            subprocess.run([
                factoria_path,
                f"{base_file_path}.dir",
                "--output",
                temp_dir
            ], check=True)
        except subprocess.CalledProcessError as err:
            print(f"Error running factoria: {err}")
            raise err

def _decompile_with_calmare(temp_dir: str):
    """
    Decompile ._sn files in ED6_DT21 into readable .clm files, and store them in ED6_DT21_CLM.

    :str temp_dir: The temporary directory created in the patch script.
    """
    calmare_path = get_tooling_path("calmare.exe")
    dt21_path = os.path.join(temp_dir, "ED6_DT21")
    for scena in os.listdir(dt21_path):
        print(f"Running {scena} through calmare...")
        scena_path = os.path.join(dt21_path, scena)
        try:
            subprocess.run([
                calmare_path,
                "--game",
                "tc",
                scena_path,
            ], check=True)
        except subprocess.CalledProcessError as err:
            print(f"Error running calmare: {err}")
            raise err
    calmare_out_dir = os.path.join(temp_dir, "ED6_DT21_CLM")
    os.makedirs(calmare_out_dir)
    _move_calmare_contents(dt21_path, calmare_out_dir)

def _move_archives_into_zip_and_remove_non_zip_files(temp_dir: str, zip_filename: str):
    """
    Move all files (that are not .zips) in temp_dir into a zip archive with the provided filename.
    Afterwards, delete all files that aren't .zips.

    :str temp_dir: The temporary directory created in the patch script.
    :str zip_filename: The filename of the zip file thats created.
    """
    with zipfile.ZipFile(os.path.join(temp_dir, zip_filename), 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if not file.endswith(".zip"):
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, temp_dir))
    for dir_name in os.listdir(temp_dir):
        if not dir_name.endswith(".zip"):
            shutil.rmtree(os.path.join(temp_dir, dir_name))

def _unzip_patch_output(temp_dir: str):
    """
    Unzip the file output.zip in the temp directory. This is the output of the patch.

    :str temp_dir: The temporary directory created in the patch script.
    """
    with zipfile.ZipFile(os.path.join(temp_dir, "output.zip"), "r") as output:
        output.extractall(temp_dir)

def _delete_zip_files(temp_dir: str):
    """
    Delete the .zip files in the temp_directory.

    :str temp_dir: The temporary directory created in the patch script.
    """
    for file in os.listdir(temp_dir):
        if file.endswith(".zip"):
            os.remove(os.path.join(temp_dir, file))

def _create_patch_file(temp_dir: str, patch_path: str):
    """
    Create the patch file. Write it to the patch_path.

    :str temp_dir: The temporary directory created in the patch script.
    :str patch_path: The path to write the patch to.
    """
    if os.path.exists(patch_path):
        os.remove(patch_path)
    patch_data = None
    with open(os.path.join(temp_dir, "input.zip"), 'rb') as input:
        with open(os.path.join(temp_dir, "output.zip"), 'rb') as output:
            input_data = input.read()
            output_data = output.read()
            patch_data = bsdiff4.diff(input_data, output_data)
    with open(patch_path, 'wb') as patch_file:
        patch_file.write(patch_data)

def _apply_patch_file(temp_dir: str, patch_path: str):
    """
    Apply the patch file. Write it to output.zip in the temp directory

    :str temp_dir: The temporary directory created in the patch script.
    :str patch_path: The path of the patch.
    """
    with open(os.path.join(temp_dir, "input.zip"), 'rb') as input:
        with open(patch_path, 'rb') as patch:
            input_data = input.read()
            patch_data = patch.read()
            output_data = bsdiff4.patch(input_data, patch_data)
    with open(os.path.join(temp_dir, "output.zip"), 'wb') as output:
        output.write(output_data)

def _print_diff(temp_dir, lb_ark_dir, prefix=""):
    """
    Print the diff between the temporary directory and the lbARK directory

    :str temp_dir: The directory of the patch file after applying it.
    :str lb_ark_dir: The lbARK directory
    :str prefix: The prefix to print in front of any diff file names.
    """
    dircmp = filecmp.dircmp(temp_dir, lb_ark_dir)
    for name in dircmp.left_only:
        print(f"Only in patch: {prefix}{name}")
    for name in dircmp.right_only:
        print(f"Only in local lbARK: {prefix}{name}")
    for name in dircmp.diff_files:
        if name.endswith(".clm"):
            file1_path = os.path.join(temp_dir, name)
            file2_path = os.path.join(lb_ark_dir, name)
            print(f"Differences in contents between patch {prefix}{name} and lbARK {prefix}{name}:")
            with open(file1_path, 'r', encoding="utf-8", errors="ignore") as file1:
                with open(file2_path, 'r', encoding="utf-8", errors="ignore") as file2:
                    diff_result = difflib.unified_diff(file1.readlines(), file2.readlines(), lineterm='')
                    for line in diff_result:
                        print(line)
        else:
            print(f"Difference detected in file {prefix}{name}")
    for sub_dircmp_dirname, sub_dircmp in dircmp.subdirs.items():
        _print_diff(sub_dircmp.left, sub_dircmp.right, f"{sub_dircmp_dirname}/")

def apply_patch():
    """
    Apply the patch tits3rdDev.patch located in this directory.
    The patch is applied against the original game files, and the outputs of the patch
    are written to the lbARKDirectory specified in the config.
    """
    patch_dir = os.path.dirname(os.path.realpath(__file__))
    patch_path = os.path.join(patch_dir, "tits3rdDev.patch")
    temp_dir = tempfile.mkdtemp(dir=patch_dir)
    try:
        config = read_dev_config_and_assert_contents()
        _decompress_with_factoria(temp_dir, config["gameDirectory"])
        _move_archives_into_zip_and_remove_non_zip_files(temp_dir, "input.zip")
        _apply_patch_file(temp_dir, patch_path)
        _unzip_patch_output(temp_dir)
        _delete_zip_files(temp_dir)
        if "ED6_DT21" in MODIFIED_ARCHIVES:
            _decompile_with_calmare(temp_dir)
        _copy_to_lb_ark_dir(temp_dir, config["lbARKDirectory"])
    finally:
        shutil.rmtree(temp_dir)

def apply_patch_to_dir_with_patch_file(destination: str, patch_path: str):
    """
    Apply the patch file provided to the destination directory provided.
    The patch is applied against the original game files, and the outputs of the patch
    are written to the destination directory provided.

    Note this function does not check if the destination directory is populated.
    It is assumed that it is not, as this function is primarily used for the diff
    tool, which aims to create a new directory.

    :str destination: The destination directory to write the patch to.
    :str patch_path: The path to the patch file to apply.
    """
    patch_dir = os.path.dirname(os.path.realpath(__file__))
    temp_dir = tempfile.mkdtemp(dir=patch_dir)
    try:
        config = read_dev_config_and_assert_contents()
        _decompress_with_factoria(temp_dir, config["gameDirectory"])
        _move_archives_into_zip_and_remove_non_zip_files(temp_dir, "input.zip")
        _apply_patch_file(temp_dir, patch_path)
        _unzip_patch_output(temp_dir)
        _delete_zip_files(temp_dir)
        if "ED6_DT21" in MODIFIED_ARCHIVES:
            _decompile_with_calmare(temp_dir)
        copy_contents(temp_dir, destination)
    finally:
        shutil.rmtree(temp_dir)

def create_patch():
    """
    Given the original game files and the lbARK directory with the desired patch output files,
    Create a patch file and write it to tits3rdDev.patch in this directory.
    """
    patch_dir = os.path.dirname(os.path.realpath(__file__))
    patch_path = os.path.join(patch_dir, "tits3rdDev.patch")
    temp_dir = tempfile.mkdtemp(dir=patch_dir)
    try:
        config = read_dev_config_and_assert_contents()
        _copy_from_lb_ark_dir(temp_dir, config["lbARKDirectory"])
        _move_archives_into_zip_and_remove_non_zip_files(temp_dir, "output.zip")
        _decompress_with_factoria(temp_dir, config["gameDirectory"])
        _move_archives_into_zip_and_remove_non_zip_files(temp_dir, "input.zip")
        _create_patch_file(temp_dir, patch_path)
    finally:
        shutil.rmtree(temp_dir)

def diff():
    """
    Get the diff between the current patch and whats currently in the lbARK directory
    """
    patch_dir = os.path.dirname(os.path.realpath(__file__))
    patch_path = os.path.join(patch_dir, "tits3rdDev.patch")
    temp_dir = tempfile.mkdtemp(dir=patch_dir)
    try:
        config = read_dev_config_and_assert_contents()
        lb_ark_dir = config["lbARKDirectory"]
        _decompress_with_factoria(temp_dir, config["gameDirectory"])
        _move_archives_into_zip_and_remove_non_zip_files(temp_dir, "input.zip")
        _apply_patch_file(temp_dir, patch_path)
        _unzip_patch_output(temp_dir)
        _delete_zip_files(temp_dir)
        if "ED6_DT21" in MODIFIED_ARCHIVES:
            _decompile_with_calmare(temp_dir)
        print("***************************************")
        print("          PATCH / LB-ARK DIFF          ")
        print("***************************************")
        _print_diff(temp_dir, lb_ark_dir)

    finally:
        shutil.rmtree(temp_dir)
