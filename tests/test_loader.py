from pathlib import Path

from botbattle.loader import load_bots
from botbattle.view import Action, BotInfo, BotView

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
    shipped = {"chaser", "coward", "example", "hit_and_run", "random_walker"}
    assert shipped | {"turret", "vulture"} <= set(names)

    view = make_view((4, 4), (7, 2))
    for _, act in bots:
        assert act(view) in Action


def test_chaser_attacks_adjacent_opponent():
    chaser = load_real_bots()["chaser"]
    assert chaser(make_view((4, 4), (5, 4))) == Action.ATTACK_RIGHT
    assert chaser(make_view((4, 4), (4, 3))) == Action.ATTACK_UP


def test_chaser_moves_toward_distant_opponent():
    chaser = load_real_bots()["chaser"]
    assert chaser(make_view((4, 4), (8, 5))) == Action.RIGHT
    assert chaser(make_view((4, 4), (3, 0))) == Action.UP


def test_chaser_and_coward_wait_when_alone():
    bots = load_real_bots()
    assert bots["chaser"](make_view((4, 4))) == Action.WAIT
    assert bots["coward"](make_view((4, 4))) == Action.WAIT


def test_coward_moves_away_from_nearby_opponent():
    coward = load_real_bots()["coward"]
    # Opponent on the right: left, up and down all gain distance, right does not.
    assert coward(make_view((4, 4), (5, 4))) in {Action.LEFT, Action.UP, Action.DOWN}
    # Opponent above and a wall behind us: only sidestepping helps.
    assert coward(make_view((0, 9), (0, 8))) == Action.RIGHT


def test_coward_fights_back_when_cornered():
    coward = load_real_bots()["coward"]
    # A 2x1 grid leaves no square to run to.
    me = BotInfo("me", 0, 0, hp=3)
    neighbour = BotInfo("neighbour", 1, 0, hp=3)
    view = BotView(me=me, others=(neighbour,), width=2, height=1, round=1)
    assert coward(view) == Action.ATTACK_RIGHT


def test_vulture_goes_for_the_weakest_opponent():
    vulture = load_real_bots()["vulture"]
    me = BotInfo("me", 4, 4, hp=3)
    strong_and_close = BotInfo("strong", 5, 4, hp=3)
    weak_and_far = BotInfo("weak", 4, 8, hp=1)
    view = BotView(
        me=me, others=(strong_and_close, weak_and_far), width=10, height=10, round=1
    )
    assert vulture(view) == Action.DOWN


def test_vulture_attacks_the_weakest_when_it_is_next_to_it():
    vulture = load_real_bots()["vulture"]
    me = BotInfo("me", 4, 4, hp=3)
    weak = BotInfo("weak", 4, 3, hp=1)
    view = BotView(me=me, others=(weak,), width=10, height=10, round=1)
    assert vulture(view) == Action.ATTACK_UP


def test_turret_never_moves():
    turret = load_real_bots()["turret"]
    assert turret(make_view((4, 4), (8, 8))) == Action.WAIT
    assert turret(make_view((4, 4), (4, 5))) == Action.ATTACK_DOWN


def test_hit_and_run_chases_when_healthy():
    hit_and_run = load_real_bots()["hit_and_run"]
    assert hit_and_run(make_view((4, 4), (5, 4))) == Action.ATTACK_RIGHT
    assert hit_and_run(make_view((4, 4), (4, 8))) == Action.DOWN


def test_hit_and_run_flees_when_hurt():
    hit_and_run = load_real_bots()["hit_and_run"]
    me = BotInfo("me", 4, 4, hp=1)
    attacker = BotInfo("attacker", 5, 4, hp=3)
    view = BotView(me=me, others=(attacker,), width=10, height=10, round=1)
    assert hit_and_run(view) in {Action.LEFT, Action.UP, Action.DOWN}
