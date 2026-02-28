# This file is auto-generated! DO NOT MODIFY BY HAND!

from pathlib import Path

requirements_name = "som"
requirements_hash = "UmnaUEyBXa-K"
requirements_mods = ("pysomr",)
# noinspection DuplicatedCode
include_py = {
    "cp311": ["cp311"],
    "cp312": ["cp312"],
    "cp313": ["cp313"],
    "cp314": ["cp314"],
}
include_plat = {
    "darwin": ["macosx"],
    "linux-gnu": ["manylinux"],
    "win": ["win"],
}
include_arch = {
    "darwin": ["universal2"],
    "linux-gnu": ["x86_64", "aarch64"],
    "win": ["amd64", "arm64"],
}


# noinspection DuplicatedCode
def _install(root: str) -> None:
    import platform
    import sys
    import sysconfig

    import platformdirs

    py_impl = platform.python_implementation()
    if py_impl not in ("CPython",):
        raise ValueError(f'Unsupported python "{py_impl}" for installation of {requirements_name} packages')
    py_impl_short = {"CPython": "cp"}[py_impl]  # There is also "py" for pure Python, but we don't care for now
    py_ver = py_impl_short + sysconfig.get_config_var("py_version_nodot")
    nodot_plat = sysconfig.get_config_var("py_version_nodot_plat").split("-", 1)[0]
    py_abi_number = nodot_plat if nodot_plat else sysconfig.get_config_var("SOABI").split("-", 2)[1]
    py_abi = py_impl_short + py_abi_number
    py_arch = sysconfig.get_platform().split("-")[-1]  # macOS always gives "universal2", which is hopefully fine
    multiarch = sysconfig.get_config_var("MULTIARCH")  # darwin for macOS
    py_os = multiarch.replace(py_arch + "-", "") if multiarch else sysconfig.get_platform().split("-")[0]
    # alternatively try to extract from SOABI or guess from platform.libc_ver(); NOTE: we want linux-gnu vs. linux-musl

    if py_os not in include_plat or py_os not in include_arch or py_arch not in include_arch[py_os]:
        raise ValueError(f"Unsupported platform {py_os}-{py_arch} for installation of {requirements_name} packages")

    # detect if out assumption of extension naming is correct so we can filter what to extract
    ext_suffix = sysconfig.get_config_var("EXT_SUFFIX")
    suffix_filter: str
    if py_os == "win" and ext_suffix == f".{py_abi}-win_{py_arch}.pyd":
        suffix_filter = "*.*-win_*.pyd"
    elif py_os == "darwin" and ext_suffix == f".{py_impl.lower()}-{py_abi_number}-darwin.so":
        suffix_filter = "*.*-*-darwin.so"
    elif py_os == "linux-gnu" and ext_suffix == f".{py_impl.lower()}-{py_abi_number}-{py_arch}-linux-gnu.so":
        suffix_filter = "*.*-*-*-linux-gnu.so"
    else:
        suffix_filter = ""

    # NOTE: we expect that files for different ABI have non-conflicting names on all supported platforms
    print(f"Installing vendored packages for {requirements_name} for {py_ver}-{py_abi} on {py_os}-{py_arch}")
    # TODO: logging?
    base_install_path = platformdirs.user_cache_path("Archipelago") / "vendored" / requirements_name / requirements_hash
    install_path = base_install_path / f"{py_os}-{py_arch}"
    identifier_path = base_install_path / f"{py_os}-{py_arch}-{py_ver}-{py_abi}.installed"
    if not install_path.is_dir() or not identifier_path.is_file():
        import importlib.resources
        from shutil import copyfileobj

        if not suffix_filter:
            print("Can not filter files by ext_suffix. May extract more than required!")  # TODO: logging?

        # noinspection DuplicatedCode
        def extract(res: "importlib.resources.abc.Traversable", dest_folder: Path) -> None:
            dest = dest_folder / res.name
            if res.is_dir():
                dest.mkdir(parents=True, exist_ok=True)
                for sub in res.iterdir():
                    extract(sub, dest)
            elif res.name.endswith(ext_suffix) or not suffix_filter or not dest.match(suffix_filter):
                assert res.is_file()
                with res.open("rb") as source_file:
                    with dest.open("wb") as dest_file:
                        copyfileobj(source_file, dest_file)

        files = importlib.resources.files(root)
        assert files.is_dir()
        for mod_name in requirements_mods:
            any_dir = files / mod_name / "any" / "any"
            mod_dir = files / mod_name / py_os / py_arch
            assert any_dir.is_dir()
            assert mod_dir.is_dir()
            for item in any_dir.iterdir():
                extract(item, install_path)
            for item in mod_dir.iterdir():
                extract(item, install_path)

        with open(identifier_path, "wb"):
            pass

    sys.path.insert(0, str(install_path))


def install() -> None:
    _install(__name__)
