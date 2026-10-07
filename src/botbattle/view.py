"""What a bot can see each turn, and the actions it can choose from."""

from dataclasses import dataclass

# Each direction is an (x, y) step. (0, 0) is the top-left square,
# so "up" makes y smaller and "down" makes it bigger.
DIRECTIONS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}

ACTIONS = {
    "up",
    "down",
    "left",
    "right",
    "attack_up",
    "attack_down",
    "attack_left",
    "attack_right",
    "wait",
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
