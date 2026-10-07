"""The example bot from the README. Copy this file to start your own bot."""

import random

from botbattle.view import ATTACKS, DIRECTIONS, Action, BotView


def act(view: BotView) -> Action:
    """Attack a neighbouring opponent if there is one, else wander."""
    me = view.me

    # Look at the square in each direction. If an opponent is standing
    # there, attack in that direction.
    for direction, (dx, dy) in DIRECTIONS.items():
        for other in view.others:
            if (other.x, other.y) == (me.x + dx, me.y + dy):
                return ATTACKS[direction]

    # Nobody is next to us, so move in a random direction.
    return random.choice(list(DIRECTIONS))
