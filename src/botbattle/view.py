"""What a bot can see each turn, and the actions it can choose from."""

from dataclasses import dataclass
from enum import StrEnum


class Action(StrEnum):
    """Everything a bot can do on its turn.

    A StrEnum member is also a plain string, so a bot can return either
    Action.ATTACK_UP or "attack_up". Typos like Action.ATTAK_UP fail loudly.
    """

    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    ATTACK_UP = "attack_up"
    ATTACK_DOWN = "attack_down"
    ATTACK_LEFT = "attack_left"
    ATTACK_RIGHT = "attack_right"
    WAIT = "wait"


# Each move is an (x, y) step. (0, 0) is the top-left square,
# so UP makes y smaller and DOWN makes it bigger.
DIRECTIONS = {
    Action.UP: (0, -1),
    Action.DOWN: (0, 1),
    Action.LEFT: (-1, 0),
    Action.RIGHT: (1, 0),
}

# The attack that goes with each direction.
ATTACKS = {
    Action.UP: Action.ATTACK_UP,
    Action.DOWN: Action.ATTACK_DOWN,
    Action.LEFT: Action.ATTACK_LEFT,
    Action.RIGHT: Action.ATTACK_RIGHT,
}


@dataclass(frozen=True)
class BotInfo:
    """What anyone can see about a bot: its name, position, and hit points."""

    name: str
    x: int
    y: int
    hp: int


@dataclass(frozen=True)
class BotView:
    """Everything a bot is told on its turn.

    The grid runs from (0, 0) in the top-left corner to
    (width - 1, height - 1) in the bottom-right corner.
    """

    me: BotInfo
    others: tuple[BotInfo, ...]  # Opponents still in the game
    width: int
    height: int
    round: int
