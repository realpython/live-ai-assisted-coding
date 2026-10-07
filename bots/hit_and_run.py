"""Fights while healthy, runs when hurt: chases at 2 HP or more, flees at 1 HP."""

from botbattle.view import ATTACKS, DIRECTIONS, Action, BotView


def distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x1 - x2) + abs(y1 - y2)


def act(view: BotView) -> Action:
    if not view.others:
        return Action.WAIT

    me = view.me
    nearest = min(view.others, key=lambda other: distance(me.x, me.y, other.x, other.y))

    # Try every move that stays on the grid, and note how far it leaves us.
    moves = {}
    for direction, (dx, dy) in DIRECTIONS.items():
        new_x, new_y = me.x + dx, me.y + dy
        if 0 <= new_x < view.width and 0 <= new_y < view.height:
            moves[direction] = distance(new_x, new_y, nearest.x, nearest.y)

    if me.hp == 1:
        # Hurt: take the move that gets farthest away.
        return max(moves, key=moves.get)

    # Healthy: attack if the nearest opponent is next to us, else close in.
    for direction, step in DIRECTIONS.items():
        if step == (nearest.x - me.x, nearest.y - me.y):
            return ATTACKS[direction]
    return min(moves, key=moves.get)
