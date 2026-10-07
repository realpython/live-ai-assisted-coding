# Real Python Live: AI-Assisted Coding

This repo is built live, in front of an audience of intermediate Python
developers. They'll read every line you write, so write code they can follow.

## Project

<!-- Filled in live during step 1 of the session. -->

**What we're building:** TBD

**Why:** TBD

## Definition of Done

<!-- Checkable criteria. These become the end-to-end acceptance tests. -->

- [ ] TBD

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

- **One unit = one commit = one push.** Commit message format:
  `Unit 3: Message and file insights`, with a short body explaining *why*.
- **Tag every unit** (`unit-1`, `unit-2`, ...) and push the tag:
  `git push origin main --tags`.
- Review feedback on a pushed unit becomes a follow-up commit:
  `Unit 3 fix: ...`
- **Never** force-push, rebase, amend, or otherwise rewrite pushed history.
- Before starting a unit, run `git pull` in case the host pushed a change.
- Don't commit secrets, `.env` files, or local artifacts.
