"""Runs from the nearest opponent. If it can't get away, it fights back."""

from botbattle.view import ATTACKS, DIRECTIONS, Action, BotView


def distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x1 - x2) + abs(y1 - y2)


def act(view: BotView) -> Action:
    if not view.others:
        return Action.WAIT

    me = view.me
    target = min(view.others, key=lambda other: distance(me.x, me.y, other.x, other.y))

    # Find the move that ends up farthest away, staying on the grid.
    best_move = Action.WAIT
    best_distance = distance(me.x, me.y, target.x, target.y)
    for direction, (dx, dy) in DIRECTIONS.items():
        new_x, new_y = me.x + dx, me.y + dy
        if not (0 <= new_x < view.width and 0 <= new_y < view.height):
            continue
        new_distance = distance(new_x, new_y, target.x, target.y)
        if new_distance > best_distance:
            best_move = direction
            best_distance = new_distance
    if best_move != Action.WAIT:
        return best_move

    # Cornered: hit an adjacent opponent if there is one.
    for direction, (dx, dy) in DIRECTIONS.items():
        for other in view.others:
            if (other.x, other.y) == (me.x + dx, me.y + dy):
                return ATTACKS[direction]
    return Action.WAIT
