# Real Python Live: AI-Assisted Coding

This repo is built live, in front of an audience of intermediate Python
developers. They'll read every line you write, so write code they can follow.

## Project

**What we're building:** Bot Battle, a terminal game where bots fight on a
grid until one is left. Each bot is a plain Python function that picks an
action every turn: move up, down, left, or right by one square, attack an
adjacent bot, or wait. Bots start with 3 HP and are removed at 0. The last bot
standing wins. Anyone can add a bot by opening a pull request with one file.

**Why:** It's a small, fun project with clear rules that's easy to build live.
Because a bot is just a function, the audience can write and submit their own.

## Definition of Done

<!-- Checkable criteria. These become the end-to-end acceptance tests. -->

- [ ] `uv run botbattle` runs a match between all bots in `bots/` on a 10×10
  grid and announces the winner.
- [ ] A bot is a plain function: it receives a read-only view of the game and
  returns one action (a move, an attack in a direction, or wait).
- [ ] Rules are enforced and tested: moves off the grid or into an occupied
  square do nothing; an attack hits only the adjacent square in its direction;
  a hit costs 1 HP; a bot at 0 HP is removed.
- [ ] A match ends with one bot left (the winner) or at a turn limit, where
  the bot with the most HP wins (a tie for the most HP is a draw). The same
  seed always replays the same match.
- [ ] A bot that raises an error, returns an invalid action, or tries to
  change the game state just waits that turn. The game never crashes.
- [ ] Adding a bot means adding one file to `bots/`, with no registration
  step. At least 3 example bots ship this way.
- [ ] `uv run botbattle` animates the match as text in the terminal: the grid
  redraws in place each round, a panel shows each bot's name and HP, defeated
  bots disappear and are marked out, and the final screen shows the result.
  `--delay` sets the speed, and `--no-animate` prints only the result.
- [ ] The README explains how to write and submit a bot.
- [ ] *(Optional)* A GitHub Actions check runs on every PR: ruff, pytest, and
  a match that includes the new bot.

## How We Work

Run `/project-protocol` to drive these steps. Add `yolo` to build every unit
without stopping once the plan is approved, and `quick` or `thorough` to set
the research depth.

1. Aims + definition of done (this file)
2. Research: write it to `RESEARCH.md`
3. Plan: write it to `PLAN.md`, broken into units
4. Plan review: manual, plus the `plan-reviewer` subagent
5. Implement unit by unit
6. Test end to end against the definition of done, then iterate
7. Retro

### Units

- One unit = one logical step: roughly 30–100 lines, reviewable on screen in
  about 5 minutes. Estimate the size of each unit in `PLAN.md`.
- Every unit includes its own tests.
- A unit is finished only when `uv run ruff check .`, `uv run ruff format --check .`,
  and `uv run pytest` all pass.

## Coding Conventions

The audience is intermediate Pythonistas. Readability beats cleverness.

- Prefer explicit over clever.
- Use descriptive names, type hints, and short docstrings.
- Stick to everyday tools: functions, classes, dataclasses, dicts,
  comprehensions, and the standard library.
- Avoid metaprogramming, dense one-liners, and obscure modules unless the
  project needs them.
- If an unusual module or technique is needed, add a 1–2 line comment
  explaining it.
- Use the `src/` layout: package code in `src/<package>/`, tests in `tests/`.
- Add third-party dependencies only when they clearly earn their place, and
  use `uv add` to do it.

## Commands

```bash
uv sync                    # install dev tools
uv run pytest              # run the tests
uv run ruff check .        # lint
uv run ruff format .       # format
```

## Git Rules

There is exactly one writer: you (Claude Code). The host and students only pull.
The one exception is bot submissions: anyone may open a PR that adds a single
file to `bots/`, and the host reviews and merges it. Pull before each unit so
merged bots don't cause conflicts.

- **One unit = one commit = one push.** Commit message format:
  `Unit 3: Message and file insights`, with a short body explaining *why*.
- **Tag every unit** (`unit-1`, `unit-2`, ...) and push the tag:
  `git push origin main --tags`.
- Review feedback on a pushed unit becomes a follow-up commit:
  `Unit 3 fix: ...`
- **Never** force-push, rebase, amend, or otherwise rewrite pushed history.
- Before starting a unit, run `git pull` in case the host pushed a change.
- Don't commit secrets, `.env` files, or local artifacts.
