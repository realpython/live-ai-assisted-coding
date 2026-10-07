"""Picks on the weakest: hunts the opponent with the least HP and attacks it."""

from botbattle.view import ATTACKS, DIRECTIONS, Action, BotView


def act(view: BotView) -> Action:
    if not view.others:
        return Action.WAIT

    me = view.me
    # Weakest first. If two are equally weak, go for the closer one.
    target = min(
        view.others,
        key=lambda other: (other.hp, abs(other.x - me.x) + abs(other.y - me.y)),
    )
    dx = target.x - me.x
    dy = target.y - me.y

    # If the target is right next to us, attack it.
    for direction, step in DIRECTIONS.items():
        if step == (dx, dy):
            return ATTACKS[direction]

    # Otherwise close the bigger gap first.
    if abs(dx) >= abs(dy):
        return Action.RIGHT if dx > 0 else Action.LEFT
    return Action.DOWN if dy > 0 else Action.UP
