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


def update():
    global update_ran
    if not update_ran:
        update_ran = True
        for req_file in requirements_files:
            path = os.path.join(os.path.dirname(sys.argv[0]), req_file)
            if not os.path.exists(path):
                path = os.path.join(os.path.dirname(__file__), req_file)
            with open(path) as requirementsfile:
                requirements = pkg_resources.parse_requirements(requirementsfile)
                for requirement in requirements:
                    requirement = str(requirement)
                    try:
                        pkg_resources.require(requirement)
                    except pkg_resources.ResolutionError:
                        import traceback
                        traceback.print_exc()
                        input(f'Requirement {requirement} is not satisfied, press enter to install it')
                        update_command()
                        return


if __name__ == "__main__":
    update()
