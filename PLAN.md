# Plan

## Overview

Bot Battle is a small package, `botbattle`, with a game engine, a bot loader,
and a text renderer, plus a `bots/` folder of one-file bots that anyone can
add to by PR. `uv run botbattle` loads every bot, plays a seeded match on a
10×10 grid, and animates it in the terminal.

## Design

**Modules** (`src/botbattle/`):

| Module | Job |
|---|---|
| `view.py` | The read-only data a bot sees, plus the list of valid actions |
| `game.py` | The rules: the board, moves, attacks, rounds, and the end of the match |
| `loader.py` | Finds and loads every bot file in `bots/` |
| `display.py` | Turns the game state into a text frame (a pure function) |
| `cli.py` | Command-line options, the animation loop, and the final result |

**Data model:**

```python
# One table drives both moves and attacks: "attack_up" uses DIRECTIONS["up"].
DIRECTIONS = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
ACTIONS = {"up", "down", "left", "right",
           "attack_up", "attack_down", "attack_left", "attack_right", "wait"}

@dataclass(frozen=True)
class BotInfo:          # what anyone can see about a bot
    name: str
    x: int
    y: int
    hp: int

@dataclass(frozen=True)
class BotView:          # what a bot receives each turn ((0, 0) is top-left)
    me: BotInfo
    others: tuple[BotInfo, ...]   # living opponents only
    width: int
    height: int
    round: int

# A bot file defines:  def act(view: BotView) -> str
```

Inside `game.py`, a mutable `Bot` dataclass (name, `act` function, x, y,
hp, letter) holds the real state, and bots never see it. `(0, 0)` is the
top-left corner and `y` grows downward, so `"up"` means `y - 1`.

**Main flow:**

1. `cli.py` reads the options: `--bots` (default `bots/`), `--seed`,
   `--delay` (default 0.3 s), and `--no-animate`. Without `--seed`, it picks
   a random seed and prints it, so any match can be replayed.
2. `loader.load_bots(folder)` returns `(name, act)` pairs, one per `*.py`
   file, sorted by name. A file that fails to import or has no `act` is
   skipped with a warning.
3. `Game(bots, size=10, max_rounds=200, seed=...)` seeds `random` itself and
   places bots on random empty squares. The round limit is a `Game` setting,
   not a command-line option.
4. Each round, `game.play_round()` shuffles the living bots, then for each one:
   build a fresh `BotView`, call `act()` safely (an error or invalid action
   becomes `"wait"`), and apply the action. A bot at 0 HP is removed at
   once and doesn't act later that round.
5. After each round, `cli.py` prints `display.render(game)` (clear the screen
   and redraw) and sleeps for `--delay`.
6. When `game.is_over` (one or no bots left, or the round limit reached),
   the final frame shows the result, `Winner: chaser` or `Draw`.

## Units

### Unit 1: Package, entry point, and the bot's view

- **Adds:** renames the project to `botbattle`, adds `uv_build` and the
  `botbattle` script, and adds `view.py` (`BotInfo`, `BotView`, `ACTIONS`).
  For now `cli.py` only prints a placeholder line.
- **Files:** `pyproject.toml`, `uv.lock`, `src/botbattle/__init__.py`,
  `src/botbattle/view.py`, `src/botbattle/cli.py`, `tests/test_view.py`
- **Tests:** the dataclasses are frozen (assigning to a field raises an
  error), `ACTIONS` contains the 9 actions, and `main()` runs.
- **Size:** about 50 lines
- **Priority:** core
- **Model:** Opus 5.5 (me). It sets the API every later unit uses.
- **Note:** it mixes tooling (rename, build backend) with the API, and the
  commit message says both.

### Unit 2: The board and its rules

- **Adds:** `Game` setup (random, non-overlapping start positions, 3 HP each)
  and `apply_action(bot, action)` for moves, attacks, waiting, and
  removing bots at 0 HP. `DIRECTIONS` (in `view.py`) drives both moves and
  attacks, which keeps the unit under 100 lines.
- **Files:** `src/botbattle/game.py`, `tests/test_rules.py`
- **Tests:** a move to an open square works; a move off the edge or into
  another bot is ignored; an attack hits only the adjacent square in its
  direction; a hit costs 1 HP; a bot at 0 HP is removed; an attack on an
  empty square does nothing.
- **Size:** about 100 lines
- **Priority:** core
- **Model:** Opus 5.5 (me). This is the core logic, where a subtle bug would
  be expensive.

### Unit 3: Rounds, safety, and the end of the match

- **Adds:** `play_round()` (shuffled order, a fresh `BotView` per call,
  `act()` wrapped in `try`/`except`), `is_over`, `winner`, and seeding.
- **Files:** `src/botbattle/game.py`, `tests/test_match.py`
- **Tests:** one bot left means it's the winner; the round limit means a draw;
  the same seed gives the same result twice; a bot that raises, returns
  `"fly"`, or returns `None` just waits; a bot that tries
  `view.me.hp = 99` just waits and its real HP is unchanged; a bot removed
  mid-round doesn't act.
- **Size:** about 90 lines
- **Priority:** core
- **Model:** Opus 5.5 (me). The determinism and error handling need care.

### Unit 4: Bot loader and three example bots

- **Adds:** `load_bots(folder)` using `importlib.util` (with a 2-line
  comment explaining it), which warns about and skips files that fail to
  import or have no `act` function, and skips names starting with `_`. Also adds `bots/random_walker.py`, `bots/chaser.py` (moves toward the
  nearest bot and attacks when next to it), and `bots/coward.py` (moves away
  from the nearest bot).
- **Files:** `src/botbattle/loader.py`, `bots/*.py`, `tests/test_loader.py`
- **Tests:** loads bots from a temporary folder; skips a file without `act`;
  skips a file with a syntax error; the three real bots load and return
  valid actions for a sample view.
- **Size:** about 90 lines
- **Priority:** core
- **Model:** Sonnet 5.5 subagent. The spec is clear and the work is routine.
  I review it before committing.

### Unit 5: Text rendering

- **Adds:** `render(game) -> str`, which shows the grid (`.` for an empty
  square, a capital letter for each bot) with an HP panel next to it, such
  as `A chaser ♥♥♡`, a defeated bot marked as out, and a header like
  `Round 12/200`. Once the match is over, the frame ends with the result.
- **Files:** `src/botbattle/display.py`, `tests/test_display.py`
- **Tests:** a small hand-built game renders exactly as expected; a removed
  bot is missing from the grid and shown as out in the panel; a finished
  game's frame shows the winner or `Draw`.
- **Size:** about 70 lines
- **Priority:** core
- **Model:** Sonnet 5.5 subagent. It's routine string building. I review it
  before committing.

### Unit 6: Command line and animation

- **Adds:** a real `cli.main()`: the `argparse` options, the redraw loop
  with ANSI clear plus `time.sleep`, `--no-animate`, and the final frame.
  With fewer than 2 bots, it prints a clear message and exits. It also picks
  a demo seed that ends in a winner with the shipped bots.
- **Files:** `src/botbattle/cli.py`, `tests/test_cli.py`
- **Tests:** `main(["--no-animate", "--seed", ...])` prints a `Winner:` or
  `Draw` line; an end-to-end run over the real `bots/` folder with the demo
  seed ends in a winner; a run without `--seed` prints the seed it used; an
  empty bots folder gives the friendly error.
- **Size:** about 70 lines
- **Priority:** core
- **Model:** Opus 5.5 (me). It's the integration point and the demo.

### Unit 7: Bot submission guide

- **Adds:** a README section on how to write a bot (the `act(view)`
  signature, the `BotView` fields, the coordinates, and the action names),
  how to try it locally, and how to open a PR with one file in `bots/`. The
  sample bot is a real file, `bots/example.py`, quoted in the README. It also
  states the known limit: a bot that loops forever hangs the game.
- **Files:** `README.md`, `bots/example.py`
- **Tests:** none new. The existing loader and end-to-end tests already
  cover `bots/example.py`, so the sample can't go stale.
- **Size:** about 60 lines
- **Priority:** core
- **Model:** Sonnet 5.5 subagent. It's documentation, and I review it before
  committing.

### Unit 8: PR check workflow

- **Adds:** `.github/workflows/check.yml`, triggered on `pull_request` and
  pushes to `main`: `actions/checkout@v7`, `astral-sh/setup-uv@v10`,
  `uv sync`, ruff check, ruff format check, pytest, and
  `uv run botbattle --no-animate` with the demo seed from Unit 6. The job
  has `timeout-minutes: 5`, so a bot that loops forever fails fast.
- **Files:** `.github/workflows/check.yml`
- **Tests:** the workflow passes on the pushed commit (checked with
  `gh run watch`).
- **Size:** about 30 lines
- **Priority:** optional
- **Model:** Haiku 4.5 subagent. It's mechanical YAML. I review it before
  committing.

## Definition of Done Mapping

| Definition of Done item | Unit |
|---|---|
| `uv run botbattle` runs a match and announces the winner | 1 (entry point), 6 |
| A bot is a plain function with a read-only view | 1, 3 |
| Rules enforced and tested | 2 |
| Winner, turn-limit draw, seeded replay | 3 |
| A misbehaving bot just waits | 3 |
| One file per bot, at least 3 examples | 4 |
| Terminal animation with HP panel, `--delay`, `--no-animate` | 5, 6 |
| README explains how to submit a bot | 7 |
| *(Optional)* PR check | 8 |

## Models

The models available now: Fable 5.1, Opus 5.5 (me, the session model),
Sonnet 5.5, and Haiku 4.5.

- **Opus 5.5 (me):** the API, the rules engine, the match loop, and the CLI
  (units 1, 2, 3, and 6), where design matters most.
- **Sonnet 5.5 subagent:** routine units with a clear spec (4, 5, and 7) and
  the plan review (the `plan-reviewer` agent already runs on Sonnet).
- **Haiku 4.5 subagent:** the mechanical CI YAML (unit 8).
- **Fable 5.1:** not needed. Nothing here is hard enough to justify the
  cost, but it's the fallback if a unit gets stuck.

Delegated units get a brief with the relevant parts of `CLAUDE.md` and this
plan. I review their work and run the quality gates before committing. Nobody
needs to switch with `/model`.

## Review

Reviewed by a Sonnet 5.5 subagent (using the `plan-reviewer` brief) and
by the host.

- Final screen not specified: fixed. `render` shows the result, and Units 5
  and 6 test it.
- No test for a bot that edits its view: fixed with a Unit 3 test.
- A bot file with a syntax error would crash the loader: fixed. It's skipped
  with a warning and tested in Unit 4.
- Global `random.seed` and the default seed: fixed. `Game` seeds itself, and
  without `--seed` the CLI prints the seed it picked.
- Demo might end in a dull draw: fixed. Unit 6 picks a demo seed that gives a
  winner, and CI uses it.
- A bot that loops forever hangs the game: accepted as a known limit. It's
  documented in the README, and CI has `timeout-minutes: 5`.
- Parsing the README to test the sample bot is fragile: fixed. The sample is
  `bots/example.py`, quoted in the README.
- `--max-rounds` isn't needed: removed from the CLI and kept as a `Game`
  setting.
- `importlib` needs a comment, action parsing was unspecified, and the
  coordinates were only in the plan: fixed with the comment, the
  `DIRECTIONS` table, and docs in the `BotView` docstring and the README.
- Split the rules into `rules.py`: won't fix. `DIRECTIONS` keeps Unit 2 small,
  and one rules file is easier to follow.
- Unit 1 mixes tooling with the API: kept as one unit, and the commit message
  says both.
- Move Unit 6 to Sonnet: host decided to keep it on Opus.
- Host decisions: bots act one at a time in a shuffled order, `"up"` means
  `y - 1`, the `BotView` stays as designed, only Windows Terminal is
  supported (not the old `cmd.exe` console), and a bot that loops forever is
  a known limit.

**Status:** Approved
