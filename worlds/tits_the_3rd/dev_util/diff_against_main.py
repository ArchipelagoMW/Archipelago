import json
import os
import subprocess
from pathlib import Path
import sys
import shutil
from itertools import zip_longest
import colorama

AP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(AP_DIR))

from worlds.tits_the_3rd.patch.patch import apply_patch_to_dir_with_patch_file

world_path = Path('Archipelago-Trails-in-the-Sky-the-3rd/worlds/tits_the_3rd')
lb_ark_path = os.path.join(world_path, 'lbARK')
patch_path = os.path.join(world_path, 'patch', 'tits3rdDev.patch')

def get_files_recursively(directory):
    """
    Get all files in directory and subdirectories.

    Args:
        directory: The path to the directory to get files from.
    """
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, directory)
            file_list.append(rel_path)
    return sorted(file_list)

def print_directory_differences(main_dir, branch_dir, branch_name):
    """
    Compare two directories and show differences.

    Args:
        main_dir: The path to the main directory.
        branch_dir: The path to the branch directory.
        branch_name: The name of the branch.
    """
    files1 = get_files_recursively(main_dir)
    files2 = get_files_recursively(branch_dir)

    # Get terminal width for display
    term_width = os.get_terminal_size().columns
    half_width = (term_width - 3) // 2  # -3 for the separator

    # Compare files
    all_files = sorted(set(files1) | set(files2))

    for file in all_files:
        path1 = os.path.join(main_dir, file)
        path2 = os.path.join(branch_dir, file)

        # File exists only in main
        if file not in files2:
            print(f"\n{colorama.Fore.RED}Only in main: {file}{colorama.Style.RESET_ALL}")
            continue

        # File exists only in the branch dir
        if file not in files1:
            print(f"\n{colorama.Fore.GREEN}Only in {branch_name}: {file}{colorama.Style.RESET_ALL}")
            continue

        # Both files exist, compare contents
        if os.path.isfile(path1) and os.path.isfile(path2):
            with open(path1, 'r', encoding='utf-8') as f1, open(path2, 'r', encoding='utf-8') as f2:
                try:
                    content1 = f1.readlines()
                    content2 = f2.readlines()
                except UnicodeDecodeError:
                    continue

                if content1 != content2:
                    print(f"\n{colorama.Fore.YELLOW}Differences in {file}:{colorama.Style.RESET_ALL}")
                    print("=" * term_width)

                    # Print header for columns
                    print(f"{colorama.Fore.RED}main{' ' * (half_width - 4)}{colorama.Style.RESET_ALL} | "
                          f"{colorama.Fore.GREEN}{branch_name}{colorama.Style.RESET_ALL}")
                    print("-" * term_width)

                    # Create side-by-side diff
                    for line1, line2 in zip_longest(content1, content2, fillvalue=''):
                        line1 = line1.rstrip('\n')
                        line2 = line2.rstrip('\n')

                        # Truncate lines if they're too long
                        if len(line1) > half_width:
                            line1 = line1[:half_width-3] + '...'
                        if len(line2) > half_width:
                            line2 = line2[:half_width-3] + '...'

                        # Pad lines to equal width
                        line1 = line1.ljust(half_width)
                        line2 = line2.ljust(half_width)

                        # Update the colored output lines to use colorama
                        if line1 != line2:
                            print(f"{colorama.Fore.RED}{line1}{colorama.Style.RESET_ALL} | {colorama.Fore.GREEN}{line2}{colorama.Style.RESET_ALL}")
                        else:
                            print(line1 + ' | ' + line2)


def setup_comparison_subdirectory(dir_path, checkout_branch):
    """
    Setup the comparison subdirectory.
    This will pull the latest from main / your current branch on remote.
    It will also apply the patch from each directory and copy the files into the comparison directory.

    Args:
        dir_path: The path to the comparison directory.
        checkout_branch: The branch to checkout.
    """
    dir_path = Path(dir_path)
    if not dir_path.exists():
        dir_path.mkdir(parents=True)
    os.chdir(dir_path)
    if not (dir_path / 'Archipelago-Trails-in-the-Sky-the-3rd').exists():
        subprocess.run([
            'git', 'clone',
            'git@github.com:Archipelago-Trails-in-the-Sky-the-3rd/Archipelago-Trails-in-the-Sky-the-3rd.git',
        ], check=True)
    os.chdir(dir_path / 'Archipelago-Trails-in-the-Sky-the-3rd')
    subprocess.run(['git', 'checkout', checkout_branch], check=True)
    subprocess.run(['git', 'pull'], check=True)
    lb_ark_dir = os.path.join(dir_path, lb_ark_path)
    patch_file = os.path.join(dir_path, patch_path)
    os.mkdir(lb_ark_dir)
    apply_patch_to_dir_with_patch_file(lb_ark_dir, patch_file)

    # Return to original directory
    os.chdir(Path(__file__).parent)


def setup_directories(comparison_dir, current_branch):
    """
    Setup the comparison directories. This will pull the latest from main / your current branch on remote.
    It will also apply the patch from each directory and copy the files into the comparison directory.

    Args:
        comparison_dir: The path to the comparison directory.
        current_branch: The branch to checkout.
    """
    main_dir = os.path.join(comparison_dir, 'main')
    branch_dir = os.path.join(comparison_dir, current_branch)

    setup_comparison_subdirectory(main_dir, 'main')
    setup_comparison_subdirectory(branch_dir, current_branch)

    return main_dir, branch_dir

def cleanup(main_dir, branch_dir):
    """
    Delete the patch contents from the comparison directories.

    Args:
        main_dir: The path to the main directory.
        branch_dir: The path to the branch directory.
    """
    main_lb_ark_dir = os.path.join(main_dir, lb_ark_path)
    branch_lb_ark_dir = os.path.join(branch_dir, lb_ark_path)
    shutil.rmtree(main_lb_ark_dir)
    shutil.rmtree(branch_lb_ark_dir)

def main():
    """
    This script compares the current branch against the main branch.
    It will show you the differences between the two branches, including patch contents.

    It does this by pulling both branches into the comparison directory,
    applying the patch, and then comparing the contents.

    It does NOT use your local, uncommited changes, it will always pull
    the latest from main / your current branch on remote.
    """
    colorama.init(convert=True, strip=False)
    with open('dev_config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    current_branch = subprocess.check_output(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
        text=True
    ).strip()

    main_dir, branch_dir = setup_directories(config['apDevComparisonDirectory'], current_branch)
    print_directory_differences(
        os.path.join(main_dir, world_path),
        os.path.join(branch_dir, world_path),
        current_branch
    )
    cleanup(main_dir, branch_dir)


if __name__ == '__main__':
    main()
