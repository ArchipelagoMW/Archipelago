import json
import sys
import warnings
from pathlib import Path
from typing import Iterable, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from multiprocessing.managers import ListProxy  # noqa

__all__ = [
    "generate_local",
]


def _generate_local_inner(games: Iterable[str],
                          dest: Union[Path, str],
                          results: "ListProxy[Union[Path, BaseException]]") -> None:
    original_argv = sys.argv
    warnings.simplefilter("ignore")
    try:
        from tempfile import TemporaryDirectory

        if not isinstance(dest, Path):
            dest = Path(dest)

        with TemporaryDirectory() as players_dir:
            with TemporaryDirectory() as output_dir:
                import Generate
                import Main

                for n, game in enumerate(games, 1):
                    player_path = Path(players_dir) / f"{n}.yaml"
                    with open(player_path, "w", encoding="utf-8") as f:
                        f.write(json.dumps({
                            "name": f"Player{n}",
                            "game": game,
                            game: {},
                            "description": f"generate_local slot {n} ('Player{n}'): {game}",
                        }))

                # this is basically copied from test/programs/test_generate.py
                # uses a reproducible seed that is different for each set of games
                sys.argv = [sys.argv[0], "--seed", str(hash(tuple(games))),
                            "--player_files_path", players_dir,
                            "--outputpath", output_dir]
                Main.main(*Generate.main())
                output_files = list(Path(output_dir).glob('*.zip'))
                assert len(output_files) == 1
                final_file = dest / output_files[0].name
                output_files[0].rename(final_file)
                results.append(final_file)
    except BaseException as e:
        results.append(e)
        raise e
    finally:
        sys.argv = original_argv


def generate_local(games: Iterable[str], dest: Union[Path, str]) -> Path:
    from multiprocessing import Manager, Process, set_start_method

    try:
        set_start_method("spawn")
    except RuntimeError:
        pass

    manager = Manager()
    results: "ListProxy[Union[Path, Exception]]" = manager.list()

    p = Process(target=_generate_local_inner, args=(games, dest, results))
    p.start()
    p.join()
    result = results[0]
    if isinstance(result, BaseException):
        raise Exception("Could not generate multiworld") from result
    return result
