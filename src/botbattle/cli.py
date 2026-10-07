"""The `botbattle` command: load the bots, play a match, and show it."""

import argparse
import random
import sys
import time

from botbattle.display import render, result_line
from botbattle.game import Game
from botbattle.loader import load_bots

# ANSI escape codes: clear the screen, then move the cursor to the top-left
# corner, so each frame is drawn over the last one.
CLEAR_SCREEN = "\033[2J\033[H"


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="botbattle",
        description="Watch bots battle on a grid until one is left.",
    )
    parser.add_argument(
        "--bots", default="bots", help="folder of bot files (default: bots)"
    )
    parser.add_argument(
        "--seed", type=int, help="replay a match by its seed (default: random)"
    )
    parser.add_argument(
        "--delay", type=float, default=0.3, help="seconds between rounds"
    )
    parser.add_argument(
        "--no-animate", action="store_true", help="only print the result"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run Bot Battle from the command line and return the exit code."""
    args = parse_args(argv)
    bots = load_bots(args.bots)
    if len(bots) < 2:
        print(
            f"Need at least 2 bots in {args.bots}/, found {len(bots)}.", file=sys.stderr
        )
        return 1

    # Without --seed, pick one at random and show it so the match can be replayed.
    seed = args.seed if args.seed is not None else random.randrange(1_000_000)
    game = Game(bots, seed=seed)

    try:
        while not game.is_over:
            if not args.no_animate:
                print(CLEAR_SCREEN + render(game), flush=True)
                time.sleep(args.delay)
            game.play_round()
    except KeyboardInterrupt:
        print("\nMatch stopped.")
        return 1

    if args.no_animate:
        print(f"{result_line(game)} after {game.round} rounds")
    else:
        print(CLEAR_SCREEN + render(game))
    print(f"Seed: {seed} (replay with --seed {seed})")
    return 0
