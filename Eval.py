import time
import sys
from Optimization import get_best_move  
from Evaluation import evaluate_board  

class AI_Evaluator:
    def __init__(self, games_to_simulate=100, depth=2):
        self.games_to_simulate = games_to_simulate
        self.depth = depth
        self.results = {
            "winrate": 0.0,
            "optimal_moves": 0.0,
            "avg_time_to_victory": 0.0,
            "avg_computation_time_per_move": 0.0,
            "avg_memory_usage": 0.0,
        }

    def simulate_games(self, game_class, board_class):
        total_wins = 0
        total_moves = 0
        total_time = 0
        total_memory = 0
        total_victory_turns = 0
        total_optimal_moves = 0
        total_ai_moves = 0

        for game_id in range(self.games_to_simulate):
            print(f"Simulating game {game_id + 1}/{self.games_to_simulate}...")
            board = board_class(width=15, length=15)
            game = game_class(board=board)
            game.reset_game()

            move_count = 0
            game_won = False

            while move_count < 225:  
                if game.current_player == 1:  
                    start_time = time.time()
                    best_move = get_best_move(game, depth=self.depth)
                    computation_time = time.time() - start_time
                    total_time += computation_time

                    if best_move:
                        x, y = best_move
                        game.put_a_piece(x, y)
                        optimal_move = self.is_optimal_move(game, best_move)
                        total_optimal_moves += int(optimal_move)
                        total_ai_moves += 1

                else:  
                    self.random_move(game)

                move_count += 1

                if game.winner_check() > 0:
                    game_won = True
                    if game.won_player == 1:
                        total_wins += 1
                        total_victory_turns += move_count
                    break

                game.switch_turns()

            total_memory += sys.getsizeof(game.board.board)

        self.results["winrate"] = total_wins / self.games_to_simulate
        self.results["optimal_moves"] = total_optimal_moves / total_ai_moves if total_ai_moves > 0 else 0
        self.results["avg_time_to_victory"] = total_victory_turns / total_wins if total_wins > 0 else 0
        self.results["avg_computation_time_per_move"] = total_time / total_ai_moves if total_ai_moves > 0 else 0
        self.results["avg_memory_usage"] = total_memory / self.games_to_simulate

    def is_optimal_move(self, game, move):
        x, y = move
        current_score = evaluate_board(game)
        best_score = float('-inf')
        for px in range(game.board.width):
            for py in range(game.board.length):
                if game.board.board[py][px] == 0:
                    game.board.board[py][px] = game.current_player
                    score = evaluate_board(game)
                    game.board.board[py][px] = 0
                    best_score = max(best_score, score)
        return current_score == best_score

    def random_move(self, game):
        import numpy as np
        while True:
            random_x = np.random.randint(0, game.board.width)
            random_y = np.random.randint(0, game.board.length)
            if game.board.board[random_y][random_x] == 0:
                game.put_a_piece(random_x, random_y)
                break

    def display_results(self):
        print("\nEvaluation Metrics:")
        print(f"Win Rate: {self.results['winrate'] * 100:.2f}%")
        print(f"Optimal Move Selection: {self.results['optimal_moves'] * 100:.2f}%")
        print(f"Average Time to Victory: {self.results['avg_time_to_victory']:.2f} turns")
        print(f"Average Computation Time per Move: {self.results['avg_computation_time_per_move']:.4f} seconds")
        print(f"Average Memory Usage: {self.results['avg_memory_usage'] / 1024:.2f} KB")
