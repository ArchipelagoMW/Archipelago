from __future__ import annotations

import argparse
import logging
import subprocess
import webbrowser
from shutil import which

import settings
import Utils
from Utils import env_cleared_lib_path, is_linux, is_macos, messagebox, open_file, open_filename, user_path

from core import ComponentKind, Err, ExportDatapackage, GenerateTemplates, InstallApworld, Ok

from launcher.bridge import dispatch
from launcher.models import LauncherEntry


def open_folder(folder_path: str) -> None:
    """Open `folder_path` in the platform file browser.

    Example::

        open_folder(user_path())
    """

    if is_linux:
        exe = which("xdg-open") or which("gnome-open") or which("kde-open")
    elif is_macos:
        exe = which("open")
    else:
        webbrowser.open(folder_path)
        return

    if exe:
        subprocess.Popen([exe, folder_path], env=env_cleared_lib_path())
    else:
        logging.warning(f"No file browser available to open {folder_path}")


def open_host_yaml(*args: str) -> str:
    """Open the user's `host.yaml` in the platform editor.

    Example::

        open_host_yaml()
    """

    current_settings = settings.get_settings()
    file = current_settings.filename
    current_settings.save()
    assert file, "host.yaml missing"

    if is_linux:
        exe = which("sensible-editor") or which("gedit") or which("xdg-open") or which("gnome-open") or which("kde-open")
    elif is_macos:
        exe = which("open")
    else:
        webbrowser.open(file)
        return "Opening in a new window..."

    subprocess.Popen([exe, file], env=env_cleared_lib_path())
    return "Opening in a new window..."


def generate_yamls(*args: str) -> str:
    """Generate template YAMLs through the core template service.

    Example::

        generate_yamls("--skip_open_folder")
    """

    parser = argparse.ArgumentParser(description="Generate Template Options", usage="[-h] [--skip_open_folder]")
    parser.add_argument("--skip_open_folder", action="store_true")
    parsed = parser.parse_args(args)

    result = dispatch(GenerateTemplates())
    if isinstance(result, Err):
        messagebox("Error", result.error.message, error=True)
        return result.error.message

    assert isinstance(result, Ok)
    if not parsed.skip_open_folder:
        open_folder(result.value.output_directory)
    return f"Generated templates in {result.value.output_directory}"


def browse_files(*args: str) -> str:
    """Open the Archipelago user folder in the file browser.

    Example::

        browse_files()
    """

    open_folder(user_path())
    return "Opening in a new window..."


def update_settings(*args: str) -> None:
    """Save the current settings file.

    Example::

        update_settings()
    """

    settings.get_settings().save()


def install_apworld(*args: str) -> str:
    """Select and install an APWorld through the core install service.

    Example::

        install_apworld("example.apworld")
    """

    apworld_path = args[0] if args else ""
    if not apworld_path:
        apworld_path = open_filename("Select APWorld file to install", (("APWorld", (".apworld",)),))
        if not apworld_path:
            logging.info("Aborting APWorld installation.")
            return "Aborting APWorld installation."

    result = dispatch(InstallApworld(apworld_path=apworld_path))
    if isinstance(result, Err):
        messagebox("Notice", result.error.message, error=True)
        logging.error(result.error.message)
        return result.error.message

    assert isinstance(result, Ok)
    message = f"Installed APWorld from {result.value.source_path}."
    if result.value.restart_required:
        message += " Restart the launcher to load the new installation."
    logging.info(f"Installed APWorld successfully, copied {result.value.source_path} to {result.value.target_path}.")
    messagebox("Install complete.", message)
    return "Install complete."


def export_datapackage(*args: str) -> str:
    """Export the datapackage and open the resulting file.

    Example::

        export_datapackage()
    """

    result = dispatch(ExportDatapackage())
    if isinstance(result, Err):
        messagebox("Error", result.error.message, error=True)
        return result.error.message

    assert isinstance(result, Ok)
    open_file(result.value.output_path)
    return f"Exported datapackage to {result.value.output_path}"


def open_patch(*args: str) -> str:
    """Open a patch file and route it through core input resolution.

    Example::

        open_patch()
    """

    from launcher.components import run_component
    from launcher.resolution import get_backend_components, resolve_input, to_launcher_entry

    suffixes: list[str] = []
    for component in get_backend_components():
        if component.kind.value == "client":
            suffixes.extend(component.file_suffixes)

    try:
        filename = open_filename("Select patch", (("Patches", suffixes),))
    except Exception as exc:
        messagebox("Error", str(exc), error=True)
        return str(exc)

    if not filename:
        return "Aborting patch selection."

    result = resolve_input(filename)
    if isinstance(result, Err):
        messagebox("Error", result.error.message, error=True)
        return result.error.message

    assert isinstance(result, Ok)
    resolved = result.value.resolved
    if not resolved.component_id:
        return "No component available."

    component = to_launcher_entry(resolved.component_id)
    if component is None:
        return "No component available."
    run_component(component, *(tuple(filter(None, (resolved.file_path, *resolved.launch_args)))))
    return "Opening in a new window..."


def get_launcher_entries() -> list[LauncherEntry]:
    """Return launcher-local utility entries.

    Example::

        entries = get_launcher_entries()
    """

    return [
        LauncherEntry(
            id="install_apworld_utility",
            display_name="Install APWorld",
            description="Install an APWorld to play games not included with Archipelago by default.",
            kind=ComponentKind.MISC,
            action=install_apworld,
        ),
        LauncherEntry(
            id="open_host_yaml",
            display_name="Open host.yaml",
            description="Open the host.yaml file to change settings for generation, games, and more.",
            kind=ComponentKind.MISC,
            action=open_host_yaml,
        ),
        LauncherEntry(
            id="open_patch",
            display_name="Open Patch",
            description="Open a patch file, downloaded from the room page or provided by the host.",
            kind=ComponentKind.MISC,
            action=open_patch,
        ),
        LauncherEntry(
            id="generate_template_options",
            display_name="Generate Template Options",
            description="Generate template YAMLs for currently installed games.",
            kind=ComponentKind.MISC,
            action=generate_yamls,
        ),
        LauncherEntry(
            id="export_datapackage_utility",
            display_name="Export Datapackage",
            description="Write item/location data for installed worlds to a file and open it.",
            kind=ComponentKind.TOOL,
            action=export_datapackage,
        ),
        LauncherEntry(
            id="archipelago_website",
            display_name="Archipelago Website",
            description="Open archipelago.gg in your browser.",
            kind=ComponentKind.MISC,
            action=lambda *args: webbrowser.open("https://archipelago.gg/") or "Opening in a new window...",
        ),
        LauncherEntry(
            id="discord_server",
            display_name="Discord Server",
            description="Join the Discord server to play public multiworlds, report issues, or just chat!",
            kind=ComponentKind.MISC,
            icon="discord",
            action=lambda *args: webbrowser.open("https://discord.gg/8Z65BR2") or "Opening in a new window...",
        ),
        LauncherEntry(
            id="after_dark_discord",
            display_name="Unrated/18+ Discord Server",
            description="Find unrated and 18+ games in the After Dark Discord server.",
            kind=ComponentKind.MISC,
            icon="discord",
            action=lambda *args: webbrowser.open("https://discord.gg/fqvNCCRsu4") or "Opening in a new window...",
        ),
        LauncherEntry(
            id="browse_files",
            display_name="Browse Files",
            description="Open the Archipelago installation folder in your file browser.",
            kind=ComponentKind.MISC,
            action=browse_files,
        ),
    ]
