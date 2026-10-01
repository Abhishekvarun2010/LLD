from __future__ import annotations

if __package__:
    from .player import Player
else:
    from player import Player


class Move:
    player: Player
    row: int
    col: int

    def __init__(self, player: Player, row: int, col: int) -> None:
        self.player = player
        self.row = row
        self.col = col

    def get_player(self) -> Player:
        return self.player

    def get_row(self) -> int:
        return self.row

    def get_col(self) -> int:
        return self.col
