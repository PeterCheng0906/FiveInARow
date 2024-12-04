from Optimization import minimax, get_best_move
from Evaluation import evaluate_board
import numpy as np

class Board:
    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.board = np.zeros((self.length, self.width), dtype=int)

    def __repr__(self):
        return '\n'.join(' '.join(str(cell) for cell in row) for row in self.board)

class FiveInARow:
    def __init__(self, board):
        self.board = board
        self.current_player = 1
        self.won_player = 0

    def reset_game(self):
        self.board.board = np.zeros((self.board.length, self.board.width), dtype=int)
        self.current_player = 1
        self.won_player = 0

    def put_a_piece(self, x=None, y=None):
        if x is None and y is None:
            while True:
                random_x = np.random.randint(0, self.board.width)
                random_y = np.random.randint(0, self.board.length)
                if self.board.board[random_y][random_x] == 0:
                    self.board.board[random_y][random_x] = self.current_player
                    break
        else:
            if self.board.board[y][x] == 0:
                self.board.board[y][x] = self.current_player
            else:
                raise ValueError(f"Cell ({x}, {y}) is already occupied.")

    def switch_turns(self):
        self.current_player = 3 - self.current_player

    def winner_check(self):
        player = self.current_player
        directions = [
            (1, 0),  
            (0, 1),  
            (1, 1),  
            (1, -1)  
        ]

        for y in range(self.board.length):
            for x in range(self.board.width):
                if self.board.board[y][x] == player:
                    for dy, dx in directions:
                        if self.is_winning_line(x, y, dx, dy, player):
                            self.won_player = player
                            return self.won_player
        return self.won_player

    def is_winning_line(self, x, y, dx, dy, player):
        for i in range(5):
            nx, ny = x + i * dx, y + i * dy
            if not (0 <= nx < self.board.width and 0 <= ny < self.board.length):
                return False  
            if self.board.board[ny][nx] != player:
                return False  
        return True  

if __name__ == '__main__':
    board = Board(width=15, length=15)
    game = FiveInARow(board=board)
    for turn in range(225):  
        try:
            game.put_a_piece() 
        except ValueError as e:
            print(e)  

        if game.winner_check() > 0:  
            print(f'Player {game.won_player} won!')
            print(board)
            break

        game.switch_turns() 

    else:
        print('Draw!')
        print(board)
        


    
