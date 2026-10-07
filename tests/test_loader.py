from pathlib import Path

from botbattle.loader import load_bots
from botbattle.view import ACTIONS, BotInfo, BotView

REAL_BOTS_FOLDER = Path(__file__).parent.parent / "bots"


def make_view(me_square, *other_squares):
    """Make a 10x10 view with our bot and any number of opponents."""
    me = BotInfo("me", *me_square, hp=3)
    others = tuple(
        BotInfo(f"other{number}", x, y, hp=3)
        for number, (x, y) in enumerate(other_squares)
    )
    return BotView(me=me, others=others, width=10, height=10, round=1)


def load_real_bots():
    return dict(load_bots(REAL_BOTS_FOLDER))


def test_loads_bots_sorted_by_name(tmp_path):
    (tmp_path / "zebra.py").write_text("def act(view):\n    return 'up'\n")
    (tmp_path / "ant.py").write_text("def act(view):\n    return 'wait'\n")

    bots = load_bots(tmp_path)

    assert [name for name, _ in bots] == ["ant", "zebra"]
    assert bots[0][1](make_view((0, 0))) == "wait"
    assert bots[1][1](make_view((0, 0))) == "up"


def test_skips_file_without_act(tmp_path, capsys):
    (tmp_path / "no_act.py").write_text("x = 1\n")

    assert load_bots(tmp_path) == []
    assert "Skipping" in capsys.readouterr().err


def test_skips_file_with_syntax_error(tmp_path, capsys):
    (tmp_path / "broken.py").write_text("def act(view\n")

    assert load_bots(tmp_path) == []
    assert "Skipping" in capsys.readouterr().err


def test_skips_file_starting_with_underscore(tmp_path):
    (tmp_path / "_helper.py").write_text("def act(view):\n    return 'wait'\n")

    assert load_bots(tmp_path) == []


def test_real_bots_load_and_return_valid_actions():
    bots = load_bots(REAL_BOTS_FOLDER)
    names = [name for name, _ in bots]
    assert {"chaser", "coward", "random_walker"} <= set(names)

    view = make_view((4, 4), (7, 2))
    for _, act in bots:
        assert act(view) in ACTIONS


def test_chaser_attacks_adjacent_opponent():
    chaser = load_real_bots()["chaser"]
    assert chaser(make_view((4, 4), (5, 4))) == "attack_right"
    assert chaser(make_view((4, 4), (4, 3))) == "attack_up"


def test_chaser_moves_toward_distant_opponent():
    chaser = load_real_bots()["chaser"]
    assert chaser(make_view((4, 4), (8, 5))) == "right"
    assert chaser(make_view((4, 4), (3, 0))) == "up"


def test_chaser_and_coward_wait_when_alone():
    bots = load_real_bots()
    assert bots["chaser"](make_view((4, 4))) == "wait"
    assert bots["coward"](make_view((4, 4))) == "wait"


def test_coward_moves_away_from_nearby_opponent():
    coward = load_real_bots()["coward"]
    # Opponent on the right: left, up and down all gain distance, right does not.
    assert coward(make_view((4, 4), (5, 4))) in {"left", "up", "down"}
    # Opponent above and a wall behind us: only sidestepping helps.
    assert coward(make_view((0, 9), (0, 8))) == "right"


def test_coward_fights_back_when_cornered():
    coward = load_real_bots()["coward"]
    # A 2x1 grid leaves no square to run to.
    me = BotInfo("me", 0, 0, hp=3)
    neighbour = BotInfo("neighbour", 1, 0, hp=3)
    view = BotView(me=me, others=(neighbour,), width=2, height=1, round=1)
    assert coward(view) == "attack_right"
