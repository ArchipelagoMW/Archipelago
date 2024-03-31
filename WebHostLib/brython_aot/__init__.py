import logging
try:
    import importlib_resources as resources  # type: ignore[import-not-found]  # py3.8 only
except ImportError:
    from importlib import resources
from pathlib import Path
from typing import Optional, cast

import quickjs


class BrythonAOT:
    context: quickjs.Context

    # code to setup a minimal js environment that looks like a browser
    _environment_js = """
        console = {};
        console.log = console.warn = console.debug = print;
        Intl = {
            DateTimeFormat: class {
                constructor() {}
                format() { return ""; }
            },
        };
        self = window = {};
        self.navigator = {};
        self.language = "en";
        self.location = {
            "href": "",
            "origin": "",
            "pathname": "",
        };
        MutationObserver = function() { return { "observe": function(){} } }

        addEventListener = function() {};
        document = {
            "currentScript": {
                "src": ""
            },
            "querySelector": function(){},
            "querySelectorAll": function(){return []},
            "dispatchEvent": function(){},
            "getElementById": function(){},
            "createTextNode": function(){},
            "getElementsByTagName": function(){return [{"src": ""}]},
        };
        """

    @staticmethod
    def find_brython_js() -> Path:
        # NOTE: the api we use is not stable, and brython has an odd `Requires:`,
        # so it is recommended to vendor a copy of brython
        if __package__:
            res = cast(Path, resources.files(__package__) / "data" / "brython.js")
        else:
            res = Path(__file__).parent / "data" / "brython.js"
        if res.exists():
            return res
        try:
            # noinspection PyPackageRequirements
            import brython  # type: ignore[import-not-found]  # this is optional
            return cast(Path, resources.files(brython) / "data" / "brython.js")
        except ImportError:
            raise FileNotFoundError("brython.js")

    def __init__(self, brython_js_path: Optional[Path] = None):
        self.context = quickjs.Context()
        if not brython_js_path:
            try:
                brython_js_path = self.find_brython_js()
            except FileNotFoundError as ex:
                raise Exception("Could not locate brython.js. Please provide a path to it.") from ex
        # set-up minimal environment for brython
        self.context.add_callable("print", lambda *args: print(",".join(map(str, args))))
        self.context.eval(self._environment_js)
        # load brython.js
        logging.debug(f"Loading brython.js from {brython_js_path}")
        with brython_js_path.open() as f:
            self.context.eval(f.read())

    def transpile(self, source: str, name: str = "") -> str:
        import json
        if '"' in name or '/' in name:
            raise ValueError("Name has to be a valid python module name")
        cmd = f"""$B.py2js({json.dumps({
            "src": source,
            "filename": name,
            "imported": False,
        })}, {json.dumps(name)}).to_js()"""
        init = f"""__BRYTHON__.imported["{name.replace('.', '_')}"] = {{}}\n"""
        js = self.context.eval(cmd)
        assert isinstance(js, str)
        return init + js
