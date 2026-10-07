"""Hunts the nearest opponent: attacks if it is next to us, else walks closer."""

from botbattle.view import ATTACKS, DIRECTIONS, Action, BotView


def act(view: BotView) -> Action:
    if not view.others:
        return Action.WAIT

    me = view.me
    for direction, (dx, dy) in DIRECTIONS.items():
        for other in view.others:
            if (other.x, other.y) == (me.x + dx, me.y + dy):
                return ATTACKS[direction]

    target = min(
        view.others, key=lambda other: abs(other.x - me.x) + abs(other.y - me.y)
    )
    dx = target.x - me.x
    dy = target.y - me.y

    # Close the bigger gap first.
    if abs(dx) >= abs(dy):
        return Action.RIGHT if dx > 0 else Action.LEFT
    return Action.DOWN if dy > 0 else Action.UP
