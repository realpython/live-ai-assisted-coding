# Retro

## What Worked

- **Aims first, by conversation.** The idea arrived in three dictated
  messages (the game, then PR submissions, then the terminal view). All three
  went into the definition of done before any code was written, so nothing
  had to be retrofitted.
- **Quick research with throwaway experiments.** Testing the `uv run`
  entry point, loading bots by file path, and the ANSI redraw before planning
  meant none of them caused trouble later.
- **A second model reviewing the plan.** The Sonnet reviewer caught real gaps:
  bot files with syntax errors, a test for bots that edit their view, a demo
  that might end in a dull draw, and a fragile plan to parse the README in a
  test.
- **Pipelining.** Each next unit was written and checked while the host
  reviewed the last one, so moving on was usually just "go ahead".
- **Reviewing delegated work.** Sonnet and Haiku subagents built units 4, 5,
  7, and 8, and every one needed small changes before committing: an
  `id(bot)` lookup, one-letter names, and steps missing from the workflow.
- **Host questions improved the design.** Asking whether plain strings were
  robust enough led to the `Action` StrEnum, added as a `Unit 1 fix` commit
  without rewriting history.
- **Simulating matches.** Running 200 seeded matches showed that half of them
  ended in a draw, which led to the most-HP tiebreak.

## What Didn't

- **Units ran over size.** Units 2 and 3 came to about 180 lines each,
  because the tests were roughly as long as the code. The plan's estimates
  only counted the code.
- **Research missed two GitHub details.** It assumed `astral-sh/setup-uv@v10`
  existed (only full tags like `v10.2.0` do), so the first CI run failed. It
  also didn't spot that pushing a workflow needs the `workflow` token
  permission, which cost an extra login round, and one code expired.
- **The project's `plan-reviewer` agent wasn't available**, because the
  session started outside the repo. Its brief had to be passed to a general
  subagent by hand.
- **Seeded tests depended on whatever was in `bots/`.** The demo seed changed
  twice (1, then 0, then 2) as bots were added. The tests would have broken
  on every submitted bot until they switched to a fixed copy of the shipped
  bots.
- **Game balance came late.** Draws were common from Unit 7 onward, but
  nobody noticed until bots were added during iteration, because the
  definition of done said nothing about matches being worth watching.
- **Small tooling surprises:** ruff now formats Python code blocks inside
  Markdown files, and one bulk edit script stopped partway and had to be
  finished by hand.

## What We'd Change Next Time

- Speed up the intro (setup and aims) to leave more time for reviewing code
  as the units land. *(Host)*
- Count tests in each unit's size estimate, and split units that need a lot
  of tests.
- In research, check the exact versions and tags that config will reference,
  and list any permissions the work needs (like `workflow`) during step 1.
- Start the session inside the repo so its agents and skills load.
- Add a "fun to watch" check to the definition of done, such as "fewer than
  25% of 200 seeded matches are draws", and simulate matches as soon as the
  first bots exist.
- Settle the bot API's types (strings vs. an enum) during plan review, since
  it's the hardest thing to change once people write bots.
- From the start, keep tests independent of files that contributors add.
- For files under about 30 lines, like the CI workflow, write them directly
  instead of delegating. Reviewing and fixing the Haiku draft took longer
  than writing it.
