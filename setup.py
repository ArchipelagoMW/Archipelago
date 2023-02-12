import base64
import datetime
import os
import platform
import shutil
import sys
import sysconfig
import typing
import zipfile
from collections.abc import Iterable
from hashlib import sha3_512
from pathlib import Path
import subprocess
import pkg_resources

# This is a bit jank. We need cx-Freeze to be able to run anything from this script, so install it
try:
    requirement = 'cx-Freeze>=6.14.1'
    pkg_resources.require(requirement)
    import cx_Freeze
except pkg_resources.ResolutionError:
    if '--yes' not in sys.argv and '-y' not in sys.argv:
        input(f'Requirement {requirement} is not satisfied, press enter to install it')
    subprocess.call([sys.executable, '-m', 'pip', 'install', requirement, '--upgrade'])
    import cx_Freeze

# .build only exists if cx-Freeze is the right version, so we have to update/install that first before this line
import setuptools.command.build

if __name__ == "__main__":
    # need to run this early to import from Utils and Launcher
    # TODO: move stuff to not require this
    import ModuleUpdate
    ModuleUpdate.update(yes="--yes" in sys.argv or "-y" in sys.argv)
    ModuleUpdate.update_ran = False  # restore for later

from Launcher import components, icon_paths
from Utils import version_tuple, is_windows, is_linux


# On  Python < 3.10 LogicMixin is not currently supported.
apworlds: set = {
    "Subnautica",
    "Factorio",
    "Rogue Legacy",
    "Donkey Kong Country 3",
    "Super Mario World",
}

if os.path.exists("X:/pw.txt"):
    print("Using signtool")
    with open("X:/pw.txt", encoding="utf-8-sig") as f:
        pw = f.read()
    signtool = r'signtool sign /f X:/_SITS_Zertifikat_.pfx /p "' + pw + \
               r'" /fd sha256 /tr http://timestamp.digicert.com/ '
else:
    signtool = None


build_platform = sysconfig.get_platform()
arch_folder = "exe.{platform}-{version}".format(platform=build_platform,
                                                version=sysconfig.get_python_version())
buildfolder = Path("build", arch_folder)
build_arch = build_platform.split('-')[-1] if '-' in build_platform else platform.machine()


# see Launcher.py on how to add scripts to setup.py
exes = [
    cx_Freeze.Executable(
        script=f'{c.script_name}.py',
        target_name=c.frozen_name + (".exe" if is_windows else ""),
        icon=icon_paths[c.icon],
        base="Win32GUI" if is_windows and not c.cli else None
    ) for c in components if c.script_name
]

extra_data = ["LICENSE", "data", "EnemizerCLI", "host.yaml", "SNI"]
extra_libs = ["libssl.so", "libcrypto.so"] if is_linux else []


def remove_sprites_from_folder(folder):
    for file in os.listdir(folder):
        if file != ".gitignore":
            os.remove(folder / file)


def _threaded_hash(filepath):
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

    def initialize_options(self):
        super().initialize_options()
        type(self).last_yes = self.yes = False

    def finalize_options(self):
        super().finalize_options()
        type(self).last_yes = self.yes


# Override cx_Freeze's build_exe command for pre and post build steps
class BuildExeCommand(cx_Freeze.command.build_exe.BuildEXE):
    user_options = cx_Freeze.command.build_exe.BuildEXE.user_options + [
        ('yes', 'y', 'Answer "yes" to all questions.'),
        ('extra-data=', None, 'Additional files to add.'),
    ]
    yes: bool
    extra_data: Iterable  # [any] not available in 3.8
    extra_libs: Iterable  # work around broken include_files

    buildfolder: Path
    libfolder: Path
    library: Path
    buildtime: datetime.datetime

    def initialize_options(self):
        super().initialize_options()
        self.yes = BuildCommand.last_yes
        self.extra_data = []
        self.extra_libs = []

    def finalize_options(self):
        super().finalize_options()
        self.buildfolder = self.build_exe
        self.libfolder = Path(self.buildfolder, "lib")
        self.library = Path(self.libfolder, "library.zip")

    def installfile(self, path, subpath=None, keep_content: bool = False):
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

    def create_manifest(self, create_hashes=False):
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

    def run(self):
        # pre build steps
        print(f"Outputting to: {self.buildfolder}")
        os.makedirs(self.buildfolder, exist_ok=True)
        import ModuleUpdate
        ModuleUpdate.requirements_files.add(os.path.join("WebHostLib", "requirements.txt"))
        ModuleUpdate.update(yes=self.yes)

        # regular cx build
        self.buildtime = datetime.datetime.utcnow()
        super().run()

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
            from kivy_deps import sdl2, glew
            for folder in sdl2.dep_bins + glew.dep_bins:
                shutil.copytree(folder, self.libfolder, dirs_exist_ok=True)
                print(f"copying {folder} -> {self.libfolder}")

        for data in self.extra_data:
            self.installfile(Path(data))

        # kivi data files
        import kivy
        shutil.copytree(os.path.join(os.path.dirname(kivy.__file__), "data"),
                        self.buildfolder / "data",
                        dirs_exist_ok=True)

        os.makedirs(self.buildfolder / "Players" / "Templates", exist_ok=True)
        from WebHostLib.options import create
        create()
        from worlds.AutoWorld import AutoWorldRegister
        assert not apworlds - set(AutoWorldRegister.world_types), "Unknown world designated for .apworld"
        folders_to_remove: typing.List[str] = []
        for worldname, worldtype in AutoWorldRegister.world_types.items():
            if not worldtype.hidden:
                file_name = worldname+".yaml"
                shutil.copyfile(os.path.join("WebHostLib", "static", "generated", "configs", file_name),
                                self.buildfolder / "Players" / "Templates" / file_name)
            if worldname in apworlds:
                file_name = os.path.split(os.path.dirname(worldtype.__file__))[1]
                world_directory = self.libfolder / "worlds" / file_name
                # this method creates an apworld that cannot be moved to a different OS or minor python version,
                # which should be ok
                with zipfile.ZipFile(self.libfolder / "worlds" / (file_name + ".apworld"), "x", zipfile.ZIP_DEFLATED,
                                     compresslevel=9) as zf:
                    entry: os.DirEntry
                    for path in world_directory.rglob("*.*"):
                        relative_path = os.path.join(*path.parts[path.parts.index("worlds")+1:])
                        zf.write(path, relative_path)
                    folders_to_remove.append(file_name)
                shutil.rmtree(world_directory)
        shutil.copyfile("meta.yaml", self.buildfolder / "Players" / "Templates" / "meta.yaml")
        # TODO: fix LttP options one day
        shutil.copyfile("playerSettings.yaml", self.buildfolder / "Players" / "Templates" / "A Link to the Past.yaml")
        try:
            from maseya import z3pr
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
            print(f"Signing SNI")
            os.system(signtool + os.path.join(self.buildfolder, "SNI", "SNI.exe"))
            print(f"Signing OoT Utils")
            for exe_path in (("Compress", "Compress.exe"), ("Decompress", "Decompress.exe")):
                os.system(signtool + os.path.join(self.buildfolder, "lib", "worlds", "oot", "data", *exe_path))

        remove_sprites_from_folder(self.buildfolder / "data" / "sprites" / "alttpr")

        self.create_manifest()

        if is_windows:
            # Inno setup stuff
            with open("setup.ini", "w") as f:
                min_supported_windows = "6.2.9200" if sys.version_info > (3, 9) else "6.0.6000"
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
            # rewrite windows-specific things in host.yaml
            host_yaml = self.buildfolder / 'host.yaml'
            with host_yaml.open('r+b') as f:
                data = f.read()
                data = data.replace(b'factorio\\\\bin\\\\x64\\\\factorio', b'factorio/bin/x64/factorio')
                f.seek(0, os.SEEK_SET)
                f.write(data)
                f.truncate()


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
    build_folder: typing.Optional[Path]
    dist_file: typing.Optional[Path]
    app_dir: typing.Optional[Path]
    app_name: str
    app_exec: typing.Optional[Path]
    app_icon: typing.Optional[Path]  # source file
    app_id: str  # lower case name, used for icon and .desktop
    yes: bool

    def write_desktop(self):
        desktop_filename = self.app_dir / f'{self.app_id}.desktop'
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

    def write_launcher(self, default_exe: Path):
        launcher_filename = self.app_dir / f'AppRun'
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
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$APPDIR/{default_exe.parent}/lib"
$APPDIR/$exe "$@"
""")
        launcher_filename.chmod(0o755)

    def install_icon(self, src: Path, name: typing.Optional[str] = None, symlink: typing.Optional[Path] = None):
        try:
            from PIL import Image
        except ModuleNotFoundError:
            if not self.yes:
                input(f'Requirement PIL is not satisfied, press enter to install it')
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

    def initialize_options(self):
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

    def finalize_options(self):
        if not self.app_dir:
            self.app_dir = self.build_folder.parent / "AppDir"
        self.app_id = self.app_name.lower()

    def run(self):
        self.dist_file.parent.mkdir(parents=True, exist_ok=True)
        if self.app_dir.is_dir():
            shutil.rmtree(self.app_dir)
        self.app_dir.mkdir(parents=True)
        opt_dir = self.app_dir / "opt" / self.distribution.metadata.name
        shutil.copytree(self.build_folder, opt_dir)
        root_icon = self.app_dir / f'{self.app_id}{self.app_icon.suffix}'
        self.install_icon(self.app_icon, self.app_id, symlink=root_icon)
        shutil.copy(root_icon, self.app_dir / '.DirIcon')
        self.write_desktop()
        self.write_launcher(self.app_exec)
        print(f'{self.app_dir} -> {self.dist_file}')
        subprocess.call(f'ARCH={build_arch} ./appimagetool -n "{self.app_dir}" "{self.dist_file}"', shell=True)


def find_libs(*args: str) -> typing.Sequence[typing.Tuple[str, str]]:
    """Try to find system libraries to be included."""
    if not args:
        return []

    arch = build_arch.replace('_', '-')
    libc = 'libc6'  # we currently don't support musl

    def parse(line):
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
        data = subprocess.run([shutil.which('ldconfig'), '-p'], capture_output=True, text=True).stdout.split('\n')[1:]
        find_libs.cache = {k: v for k, v in (parse(line) for line in data if '=>' in line)}

    def find_lib(lib, arch, libc):
        for k, v in find_libs.cache.items():
            if k == (lib, arch, libc):
                return v
        for k, v, in find_libs.cache.items():
            if k[0].startswith(lib) and k[1] == arch and k[2] == libc:
                return v
        return None

    res = []
    for arg in args:
        # try exact match, empty libc, empty arch, empty arch and libc
        file = find_lib(arg, arch, libc)
        file = file or find_lib(arg, arch, '')
        file = file or find_lib(arg, '', libc)
        file = file or find_lib(arg, '', '')
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
    ext_modules=[],  # required to disable auto-discovery with setuptools>=61
    options={
        "build_exe": {
            "packages": ["websockets", "worlds", "kivy"],
            "includes": [],
            "excludes": ["numpy", "Cython", "PySide2", "PIL",
                         "pandas"],
            "zip_include_packages": ["*"],
            "zip_exclude_packages": ["worlds", "sc2"],
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
