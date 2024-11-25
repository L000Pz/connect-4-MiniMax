# Connect-4 using minimax 🤖🎮

A feature-rich **Connect 4 game** designed for competitive fun and strategic challenges! This project includes a powerful AI player with dynamic difficulty adjustment, a visually appealing game board, and multiple gameplay modes.

## Features 🌟

- **Dynamic AI Depth Adjustment**:
  - The AI adapts its difficulty based on the game state:
    - 🟢 **Early Game**: Faster decisions for a larger board.
    - 🟡 **Mid Game**: Balanced strategy and performance.
    - 🔴 **Late Game**: Intense and precise moves to secure a win!

- **Two Turn Order Modes**:
  - **Random**: Players are chosen randomly for each turn.
  - **Fixed**: Players alternate in a predefined order.

- **Optimized AI**:
  - Uses **alpha-beta pruning** for fast and intelligent decisions.
  - Prioritizes strategic moves like controlling the center column.
  - Scores board positions dynamically to block opponents and maximize its chances of winning.

- **Clean and Intuitive Game Board**:
  - Symbols:
    - 🔴: Player 1
    - 🔵: Player 2
    - 🤖: AI
  - Easy-to-read column numbering and visually distinct symbols.

- **Scalable Board**:
  - Set to a 10x10 grid for this project, but can be adjusted for other sizes.

## Gameplay Instructions 🎮

1. **Run the Game**:
   - Clone this repository:
     ```bash
     git clone https://github.com/L000Pz/connect-4-MiniMax.git
     ```
   - Navigate to the project directory and run the game:
     ```bash
     python main.py
     ```

2. **Choose a Turn Order Mode**:
   - When prompted, select the turn order mode:
     - `[1] Random`: Players are selected randomly for each turn.
     - `[2] Normal`: Fixed turn order: Player 1 → Player 2 → AI.

3. **Make Your Move**:
   - Players take turns entering a column number (1-10) to drop their piece into the board.
   - The AI will calculate its moves and display its chosen column.

4. **Win the Game**:
   - Get four pieces in a row (horizontally, vertically, or diagonally) to win!

5. **Tie Game**:
   - If the board fills up and no player has won, the game ends in a tie.

## How It Works 🛠️

### AI Logic
- **Dynamic Depth**: Adjusts the depth of the minimax algorithm based on the number of empty cells on the board.
- **Alpha-Beta Pruning**: Speeds up decision-making by ignoring unnecessary branches of the game tree.
- **Heuristic Evaluation**: Scores board positions based on:
  - Number of consecutive pieces for the player.
  - Blocking opponent moves.
  - Prioritizing central control for maximum flexibility.

### Board Mechanics
- A 10x10 grid represented as a 2D NumPy array.
- Players make moves by filling the lowest available cell in the chosen column.
- The game checks for wins after every move.


