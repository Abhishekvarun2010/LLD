from __future__ import annotations

if __package__:
    from .board import Board
    from .game_state import GameState
    from .move import Move
    from .player import Player
else:
    from board import Board
    from game_state import GameState
    from move import Move
    from player import Player


class Game:
    board: Board
    player1: Player
    player2: Player
    current_player: Player
    state: GameState
    winner: Player | None
    moves: list[Move]

    def __init__(self, player1: Player, player2: Player) -> None:
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.state = GameState.IN_PROGRESS
        self.winner = None
        self.board = Board()
        self.moves = []

    def make_move(self, player: Player, column: int) -> bool:
        if player != self.current_player or self.state != GameState.IN_PROGRESS:
            return False
        
        try:
            row = self.board.place_disc(column, player.get_color())
            self.moves.append(Move(player, row, column))
            if self.board.check_win(row, column, player.get_color()):
                self.state = GameState.WON
                self.winner = player
            elif self.board.is_full():
                self.state = GameState.DRAW
            else:
                self.current_player = self.player2 if self.current_player == self.player1 else self.player1
            return True
        except ValueError:
            return False

    def undo(self) -> bool:
        if not self.moves:
            return False

        last_move = self.moves.pop()
        self.board.clear_cell(last_move.get_row(), last_move.get_col())
        self.current_player = last_move.get_player()
        self.state = GameState.IN_PROGRESS
        self.winner = None
        return True

    def can_undo(self) -> bool:
        return len(self.moves) > 0

    def get_moves(self) -> list[Move]:
        return self.moves

    def get_current_player(self) -> Player:
        return self.current_player

    def get_game_state(self) -> GameState:
        return self.state

    def get_winner(self) -> Player | None:
        return self.winner

    def get_board(self) -> Board:
        return self.board

