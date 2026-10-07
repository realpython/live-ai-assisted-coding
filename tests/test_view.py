import dataclasses

import pytest

from botbattle.view import ATTACKS, DIRECTIONS, Action, BotInfo, BotView


def make_view() -> BotView:
    me = BotInfo(name="me", x=1, y=2, hp=3)
    other = BotInfo(name="other", x=4, y=5, hp=2)
    return BotView(me=me, others=(other,), width=10, height=10, round=1)


def test_bot_info_is_read_only():
    view = make_view()
    with pytest.raises(dataclasses.FrozenInstanceError):
        view.me.hp = 99


def test_bot_view_is_read_only():
    view = make_view()
    with pytest.raises(dataclasses.FrozenInstanceError):
        view.round = 5


def test_actions_are_four_moves_four_attacks_and_wait():
    assert len(Action) == 9
    assert len(DIRECTIONS) == 4
    assert set(ATTACKS) == set(DIRECTIONS)
    assert Action.WAIT in Action


def test_actions_are_also_plain_strings():
    assert Action.ATTACK_UP == "attack_up"
    assert Action("wait") is Action.WAIT


def test_up_makes_y_smaller():
    assert DIRECTIONS[Action.UP] == (0, -1)
    assert DIRECTIONS[Action.DOWN] == (0, 1)
