def evaluate_board(game):
    score = 0
    for y in range(game.board.length):
        for x in range(game.board.width):
            if game.board.board[y][x] == game.current_player:
                score += evaluate_position(game, x, y, game.current_player)
            elif game.board.board[y][x] != 0:
                score -= evaluate_position(game, x, y, 3 - game.current_player)
    return score

def evaluate_position(game, x, y, player):
    directions = [
        (1, 0),  
        (0, 1),  
        (1, 1),  
        (1, -1)  
    ]
    score = 0
    for dx, dy in directions:
        count, open_ends = count_consecutive(game, x, y, dx, dy, player)
        if count == 5:
            return float('inf') 
        elif count == 4 and open_ends > 0:
            score += 100
        elif count == 3 and open_ends > 0:
            score += 10
        elif count == 2 and open_ends > 0:
            score += 1
    return score

def count_consecutive(game, x, y, dx, dy, player):
    count = 0
    open_ends = 0

    for i in range(5):
        nx, ny = x + i * dx, y + i * dy
        if 0 <= nx < game.board.width and 0 <= ny < game.board.length:
            if game.board.board[ny][nx] == player:
                count += 1
            elif game.board.board[ny][nx] == 0:
                open_ends += 1
                break
            else:
                break
        else:
            break

    for i in range(1, 5):  
        nx, ny = x - i * dx, y - i * dy
        if 0 <= nx < game.board.width and 0 <= ny < game.board.length:
            if game.board.board[ny][nx] == player:
                count += 1
            elif game.board.board[ny][nx] == 0:
                open_ends += 1
                break
            else:
                break
        else:
            break

    return count, open_ends
