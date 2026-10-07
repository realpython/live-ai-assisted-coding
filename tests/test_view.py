import dataclasses

import pytest

from botbattle.view import ACTIONS, DIRECTIONS, BotInfo, BotView


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


def test_actions_are_moves_attacks_and_wait():
    assert len(ACTIONS) == 9
    for direction in DIRECTIONS:
        assert direction in ACTIONS
        assert f"attack_{direction}" in ACTIONS
    assert "wait" in ACTIONS


def test_up_makes_y_smaller():
    assert DIRECTIONS["up"] == (0, -1)
    assert DIRECTIONS["down"] == (0, 1)
