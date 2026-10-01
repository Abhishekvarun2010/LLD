from __future__ import annotations

import argparse
import json
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

if __package__:
    from .disc_color import DiscColor
    from .game import Game
    from .player import Player
else:
    from disc_color import DiscColor
    from game import Game
    from player import Player


def new_game() -> Game:
    return Game(
        Player("Red", DiscColor.RED),
        Player("Yellow", DiscColor.YELLOW),
    )


def game_data(game: Game) -> dict[str, object]:
    winner = game.get_winner()
    current_player = game.get_current_player()
    return {
        "board": [
            [cell.value.lower() if cell is not None else None for cell in row]
            for row in game.get_board().grid
        ],
        "state": game.get_game_state().value,
        "currentPlayer": current_player.get_name(),
        "currentColor": current_player.get_color().value.lower(),
        "winner": winner.get_name() if winner is not None else None,
        "canUndo": game.can_undo(),
    }


class ConnectFourHandler(SimpleHTTPRequestHandler):
    game = new_game()

    def do_GET(self) -> None:
        if self.path == "/api/game":
            self.send_json(game_data(self.game))
            return
        super().do_GET()

    def do_POST(self) -> None:
        if self.path == "/api/game":
            self.game = new_game()
            type(self).game = self.game
            self.send_json(game_data(self.game))
            return

        if self.path == "/api/move":
            payload = self.read_json()
            column = payload.get("column") if payload is not None else None
            if not isinstance(column, int):
                self.send_json({"error": "'column' must be an integer."}, HTTPStatus.BAD_REQUEST)
                return

            accepted = self.game.make_move(self.game.get_current_player(), column)
            self.send_json({"accepted": accepted, "game": game_data(self.game)})
            return

        if self.path == "/api/undo":
            accepted = self.game.undo()
            self.send_json({"accepted": accepted, "game": game_data(self.game)})
            return

        self.send_error(HTTPStatus.NOT_FOUND)

    def read_json(self) -> dict[str, object] | None:
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(content_length)
            payload = json.loads(body)
        except (ValueError, json.JSONDecodeError):
            return None
        return payload if isinstance(payload, dict) else None

    def send_json(self, data: dict[str, object], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Connect Four web app.")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    directory = Path(__file__).parent
    handler = lambda *args, **kwargs: ConnectFourHandler(*args, directory=directory, **kwargs)
    server = ThreadingHTTPServer(("localhost", args.port), handler)
    print(f"Open http://localhost:{args.port} in your browser")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
