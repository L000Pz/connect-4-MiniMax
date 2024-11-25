import numpy as np
import random
from typing import Tuple, Optional

# Constants for the game
BOARD_SIZE = 10  # Size of the board (10x10 grid)
EMPTY = 0        # Empty cell
P1 = 1           # Player 1
P2 = 2           # Player 2
AI = 3           # AI player

class Connect4:
    """
    A class representing the Connect 4 game. Supports a 10x10 board, dynamic AI depth,
    and two modes of turn selection (random or fixed turn order).
    """
    def __init__(self):
        """
        Initializes the Connect 4 board and related variables.
        """
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE))  # Create an empty board
        self.last_two_players = []  # Keep track of the last two players for random turn logic
        self.turn_order = [P1, P2, AI]  # Fixed turn order
        self.current_turn_index = 0  # Index for tracking fixed turn order

    def print_board(self):
        """
        Prints the current state of the board to the console.
        """
        # Print column numbers
        print(" ", end=" ")
        for i in range(BOARD_SIZE):
            print(f"{i+1:2}", end=" ")
        print()
        
        # Print the board with symbols
        for row in self.board:
            for cell in row:
                if cell == EMPTY:
                    print("⬜", end=" ")  # Empty cell
                elif cell == P1:
                    print("🔴", end=" ")  # Player 1
                elif cell == P2:
                    print("🔵", end=" ")  # Player 2
                elif cell == AI:
                    print("🤖", end=" ")  # AI player
            print()

    def check_for_win(self, player: int) -> bool:
        """
        Checks if the given player has won the game.

        Args:
            player (int): The player to check for a win.

        Returns:
            bool: True if the player has a winning position, False otherwise.
        """
        # Horizontal check
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE - 3):
                if np.all(self.board[row, col:col+4] == player):
                    return True
        
        # Vertical check
        for row in range(BOARD_SIZE - 3):
            for col in range(BOARD_SIZE):
                if np.all(self.board[row:row+4, col] == player):
                    return True
        
        # Diagonal check (positive slope)
        for row in range(BOARD_SIZE - 3):
            for col in range(BOARD_SIZE - 3):
                if np.all([self.board[row+i, col+i] == player for i in range(4)]):
                    return True
        
        # Diagonal check (negative slope)
        for row in range(3, BOARD_SIZE):
            for col in range(BOARD_SIZE - 3):
                if np.all([self.board[row-i, col+i] == player for i in range(4)]):
                    return True
        
        return False

    def is_valid_move(self, col: int) -> bool:
        """
        Checks if a move in the given column is valid.

        Args:
            col (int): The column to check.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        return 0 <= col < BOARD_SIZE and self.board[0][col] == EMPTY

    def get_valid_moves(self) -> list:
        """
        Gets a list of all valid moves (columns) where a move can be made.

        Returns:
            list: A list of valid column indices.
        """
        return [col for col in range(BOARD_SIZE) if self.is_valid_move(col)]

    def make_move(self, col: int, player: int) -> bool:
        """
        Places a piece for the player in the specified column.

        Args:
            col (int): The column to place the piece.
            player (int): The player making the move.

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        for row in range(BOARD_SIZE-1, -1, -1):  # Start from the bottom of the column
            if self.board[row, col] == EMPTY:
                self.board[row, col] = player
                return True
        return False

    def evaluate_window(self, window: np.ndarray, player: int) -> int:
        """
        Evaluates a window of 4 cells and assigns a score based on the player's advantage.

        Args:
            window (np.ndarray): The window of 4 cells.
            player (int): The player for whom to evaluate.

        Returns:
            int: The score for the window.
        """
        score = 0
        opponent = P1 if player != P1 else P2
        
        # Scoring based on the number of pieces in the window
        if np.sum(window == player) == 4:
            score += 100  # Win condition
        elif np.sum(window == player) == 3 and np.sum(window == EMPTY) == 1:
            score += 10  # Strong position
        elif np.sum(window == player) == 2 and np.sum(window == EMPTY) == 2:
            score += 5   # Decent position
        
        # Penalize if the opponent is in a strong position
        if np.sum(window == opponent) == 3 and np.sum(window == EMPTY) == 1:
            score -= 8
        
        return score

    def score_position(self, player: int) -> int:
        """
        Scores the entire board for the given player.

        Args:
            player (int): The player for whom to score the board.

        Returns:
            int: The total score for the board.
        """
        score = 0
        
        # Center column weighting
        center_array = self.board[:, BOARD_SIZE // 2]
        center_count = np.sum(center_array == player)
        score += center_count * 6  # Increased weight for central control
        
        # Horizontal, vertical, and diagonal scoring
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE - 3):
                window = self.board[r, c:c+4]
                score += self.evaluate_window(window, player)
        
        for c in range(BOARD_SIZE):
            for r in range(BOARD_SIZE - 3):
                window = self.board[r:r+4, c]
                score += self.evaluate_window(window, player)
        
        for r in range(BOARD_SIZE - 3):
            for c in range(BOARD_SIZE - 3):
                window = [self.board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(np.array(window), player)
        
        for r in range(3, BOARD_SIZE):
            for c in range(BOARD_SIZE - 3):
                window = [self.board[r - i][c + i] for i in range(4)]
                score += self.evaluate_window(np.array(window), player)

        return score

    def dynamic_depth(self) -> int:
        """
        Adjusts the search depth dynamically based on the number of empty cells.

        Returns:
            int: The depth to use for minimax.
        """
        empty_cells = np.sum(self.board == EMPTY)
        if empty_cells > 60:  # Early game
            return 3
        elif empty_cells > 30:  # Mid game
            return 4
        else:  # Late game
            return 5

def game():
    """
    The main function to start and manage the Connect 4 game.
    """
    game = Connect4()
    
    print("Welcome to Connect 4!")
    print("Player 1: 🔴")
    print("Player 2: 🔵")
    print("AI: 🤖")
    
    turn_mode = input("Choose turn order mode: [1] Random, [2] Normal: ").strip()
    use_normal_turns = turn_mode == "2"
    
    while True:
        game.print_board()
        if use_normal_turns:
            current_player = game.get_next_player()
        else:
            current_player = game.get_next_player_random()
        
        player_symbols = {P1: "🔴", P2: "🔵", AI: "🤖"}
        print(f"\nPlayer {player_symbols[current_player]}'s turn")
        
        if current_player == AI:
            depth = game.dynamic_depth()  # Adjust depth dynamically
            col, _ = game.minimax(depth, float('-inf'), float('inf'), True)
            if col is not None:
                game.make_move(col, AI)
                print(f"AI chose column {col + 1}")
        else:
            while True:
                try:
                    col = int(input(f"Enter a column (1-{BOARD_SIZE}): ")) - 1
                    if game.is_valid_move(col):
                        game.make_move(col, current_player)
                        break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print(f"Please enter a number between 1 and {BOARD_SIZE}")
        
        if game.check_for_win(current_player):
            game.print_board()
            print(f"\nPlayer {player_symbols[current_player]} wins!")
            break
            
        if not game.get_valid_moves():
            game.print_board()
            print("\nIt's a tie!")
            break

if __name__ == "__main__":
    game()
