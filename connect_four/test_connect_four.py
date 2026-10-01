import unittest

from disc_color import DiscColor
from game import Game
from game_state import GameState
from move import Move
from player import Player


class TestConnectFourUndo(unittest.TestCase):
    def setUp(self):
        self.p1 = Player("Red", DiscColor.RED)
        self.p2 = Player("Yellow", DiscColor.YELLOW)
        self.game = Game(self.p1, self.p2)

    def test_move_class(self):
        move = Move(self.p1, 5, 3)
        self.assertEqual(move.get_player(), self.p1)
        self.assertEqual(move.get_row(), 5)
        self.assertEqual(move.get_col(), 3)

    def test_board_clear_cell(self):
        board = self.game.get_board()
        row = board.place_disc(0, DiscColor.RED)
        self.assertEqual(board.get_cell(row, 0), DiscColor.RED)
        board.clear_cell(row, 0)
        self.assertIsNone(board.get_cell(row, 0))
        # Test clearCell alias
        row2 = board.place_disc(0, DiscColor.YELLOW)
        board.clearCell(row2, 0)
        self.assertIsNone(board.get_cell(row2, 0))

    def test_undo_empty(self):
        self.assertFalse(self.game.can_undo())
        self.assertFalse(self.game.undo())

    def test_undo_single_move(self):
        self.assertEqual(self.game.get_current_player(), self.p1)
        self.assertTrue(self.game.make_move(self.p1, 2))
        self.assertEqual(self.game.get_current_player(), self.p2)
        self.assertEqual(len(self.game.get_moves()), 1)
        self.assertTrue(self.game.can_undo())

        # Undo move
        self.assertTrue(self.game.undo())
        self.assertEqual(self.game.get_current_player(), self.p1)
        self.assertFalse(self.game.can_undo())
        self.assertIsNone(self.game.get_board().get_cell(5, 2))

    def test_undo_multiple_moves(self):
        self.game.make_move(self.p1, 0) # Red at (5, 0)
        self.game.make_move(self.p2, 0) # Yellow at (4, 0)
        self.game.make_move(self.p1, 1) # Red at (5, 1)

        self.assertEqual(len(self.game.get_moves()), 3)
        self.assertEqual(self.game.get_current_player(), self.p2)

        # Undo 1
        self.assertTrue(self.game.undo())
        self.assertEqual(self.game.get_current_player(), self.p1)
        self.assertIsNone(self.game.get_board().get_cell(5, 1))

        # Undo 2
        self.assertTrue(self.game.undo())
        self.assertEqual(self.game.get_current_player(), self.p2)
        self.assertIsNone(self.game.get_board().get_cell(4, 0))

        # Undo 3
        self.assertTrue(self.game.undo())
        self.assertEqual(self.game.get_current_player(), self.p1)
        self.assertIsNone(self.game.get_board().get_cell(5, 0))
        self.assertFalse(self.game.can_undo())

    def test_undo_winning_move(self):
        # Setup vertical win for p1 in column 0
        # Red: col 0, Yellow: col 1
        for _ in range(3):
            self.game.make_move(self.p1, 0)
            self.game.make_move(self.p2, 1)

        # Winning move for p1
        self.assertTrue(self.game.make_move(self.p1, 0))
        self.assertEqual(self.game.get_game_state(), GameState.WON)
        self.assertEqual(self.game.get_winner(), self.p1)

        # Undo winning move
        self.assertTrue(self.game.undo())
        self.assertEqual(self.game.get_game_state(), GameState.IN_PROGRESS)
        self.assertIsNone(self.game.get_winner())
        self.assertEqual(self.game.get_current_player(), self.p1)
        self.assertIsNone(self.game.get_board().get_cell(2, 0))


if __name__ == "__main__":
    unittest.main()
