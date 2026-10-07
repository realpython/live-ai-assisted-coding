"""The rules of Bot Battle: the board, moves, attacks, and hit points."""

import random
from collections.abc import Callable
from dataclasses import dataclass

from botbattle.view import ACTIONS, DIRECTIONS, BotInfo, BotView

STARTING_HP = 3

# A bot is any function that takes a BotView and returns an action name.
BotFunction = Callable[[BotView], str]


@dataclass
class Bot:
    """A bot's real state. Bots never see this, only a BotView."""

    name: str
    act: BotFunction
    x: int
    y: int
    hp: int = STARTING_HP

    @property
    def is_alive(self) -> bool:
        return self.hp > 0


class Game:
    """A match between bots on a square grid."""

    def __init__(
        self,
        bots: list[tuple[str, BotFunction]],
        size: int = 10,
        max_rounds: int = 200,
        seed: int | None = None,
    ) -> None:
        if len(bots) > size * size:
            raise ValueError(f"{len(bots)} bots don't fit on a {size}x{size} grid")
        self.size = size
        self.max_rounds = max_rounds
        self.round = 0

        # Seeding the random module makes the whole match repeatable,
        # including any bots that use random to make their choices.
        random.seed(seed)

        # Pick a different random square for each bot.
        squares = [(x, y) for x in range(size) for y in range(size)]
        start_squares = random.sample(squares, len(bots))
        self.bots = [
            Bot(name=name, act=act, x=x, y=y)
            for (name, act), (x, y) in zip(bots, start_squares, strict=True)
        ]

    @property
    def is_over(self) -> bool:
        """The match ends when one bot (or none) is left, or time runs out."""
        return len(self.living_bots()) <= 1 or self.round >= self.max_rounds

    @property
    def winner(self) -> Bot | None:
        """Return the last bot standing, or None if there isn't one."""
        living = self.living_bots()
        return living[0] if len(living) == 1 else None

    def play_round(self) -> None:
        """Let every living bot act once, in a random order."""
        self.round += 1
        order = self.living_bots()
        random.shuffle(order)
        for bot in order:
            if bot.is_alive:  # It may have been knocked out earlier this round
                self.apply_action(bot, self.choose_action(bot))

    def choose_action(self, bot: Bot) -> str:
        """Ask a bot for its action. A crash or an invalid answer means "wait"."""
        try:
            action = bot.act(self.make_view(bot))
        except Exception:
            # A broken bot must never stop the match, so it just loses its turn.
            return "wait"
        if not isinstance(action, str) or action not in ACTIONS:
            return "wait"
        return action

    def make_view(self, bot: Bot) -> BotView:
        """Build a fresh, read-only view of the game for one bot."""
        others = tuple(
            BotInfo(name=other.name, x=other.x, y=other.y, hp=other.hp)
            for other in self.living_bots()
            if other is not bot
        )
        return BotView(
            me=BotInfo(name=bot.name, x=bot.x, y=bot.y, hp=bot.hp),
            others=others,
            width=self.size,
            height=self.size,
            round=self.round,
        )

    def living_bots(self) -> list[Bot]:
        """Return the bots that are still in the game."""
        return [bot for bot in self.bots if bot.is_alive]

    def bot_at(self, x: int, y: int) -> Bot | None:
        """Return the living bot on square (x, y), or None if it's empty."""
        for bot in self.living_bots():
            if bot.x == x and bot.y == y:
                return bot
        return None

    def is_on_grid(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size

    def apply_action(self, bot: Bot, action: str) -> None:
        """Carry out one bot's action. Anything not allowed does nothing."""
        if action in DIRECTIONS:
            self.move(bot, action)
        elif action.startswith("attack_"):
            direction = action.removeprefix("attack_")
            if direction in DIRECTIONS:
                self.attack(bot, direction)
        # "wait" needs no code: the bot simply does nothing.

    def move(self, bot: Bot, direction: str) -> None:
        """Move one square, unless that's off the grid or already taken."""
        dx, dy = DIRECTIONS[direction]
        new_x, new_y = bot.x + dx, bot.y + dy
        if self.is_on_grid(new_x, new_y) and self.bot_at(new_x, new_y) is None:
            bot.x, bot.y = new_x, new_y

    def attack(self, bot: Bot, direction: str) -> None:
        """Hit the bot on the neighbouring square, if there is one."""
        dx, dy = DIRECTIONS[direction]
        target = self.bot_at(bot.x + dx, bot.y + dy)
        if target is not None:
            target.hp -= 1  # At 0 HP, it drops out of living_bots()
