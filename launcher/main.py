from __future__ import annotations

import argparse
import logging
from collections.abc import Sequence

from core import Err, Ok, ResolutionKind

from .components import run_component
from .components.functions import update_settings
from .resolution import resolve_input, to_launcher_entry
from .runtime import join_processes


def main(args: argparse.Namespace | dict | None = None) -> None:
    """Run the launcher from parsed args or a compatible dict.

    Example::

        main({"Patch|Game|Component|url": "Text Client", "args": ()})
    """

    if isinstance(args, argparse.Namespace):
        normalized_args = {key: value for key, value in args._get_kwargs()}
    elif not args:
        normalized_args = {}
    else:
        normalized_args = dict(args)

    normalized_args.setdefault("update_settings", False)
    normalized_args.setdefault("args", ())

    if normalized_args["update_settings"]:
        update_settings()
        return

    path = normalized_args.get("Patch|Game|Component|url")
    if path is not None:
        logging.info("Launcher resolving input: %s", path)
        result = resolve_input(path)
        if isinstance(result, Err):
            logging.warning(result.error.message)
            return

        assert isinstance(result, Ok)
        resolved = result.value.resolved
        logging.info(
            "Launcher resolved input '%s' to kind=%s component_id=%s file_path=%s",
            path,
            resolved.kind,
            resolved.component_id,
            resolved.file_path,
        )
        launch_args = tuple(normalized_args.get("args", ()))

        uri_components = resolved.launch_components or resolved.candidates
        if resolved.kind is ResolutionKind.URI and uri_components:
            from .gui import run_gui

            launch_components = []
            if resolved.component_id:
                component = to_launcher_entry(resolved.component_id)
                if component is not None:
                    launch_components.append(component)
            launch_components.extend(
                [entry for entry in (to_launcher_entry(component.id) for component in uri_components) if entry]
            )
            run_gui(launch_components, resolved.launch_args)
            return

        if resolved.component_id:
            component = to_launcher_entry(resolved.component_id)
            if component is None:
                logging.warning(f"Could not identify Component responsible for {path}")
                return

            args_to_pass = (
                tuple(filter(None, (resolved.file_path, *resolved.launch_args)))
                if resolved.kind in {ResolutionKind.FILE, ResolutionKind.URI}
                else ()
            )
            run_component(component, *(args_to_pass + launch_args))
            return

        logging.warning(f"Could not identify Component responsible for {path}")
        return

    from .gui import run_gui

    run_gui(None, normalized_args.get("args", ()))


def cli(argv: Sequence[str] | None = None) -> None:
    """Parse launcher CLI arguments and run the launcher.

    Example::

        cli(["Text Client"])
    """

    parser = argparse.ArgumentParser(
        description="Archipelago Launcher",
        usage="[-h] [--update_settings] [Patch|Game|Component] [-- component args here]",
    )
    run_group = parser.add_argument_group("Run")
    run_group.add_argument("--update_settings", action="store_true", help="Update host.yaml and exit.")
    run_group.add_argument(
        "Patch|Game|Component|url",
        type=str,
        nargs="?",
        help="Pass either a patch file, a generated game, the component name to run, or a url to connect with.",
    )
    run_group.add_argument("args", nargs="*", help="Arguments to pass to component.")
    main(parser.parse_args(argv))
    join_processes()
