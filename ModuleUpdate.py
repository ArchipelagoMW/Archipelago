import os
import sys
import subprocess
import importlib

update_ran = hasattr(sys, "frozen") and getattr(sys, "frozen")  # don't run update if environment is frozen/compiled


def update_command():
    subprocess.call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '--upgrade'])


naming_specialties = {"PyYAML": "yaml"}  # PyYAML is imported as the name yaml


def update():
    global update_ran
    if not update_ran:
        update_ran = True
        with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as requirementsfile:
            for line in requirementsfile.readlines():
                module, remoteversion = line.split(">=")
                module = naming_specialties.get(module, module)
                try:
                    module = importlib.import_module(module)
                except:
                    import traceback
                    traceback.print_exc()
                    input(f'Required python module {module} not found, press enter to install it')
                    update_command()
                else:
                    if hasattr(module, "__version__"):
                        module_version = module.__version__
                        module = module.__name__ #also unloads the module to make it writable
                        if type(module_version) == str:
                            module_version = tuple(int(part.strip()) for part in module_version.split("."))
                        remoteversion = tuple(int(part.strip()) for part in remoteversion.split("."))
                        if module_version < remoteversion:
                            input(f'Required python module {module} is outdated ({module_version}<{remoteversion}), press enter to upgrade it')
                            update_command()

if __name__ == "__main__":
    update()
