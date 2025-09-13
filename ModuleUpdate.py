import os
import sys
import subprocess
import multiprocessing
import warnings


if sys.platform in ("win32", "darwin") and sys.version_info < (3, 11, 9):
    # Official micro version updates. This should match the number in docs/running from source.md.
    raise RuntimeError(f"Incompatible Python Version found: {sys.version_info}. Official 3.11.9+ is supported.")
elif sys.platform in ("win32", "darwin") and sys.version_info < (3, 11, 13):
    # There are known security issues, but no easy way to install fixed versions on Windows for testing.
    warnings.warn(f"Python Version {sys.version_info} has security issues. Don't use in production.")
elif sys.version_info < (3, 11, 0):
    # Other platforms may get security backports instead of micro updates, so the number is unreliable.
    raise RuntimeError(f"Incompatible Python Version found: {sys.version_info}. 3.11.0+ is supported.")

# don't run update if environment is frozen/compiled or if not the parent process (skip in subprocess)
_skip_update = bool(
    getattr(sys, "frozen", False) or 
    multiprocessing.parent_process() or 
    os.environ.get("SKIP_REQUIREMENTS_UPDATE", "").lower() in ("1", "true", "yes")
)
update_ran = _skip_update


class RequirementsSet(set):
    def add(self, e):
        global update_ran
        update_ran &= _skip_update
        super().add(e)

    def update(self, *s):
        global update_ran
        update_ran &= _skip_update
        super().update(*s)


local_dir = os.path.dirname(__file__)
requirements_files = RequirementsSet((os.path.join(local_dir, 'requirements.txt'),))

if not update_ran:
    for entry in os.scandir(os.path.join(local_dir, "worlds")):
        # skip .* (hidden / disabled) folders
        if not entry.name.startswith("."):
            if entry.is_dir():
                req_file = os.path.join(entry.path, "requirements.txt")
                if os.path.exists(req_file):
                    requirements_files.add(req_file)


def check_pip():
    # detect if pip is available
    try:
        import pip  # noqa: F401
    except ImportError:
        raise RuntimeError("pip not available. Please install pip.")


def confirm(msg: str):
    try:
        input(f"\n{msg}")
    except KeyboardInterrupt:
        print("\nAborting")
        sys.exit(1)


def update_command():
    check_pip()
    for file in requirements_files:
        subprocess.call([sys.executable, "-m", "pip", "install", "-r", file, "--upgrade"])


def install_pkg_resources(yes=False):
    try:
        import pkg_resources  # noqa: F401
    except (AttributeError, ImportError):
        check_pip()
        if not yes:
            confirm("pkg_resources not found, press enter to install it")
        subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", "setuptools>=75,<81"])


def update(yes: bool = False, force: bool = False) -> None:
    global update_ran
    if not update_ran:
        update_ran = True

        install_pkg_resources(yes=yes)
        import pkg_resources

        if force:
            update_command()
            return

        prev = ""  # if a line ends in \ we store here and merge later
        for req_file in requirements_files:
            path = os.path.join(os.path.dirname(sys.argv[0]), req_file)
            if not os.path.exists(path):
                path = os.path.join(os.path.dirname(__file__), req_file)
            with open(path) as requirementsfile:
                for line in requirementsfile:
                    if not line or line.lstrip(" \t")[0] == "#":
                        if not prev:
                            continue  # ignore comments
                        line = ""
                    elif line.rstrip("\r\n").endswith("\\"):
                        prev = prev + line.rstrip("\r\n")[:-1] + " "  # continue on next line
                        continue
                    line = prev + line
                    line = line.split("--hash=")[0]  # remove hashes from requirement for version checking
                    prev = ""
                    if line.startswith(("https://", "git+https://")):
                        # extract name and version for url
                        rest = line.split('/')[-1]
                        line = ""
                        if "#egg=" in rest:
                            # from egg info
                            rest, egg = rest.split("#egg=", 1)
                            egg = egg.split(";", 1)[0].rstrip()
                            if any(compare in egg for compare in ("==", ">=", ">", "<", "<=", "!=")):
                                warnings.warn(f"Specifying version as #egg={egg} will become unavailable in pip 25.0. "
                                              "Use name @ url#version instead.", DeprecationWarning)
                                line = egg
                        else:
                            egg = ""
                        if "@" in rest and not line:
                            raise ValueError("Can't deduce version from requirement")
                        elif not line:
                            # from filename
                            rest = rest.replace(".zip", "-").replace(".tar.gz", "-")
                            name, version, _ = rest.split("-", 2)
                            line = f'{egg or name}=={version}'
                    elif "@" in line and "#" in line:
                        # PEP 508 does not allow us to specify a version, so we use custom syntax
                        # name @ url#version ; marker
                        name, rest = line.split("@", 1)
                        version = rest.split("#", 1)[1].split(";", 1)[0].rstrip()
                        line = f"{name.rstrip()}=={version}"
                        if ";" in rest:  # keep marker
                            line += rest[rest.find(";"):]
                    requirements = pkg_resources.parse_requirements(line)
                    for requirement in map(str, requirements):
                        try:
                            pkg_resources.require(requirement)
                        except pkg_resources.ResolutionError:
                            if not yes:
                                import traceback
                                traceback.print_exc()
                                confirm(f"Requirement {requirement} is not satisfied, press enter to install it")
                            update_command()
                            return


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Install archipelago requirements')
    parser.add_argument('-y', '--yes', dest='yes', action='store_true', help='answer "yes" to all questions')
    parser.add_argument('-f', '--force', dest='force', action='store_true', help='force update')
    parser.add_argument('-a', '--append', nargs="*", dest='additional_requirements',
                        help='List paths to additional requirement files.')
    args = parser.parse_args()
    if args.additional_requirements:
        requirements_files.update(args.additional_requirements)
    update(args.yes, args.force)
