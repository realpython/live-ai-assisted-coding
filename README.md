# Real Python Live: AI-Assisted Coding

This project gets built live, from scratch, by Claude Code during a
Real Python Live session, with the group reviewing each step as it lands.

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
```
