import time
import random

import chess as ch
import engine as engine
import chess.svg

def save_board_state(board, filename='chess_board.svg'):
    time.sleep(2)
    image = chess.svg.board(board)
    with open(filename, 'w') as f:
        f.write(image)

def play_engine_move(board, color, max_depth):
    salmon_ai = engine.SalmonAI(board, color, max_depth)
    move = salmon_ai.choose_move()
    if isinstance(move, ch.Move):
        board.push(move)
        save_board_state(board)

def play_human_move(board, is_crazy=False):
    try:
        if len(list(board.legal_moves)) == 0:
            return
        else:
            legal_moves = list(board.legal_moves)
            legal_moves = [move.uci() for move in legal_moves]
            legal_moves_str = ' '.join(legal_moves)
            print('enter UNDO/END to interrupt the game...')
            print(f'legal moves: {legal_moves_str}')
            move = input('enter your move: ') if not is_crazy else random.choice(legal_moves)
            if move.upper() == 'UNDO':
                try:
                    board.pop()
                    board.pop()
                    save_board_state(board)
                    play_human_move(board, is_crazy)
                except IndexError:
                    print("no more moves to undo...")
                    play_human_move(board, is_crazy)
            elif move.upper() == 'END':
                board.reset()
                save_board_state(board)
                print('the game is now terminated...')
                exit()
            else:
                board.push_san(move)
                save_board_state(board)
    except ValueError:
        print('invalid move! please try again...')
        play_human_move(board, is_crazy)

def start_game(color, max_depth, is_crazy=False, is_bot=False):
    board = ch.Board()
    save_board_state(board)

    while not board.is_game_over():
        if color in ['b', 'black']:
            print('the engine is thinking...')
            play_engine_move(board, ch.WHITE, max_depth)

            if not is_bot:
                play_human_move(board, is_crazy)
            else:
                play_engine_move(board, ch.BLACK, max_depth)
        else:
            if not is_bot:
                play_human_move(board, is_crazy)
            else:
                play_engine_move(board, ch.WHITE, max_depth)

            print('the engine is thinking...')
            play_engine_move(board, ch.BLACK, max_depth)

    save_board_state(board)

    outcome = board.outcome()
    if outcome.winner is None:
        print('GAME OVER - Draw')
    elif (outcome.winner == ch.WHITE and color in ['w', 'white']) or (outcome.winner == ch.BLACK and color in ['b', 'black']):
        print('YOU WIN')
    else:
        print('YOU LOSE')

    board.reset()
    time.sleep(8)
    save_board_state(board)

def get_user_input():
    colors = ['b', 'black', 'w', 'white']
    levels = {'easy': 3, 'medium': 5, 'difficult': 7, 'auto': 5}
    boolean_values = {'y': True, 'yes': True, 'n': False, 'no': False}

    while True:
        color = input('choose your color (B/W): ').lower()
        if color in colors:
            break

    while True:
        level = input('choose difficulty level (AUTO/EASY/MEDIUM/DIFFICULT): ').lower()
        if level in levels:
            max_depth = levels[level]
            break

    while True:
        bot = input('bot level? (yes/no): ').lower()
        if bot in boolean_values:
            is_bot = boolean_values[bot]
            break

    is_crazy = False
    if not is_bot:
        while True:
            crazy = input('crazy level? (yes/no): ').lower()
            if crazy in boolean_values:
                is_crazy = boolean_values[crazy]
                break

    start_game(color, max_depth, is_crazy, is_bot)

def main():
    get_user_input()

if __name__ == "__main__":
    main()
