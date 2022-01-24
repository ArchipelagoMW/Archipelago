import os
import sys
import subprocess
import pkg_resources

requirements_files = {'requirements.txt'}

if sys.version_info < (3, 8, 6):
    raise RuntimeError("Incompatible Python Version. 3.8.7+ is supported.")

update_ran = getattr(sys, "frozen", False)  # don't run update if environment is frozen/compiled

if not update_ran:
    for entry in os.scandir("worlds"):
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
                    if line.startswith('https://'):
                        # extract name and version from url
                        wheel = line.split('/')[-1]
                        name, version, _ = wheel.split('-', 2)
                        line = f'{name}=={version}'
                    requirements = pkg_resources.parse_requirements(line)
                    for requirement in requirements:
                        requirement = str(requirement)
                        try:
                            pkg_resources.require(requirement)
                        except pkg_resources.ResolutionError:
                            if not yes:
                                import traceback
                                traceback.print_exc()
                                input(f'Requirement {requirement} is not satisfied, press enter to install it')
                            update_command()
                            return


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Install archipelago requirements')
    parser.add_argument('-y', '--yes', dest='yes', action='store_true', help='answer "yes" to all questions')
    parser.add_argument('-f', '--force', dest='force', action='store_true', help='force update')
    args = parser.parse_args()

    update(args.yes, args.force)
