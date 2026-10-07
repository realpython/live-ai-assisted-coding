"""Wanders aimlessly: each turn it picks a random move or waits."""

import random

from botbattle.view import DIRECTIONS, BotView

CHOICES = list(DIRECTIONS) + ["wait"]


def act(view: BotView) -> str:
    return random.choice(CHOICES)
