"""Wanders aimlessly: each turn it picks a random move or waits."""

import random

from botbattle.view import DIRECTIONS, Action, BotView

CHOICES = list(DIRECTIONS) + [Action.WAIT]


def act(view: BotView) -> Action:
    return random.choice(CHOICES)
