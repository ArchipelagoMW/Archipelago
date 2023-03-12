import os
import sys
import subprocess
import pkg_resources
import warnings

local_dir = os.path.dirname(__file__)
requirements_files = {os.path.join(local_dir, 'requirements.txt')}

if sys.version_info < (3, 8, 6):
    raise RuntimeError("Incompatible Python Version. 3.8.7+ is supported.")

update_ran = getattr(sys, "frozen", False)  # don't run update if environment is frozen/compiled

if not update_ran:
    for entry in os.scandir(os.path.join(local_dir, "worlds")):
        # skip .* (hidden / disabled) folders
        if not entry.name.startswith("."):
            if entry.is_dir():
                req_file = os.path.join(entry.path, "requirements.txt")
                if os.path.exists(req_file):
                    requirements_files.add(req_file)


def update_command():
    for file in requirements_files:
        subprocess.call([sys.executable, '-m', 'pip', 'install', '-r', file, '--upgrade'])


def update(yes=False, force=False):
    global update_ran
    if not update_ran:
        update_ran = True
        if force:
            update_command()
            return
        for req_file in requirements_files:
            path = os.path.join(os.path.dirname(sys.argv[0]), req_file)
            if not os.path.exists(path):
                path = os.path.join(os.path.dirname(__file__), req_file)
            with open(path) as requirementsfile:
                for line in requirementsfile:
                    if not line or line[0] == "#":
                        continue  # ignore comments
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
                                try:
                                    input(f"\nRequirement {requirement} is not satisfied, press enter to install it")
                                except KeyboardInterrupt:
                                    print("\nAborting")
                                    sys.exit(1)
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
