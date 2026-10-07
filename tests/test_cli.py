import shutil
from pathlib import Path

import pytest

from botbattle.cli import CLEAR_SCREEN, main

REAL_BOTS_FOLDER = Path(__file__).parent.parent / "bots"
SHIPPED_BOTS = ["chaser.py", "coward.py", "example.py", "random_walker.py"]
DEMO_SEED = "0"  # The shipped bots play to a winner with this seed


@pytest.fixture
def shipped_bots(tmp_path):
    """Copy only the bots that ship with the project into a temporary folder.

    Bots submitted by PR change how a seeded match plays out, so tests that
    expect an exact outcome use this fixed set instead of everything in bots/.
    """
    for file_name in SHIPPED_BOTS:
        shutil.copy(REAL_BOTS_FOLDER / file_name, tmp_path)
    return str(tmp_path)


def test_no_animate_prints_only_the_result(shipped_bots, capsys):
    exit_code = main(["--bots", shipped_bots, "--seed", DEMO_SEED, "--no-animate"])
    output = capsys.readouterr().out
    assert exit_code == 0
    assert output.splitlines()[0].startswith("Winner: ")
    assert f"Seed: {DEMO_SEED}" in output
    assert CLEAR_SCREEN not in output


def test_animation_redraws_every_round_and_ends_with_the_result(shipped_bots, capsys):
    main(["--bots", shipped_bots, "--seed", DEMO_SEED, "--delay", "0"])
    frames = capsys.readouterr().out.split(CLEAR_SCREEN)[1:]
    assert frames[0].startswith("Round 0/200")
    assert "Winner: " in frames[-1]
    assert "Winner: " not in frames[-2]


def test_without_a_seed_it_prints_one_that_replays_the_match(shipped_bots, capsys):
    main(["--bots", shipped_bots, "--no-animate"])
    first_run = capsys.readouterr().out
    seed = first_run.split("Seed: ")[1].split()[0]

    main(["--bots", shipped_bots, "--no-animate", "--seed", seed])
    assert capsys.readouterr().out == first_run


def test_a_match_with_every_bot_in_the_bots_folder_finishes(capsys):
    exit_code = main(["--bots", str(REAL_BOTS_FOLDER), "--no-animate"])
    first_line = capsys.readouterr().out.splitlines()[0]
    assert exit_code == 0
    assert first_line.startswith(("Winner: ", "Draw"))


def test_too_few_bots_is_a_friendly_error(tmp_path, capsys):
    exit_code = main(["--bots", str(tmp_path), "--no-animate"])
    assert exit_code == 1
    assert "Need at least 2 bots" in capsys.readouterr().err
