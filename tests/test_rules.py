import pytest

from botbattle.game import STARTING_HP, Game
from botbattle.view import Action


def wait_bot(view):
    return Action.WAIT


def make_game(*positions):
    """Make a 5x5 game with one bot on each of the given squares."""
    bots = [(f"bot{number}", wait_bot) for number in range(len(positions))]
    game = Game(bots, size=5)
    for bot, (x, y) in zip(game.bots, positions, strict=True):
        bot.x, bot.y = x, y
    return game


def test_bots_start_on_different_squares_with_full_hp():
    bots = [(f"bot{number}", wait_bot) for number in range(25)]
    game = Game(bots, size=5)
    squares = {(bot.x, bot.y) for bot in game.bots}
    assert len(squares) == 25
    assert all(bot.hp == STARTING_HP for bot in game.bots)


def test_too_many_bots_is_an_error():
    bots = [(f"bot{number}", wait_bot) for number in range(26)]
    with pytest.raises(ValueError):
        Game(bots, size=5)


def test_move_to_an_open_square():
    game = make_game((2, 2))
    bot = game.bots[0]
    game.apply_action(bot, Action.UP)
    assert (bot.x, bot.y) == (2, 1)
    game.apply_action(bot, Action.RIGHT)
    assert (bot.x, bot.y) == (3, 1)


def test_move_off_the_grid_is_ignored():
    game = make_game((0, 0))
    bot = game.bots[0]
    game.apply_action(bot, Action.UP)
    game.apply_action(bot, Action.LEFT)
    assert (bot.x, bot.y) == (0, 0)


def test_move_into_another_bot_is_ignored():
    game = make_game((1, 1), (2, 1))
    bot = game.bots[0]
    game.apply_action(bot, Action.RIGHT)
    assert (bot.x, bot.y) == (1, 1)


def test_attack_hits_the_neighbour_in_that_direction():
    game = make_game((1, 1), (2, 1))
    attacker, target = game.bots
    game.apply_action(attacker, Action.ATTACK_RIGHT)
    assert target.hp == STARTING_HP - 1


def test_attack_in_another_direction_misses():
    game = make_game((1, 1), (2, 1))
    attacker, target = game.bots
    game.apply_action(attacker, Action.ATTACK_LEFT)
    game.apply_action(attacker, Action.ATTACK_UP)
    assert target.hp == STARTING_HP


def test_attack_on_an_empty_square_does_nothing():
    game = make_game((1, 1), (3, 3))
    game.apply_action(game.bots[0], Action.ATTACK_DOWN)
    assert all(bot.hp == STARTING_HP for bot in game.bots)


def test_bot_at_zero_hp_is_removed():
    game = make_game((1, 1), (2, 1))
    attacker, target = game.bots
    for _ in range(STARTING_HP):
        game.apply_action(attacker, Action.ATTACK_RIGHT)
    assert not target.is_alive
    assert game.living_bots() == [attacker]
    assert game.bot_at(2, 1) is None
    # The square is free again.
    game.apply_action(attacker, Action.RIGHT)
    assert (attacker.x, attacker.y) == (2, 1)


def test_wait_does_nothing():
    game = make_game((1, 1), (2, 1))
    attacker, target = game.bots
    game.apply_action(attacker, Action.WAIT)
    assert (attacker.x, attacker.y) == (1, 1)
    assert target.hp == STARTING_HP
