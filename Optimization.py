from Evaluation import evaluate_board

def minimax(game, depth, alpha, beta, maximizing):
    if depth == 0 or game.winner_check() > 0:
        return evaluate_board(game)

    if maximizing:
        max_eval = float('-inf')
        candidates = get_candidate_moves(game)
        for x, y in candidates:
            game.board.board[y][x] = game.current_player  # Simulate move
            eval = minimax(game, depth - 1, alpha, beta, False)
            game.board.board[y][x] = 0  # Undo move
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:  # Prune
                break
        return max_eval
    else:
        min_eval = float('inf')
        opponent = 3 - game.current_player
        candidates = get_candidate_moves(game)
        for x, y in candidates:
            game.board.board[y][x] = opponent  # Simulate move
            eval = minimax(game, depth - 1, alpha, beta, True)
            game.board.board[y][x] = 0  # Undo move
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:  # Prune
                break
        return min_eval

def get_best_move(game, depth):
    best_score = float('-inf')
    best_move = None
    candidates = get_candidate_moves(game)  # Focus on relevant cells
    for x, y in candidates:
        game.board.board[y][x] = game.current_player  # Simulate move
        score = minimax(game, depth - 1, float('-inf'), float('inf'), False)
        game.board.board[y][x] = 0  # Undo move
        if score > best_score:
            best_score = score
            best_move = (x, y)
    return best_move

def get_candidate_moves(game, radius=2):
    candidates = set()
    for y in range(game.board.length):
        for x in range(game.board.width):
            if game.board.board[y][x] != 0:  # Look at occupied cells
                for dy in range(-radius, radius + 1):
                    for dx in range(-radius, radius + 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < game.board.width and 0 <= ny < game.board.length:
                            if game.board.board[ny][nx] == 0:  # Only empty cells
                                candidates.add((nx, ny))
    return candidates

