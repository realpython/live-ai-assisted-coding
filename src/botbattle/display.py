"""Turn a game into one frame of text: a header, the grid, and an HP panel."""

import string
from itertools import zip_longest

from botbattle.game import STARTING_HP, Bot, Game

# Capitals first, then lowercase, so even a big match gets a letter per bot.
LETTERS = string.ascii_uppercase + string.ascii_lowercase

GAP = " " * 4  # Space between the grid and the HP panel


def letter_for(index: int) -> str:
    """Return the letter that stands for the bot at this position."""
    return LETTERS[index % len(LETTERS)]


def hearts_for(bot: Bot) -> str:
    """Show remaining HP as ♥ and lost HP as ♡, or "out" if defeated."""
    if not bot.is_alive:
        return "out"
    return "♥" * bot.hp + "♡" * (STARTING_HP - bot.hp)


def render_grid(game: Game) -> list[str]:
    """Draw the grid: one line per row, with `.` for an empty square."""
    rows = [["."] * game.size for _ in range(game.size)]
    for index, bot in enumerate(game.bots):
        if bot.is_alive:
            rows[bot.y][bot.x] = letter_for(index)
    return [" ".join(row) for row in rows]


def render_panel(game: Game) -> list[str]:
    """Draw one line per bot with its letter, name, and hearts."""
    name_width = max(len(bot.name) for bot in game.bots)
    lines = []
    for index, bot in enumerate(game.bots):
        letter = letter_for(index)
        hearts = hearts_for(bot)
        lines.append(f"{letter} {bot.name:<{name_width}} {hearts}")
    return lines


def render(game: Game) -> str:
    """Return one frame of the match as text."""
    lines = [f"Round {game.round}/{game.max_rounds}", ""]

    grid_lines = render_grid(game)
    panel_lines = render_panel(game)
    grid_width = len(grid_lines[0])
    for grid_line, panel_line in zip_longest(grid_lines, panel_lines, fillvalue=""):
        lines.append(f"{grid_line:<{grid_width}}{GAP}{panel_line}".rstrip())

    if game.is_over:
        lines.append("")
        if game.winner is None:
            lines.append("Draw")
        else:
            lines.append(f"Winner: {game.winner.name}")
    return "\n".join(lines)
