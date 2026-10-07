import random

import pytest

from botbattle.game import STARTING_HP, Game
from botbattle.view import ACTIONS


def wait_bot(view):
    return "wait"


def attack_right_bot(view):
    return "attack_right"


def attack_left_bot(view):
    return "attack_left"


def random_bot(view):
    return random.choice(sorted(ACTIONS))


def make_game(*bots_and_squares, max_rounds=200):
    """Make a 5x5 game from (bot function, (x, y)) pairs."""
    bots = [(f"bot{number}", act) for number, (act, _) in enumerate(bots_and_squares)]
    game = Game(bots, size=5, max_rounds=max_rounds)
    for bot, (_, (x, y)) in zip(game.bots, bots_and_squares, strict=True):
        bot.x, bot.y = x, y
    return game


def play_to_end(game):
    while not game.is_over:
        game.play_round()


def test_last_bot_standing_wins():
    game = make_game((attack_right_bot, (1, 1)), (wait_bot, (2, 1)))
    play_to_end(game)
    assert game.winner is game.bots[0]
    assert game.round == STARTING_HP


def test_round_limit_is_a_draw():
    game = make_game((wait_bot, (0, 0)), (wait_bot, (4, 4)), max_rounds=5)
    play_to_end(game)
    assert game.round == 5
    assert game.winner is None


def test_same_seed_replays_the_same_match():
    def play_and_record(seed):
        bots = [(f"bot{number}", random_bot) for number in range(4)]
        game = Game(bots, seed=seed)
        history = []
        while not game.is_over:
            game.play_round()
            history.append([(bot.x, bot.y, bot.hp) for bot in game.bots])
        return history

    assert play_and_record(seed=42) == play_and_record(seed=42)


def test_bot_sees_itself_and_living_opponents():
    seen = []

    def watching_bot(view):
        seen.append(view)
        return "wait"

    game = make_game((watching_bot, (0, 0)), (wait_bot, (3, 3)), (wait_bot, (4, 4)))
    game.bots[2].hp = 0
    game.play_round()
    view = seen[0]
    assert (view.me.x, view.me.y, view.me.hp) == (0, 0, STARTING_HP)
    assert [other.name for other in view.others] == ["bot1"]
    assert view.round == 1


def crashing_bot(view):
    raise RuntimeError("Oops")


def cheating_bot(view):
    view.me.hp = 99  # Not allowed: the view is read-only
    return "up"


@pytest.mark.parametrize(
    "bad_bot",
    [
        crashing_bot,
        cheating_bot,
        lambda view: "fly",
        lambda view: None,
        lambda view: ["up"],
    ],
)
def test_misbehaving_bot_just_waits(bad_bot):
    game = make_game((bad_bot, (1, 1)), (wait_bot, (2, 1)))
    game.play_round()
    bad, neighbour = game.bots
    assert (bad.x, bad.y, bad.hp) == (1, 1, STARTING_HP)
    assert neighbour.hp == STARTING_HP


def test_bot_knocked_out_mid_round_does_not_act(monkeypatch):
    # Turn off shuffling so the bots act in order: bot0, then bot1.
    monkeypatch.setattr(random, "shuffle", lambda items: None)
    game = make_game((attack_right_bot, (1, 1)), (attack_left_bot, (2, 1)))
    attacker, target = game.bots
    target.hp = 1
    game.play_round()
    assert not target.is_alive
    assert attacker.hp == STARTING_HP
