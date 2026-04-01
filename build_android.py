import os
import subprocess
import shutil

from jinja2 import Template

from Utils import __version__

def main():
    setup_py = "setup.py"
    setup_back = "setup.py.back"

    # Rename setup.py to setup.py.back if it exists
    if os.path.exists(setup_py):
        print(f"Renaming {setup_py} to {setup_back}...")
        shutil.move(setup_py, setup_back)

    try:
        # Use jinja to fill out the buildozer.spec.template to create buildozer.spec
        print("Creating buildozer.spec from template...")
        with open("buildozer.spec.template", "r", encoding="utf-8-sig") as f:
            template_text = f.read()

        template = Template(template_text)
        rendered = template.render(version_string=__version__)

        with open("buildozer.spec", "w", encoding="utf-8") as f:
            f.write(rendered)

        # Run docker with kivy/buildozer container. May need to be pulled manually first.
        user_profile = os.path.abspath(os.environ.get("USERPROFILE", os.path.expanduser("~")))
        pwd = os.getcwd()

        command = [
            "docker", "run", "--rm", "-i",
            "-v", f"{user_profile}/.buildozer:/home/user/.buildozer",
            "-v", f"{pwd}:/home/user/hostcwd",
            "kivy/buildozer", "android", "debug"
        ]

        print(f"Executing: {' '.join(command)}")
        # We pass 'y\n' to the subprocess to automatically handle the "Buildozer is running as root!" prompt.
        subprocess.run(command, input=b"y\n", check=True)

    except subprocess.CalledProcessError as e:
        print(f"Docker command failed with return code {e.returncode}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Rename setup.py.back to setup.py if it exists
        if os.path.exists(setup_back):
            print(f"Restoring {setup_py} from {setup_back}...")
            shutil.move(setup_back, setup_py)

if __name__ == "__main__":
    main()
