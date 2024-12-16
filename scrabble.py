import random
import copy
import itertools as it
from dataclasses import dataclass
from enum import IntEnum
from typing import List, Tuple


# Alias for readability
Letter = str  # synonym for str, but it's clear this represents game letters
CellCoord = Tuple[int, int]


class Direction(IntEnum):
    ACROSS = 1
    DOWN = 2


@dataclass(frozen=True, order=True)
class Position:
    direction: Direction
    row: int
    col: int


class Board:
    size: int
    _tiles: List[List[Letter]]

    def __init__(self) -> None:
        self.size = 15
        self._tiles = [["."] * self.size for _ in range(self.size)]

    def __str__(self) -> str:
        return "\n".join(" ".join(x if x != "." else "_" for x in row) for row in self._tiles)

    def all_positions(self) -> List[CellCoord]:
        """Returns all possible positions on the board."""
        return list(it.product(range(self.size), range(self.size)))

    def tile(self, pos: CellCoord) -> Letter:
        """Returns the tile at a given position."""
        row, col = pos
        return self._tiles[row][col]

    def set_tile(self, pos: CellCoord, tile: Letter) -> None:
        """Sets a tile at a given position."""
        row, col = pos
        self._tiles[row][col] = tile

    def in_bounds(self, pos: CellCoord) -> bool:
        """Checks if a given position is within the board's bounds."""
        row, col = pos
        return 0 <= row < self.size and 0 <= col < self.size

    def is_empty(self, pos: CellCoord) -> bool:
        """Checks if a position is empty."""
        return self.in_bounds(pos) and self.tile(pos) == "."

    def is_first_turn(self) -> bool:
        """Checks if it's the first move by checking if all cells are still empty."""
        return all(cell == "." for row in self._tiles for cell in row)

    def copy(self) -> "Board":
        """Returns a deep copy of the board state."""
        return copy.deepcopy(self)

    def place_word(self, word: str, start: CellCoord, direction: Direction) -> bool:
        """
        Places a word on the board if it's valid.
        :param word: Word to place
        :param start: Starting position (row, col)
        :param direction: Direction of placement (ACROSS or DOWN)
        """
        # Check if word can fit in the specified direction
        if direction == Direction.ACROSS:
            if start[1] + len(word) > self.size:
                return False
            for i, letter in enumerate(word):
                if not self.is_empty((start[0], start[1] + i)) and self.tile((start[0], start[1] + i)) != letter:
                    return False
        elif direction == Direction.DOWN:
            if start[0] + len(word) > self.size:
                return False
            for i, letter in enumerate(word):
                if not self.is_empty((start[0] + i, start[1])) and self.tile((start[0] + i, start[1])) != letter:
                    return False

        # If checks pass, place the word on the board
        for i, letter in enumerate(word):
            if direction == Direction.ACROSS:
                self.set_tile((start[0], start[1] + i), letter)
            elif direction == Direction.DOWN:
                self.set_tile((start[0] + i, start[1]), letter)

        return True


class TileManager:
    def __init__(self):
        self.pool = self.initialize_tile_pool()

    def initialize_tile_pool(self) -> List[Letter]:
        """
        Create a Scrabble-like tile pool based on actual distribution.
        """
        tile_distribution = {
            'A': 9, 'B': 2, 'C': 2, 'D': 4, 'E': 12, 'F': 2, 'G': 3,
            'H': 2, 'I': 9, 'J': 1, 'K': 1, 'L': 4, 'M': 2, 'N': 6,
            'O': 8, 'P': 2, 'Q': 1, 'R': 6, 'S': 4, 'T': 6, 'U': 4,
            'V': 2, 'W': 2, 'X': 1, 'Y': 2, 'Z': 1
        }
        pool = []
        for tile, count in tile_distribution.items():
            pool.extend([tile] * count)
        random.shuffle(pool)
        return pool

    def draw_tiles(self, num: int) -> List[Letter]:
        """Draws tiles from the pool."""
        drawn_tiles = [self.pool.pop() for _ in range(num) if self.pool]
        return drawn_tiles


class GameState:
    def __init__(self):
        self.board = Board()
        self.tile_manager = TileManager()
        self.players = {"human": [], "computer": []}

    def draw_player_tiles(self):
        """Draw initial tiles for a hypothetical player."""
        self.players["human"] = self.tile_manager.draw_tiles(7)

    def display_state(self):
        """Displays the board state and the player's hand."""
        print("\nCurrent Board State:\n")
        print(self.board)
        print("\nYour Tiles:", self.players['human'])

    def player_turn(self):
        """Handles the player's turn."""
        self.display_state()
        word = input("\nEnter a word to play: ").strip().upper()
        row = int(input("Enter starting row (1-15): ")) - 1
        col = int(input("Enter starting column (1-15): ")) - 1
        direction_input = input("Enter direction (ACROSS or DOWN): ").strip().upper()

        direction = Direction.ACROSS if direction_input == "ACROSS" else Direction.DOWN

        if word and self.board.place_word(word, (row, col), direction):
            for letter in word:
                if letter in self.players["human"]:
                    self.players["human"].remove(letter)
            self.players["human"] += self.tile_manager.draw_tiles(len(word))
            print("\nWord placed successfully!")
        else:
            print("\nInvalid move, try again!")

    def game_loop(self):
        """Main game loop."""
        self.draw_player_tiles()
        while True:
            self.player_turn()
            self.display_state()

    def start_game(self):
        """Ask the user to start or quit the game."""
        while True:
            user_input = input("Do you want to start the game? (yes/quit): ").strip().lower()
            if user_input == "yes":
                print("\nStarting the game...\n")
                self.game_loop()
                break
            elif user_input == "quit":
                print("\nExiting the game. Goodbye!")
                break
            else:
                print("\nInvalid input. Please type 'yes' to start or 'quit' to exit.")


if __name__ == "__main__":
    game = GameState()
    game.start_game()
