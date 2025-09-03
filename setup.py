import base64
import datetime
import io
import json
import os
import platform
import shutil
import subprocess
import sys
import sysconfig
import threading
import urllib.error
import urllib.request
import warnings
import zipfile
from collections.abc import Iterable, Sequence
from hashlib import sha3_512
from pathlib import Path


SNI_VERSION = "v0.0.100"  # change back to "latest" once tray icon issues are fixed


# This is a bit jank. We need cx-Freeze to be able to run anything from this script, so install it
requirement = 'cx-Freeze==8.0.0'
try:
    import pkg_resources
    try:
        pkg_resources.require(requirement)
        install_cx_freeze = False
    except pkg_resources.ResolutionError:
        install_cx_freeze = True
except (AttributeError, ImportError):
    install_cx_freeze = True
    pkg_resources = None  # type: ignore[assignment]

if install_cx_freeze:
    # check if pip is available
    try:
        import pip  # noqa: F401
    except ImportError:
        raise RuntimeError("pip not available. Please install pip.")
    # install and import cx_freeze
    if '--yes' not in sys.argv and '-y' not in sys.argv:
        input(f'Requirement {requirement} is not satisfied, press enter to install it')
    subprocess.call([sys.executable, '-m', 'pip', 'install', requirement, '--upgrade'])
    import pkg_resources

import cx_Freeze

# .build only exists if cx-Freeze is the right version, so we have to update/install that first before this line
import setuptools.command.build

if __name__ == "__main__":
    # need to run this early to import from Utils and Launcher
    # TODO: move stuff to not require this
    import ModuleUpdate
    ModuleUpdate.update(yes="--yes" in sys.argv or "-y" in sys.argv)

from worlds.LauncherComponents import components, icon_paths
from Utils import version_tuple, is_windows, is_linux
from Cython.Build import cythonize


non_apworlds: set[str] = {
    "A Link to the Past",
    "Adventure",
    "ArchipIDLE",
    "Archipelago",
    "Lufia II Ancient Cave",
    "Meritous",
    "Ocarina of Time",
    "Overcooked! 2",
    "Raft",
    "Sudoku",
    "Super Mario 64",
    "VVVVVV",
    "Wargroove",
}


def download_SNI() -> None:
    print("Updating SNI")
    machine_to_go = {
        "x86_64": "amd64",
        "aarch64": "arm64",
        "armv7l": "arm"
    }
    platform_name = platform.system().lower()
    machine_name = platform.machine().lower()
    # force amd64 on macos until we have universal2 sni, otherwise resolve to GOARCH
    machine_name = "universal" if platform_name == "darwin" else machine_to_go.get(machine_name, machine_name)
    sni_version_ref = "latest" if SNI_VERSION == "latest" else f"tags/{SNI_VERSION}"
    with urllib.request.urlopen(f"https://api.github.com/repos/alttpo/SNI/releases/{sni_version_ref}") as request:
        data = json.load(request)
    files = data["assets"]

    source_url = None

    for file in files:
        download_url: str = file["browser_download_url"]
        machine_match = download_url.rsplit("-", 1)[1].split(".", 1)[0] == machine_name
        if platform_name in download_url and machine_match:
            source_url = download_url
            # prefer "many" builds
            if "many" in download_url:
                break
            # prefer non-windows7 builds to get up-to-date dependencies
            if platform_name == "windows" and "windows7" not in download_url:
                break

    if source_url and source_url.endswith(".zip"):
        with urllib.request.urlopen(source_url) as download:
            with zipfile.ZipFile(io.BytesIO(download.read()), "r") as zf:
                for zf_member in zf.infolist():
                    zf.extract(zf_member, path="SNI")
        print(f"Downloaded SNI from {source_url}")

    elif source_url and (source_url.endswith(".tar.xz") or source_url.endswith(".tar.gz")):
        import tarfile
        mode = "r:xz" if source_url.endswith(".tar.xz") else "r:gz"
        with urllib.request.urlopen(source_url) as download:
            sni_dir = None
            with tarfile.open(fileobj=io.BytesIO(download.read()), mode=mode) as tf:
                for member in tf.getmembers():
                    if member.name.startswith("/") or "../" in member.name:
                        raise ValueError(f"Unexpected file '{member.name}' in {source_url}")
                    elif member.isdir() and not sni_dir:
                        sni_dir = member.name
                    elif member.isfile() and not sni_dir or sni_dir and not member.name.startswith(sni_dir):
                        raise ValueError(f"Expected folder before '{member.name}' in {source_url}")
                    elif member.isfile() and sni_dir:
                        tf.extract(member)
            # sadly SNI is in its own folder on non-windows, so we need to rename
            if not sni_dir:
                raise ValueError("Did not find SNI in archive")
            shutil.rmtree("SNI", True)
            os.rename(sni_dir, "SNI")
        print(f"Downloaded SNI from {source_url}")

    elif source_url:
        print(f"Don't know how to extract SNI from {source_url}")

    else:
        print(f"No SNI found for system spec {platform_name} {machine_name}")


signtool: str | None = None
try:
    with urllib.request.urlopen('http://192.168.206.4:12345/connector/status') as response:
        html = response.read()
    if b"status=OK\n" in html:
        signtool = (r'signtool sign /sha1 6df76fe776b82869a5693ddcb1b04589cffa6faf /fd sha256 /td sha256 '
                    r'/tr http://timestamp.digicert.com/ ')
        print("Using signtool")
except (ConnectionError, TimeoutError, urllib.error.URLError) as e:
    pass


build_platform = sysconfig.get_platform()
arch_folder = "exe.{platform}-{version}".format(platform=build_platform,
                                                version=sysconfig.get_python_version())
buildfolder = Path("build", arch_folder)
build_arch = build_platform.split('-')[-1] if '-' in build_platform else platform.machine()


# see Launcher.py on how to add scripts to setup.py
def resolve_icon(icon_name: str):
    base_path = icon_paths[icon_name]
    if is_windows:
        path, extension = os.path.splitext(base_path)
        ico_file = path + ".ico"
        assert os.path.exists(ico_file), f"ico counterpart of {base_path} should exist."
        return ico_file
    else:
        return base_path


exes = [
    cx_Freeze.Executable(
        script=f"{c.script_name}.py",
        target_name=c.frozen_name + (".exe" if is_windows else ""),
        icon=resolve_icon(c.icon),
        base="Win32GUI" if is_windows and not c.cli else None
    ) for c in components if c.script_name and c.frozen_name
]

if is_windows:
    # create a duplicate Launcher for Windows, which has a working stdout/stderr, for debugging and --help
    c = next(component for component in components if component.script_name == "Launcher")
    exes.append(cx_Freeze.Executable(
        script=f"{c.script_name}.py",
        target_name=f"{c.frozen_name}Debug.exe",
        icon=resolve_icon(c.icon),
    ))

extra_data = ["LICENSE", "data", "EnemizerCLI", "SNI"]
extra_libs = ["libssl.so", "libcrypto.so"] if is_linux else []


def remove_sprites_from_folder(folder: Path) -> None:
    if os.path.isdir(folder):
        for file in os.listdir(folder):
            if file != ".gitignore":
                os.remove(folder / file)


def _threaded_hash(filepath: str | Path) -> str:
    hasher = sha3_512()
    hasher.update(open(filepath, "rb").read())
    return base64.b85encode(hasher.digest()).decode()


# cx_Freeze's build command runs other commands. Override to accept --yes and store that.
class BuildCommand(setuptools.command.build.build):
    user_options = [
        ('yes', 'y', 'Answer "yes" to all questions.'),
    ]
    yes: bool
    last_yes: bool = False  # used by sub commands of build

    def initialize_options(self) -> None:
        super().initialize_options()
        type(self).last_yes = self.yes = False

    def finalize_options(self) -> None:
        super().finalize_options()
        type(self).last_yes = self.yes


# Override cx_Freeze's build_exe command for pre and post build steps
class BuildExeCommand(cx_Freeze.command.build_exe.build_exe):
    user_options = cx_Freeze.command.build_exe.build_exe.user_options + [
        ('yes', 'y', 'Answer "yes" to all questions.'),
        ('extra-data=', None, 'Additional files to add.'),
    ]
    yes: bool
    extra_data: Iterable[str]
    extra_libs: Iterable[str]  # work around broken include_files

    buildfolder: Path
    libfolder: Path
    library: Path
    buildtime: datetime.datetime

    def initialize_options(self) -> None:
        super().initialize_options()
        self.yes = BuildCommand.last_yes
        self.extra_data = []
        self.extra_libs = []

    def finalize_options(self) -> None:
        super().finalize_options()
        self.buildfolder = self.build_exe
        self.libfolder = Path(self.buildfolder, "lib")
        self.library = Path(self.libfolder, "library.zip")

    def installfile(self, path: Path, subpath: str | Path | None = None, keep_content: bool = False) -> None:
        folder = self.buildfolder
        if subpath:
            folder /= subpath
        print('copying', path, '->', folder)
        if path.is_dir():
            folder /= path.name
            if folder.is_dir() and not keep_content:
                shutil.rmtree(folder)
            shutil.copytree(path, folder, dirs_exist_ok=True)
        elif path.is_file():
            shutil.copy(path, folder)
        else:
            print('Warning,', path, 'not found')

    def create_manifest(self, create_hashes: bool = False) -> None:
        # Since the setup is now split into components and the manifest is not,
        # it makes most sense to just remove the hashes for now. Not aware of anyone using them.
        hashes = {}
        manifestpath = os.path.join(self.buildfolder, "manifest.json")
        if create_hashes:
            from concurrent.futures import ThreadPoolExecutor
            pool = ThreadPoolExecutor()
            for dirpath, dirnames, filenames in os.walk(self.buildfolder):
                for filename in filenames:
                    path = os.path.join(dirpath, filename)
                    hashes[os.path.relpath(path, start=self.buildfolder)] = pool.submit(_threaded_hash, path)

        import json
        manifest = {
            "buildtime": self.buildtime.isoformat(sep=" ", timespec="seconds"),
            "hashes": {path: hash.result() for path, hash in hashes.items()},
            "version": version_tuple}

        json.dump(manifest, open(manifestpath, "wt"), indent=4)
        print("Created Manifest")

    def run(self) -> None:
        # start downloading sni asap
        sni_thread = threading.Thread(target=download_SNI, name="SNI Downloader")
        sni_thread.start()

        # pre-build steps
        print(f"Outputting to: {self.buildfolder}")
        os.makedirs(self.buildfolder, exist_ok=True)
        import ModuleUpdate
        ModuleUpdate.update(yes=self.yes)

        # auto-build cython modules
        build_ext = self.distribution.get_command_obj("build_ext")
        build_ext.inplace = False
        self.run_command("build_ext")
        # find remains of previous in-place builds, try to delete and warn otherwise
        for path in build_ext.get_outputs():
            parts = os.path.split(path)[-1].split(".")
            pattern = parts[0] + ".*." + parts[-1]
            for match in Path().glob(pattern):
                try:
                    match.unlink()
                    print(f"Removed {match}")
                except Exception as ex:
                    warnings.warn(f"Could not delete old build output: {match}\n"
                                  f"{ex}\nPlease close all AP instances and delete manually.")

        # regular cx build
        self.buildtime = datetime.datetime.now(datetime.timezone.utc)
        super().run()

        # manually copy built modules to lib folder. cx_Freeze does not know they exist.
        for src in build_ext.get_outputs():
            print(f"copying {src} -> {self.libfolder}")
            shutil.copy(src, self.libfolder, follow_symlinks=False)

        # need to finish download before copying
        sni_thread.join()

        # include_files seems to not be done automatically. implement here
        for src, dst in self.include_files:
            print(f"copying {src} -> {self.buildfolder / dst}")
            shutil.copyfile(src, self.buildfolder / dst, follow_symlinks=False)

        # now that include_files is completely broken, run find_libs here
        for src, dst in find_libs(*self.extra_libs):
            print(f"copying {src} -> {self.buildfolder / dst}")
            shutil.copyfile(src, self.buildfolder / dst, follow_symlinks=False)

        # post build steps
        if is_windows:  # kivy_deps is win32 only, linux picks them up automatically
            from kivy_deps import sdl2, glew  # type: ignore
            for folder in sdl2.dep_bins + glew.dep_bins:
                shutil.copytree(folder, self.libfolder, dirs_exist_ok=True)
                print(f"copying {folder} -> {self.libfolder}")
            # windows needs Visual Studio C++ Redistributable
            # Installer works for x64 and arm64
            print("Downloading VC Redist")
            import certifi
            import ssl
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=certifi.where())
            with urllib.request.urlopen(r"https://aka.ms/vs/17/release/vc_redist.x64.exe",
                                        context=context) as download:
                vc_redist = download.read()
            print(f"Download complete, {len(vc_redist) / 1024 / 1024:.2f} MBytes downloaded.", )
            with open("VC_redist.x64.exe", "wb") as vc_file:
                vc_file.write(vc_redist)

        for data in self.extra_data:
            self.installfile(Path(data))

        # kivi data files
        import kivy  # type: ignore[import-untyped]
        shutil.copytree(os.path.join(os.path.dirname(kivy.__file__), "data"),
                        self.buildfolder / "data",
                        dirs_exist_ok=True)

        os.makedirs(self.buildfolder / "Players" / "Templates", exist_ok=True)
        from Options import generate_yaml_templates
        from worlds.AutoWorld import AutoWorldRegister
        assert not non_apworlds - set(AutoWorldRegister.world_types), \
            f"Unknown world {non_apworlds - set(AutoWorldRegister.world_types)} designated for .apworld"
        folders_to_remove: list[str] = []
        generate_yaml_templates(self.buildfolder / "Players" / "Templates", False)
        for worldname, worldtype in AutoWorldRegister.world_types.items():
            if worldname not in non_apworlds:
                file_name = os.path.split(os.path.dirname(worldtype.__file__))[1]
                world_directory = self.libfolder / "worlds" / file_name
                # this method creates an apworld that cannot be moved to a different OS or minor python version,
                # which should be ok
                with zipfile.ZipFile(self.libfolder / "worlds" / (file_name + ".apworld"), "x", zipfile.ZIP_DEFLATED,
                                     compresslevel=9) as zf:
                    for path in world_directory.rglob("*.*"):
                        relative_path = os.path.join(*path.parts[path.parts.index("worlds")+1:])
                        zf.write(path, relative_path)
                    folders_to_remove.append(file_name)
                shutil.rmtree(world_directory)
        shutil.copyfile("meta.yaml", self.buildfolder / "Players" / "Templates" / "meta.yaml")
        try:
            from maseya import z3pr  # type: ignore[import-untyped]
        except ImportError:
            print("Maseya Palette Shuffle not found, skipping data files.")
        else:
            # maseya Palette Shuffle exists and needs its data files
            print("Maseya Palette Shuffle found, including data files...")
            file = z3pr.__file__
            self.installfile(Path(os.path.dirname(file)) / "data", keep_content=True)

        if signtool:
            for exe in self.distribution.executables:
                print(f"Signing {exe.target_name}")
                os.system(signtool + os.path.join(self.buildfolder, exe.target_name))
            print("Signing SNI")
            os.system(signtool + os.path.join(self.buildfolder, "SNI", "SNI.exe"))
            print("Signing OoT Utils")
            for exe_path in (("Compress", "Compress.exe"), ("Decompress", "Decompress.exe")):
                os.system(signtool + os.path.join(self.buildfolder, "lib", "worlds", "oot", "data", *exe_path))

        remove_sprites_from_folder(self.buildfolder / "data" / "sprites" / "alttpr")
        remove_sprites_from_folder(self.buildfolder / "data" / "sprites" / "alttp" / "remote")

        self.create_manifest()

        if is_windows:
            # Inno setup stuff
            with open("setup.ini", "w") as f:
                min_supported_windows = "6.2.9200"
                f.write(f"[Data]\nsource_path={self.buildfolder}\nmin_windows={min_supported_windows}\n")
            with open("installdelete.iss", "w") as f:
                f.writelines("Type: filesandordirs; Name: \"{app}\\lib\\worlds\\"+world_directory+"\"\n"
                             for world_directory in folders_to_remove)
        else:
            # make sure extra programs are executable
            enemizer_exe = self.buildfolder / 'EnemizerCLI/EnemizerCLI.Core'
            sni_exe = self.buildfolder / 'SNI/sni'
            extra_exes = (enemizer_exe, sni_exe)
            for extra_exe in extra_exes:
                if extra_exe.is_file():
                    extra_exe.chmod(0o755)


class AppImageCommand(setuptools.Command):
    description = "build an app image from build output"
    user_options = [
        ("build-folder=", None, "Folder to convert to AppImage."),
        ("dist-file=", None, "AppImage output file."),
        ("app-dir=", None, "Folder to use for packaging."),
        ("app-icon=", None, "The icon to use for the AppImage."),
        ("app-exec=", None, "The application to run inside the image."),
        ("yes", "y", 'Answer "yes" to all questions.'),
    ]
    build_folder: Path | None
    dist_file: Path | None
    app_dir: Path | None
    app_name: str
    app_exec: Path | None
    app_icon: Path | None  # source file
    app_id: str  # lower case name, used for icon and .desktop
    yes: bool

    def write_desktop(self) -> None:
        assert self.app_dir, "Invalid app_dir"
        desktop_filename = self.app_dir / f"{self.app_id}.desktop"
        with open(desktop_filename, 'w', encoding="utf-8") as f:
            f.write("\n".join((
                "[Desktop Entry]",
                f'Name={self.app_name}',
                f'Exec={self.app_exec}',
                "Type=Application",
                "Categories=Game",
                f'Icon={self.app_id}',
                ''
            )))
        desktop_filename.chmod(0o755)

    def write_launcher(self, default_exe: Path) -> None:
        assert self.app_dir, "Invalid app_dir"
        launcher_filename = self.app_dir / "AppRun"
        with open(launcher_filename, 'w', encoding="utf-8") as f:
            f.write(f"""#!/bin/sh
exe="{default_exe}"
match="${{1#--executable=}}"
if [ "${{#match}}" -lt "${{#1}}" ]; then
    exe="$match"
    shift
elif [ "$1" = "-executable" ] || [ "$1" = "--executable" ]; then
    exe="$2"
    shift; shift
fi
tmp="${{exe#*/}}"
if [ ! "${{#tmp}}" -lt "${{#exe}}" ]; then
    exe="{default_exe.parent}/$exe"
fi
export LD_LIBRARY_PATH="${{LD_LIBRARY_PATH:+$LD_LIBRARY_PATH:}}$APPDIR/{default_exe.parent}/lib"
$APPDIR/$exe "$@"
""")
        launcher_filename.chmod(0o755)

    def install_icon(self, src: Path, name: str | None = None, symlink: Path | None = None) -> None:
        assert self.app_dir, "Invalid app_dir"
        try:
            from PIL import Image
        except ModuleNotFoundError:
            if not self.yes:
                input("Requirement PIL is not satisfied, press enter to install it")
            subprocess.call([sys.executable, '-m', 'pip', 'install', 'Pillow', '--upgrade'])
            from PIL import Image
        im = Image.open(src)
        res, _ = im.size

        if not name:
            name = src.stem
        ext = src.suffix
        dest_dir = Path(self.app_dir / f'usr/share/icons/hicolor/{res}x{res}/apps')
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_file = dest_dir / f'{name}{ext}'
        shutil.copy(src, dest_file)
        if symlink:
            symlink.symlink_to(dest_file.relative_to(symlink.parent))

    def initialize_options(self) -> None:
        assert self.distribution.metadata.name
        self.build_folder = None
        self.app_dir = None
        self.app_name = self.distribution.metadata.name
        self.app_icon = self.distribution.executables[0].icon
        self.app_exec = Path('opt/{app_name}/{exe}'.format(
            app_name=self.distribution.metadata.name, exe=self.distribution.executables[0].target_name
        ))
        self.dist_file = Path("dist", "{app_name}_{app_version}_{platform}.AppImage".format(
            app_name=self.distribution.metadata.name, app_version=self.distribution.metadata.version,
            platform=sysconfig.get_platform()
        ))
        self.yes = False

    def finalize_options(self) -> None:
        assert self.build_folder
        if not self.app_dir:
            self.app_dir = self.build_folder.parent / "AppDir"
        self.app_id = self.app_name.lower()

    def run(self) -> None:
        assert self.build_folder and self.dist_file, "Command not properly set up"
        assert (
            self.app_icon and self.app_id and self.app_dir and self.app_exec and self.app_name
        ), "AppImageCommand not properly set up"
        self.dist_file.parent.mkdir(parents=True, exist_ok=True)
        if self.app_dir.is_dir():
            shutil.rmtree(self.app_dir)
        self.app_dir.mkdir(parents=True)
        opt_dir = self.app_dir / "opt" / self.app_name
        shutil.copytree(self.build_folder, opt_dir)
        root_icon = self.app_dir / f'{self.app_id}{self.app_icon.suffix}'
        self.install_icon(self.app_icon, self.app_id, symlink=root_icon)
        shutil.copy(root_icon, self.app_dir / '.DirIcon')
        self.write_desktop()
        self.write_launcher(self.app_exec)
        print(f'{self.app_dir} -> {self.dist_file}')
        subprocess.call(f'ARCH={build_arch} ./appimagetool -n "{self.app_dir}" "{self.dist_file}"', shell=True)


def find_libs(*args: str) -> Sequence[tuple[str, str]]:
    """Try to find system libraries to be included."""
    if not args:
        return []

    arch = build_arch.replace('_', '-')
    libc = 'libc6'  # we currently don't support musl

    def parse(line: str) -> tuple[tuple[str, str, str], str]:
        lib, path = line.strip().split(' => ')
        lib, typ = lib.split(' ', 1)
        for test_arch in ('x86-64', 'i386', 'aarch64'):
            if test_arch in typ:
                lib_arch = test_arch
                break
        else:
            lib_arch = ''
        for test_libc in ('libc6',):
            if test_libc in typ:
                lib_libc = test_libc
                break
        else:
            lib_libc = ''
        return (lib, lib_arch, lib_libc), path

    if not hasattr(find_libs, "cache"):
        ldconfig = shutil.which("ldconfig")
        assert ldconfig, "Make sure ldconfig is in PATH"
        data = subprocess.run([ldconfig, "-p"], capture_output=True, text=True).stdout.split("\n")[1:]
        find_libs.cache = {  # type: ignore[attr-defined]
            k: v for k, v in (parse(line) for line in data if "=>" in line)
        }

    def find_lib(lib: str, arch: str, libc: str) -> str | None:
        cache: dict[tuple[str, str, str], str] = getattr(find_libs, "cache")
        for k, v in cache.items():
            if k == (lib, arch, libc):
                return v
        for k, v, in cache.items():
            if k[0].startswith(lib) and k[1] == arch and k[2] == libc:
                return v
        return None

    res: list[tuple[str, str]] = []
    for arg in args:
        # try exact match, empty libc, empty arch, empty arch and libc
        file = find_lib(arg, arch, libc)
        file = file or find_lib(arg, arch, '')
        file = file or find_lib(arg, '', libc)
        file = file or find_lib(arg, '', '')
        if not file:
            raise ValueError(f"Could not find lib {arg}")
        # resolve symlinks
        for n in range(0, 5):
            res.append((file, os.path.join('lib', os.path.basename(file))))
            if not os.path.islink(file):
                break
            dirname = os.path.dirname(file)
            file = os.readlink(file)
            if not os.path.isabs(file):
                file = os.path.join(dirname, file)
    return res


cx_Freeze.setup(
    name="Archipelago",
    version=f"{version_tuple.major}.{version_tuple.minor}.{version_tuple.build}",
    description="Archipelago",
    executables=exes,
    ext_modules=cythonize("_speedups.pyx"),
    options={
        "build_exe": {
            "packages": ["worlds", "kivy", "cymem", "websockets", "kivymd"],
            "includes": [],
            "excludes": ["numpy", "Cython", "PySide2", "PIL",
                         "pandas"],
            "zip_includes": [],
            "zip_include_packages": ["*"],
            "zip_exclude_packages": ["worlds", "sc2", "kivymd"],
            "include_files": [],  # broken in cx 6.14.0, we use more special sauce now
            "include_msvcr": False,
            "replace_paths": ["*."],
            "optimize": 1,
            "build_exe": buildfolder,
            "extra_data": extra_data,
            "extra_libs": extra_libs,
            "bin_includes": ["libffi.so", "libcrypt.so"] if is_linux else []
        },
        "bdist_appimage": {
           "build_folder": buildfolder,
        },
    },
    # override commands to get custom stuff in
    cmdclass={
        "build": BuildCommand,
        "build_exe": BuildExeCommand,
        "bdist_appimage": AppImageCommand,
    },
)
