from __future__ import annotations

if __package__:
    from .disc_color import DiscColor
else:
    from disc_color import DiscColor


class Board:
    rows: int = 6
    cols: int = 7
    grid: list[list[DiscColor | None]]

    def __init__(self) -> None:
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def can_place(self, column: int) -> bool:
        if not (0 <= column < self.cols):
            return False
        return self.grid[0][column] is None

    def place_disc(self, column: int, color: DiscColor) -> int:
        if not self.can_place(column):
            raise ValueError("Cannot place disc in this column")

        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][column] is None:
                self.grid[row][column] = color
                return row
        raise Exception("Board full but can_place said it was possible")  # Should not happen

    def is_full(self) -> bool:
        return all(self.grid[0][col] is not None for col in range(self.cols))

    def check_win(self, row: int, column: int, color: DiscColor) -> bool:
        directions = [
            (1, 0),  # vertical
            (0, 1),  # horizontal
            (1, 1),  # diagonal \\ 
            (1, -1), # diagonal //
        ]

        for dr, dc in directions:
            count = 1
            # check in one direction
            for i in range(1, 4):
                r, c = row + i * dr, column + i * dc
                if 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] == color:
                    count += 1
                else:
                    break
            
            # check in opposite direction
            for i in range(1, 4):
                r, c = row - i * dr, column - i * dc
                if 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] == color:
                    count += 1
                else:
                    break
            
            if count >= 4:
                return True

        return False

    def get_cell(self, row: int, column: int) -> DiscColor | None:
        return self.grid[row][column]

    def clear_cell(self, row: int, column: int) -> None:
        if 0 <= row < self.rows and 0 <= column < self.cols:
            self.grid[row][column] = None

    clearCell = clear_cell
