# Low Level Design (LLD)

A repository dedicated to Low Level Design (LLD) problems, object-oriented design patterns, and implementations.

## Projects

- [Connect Four](./connect_four) - Connect Four game design and implementation.

---

## Connect Four

> 💡 **Problem Statement:**  
> Build the object-oriented design for a two-player Connect Four game. Players take turns dropping discs into a 7-column, 6-row board. The first to align four of their own discs vertically, horizontally, or diagonally wins.

### Interview Clarification Notes

Get concrete specs from the interviewer based on this prompt:
- **System boundaries**
- **Future extensions**
- **Error cases**
- **Check if UI support is needed**

---

### Class Design

```
class Game:
    - board: Board
    - player1: Player
    - player2: Player
    - currentPlayer: Player
    - state: GameState        // IN_PROGRESS, WON, DRAW
    - winner: Player?
    - moves: Stack<Move>

    + Game(player1, player2)
    + makeMove(player, column) -> bool
    + undo() -> bool
    + getCurrentPlayer() -> Player
    + getGameState() -> GameState
    + getWinner() -> Player?
    + getBoard() -> Board
    + getMoves() -> List<Move>

class Board:
    - rows: int = 6
    - cols: int = 7
    - grid: DiscColor?[rows][cols]

    + Board()
    + canPlace(column) -> bool
    + placeDisc(column, color) -> int
    + clearCell(row, column) -> void
    + isFull() -> bool
    + checkWin(row, column, color) -> bool
    + getCell(row, column) -> DiscColor?

class Move:
    - player: Player
    - row: int
    - col: int

    + Move(player, row, col)
    + getPlayer() -> Player
    + getRow() -> int
    + getCol() -> int

class Player:
    - name: string
    - color: DiscColor

    + Player(name, color)
    + getName() -> string
    + getColor() -> DiscColor

enum GameState:
    IN_PROGRESS
    WON
    DRAW

enum DiscColor:
    RED
    YELLOW
```

---

### Implementation Focus

- **Core logic**: Turn switching, disc dropping gravity, 4-in-a-row checks (horizontal, vertical, diagonal).
- **Edge cases**: Out-of-bounds column inputs, full columns, draw conditions (full board).

### Key Rule

> [!IMPORTANT]
> Always separate the business logic, data, and UI.

---

### Running the App

```bash
cd connect_four
poetry run python server.py
```
Open [http://localhost:8000](http://localhost:8000) in your browser.
