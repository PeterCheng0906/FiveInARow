from main_game import FiveInARow, Board
from Eval import AI_Evaluator

if __name__ == '__main__':
    
    evaluator = AI_Evaluator(games_to_simulate=100, depth=2) 
    evaluator.simulate_games(FiveInARow, Board)
    evaluator.display_results()
