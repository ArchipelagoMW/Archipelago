"""
Archipelago launcher for bundled app.

* if run with APBP as argument, launch corresponding client.
* if run with executable as argument, run it passing argv[2:] as arguments
* if run without arguments, open launcher GUI
"""
import argparse
import os.path
import sys
import typing
import subprocess
import itertools
from Utils import is_frozen, user_path, local_path
from shutil import which
import shlex


is_linux = sys.platform.startswith('linux')
is_macos = sys.platform == 'darwin'
is_windows = sys.platform in ("win32", "cygwin", "msys")


sni_suffixes = ('.apz3', '.apm3', '.apsoe', '.aplttp', '.apsm', '.apsmz3')
patch_suffixes = {
    'SNIClient': sni_suffixes
}
_frozen_name_rewrites = {
    'MultiServer': 'ArchipelagoServer',
    'CommonClient': 'ArchipelagoTextClient',
}
_canonical_names = {
    'Server': 'MultiServer',
    'TextClient': 'CommonClient',
}
_cli_components = ('Generate', 'MultiServer')
_tools = {
    'Generate': 'Generate',
    'Host': 'MultiServer',
    'LttP Adjuster': 'LttPAdjuster',
    'OoT Adjuster': 'OoTAdjuster',
}
_clients = {
    'SNI Client': 'SNIClient',
    'Factorio Client': 'FactorioClient',
    'FF1 Client': 'FF1Client',
    'Minecraft Client': 'MinecraftClient',
    'Text Client': 'CommonClient',
}


def open_host_yaml():
    file = user_path('host.yaml')
    if is_linux:
        exe = which('sensible-editor') or which('gedit') or \
              which('xdg-open') or which('gnome-open') or which('kde-open')
        subprocess.Popen([exe, file])
    elif is_macos:
        exe = which("open")
        subprocess.Popen([exe, file])
    else:
        import webbrowser
        webbrowser.open(file)


def browse_files():
    file = user_path()
    if is_linux:
        exe = which('xdg-open') or which('gnome-open') or which('kde-open')
        subprocess.Popen([exe, file])
    elif is_macos:
        exe = which("open")
        subprocess.Popen([exe, file])
    else:
        import webbrowser
        webbrowser.open(file)


_funcs = {
    'Open host.yaml': open_host_yaml,
    'Browse Files': browse_files,
}


def identify(path: typing.Union[None, str]):
    if path is None:
        return None, None
    if path.endswith('.archipelago') or path.endswith('.zip'):
        return path, 'MultiServer'
    for component, suffixes in patch_suffixes.items():
        for suffix in suffixes:
            if path.endswith(suffix):
                return path, component
    return None, None if '/' in path or '\\' in path else path


def get_frozen_name(name: str) -> str:
    if name in _frozen_name_rewrites:
        return _frozen_name_rewrites[name]
    return f'Archipelago{name}'


def get_exe(component: str) -> str:
    if component.startswith('Archipelago'):
        component = component[11:]
    if component.endswith('.exe'):
        component = component[:-4]
    if component.endswith('.py'):
        component = component[:-3]
    if not component:
        return None
    if component in _canonical_names:
        component = _canonical_names[component]
    if is_frozen():
        suffix = '.exe' if is_windows else ''
        return [local_path(f'{get_frozen_name(component)}{suffix}')]
    else:
        return [sys.executable, local_path(f'{component}.py')]


def launch(exe, in_terminal=False):
    if in_terminal:
        if is_windows:
            subprocess.Popen(['start', *exe], shell=True)
            return
        elif is_linux:
            terminal = which('x-terminal-emulator') or which('gnome-terminal') or which('xterm')
            if terminal:
                subprocess.Popen([terminal, '-e', shlex.join(exe)])
                return
        elif is_macos:
            terminal = [which('open'), '-W', '-a', 'Terminal.app']
            subprocess.Popen([*terminal, *exe])
            return
    subprocess.Popen(exe)


def run_gui():
    if not sys.stdout:
        from kvui import App, ContainerLayout, GridLayout, Button, Label  # this kills stdout
    else:
        from kivy.app import App
        from kivy.uix.button import Button
        from kivy.uix.gridlayout import GridLayout as GridLayout
        from kivy.uix.floatlayout import FloatLayout as ContainerLayout
        from kivy.uix.label import Label

    class Launcher(App):
        base_title: str = "Archipelago Launcher"

        def __init__(self, ctx=None):
            self.title = self.base_title
            self.ctx = ctx
            self.icon = r"data/icon.png"
            super().__init__()

        def build(self):
            self.container = ContainerLayout()
            self.grid = GridLayout(cols=3)
            self.container.add_widget(self.grid)

            self.button_layout = self.grid  # make buttons fill the window
            for (tool, client, func) in itertools.zip_longest(_tools.items(), _clients.items(), _funcs.items()):
                # column 1
                if tool:
                    button = Button(text=tool[0])
                    button.component = tool[1]
                    button.bind(on_release=self.component_action)
                    self.button_layout.add_widget(button)
                else:
                    self.button_layout.add_widget(Label())
                # column 2
                if client:
                    button = Button(text=client[0])
                    button.component = client[1]
                    button.bind(on_press=self.component_action)
                    self.button_layout.add_widget(button)
                else:
                    self.button_layout.add_widget(Label())
                # column 3
                if func:
                    button = Button(text=func[0])
                    button.func = func[1]
                    button.bind(on_press=self.func_action)
                    self.button_layout.add_widget(button)
                else:
                    self.button_layout.add_widget(Label())

            return self.container

        def component_action(self, button):
            launch(get_exe(button.component), button.component in _cli_components)

        def func_action(self, button):
            button.func()

    Launcher().run()


def main(args: typing.Union[argparse.Namespace, dict] = {}):
    if type(args) is argparse.Namespace:
        args = {k: v for k, v in args._get_kwargs()}

    if "Patch|Game|Component" in args:
        file, component = identify(args["Patch|Game|Component"])
        if file:
            args['file'] = file
        if component:
            args['component'] = component

    if 'file' in args:
        subprocess.run([*get_exe(args['component']), args['file'], *args['args']])
    elif 'component' in args:
        subprocess.run([*get_exe(args['component']), *args['args']])
    else:
        run_gui()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Archipelago Launcher')
    parser.add_argument('Patch|Game|Component', type=str, nargs='?',
                        help="Pass either a patch file, a generated game or the name of a component to run.")
    parser.add_argument('args', nargs="*", help="Arguments to pass to component.")
    main(parser.parse_args())
