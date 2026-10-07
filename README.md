# Real Python Live: AI-Assisted Coding

This project gets built live, from scratch, by Claude Code during a
Real Python Live session, with the group reviewing each step as it lands.

The project is **Bot Battle**, a terminal game where bots fight on a grid
until only one is left. Each bot is a plain Python function, so you can
write your own and submit it with a pull request.

## Follow Along

You'll need git, Python 3.14+, and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/realpython/live-ai-assisted-coding.git
cd live-ai-assisted-coding
uv sync
```

After each unit is pushed, run `git pull` to get the latest changes.

**Please don't edit files on `main` in your clone,** or your pulls will
conflict. If you want to experiment, do it on a branch:

```bash
git switch -c my-experiments
```

## Play a Match

```bash
uv run botbattle
```

The match is animated in your terminal, so make it at least 15 rows tall.
Press Ctrl+C to stop. These options are available:

- `--seed N` replays a match. The seed is printed at the end of every match.
- `--delay SECONDS` sets the pause between rounds (default 0.3).
- `--no-animate` skips the animation and only prints the result.
- `--bots FOLDER` plays the bots in another folder (default `bots`).

## The Rules

- The grid is 10×10, and every bot starts with 3 HP.
- Each round, every living bot acts once, in a random order.
- A move off the grid or into an occupied square does nothing.
- An attack hits the bot on the neighbouring square in that direction for 1 HP.
- At 0 HP a bot is out. The last bot standing wins.
- After 200 rounds, the match is a draw.

## Write Your Own Bot

A bot is a file in `bots/` with a function `act(view)` that returns an
`Action`. The file name is the bot's name.

The `view` tells the bot what it can see:

| Field | What it is |
|---|---|
| `view.me` | a `BotInfo` for your bot, with `name`, `x`, `y`, and `hp` |
| `view.others` | a tuple of `BotInfo` for the living opponents |
| `view.width`, `view.height` | the size of the grid |
| `view.round` | the current round number |

The point (0, 0) is the top-left corner, and `Action.UP` makes `y` smaller.
`DIRECTIONS` maps each move to its (x, y) step, and `ATTACKS` maps each
direction to its attack.

There are 9 actions: `Action.UP`, `Action.DOWN`, `Action.LEFT`,
`Action.RIGHT`, `Action.ATTACK_UP`, `Action.ATTACK_DOWN`,
`Action.ATTACK_LEFT`, `Action.ATTACK_RIGHT`, and `Action.WAIT`. Plain strings
like `"attack_up"` also work.

Here is `bots/example.py` in full:

```python
"""The example bot from the README. Copy this file to start your own bot."""

import random

from botbattle.view import ATTACKS, DIRECTIONS, Action, BotView


def act(view: BotView) -> Action:
    """Attack a neighbouring opponent if there is one, else wander."""
    me = view.me

    # Look at the square in each direction. If an opponent is standing
    # there, attack in that direction.
    for direction, (dx, dy) in DIRECTIONS.items():
        for other in view.others:
            if (other.x, other.y) == (me.x + dx, me.y + dy):
                return ATTACKS[direction]

    # Nobody is next to us, so move in a random direction.
    return random.choice(list(DIRECTIONS))
```

**If a bot misbehaves,** it just waits that turn. That covers `act` raising
an error, returning something that isn't an action, or trying to change the
view (it's read-only). A bot file that fails to import is skipped with a
warning.

**Try it locally:** copy `bots/example.py` to `bots/your_name.py`, edit it,
and run `uv run botbattle`. To test against a single opponent, put just two
bots in a separate folder and use `--bots`.

**Known limit:** a bot that loops forever freezes the game, so keep `act`
fast and simple.

## Submit Your Bot

1. Fork the repo and create a branch.
2. Add exactly one file: `bots/<your_bot_name>.py`. Use lowercase with
   underscores, like `sneaky_sam.py`. Names starting with `_` are ignored.
3. Only import from the standard library and `botbattle.view`.
4. Run the checks (see below).
5. Open a pull request.

The host reviews every bot before merging, because bots run on the host's
machine. This repo's git rules make an exception for pull requests that add
a single bot file.

## Revisit Any Stage

Each unit is tagged, so you can check out the code as it was at any point:

```bash
git checkout start     # the empty starter template
git checkout unit-3    # the project after unit 3
git switch main        # back to the latest
```

## Running the Checks

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```
