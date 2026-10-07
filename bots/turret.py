"""Never moves: attacks any opponent that comes next to it, and otherwise waits."""

from botbattle.view import ATTACKS, DIRECTIONS, Action, BotView


def act(view: BotView) -> Action:
    me = view.me
    for direction, (dx, dy) in DIRECTIONS.items():
        for other in view.others:
            if (other.x, other.y) == (me.x + dx, me.y + dy):
                return ATTACKS[direction]
    return Action.WAIT
