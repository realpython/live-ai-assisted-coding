"""Finds bot files in a folder and loads their `act` functions."""

import importlib.util
import sys
from pathlib import Path

from botbattle.game import BotFunction


def load_bots(folder: Path | str) -> list[tuple[str, BotFunction]]:
    """Load every bot in a folder as a (name, act function) pair.

    A bot's name is its file name without ".py". Files that start with "_"
    are ignored. A file that fails to load is skipped with a warning.
    """
    bots = []
    for path in sorted(Path(folder).glob("*.py")):
        if path.name.startswith("_"):
            continue
        try:
            # Bots live in a plain folder, not a package. This loads a Python
            # file straight from its path, so no __init__.py or registration.
            spec = importlib.util.spec_from_file_location(f"bots.{path.stem}", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            act = getattr(module, "act", None)
            if not callable(act):
                raise ValueError("no act() function found")
        except Exception as error:
            print(f"Skipping {path}: {error}", file=sys.stderr)
            continue
        bots.append((path.stem, act))
    return bots
