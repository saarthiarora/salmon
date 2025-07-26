import chess
import random

class ChessAI:

    def __init__(self, board, color, max_depth, enable_entropy=True):
        self.board = board
        self.color = color
        self.depth_limit = max_depth
        self.entropy_enabled = enable_entropy
        self.board_size = 8

    def evaluate_checkmate(self):
        if self.board.is_checkmate():
            return 1000 if self.board.turn != self.color else -1000
        return 0

    def material_score(self, square):
        piece_type = self.board.piece_type_at(square)
        if piece_type is None:
            return 0

        values = {
            chess.PAWN: 1.00,
            chess.KNIGHT: 3.05,
            chess.BISHOP: 3.33,
            chess.ROOK: 5.63,
            chess.QUEEN: 9.50,
            chess.KING: 0.00
        }

        value = values.get(piece_type, 0.0)
        return value if self.board.color_at(square) == self.color else -value

    def early_game_bonus(self):
        bonus = 0.64
        early_game_moves = 8

        if self.board.fullmove_number < early_game_moves:
            multiplier = 1 if self.board.turn == self.color else -1
            return bonus * len(list(self.board.legal_moves)) * multiplier
        return 0

    def evaluate_board(self):
        score = 0
        score += sum(self.material_score(sq) for sq in chess.SQUARES)
        score += self.early_game_bonus()
        score += self.evaluate_checkmate()

        if self.entropy_enabled:
            score += (random.random() - 0.5)

        return score

    def maximize(self, depth, alpha, beta):
        if depth == self.depth_limit or not self.board.legal_moves:
            return self.evaluate_board()

        best_score = float('-inf')
        best_move = None

        for move in self.board.legal_moves:
            self.board.push(move)
            score = self.minimize(depth + 1, alpha, beta)
            self.board.pop()

            if score > best_score:
                best_score = score
                if depth == 0:
                    best_move = move

            alpha = max(alpha, best_score)
            if alpha >= beta:
                break

        return best_move if depth == 0 else best_score

    def minimize(self, depth, alpha, beta):
        if depth == self.depth_limit or not self.board.legal_moves:
            return self.evaluate_board()

        worst_score = float('inf')

        for move in self.board.legal_moves:
            self.board.push(move)
            score = self.maximize(depth + 1, alpha, beta)
            self.board.pop()

            if score < worst_score:
                worst_score = score

            beta = min(beta, worst_score)
            if alpha >= beta:
                break

        return worst_score

    def choose_move(self):
        return self.maximize(0, float('-inf'), float('inf'))
