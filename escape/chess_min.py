# Minimal pygbag-safe chess engine module

WHITE = "w"
BLACK = "b"

PAWN = "P"
QUEEN = "Q"
ROOK = "R"
BISHOP = "B"
KNIGHT = "N"
KING = "K"

def square(file, rank):
    """Convert file/rank (0–7) to square index (0–63)."""
    return rank * 8 + file

class Piece:
    def __init__(self, type_char, color):
        self.piece_type = type_char.upper()  # 'K','Q','R','B','N','P'
        self.color = color             # 'w' or 'b'

    def __str__(self):
        return self.piece_type if self.color == 'w' else self.piece_type.lower()

    def __repr__(self):
        return f"Piece({self.piece_type!r}, {self.color!r})"


class Move:
    def __init__(self, from_square, to_square, promotion=None):
        self.from_square = from_square
        self.to_square = to_square
        self.promotion = promotion

    def __eq__(self, other):
        return (
            isinstance(other, Move)
            and self.from_square == other.from_square
            and self.to_square == other.to_square
            and self.promotion == other.promotion
        )

    def __hash__(self):
        return hash((self.from_square, self.to_square, self.promotion))

    def __repr__(self):
        return f"Move({self.from_square}->{self.to_square}, promo={self.promotion})"

    @staticmethod
    def from_uci(uci):
        file_map = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
        from_sq = file_map[uci[0]] + (int(uci[1]) - 1) * 8
        to_sq = file_map[uci[2]] + (int(uci[3]) - 1) * 8
        promo = uci[4].upper() if len(uci) == 5 else None
        return Move(from_sq, to_sq, promo)


class Board:
    def __init__(self, fen=None):
        if fen:
            self.set_fen(fen)
        else:
            self.reset()

    def reset(self):
        chars = list(
            "rnbqkbnr" +
            "pppppppp" +
            "........" * 4 +
            "PPPPPPPP" +
            "RNBQKBNR"
        )
        self.board = [self._char_to_piece(c) for c in chars]
        self.turn = "w"

    def _char_to_piece(self, c):
        if c == ".":
            return "."
        color = "w" if c.isupper() else "b"
        return Piece(c.upper(), color)

    def piece_at(self, index):
        val = self.board[index]
        return val if isinstance(val, Piece) else None

    def set_piece_at(self, index, piece):
        self.board[index] = piece if piece else "."

    def set_fen(self, fen):
        parts = fen.split()
        rows = parts[0].split('/')
        self.board = []
        for row in reversed(rows):
            for c in row:
                if c.isdigit():
                    self.board.extend(["."] * int(c))
                else:
                    self.board.append(self._char_to_piece(c))
        self.turn = parts[1] if len(parts) > 1 else "w"

    def fen(self):
        rows = []
        for r in range(7, -1, -1):
            fen_row = ""
            empty = 0
            for sq in self.board[r * 8:(r + 1) * 8]:
                if sq == ".":
                    empty += 1
                else:
                    if empty:
                        fen_row += str(empty)
                        empty = 0
                    fen_row += str(sq)
            if empty:
                fen_row += str(empty)
            rows.append(fen_row)
        return "/".join(rows) + f" {self.turn} - - 0 1"

    def push(self, move: Move):
        piece = self.piece_at(move.from_square)
        if not piece:
            return
        if move.promotion:
            promoted_piece = Piece(move.promotion, piece.color)
            self.set_piece_at(move.to_square, promoted_piece)
        else:
            self.set_piece_at(move.to_square, piece)
        self.set_piece_at(move.from_square, ".")
        self.turn = "b" if self.turn == "w" else "w"

    def legal_moves(self):
        """Generate pseudo-legal moves for current player."""
        moves = []
        for i, piece in enumerate(self.board):
            if piece == "." or piece.color != self.turn:
                continue

            file = i % 8
            rank = i // 8

            # Pawn moves
            if piece.piece_type == "P":
                direction = 1 if piece.color == "w" else -1
                forward = i + 8 * direction
                if 0 <= forward < 64 and self.board[forward] == ".":
                    if (forward // 8 == 7 and piece.color == "w") or (forward // 8 == 0 and piece.color == "b"):
                        for promo in "QRNB":
                            moves.append(Move(i, forward, promo))
                    else:
                        moves.append(Move(i, forward))
                    # Two-square advance
                    start_rank = 1 if piece.color == "w" else 6
                    if rank == start_rank:
                        two_forward = i + 16 * direction
                        if self.board[two_forward] == ".":
                            moves.append(Move(i, two_forward))
                # Captures
                for df in (-1, 1):
                    f2 = file + df
                    if 0 <= f2 < 8:
                        target = i + 8 * direction + df
                        if 0 <= target < 64:
                            t_piece = self.board[target]
                            if t_piece != "." and t_piece.color != piece.color:
                                if (target // 8 == 7 and piece.color == "w") or (target // 8 == 0 and piece.color == "b"):
                                    for promo in "QRNB":
                                        moves.append(Move(i, target, promo))
                                else:
                                    moves.append(Move(i, target))

            # Knight moves
            elif piece.piece_type == "N":
                offsets = [6, 10, 15, 17, -6, -10, -15, -17]
                for off in offsets:
                    target = i + off
                    if 0 <= target < 64:
                        tf, tr = target % 8, target // 8
                        if abs(tf - file) <= 2 and abs(tr - rank) <= 2:
                            t_piece = self.board[target]
                            if t_piece == "." or t_piece.color != piece.color:
                                moves.append(Move(i, target))

            # Bishop moves (diagonals)
            elif piece.piece_type == "B":
                for off in (7, 9, -7, -9):
                    t = i
                    while True:
                        next_t = t + off
                        if not (0 <= next_t < 64):
                            break
                        # check if wrapped horizontally
                        if abs((next_t % 8) - (t % 8)) != 1:
                            break
                        target_piece = self.board[next_t]
                        if target_piece == ".":
                            moves.append(Move(i, next_t))
                        elif target_piece.color != piece.color:
                            moves.append(Move(i, next_t))
                            break
                        else:
                            break
                        t = next_t

            # Rook moves (horizontal & vertical only)
            elif piece.piece_type == "R":
                for off in (1, -1, 8, -8):
                    t = i
                    while True:
                        next_t = t + off
                        if not (0 <= next_t < 64):
                            break
                        # prevent wrap across ranks for horizontal moves
                        if off in (1, -1) and (next_t // 8 != t // 8):
                            break
                        target_piece = self.board[next_t]
                        if target_piece == ".":
                            moves.append(Move(i, next_t))
                        elif target_piece.color != piece.color:
                            moves.append(Move(i, next_t))
                            break
                        else:
                            break
                        t = next_t

            # Queen moves (combines rook + bishop directions)
            elif piece.piece_type == "Q":
                for off in (1, -1, 8, -8, 7, 9, -7, -9):
                    t = i
                    while True:
                        next_t = t + off
                        if not (0 <= next_t < 64):
                            break
                        # prevent horizontal wrapping
                        if off in (1, -1, 7, -9, 9, -7) and abs((next_t % 8) - (t % 8)) != 1:
                            break
                        target_piece = self.board[next_t]
                        if target_piece == ".":
                            moves.append(Move(i, next_t))
                        elif target_piece.color != piece.color:
                            moves.append(Move(i, next_t))
                            break
                        else:
                            break
                        t = next_t

            # King moves
            elif piece.piece_type == "K":
                for off in [1, -1, 8, -8, 9, -9, 7, -7]:
                    target = i + off
                    if 0 <= target < 64 and abs((target % 8) - file) <= 1:
                        t_piece = self.board[target]
                        if t_piece == "." or t_piece.color != piece.color:
                            moves.append(Move(i, target))

        return moves
