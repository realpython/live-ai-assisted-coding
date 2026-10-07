---
name: project-protocol
description: Runs a 7-step protocol for building a project with an AI agent (aims, research, plan, plan review, units, test and iterate, retro), one step at a time or in yolo mode. Use when starting a new project, moving to the next step, building the next unit, or iterating on a finished draft.
argument-hint: "[next | aims | research | plan | review | unit N | test | retro] [yolo] [quick | thorough]"
---

# Project Protocol

A repeatable way to build a project with an AI agent: agree on what "done"
means, plan in small reviewable units, have a second model review the plan,
build one unit at a time, then test, iterate, and reflect.

This skill holds the procedure. The project's own `CLAUDE.md` holds the
rules (conventions, commands, git rules), and those rules win wherever they
differ from the defaults below.

## Modes

- **Step mode (default):** do exactly one step, then stop and say what the
  next step is. Best when people are reviewing along, such as a pair, a team,
  or a live audience.
- **Yolo mode (`yolo` in the arguments, or the user asks for it):** same
  steps, fewer stops. Steps 1–4 still stop at their checkpoints, because the
  user must approve the aims and the plan. Once the plan is approved, build
  every unit back to back without waiting for review, then stop at step 6
  with a finished draft. Each unit is still its own commit.

Research depth is a separate choice: **quick** or **thorough** (see step 2).

## Before You Start

Read the project's `CLAUDE.md` (create it if it's missing) and work out:

- **Quality gates:** the lint, format, type-check, and test commands. Use
  the ones in `CLAUDE.md`. If none are listed, detect them from the project
  (for example, `ruff` and `pytest` in `pyproject.toml`), and if there are
  none at all, propose a minimal set during step 3 and set it up in unit 1.
- **Readers:** who will read the code (for example, "intermediate
  Pythonistas"). Write for them. If `CLAUDE.md` doesn't say, ask in step 1.
- **Git:** whether there's a remote to push to. If there isn't one, commit
  and tag as usual and skip every "push" below. If there's no git repo at
  all, ask before running `git init`.
- **Time limit:** whether the user is working to a clock, such as a live
  session or a timeboxed workshop. If so, see "Timeboxed Sessions" at the end.

## Choosing the Step

With no step given (or `next`), work out the step from the repo:

| Repo state | Step |
|---|---|
| No Definition of Done in `CLAUDE.md`, or it's only placeholders | 1. Aims |
| No `RESEARCH.md` | 2. Research |
| No `PLAN.md` | 3. Plan |
| `PLAN.md` has no `**Status:** Approved` line | 4. Plan review |
| A unit in `PLAN.md` has no `unit-N` git tag | 5. Next unit |
| All units tagged, no `RETRO.md` | 6. Test and iterate |
| `RETRO.md` exists | Done. Say so and offer more iteration. |

Pull first if there's a remote, and check tags with `git tag --list 'unit-*'`.
Start by saying, in one line, which step you're on.

## The Steps

### 1. Aims and Definition of Done

1. Ask the user what we're building, why, and who will read the code. If
   they've already said, confirm it in one or two sentences instead of asking
   again.
2. Draft a **Project** section for `CLAUDE.md` (what we're building and why)
   and a **Definition of Done** with 4–7 checkboxes. Each criterion must be
   *checkable*: a test or a single command can confirm it. Write
   "`wordcount notes.txt` prints the top 10 words with their counts" rather
   than "the output is useful".
3. Keep the scope realistic for the time and budget the user has in mind.
4. Show the draft and **stop** for the user to confirm or adjust it.
5. Once confirmed, write it to `CLAUDE.md`, commit
   `Step 1: Aims and definition of done`, and push.

### 2. Research

**Choose the depth first.** If the user passed `quick` or `thorough`, or
already said which they want, use that. Otherwise ask in one line, and
recommend **quick** when they're working to a clock or the project is small
and familiar, **thorough** otherwise.

- **Quick:** answer only the questions that would change the design or block
  unit 1. Still confirm the current version and usage of each key library or
  API (a quick docs check, not memory), but skip the broader survey.
  `RESEARCH.md` is a short bulleted list: findings, decisions, sources, open
  questions.
- **Thorough:** the full groundwork described below.

**Thorough research** is what a careful team would do before planning:
complete, but in proportion to the project. Start by listing what the plan
depends on, then answer each item. Typical areas:

- **The domain:** the rules, formats, or concepts the project deals with.
- **Prior art:** existing tools or libraries that already solve part of the
  problem, and whether to use them or build our own.
- **Libraries and APIs:** what's available, current versions, and how they're
  actually used today. Your training data may be out of date, so check
  official docs and release notes rather than relying on memory.
- **Pitfalls:** known gotchas, edge cases, platform quirks, licensing, limits.
- **Design options:** two or three ways to structure the solution, with their
  trade-offs.

Use web search and official documentation as needed, and cite sources. For a
question that's quicker to answer by trying it, run a small throwaway
experiment instead (don't commit it). Research subagents can run several
lines of inquiry in parallel.

For thorough research, write `RESEARCH.md` with one short section per area:
the findings, the decision or recommendation, and sources. End with **Open
questions** that still need the user's input.

At either depth, commit `Step 2: Research` and push. Stop only if the
findings change the aims or raise open questions. Otherwise go straight on to
step 3.

### 3. Plan

Write `PLAN.md` with these sections:

1. **Overview:** two or three sentences.
2. **Design:** the modules and their jobs, the core data model, and the main
   flow, building on the decisions in `RESEARCH.md`. Keep it small enough to
   read on one screen.
3. **Units:** a numbered list. For each unit, give:
    - a title (it becomes the commit message, `Unit N: <title>`)
    - what it adds, in one or two sentences
    - the files it touches
    - its tests
    - an estimated size: one logical step, roughly 30–100 lines including
      tests, or about 5 minutes to review on screen
    - its priority: **core** (needed for the Definition of Done) or
      **optional** (worth having, but the project works without it)
    - the model tier it needs (see Models)
4. **Definition of Done mapping:** which unit satisfies each Definition of
   Done item.
5. **Models:** which model handles which kind of work, balancing quality,
   speed, and cost. Check which models are currently available rather than
   assuming. A typical split:
    - **Strongest model:** design-heavy or tricky units, and anything where a
      subtle bug would be expensive.
    - **Mid-tier model:** routine units with a clear spec, research
      subagents, and the plan review (if it differs from your own model).
    - **Fast, cheap model:** mechanical work such as boilerplate, renames,
      bulk test data, or summarizing large outputs.

   You can't switch your own model mid-session. A unit assigned to another
   model is either delegated to a subagent on that model, with a brief that
   includes the relevant parts of `CLAUDE.md` and `PLAN.md`, or the user
   switches with `/model`. Say which, per unit.
6. **Review:** a placeholder for step 4.

If the quality gates aren't set up yet, make that unit 1. Commit
`Step 3: Plan` and push so the user can read it in their editor. Then **stop**
(in both modes) and offer to run the plan review.

### 4. Plan Review

1. Start a reviewer subagent **in the background**, on a *different model*
   from yours, because a different model catches different things. If the
   project has a reviewer agent (for example `.claude/agents/plan-reviewer.md`),
   use that. Otherwise brief a subagent with the review brief below.
2. While it runs, tell the user it's their turn to review by hand, and say
   which parts of the plan most need human judgment.
3. When both reviews are in, list the findings briefly, grouped as *will fix*,
   *won't fix* (with a reason), and *needs your call*.
4. Once the user decides, update `PLAN.md`. Fill in its **Review** section with
   a one-line summary per finding and what was done about it.
5. **Stop** for go/no-go. When the user approves, add `**Status:** Approved` to
   the Review section, commit `Step 4: Plan reviewed and approved`, and push.

**Review brief** (for a subagent without one): read `CLAUDE.md`,
`RESEARCH.md`, and `PLAN.md`, then report at most 3 findings per category,
most important first, each with a concrete suggestion: **gaps** against the
Definition of Done, **risks** (edge cases, likely bugs), **overengineering**,
**unit sizing** (too big to review in about 5 minutes, or too small to
matter), and **readability** for the intended readers. Say "none" for an empty
category. End with a one-line verdict: ready to build, or fix first.

### 5. Units

For each unit:

1. Pull, in case someone else pushed a change.
2. Write the code and its tests, following `CLAUDE.md`, on the model the
   plan assigns. When it's delegated to a subagent, review its work before
   committing: you're still responsible for the unit.
3. Run the quality gates and fix anything that fails. Never commit a unit
   with failing gates.
4. Commit `Unit N: <title>` with a short body explaining *why*, tag `unit-N`,
   and push with the tag.
5. Print a **review note** of at most 4 bullets: what this unit adds, the one
   or two places in the diff worth reading closely, and anything you weren't
   sure about.

**Pipelining (step mode):** after pushing unit N, start unit N+1 locally
while the user reviews N, but don't commit it yet. When feedback on unit N
arrives:

- Apply it as a follow-up commit, `Unit N fix: <what>`, unless the user asks
  you to pause instead. Run the gates first. Leave the `unit-N` tag where it
  is; the fix commit stands on its own.
- Then carry on with N+1.

If no feedback has arrived, get N+1 ready to commit, then stop and wait.
Commit and push N+1 only when the user says to move on.

**Yolo mode:** build all the remaining units back to back. Keep the review
notes, but don't wait for replies.

**If scope needs to shrink** (time, budget, or a blocker): suggest dropping
or deferring **optional** units rather than cutting corners on core ones.

### 6. Test and Iterate

1. Run the full quality gates.
2. Check every Definition of Done item with a command or test. Mark it `[x]`
   in `CLAUDE.md`, or leave it `[ ]` with a short note. Add an end-to-end
   test if no existing test covers the whole flow.
3. If an item fails, fix it as an `Iteration: <what>` commit before the demo.
   If the fix is bigger than a unit, tell the user and let them decide.
4. Give the user the exact command to run the demo, and show its output.
5. Commit `Step 6: Definition of done checked` and push.
6. **Iterate.** The user (and anyone watching) will suggest changes: fixes,
   tweaks, small features. For each one:
    - If it's small, just do it. If it's bigger than a unit or changes the
      aims, say so and confirm first.
    - Run the gates, commit `Iteration: <what>`, and push. Iterations get no
      tags.
    - Re-check any Definition of Done item the change could affect.
    - Show the demo output again if it changed.
7. Stay in this loop until the user says to move on to the retro.

### 7. Retro

Write `RETRO.md` with three short sections: **What worked**, **What didn't**,
and **What we'd change next time**. Focus on the human/AI workflow (the aims,
the plan review, unit sizing, pipelining), not only the code. Draft it from
what happened, then ask the user to add or correct points. Commit
`Step 7: Retro` and push.

## Always

- If people are reviewing along, you're the only one who commits. If the user
  pushes a change, pull before you continue.
- Never force-push, rebase, amend, or move a pushed tag.
- Keep step announcements to one line. Put the detail in the files and the
  review notes, not in long messages.

## Timeboxed Sessions

When the user is working to a clock, announce each step's budget as you start
it, flag overruns early, and lean on priorities. Research shrinks to the
questions that block the design (quick research, unless the user chooses
otherwise), and optional units are the first to go. A
rough split for a 60–80 minute session:

| Step | Budget |
|---|---|
| 1. Aims | 5 min |
| 2. Research | 3–5 min |
| 3. Plan | 5 min |
| 4. Plan review | 5 min |
| 5. Units | 5–8 min each, about five units |
| 6. Test and iterate | 5–10 min |
| 7. Retro | 3–5 min |
