import numpy as np
import random
from typing import Tuple, Optional

BOARD_SIZE = 10  # Changed to 10x10 as per requirements
EMPTY = 0
P1 = 1
P2 = 2
AI = 3

class Connect4:
    def __init__(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE))
        self.last_two_players = []
        self.turn_order = [P1, P2, AI]
        self.current_turn_index = 0
    def print_board(self):
        print(" ", end=" ")
        for i in range(BOARD_SIZE):
            print(f"{i+1:2}", end=" ")
        print()
        
        for row in self.board:
            for cell in row:
                if cell == EMPTY:
                    print("⬜", end=" ")
                elif cell == P1:
                    print("🔴", end=" ")
                elif cell == P2:
                    print("🔵", end=" ")
                elif cell == AI:
                    print("🤖", end=" ")
            print()

    def check_for_win(self, player: int) -> bool:
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
        return 0 <= col < BOARD_SIZE and self.board[0][col] == EMPTY

    def get_valid_moves(self) -> list:
        return [col for col in range(BOARD_SIZE) if self.is_valid_move(col)]

    def make_move(self, col: int, player: int) -> bool:
        for row in range(BOARD_SIZE-1, -1, -1):
            if self.board[row, col] == EMPTY:
                self.board[row, col] = player
                return True
        return False

    def evaluate_window(self, window: np.ndarray, player: int) -> int:
        score = 0
        opponent = P1 if player != P1 else P2
        
        if np.sum(window == player) == 4:
            score += 100  # Win condition
        elif np.sum(window == player) == 3 and np.sum(window == EMPTY) == 1:
            score += 10  # Strong position
        elif np.sum(window == player) == 2 and np.sum(window == EMPTY) == 2:
            score += 5   # Decent position
        
        if np.sum(window == opponent) == 3 and np.sum(window == EMPTY) == 1:
            score -= 8  # Block opponent's strong position
        
        return score


    def score_position(self, player: int) -> int:
        score = 0
        opponent = P1 if player != P1 else P2
        
        # Center column weighting
        center_array = self.board[:, BOARD_SIZE // 2]
        center_count = np.sum(center_array == player)
        score += center_count * 6  # Increased weight for central control
        
        # Horizontal scoring
        for r in range(BOARD_SIZE):
            row_array = self.board[r, :]
            for c in range(BOARD_SIZE - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, player)
        
        # Vertical scoring
        for c in range(BOARD_SIZE):
            col_array = self.board[:, c]
            for r in range(BOARD_SIZE - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, player)
        
        # Positive slope diagonal scoring
        for r in range(BOARD_SIZE - 3):
            for c in range(BOARD_SIZE - 3):
                window = [self.board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(np.array(window), player)
        
        # Negative slope diagonal scoring
        for r in range(3, BOARD_SIZE):
            for c in range(BOARD_SIZE - 3):
                window = [self.board[r - i][c + i] for i in range(4)]
                score += self.evaluate_window(np.array(window), player)

        return score

    def minimax(self, depth: int, alpha: float, beta: float, maximizing_player: bool) -> Tuple[Optional[int], int]:
        valid_moves = self.get_valid_moves()
        is_terminal = self.check_for_win(P1) or self.check_for_win(P2) or self.check_for_win(AI) or not valid_moves

        # Terminal node or depth reached
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.check_for_win(AI):
                    return None, 1000000
                elif self.check_for_win(P1) or self.check_for_win(P2):
                    return None, -1000000
                else:
                    return None, 0
            else:
                return None, self.score_position(AI)

        # Prioritize center column and nearby columns
        center_col = BOARD_SIZE // 2
        valid_moves.sort(key=lambda col: abs(col - center_col))

        if maximizing_player:
            value = float('-inf')
            column = valid_moves[0]

            for col in valid_moves:
                # Simulate move
                for row in range(BOARD_SIZE - 1, -1, -1):
                    if self.board[row, col] == EMPTY:
                        self.board[row, col] = AI
                        break

                new_score = self.minimax(depth - 1, alpha, beta, False)[1]
                # Undo move
                self.board[row, col] = EMPTY

                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:
            value = float('inf')
            column = valid_moves[0]

            for col in valid_moves:
                opponent = P1 if self.score_position(P1) > self.score_position(P2) else P2
                # Simulate move
                for row in range(BOARD_SIZE - 1, -1, -1):
                    if self.board[row, col] == EMPTY:
                        self.board[row, col] = opponent
                        break

                new_score = self.minimax(depth - 1, alpha, beta, True)[1]
                # Undo move
                self.board[row, col] = EMPTY

                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value


    def get_next_player_random(self) -> int:
        if len(self.last_two_players) < 2:
            next_player = random.choice([P1, P2, AI])
        else:
            if self.last_two_players[-1] == self.last_two_players[-2]:
                possible_players = [p for p in [P1, P2, AI] if p != self.last_two_players[-1]]
                next_player = random.choice(possible_players)
            else:
                next_player = random.choice([P1, P2, AI])
        
        self.last_two_players.append(next_player)
        if len(self.last_two_players) > 2:
            self.last_two_players.pop(0)
        return next_player
    
    def get_next_player(self) -> int:
        player = self.turn_order[self.current_turn_index]
        self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_order)
        return player
    def dynamic_depth(self) -> int:
        """
        Adjust the depth of the minimax algorithm dynamically based on the number of empty cells.
        """
        empty_cells = np.sum(self.board == EMPTY)

        # Adjust depth based on the game phase
        if empty_cells > 60:  # Early game
            return 3
        elif empty_cells > 30:  # Mid game
            return 4
        else:  # Late game
            return 5

def game():
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
            depth = game.dynamic_depth()  # Determine depth dynamically
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