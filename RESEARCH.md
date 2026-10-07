# Research (Quick)

Only the questions that change the design or block unit 1.

## Findings and Decisions

- **Terminal animation: standard library, not `rich`.** Two ANSI escape codes,
  `"\033[2J\033[H"` (clear the screen, move the cursor home), redraw the grid
  in place. Tested here and it works. macOS, Linux, and Windows Terminal
  (the default on Windows 11) all support them. `rich` 15.0.0 is the current
  release and would give colours and panels, but it adds a dependency for
  something we can do in ~5 lines. Rendering a frame stays a pure function
  that returns a string, which also makes it easy to test.
- **`uv run botbattle` needs a build backend.** Add `[project.scripts]` plus
  `[build-system]` with `uv_build` (current release 0.12.23; uv here is
  0.11.26). Tested in a throwaway project and it works with the `src/` layout.
  Rename the project from `live-session-project` to `botbattle` at the same
  time.
- **Bot discovery: load files from a top-level `bots/` folder.**
  `importlib.util.spec_from_file_location` loads a `.py` file by path, so
  contributors drop a file in `bots/` with no `__init__.py` or registration.
  Tested and it works. Convention: each file defines `act(view)`, and the file
  name is the bot's name. It's an unusual module for this audience, so it gets
  a short comment.
- **Read-only view: frozen dataclasses holding tuples.** The engine builds a
  new view for each bot every turn from its own state, so even if a bot
  works around `frozen=True`, it can't change the real game.
- **Actions: plain strings.** `"up"`, `"down"`, `"left"`, `"right"`,
  `"attack_up"`, ... `"wait"`. They're easy to write in a bot file and easy to
  validate against a set. Anything else counts as `"wait"`.
- **Determinism: seed the `random` module at match start.** The engine uses
  `random` for start positions and turn order. Bots that use `random` then
  replay identically too. With a separate `random.Random(seed)`, bot
  randomness wouldn't be covered.
- **Bot errors:** wrap each `act()` call in `try`/`except Exception`, and
  treat an error as `"wait"`. A bot that loops forever would still hang the
  game. A timeout needs threads or subprocesses, so it's out of scope (see
  open questions).
- **PR check (optional unit):** `actions/checkout@v7` (v7.0.1) and
  `astral-sh/setup-uv@v10` (v10.2.0) are current. Use the `pull_request`
  trigger: PRs from forks run with a read-only token and no secrets, and
  first-time contributors need a maintainer's approval before their workflow
  runs. Never use `pull_request_target` for untrusted bot code.

## Sources

- Local experiments in a throwaway project (uv 0.11.26, Python 3.14.6)
- PyPI JSON API: `rich`, `uv-build`
- GitHub releases: `astral-sh/setup-uv`, `actions/checkout`
- Python docs: `importlib.util`, `dataclasses`
- GitHub docs: "Events that trigger workflows", `pull_request` from forks

## Open Questions

- **Runaway bots:** OK to leave "a bot that loops forever hangs the game" as a
  known limit, caught by the host reviewing PRs?
- **Legacy Windows console:** the old `cmd.exe` console may not show ANSI
  codes. We'll only support Windows Terminal unless someone needs the old
  console.
