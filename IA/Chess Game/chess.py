import time
import chess
from random import randint, choice, shuffle

#TODO: permettre d'évaluer suivant un joueur donné
# Evalue en tant que Blanc
def evaluate(b):
    scores = {'k':200, 'q':9, 'r':5, 'b':3, 'n':3, 'p':1}
    coefPionReine = 1 / 150
    scoreTotal = 0
    for k, p in b.piece_map().items():
        psc = scores[p.symbol().lower()]
        if p.symbol().lower() == p.symbol():
            psc = -psc
        scoreTotal += psc
        if p.symbol().lower() == 'p':
            ligne = k // 8
            col = k % 8
            if p.symbol().lower() == p.symbol():
                scoreTotal -= (8-ligne) * coefPionReine
            else:
                scoreTotal += (ligne) * coefPionReine
    return scoreTotal

def choose_action(state,max_depth):
    for depth in range(max_depth+1):
        start_time = time.time()
        print("MINIMAX AB ID(%d) : Wait AI is choosing" % (depth))
        list_action = state.generate_legal_moves()
        eval_score, selected_action, node_expanded = _minimax(0,state,True,float('-inf'),float('inf'),max_depth)
        print("MINIMAX AB ID(%d) : Done, eval = %d, expanded %d" % (depth, eval_score, node_expanded))
        print("--- %s seconds ---" % (time.time() - start_time))
    return selected_action

def minimax(current_depth, state, is_max_turn, alpha, beta, max_depth):
        if current_depth == max_depth or state.is_game_over():
            return (evaluate(state), None, 1) # self.player_color
        total_node_expanded = 0
        key_of_actions = list(state.generate_legal_moves())
        shuffle(key_of_actions) #randomness
        best_value = float('-inf') if is_max_turn else float('inf')
        action_target = None
        for action_key in key_of_actions:
            state.push(action_key)
            eval_child, action_child, node_expanded = minimax(current_depth+1,state,not is_max_turn, alpha, beta, max_depth)
            state.pop()
            total_node_expanded += node_expanded
            if is_max_turn and best_value < eval_child:
                best_value = eval_child
                action_target = action_key
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            elif (not is_max_turn) and best_value > eval_child:
                best_value = eval_child
                action_target = action_key
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
        return (best_value, action_target, total_node_expanded)

# C'est partie
board = chess.Board()
depth = 4
while not board.is_game_over():
    print(board)
    coup = choose_action(board,depth)
    print("Meilleur coup pour Ami :", coup)
    board.push(coup)
    if board.is_game_over():
        break
    coup = choice(list(board.generate_legal_moves()))
    print("Coup joueur Aleatoire :", coup)
    board.push(coup)
print(board)
print(board.result())


