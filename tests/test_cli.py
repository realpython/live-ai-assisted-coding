from pathlib import Path

from botbattle.cli import CLEAR_SCREEN, main

REAL_BOTS_FOLDER = str(Path(__file__).parent.parent / "bots")
DEMO_SEED = "1"  # The shipped bots play to a winner with this seed


def test_no_animate_prints_only_the_result(capsys):
    exit_code = main(["--bots", REAL_BOTS_FOLDER, "--seed", DEMO_SEED, "--no-animate"])
    output = capsys.readouterr().out
    assert exit_code == 0
    assert output.splitlines()[0].startswith("Winner: ")
    assert "Seed: 1" in output
    assert CLEAR_SCREEN not in output


def test_animation_redraws_every_round_and_ends_with_the_result(capsys):
    main(["--bots", REAL_BOTS_FOLDER, "--seed", DEMO_SEED, "--delay", "0"])
    frames = capsys.readouterr().out.split(CLEAR_SCREEN)[1:]
    assert frames[0].startswith("Round 0/200")
    assert "Winner: " in frames[-1]
    assert "Winner: " not in frames[-2]


def test_without_a_seed_it_prints_one_that_replays_the_match(capsys):
    main(["--bots", REAL_BOTS_FOLDER, "--no-animate"])
    first_run = capsys.readouterr().out
    seed = first_run.split("Seed: ")[1].split()[0]

    main(["--bots", REAL_BOTS_FOLDER, "--no-animate", "--seed", seed])
    assert capsys.readouterr().out == first_run


def test_too_few_bots_is_a_friendly_error(tmp_path, capsys):
    exit_code = main(["--bots", str(tmp_path), "--no-animate"])
    assert exit_code == 1
    assert "Need at least 2 bots" in capsys.readouterr().err
