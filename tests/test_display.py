from botbattle.display import render
from botbattle.game import Game
from botbattle.view import Action


def wait_bot(view):
    return Action.WAIT


def make_game(max_rounds=200):
    """Make a 3x3 game: chaser at the top-left, coward at the bottom-right."""
    game = Game(
        [("chaser", wait_bot), ("coward", wait_bot)], size=3, max_rounds=max_rounds
    )
    game.bots[0].x, game.bots[0].y = 0, 0
    game.bots[1].x, game.bots[1].y = 2, 2
    return game


def test_fresh_game_frame():
    game = make_game()
    assert render(game) == "\n".join(
        [
            "Round 0/200",
            "",
            "A . .    A chaser ♥♥♥",
            ". . .    B coward ♥♥♥",
            ". . B",
        ]
    )


def test_lost_hp_shows_empty_hearts():
    game = make_game()
    game.round = 12
    game.bots[0].hp = 1
    assert render(game) == "\n".join(
        [
            "Round 12/200",
            "",
            "A . .    A chaser ♥♡♡",
            ". . .    B coward ♥♥♥",
            ". . B",
        ]
    )


def test_removed_bot_is_not_drawn_and_shows_out():
    game = make_game()
    game.bots[1].hp = 0
    frame = render(game)
    assert "B coward out" in frame
    assert frame.splitlines()[4] == ". . ."  # The coward's square is empty


def test_finished_game_shows_the_winner():
    game = make_game()
    game.round = 7
    game.bots[1].hp = 0
    assert render(game) == "\n".join(
        [
            "Round 7/200",
            "",
            "A . .    A chaser ♥♥♥",
            ". . .    B coward out",
            ". . .",
            "",
            "Winner: chaser",
        ]
    )


def test_round_limit_shows_a_draw():
    game = make_game(max_rounds=5)
    game.round = 5
    assert render(game).endswith("\n\nDraw")
