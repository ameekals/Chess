# This class is responsible for storing all the information about the current state of a chess game. It will also be
# responsible for determining the valid moves at the current state. It will also keep a move log.


class GameState:
    def __init__(self):
        # Can use numpy arrays to be more efficient
        # Board is a 8x8 2d list, each element of the list has 2 characters
        # The first char represents the color of the piece, "b" or "w"
        # The second char represents the type of the piece, "K", "Q"...
        # "--" - represents an empty space with no piece
        self.board = \
            [
                ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
            ]
        # Use this dictionary to simplify the logic of determing the if statements
        # self.move_functions = {'P': self.get_pawn_moves,
        #                        'R': self.get_rook_moves,
        #                        'N': self.get_knight_moves,
        #                        'B': self.get_bishop_moves,
        #                        'Q': self.get_queen_moves,
        #                        'K': self.get_king_moves}

        self.white_to_move = True
        self.move_log = []

    # Takes a move as a parameter and executes it (will not work for castling or pawn promotion)
    def make_move(self, move):
        self.board[move.start_row][move.start_column] = "--"
        self.board[move.end_row][move.end_column] = move.piece_moved
        self.move_log.append(move)  # Log the move, so we can undo it later (or keep history)
        self.white_to_move = not self.white_to_move  # Switch turns

    # Undo last move made
    def undo_move(self):
        # Make sure that there is a move to undo
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_column] = move.piece_moved
            self.board[move.end_row][move.end_column] = move.piece_captured
            self.white_to_move = not self.white_to_move

    # All moves considering checks
    # Get all possible moves, for each possible move, check to see if it's a valid move
    # -make the move
    # -generate all possible moves for the opposing player
    # -see if any of the moves attack your king
    # -if your king is safe, it is a valid move and add it to a list
    # -return the list of valid moves only
    def get_valid_moves(self):
        # For now, we will not worry about checks
        return self.get_all_possible_moves()

    # All moves without considering checks
    def get_all_possible_moves(self):
        moves = []
        for row in range(len(self.board)):                          # Number of rows
            for column in range(len(self.board[row])):              # Number of columns in given row
                piece_color = self.board[row][column][0]            # Checking first character => the piece color
                if (piece_color == 'w' and self.white_to_move) or (piece_color == 'b' and not self.white_to_move):
                    piece = self.board[row][column][1]
                    # self.move_functions[piece](row, column, moves)
                    if piece == "P":
                        self.get_pawn_moves(row, column, moves)
                    elif piece == "R":
                        self.get_rook_moves(row, column, moves)
                    elif piece == "K":
                        self.get_knight_moves(row, column, moves)
                    elif piece == "B":
                        self.get_bishop_moves(row, column, moves)
                    elif piece == "Q":
                        self.get_queen_moves(row, column, moves)
                    elif piece == "K":
                        self.get_king_moves(row, column, moves)
        return moves

    def get_pawn_moves(self, row, column, moves):
        if self.white_to_move:
            # 1 square pawn advance
            if self.board[row - 1][column] == "--":
                moves.append(Move((row, column), (row - 1, column), self.board))
                # 2 square pawn advance
                if row == 6 and self.board[row - 2][column] == "--":
                    moves.append(Move((row, column), (row - 2, column), self.board))
            # Capture pieces
            # Capture to the left
            # "b" => enemy piece to capture
            if column - 1 >= 0:
                if self.board[row - 1][column - 1][0] == "b":
                    moves.append(Move((row, column), (row - 1, column - 1), self.board))
            # Don't do elif because it will only capture to one side (left or right)
            # Capture to the right
            # "b" => enemy piece to capture
            if column + 1 <= 7:
                if self.board[row - 1][column + 1][0] == "b":
                    moves.append(Move((row, column), (row - 1, column + 1), self.board))
        # Black pawn moves (keep in mind you are going down the board and don't mirror left and rights)
        else:
            # 1 square pawn advance
            if self.board[row + 1][column] == "--":
                moves.append(Move((row, column), (row + 1, column), self.board))
                # 2 square pawn advance
                if row == 1 and self.board[row + 2][column] == "--":
                    moves.append(Move((row, column), (row + 2, column), self.board))
            # Capture pieces
            # Capture to the left
            # "w" => enemy piece to capture
            # if column + 1 <= 7:
            if column - 1 >= 0:
                if self.board[row + 1][column - 1][0] == "w":
                    moves.append(Move((row, column), (row + 1, column - 1), self.board))
            # Don't do elif because it will only capture to one side (left or right)
            # Capture to the right
            # "w" => enemy piece to capture
            if column + 1 <= 7:
                if self.board[row + 1][column + 1][0] == "w":
                    moves.append(Move((row, column), (row + 1, column + 1), self.board))

    def get_rook_moves(self, row, column, moves):
        enemy_color = "b" if self.white_to_move else "w"

        # Moving up and down (negative for up and positive for down)
        # Moving left and right (negative for left and positive for right)
        for i in range(1, 8):
            end_row_up = row - 1 * i
            end_column_up = column
            end_row_down = row + 1 * i
            end_column_down = column
            end_row_left = row
            end_column_left = column - 1 * i
            end_row_right = row
            end_column_right = column + 1 * i

            # Follows for the same coding pattern probably make a helper method for this
            if 0 <= end_row_up <= 8 or 0 <= end_column_up <= 8:
                end_piece_up = self.board[end_row_up][end_column_up]
                # If end_piece is an empty space
                if end_piece_up == "--":
                    moves.append(Move((row, column), (end_row_up, end_column_up), self.board))
                # If end_piece is a enemy piece
                elif end_piece_up[0] == enemy_color:
                    moves.append(Move((row, column), (end_row_up, end_column_up), self.board))
                # If end_piece is a friendly piece
                else:
                    break
            # Reach the end of the board
            else:
                break

            if 0 <= end_row_down <= 8 or 0 <= end_column_down <= 8:
                end_piece_down = self.board[end_row_down][end_column_down]
                if end_piece_down == "--":
                    moves.append(Move((row, column), (end_row_down, end_column_down), self.board))
                elif end_piece_down[0] == enemy_color:
                    moves.append(Move((row, column), (end_row_down, end_column_down), self.board))
                else:
                    break
            else:
                break

            if 0 <= end_row_left <= 8 or 0 <= end_column_left <= 8:
                end_piece_left = self.board[end_row_left][end_column_left]
                if end_piece_left == "--":
                    moves.append(Move((row, column), (end_row_left, end_column_left), self.board))
                elif end_piece_left[0] == enemy_color:
                    moves.append(Move((row, column), (end_row_left, end_column_left), self.board))
                else:
                    break
            else:
                break

            if 0 <= end_row_right <= 8 or 0 <= end_column_right <= 8:
                end_piece_right = self.board[end_row_right][end_column_right]
                if end_piece_right == "--":
                    moves.append(Move((row, column), (end_row_right, end_column_right), self.board))
                elif end_piece_right[0] == enemy_color:
                    moves.append(Move((row, column), (end_row_right, end_column_right), self.board))
                else:
                    break
            else:
                break

            #     # If end_piece is an empty space
            #     if end_piece_up == "--":
            #         moves.append(Move((row, column), (end_row_up, end_column_up), self.board))
            #     elif end_piece_down == "--":
            #         moves.append(Move((row, column), (end_row_down, end_column_down), self.board))
            #     elif end_piece_left == "--":
            #         moves.append(Move((row, column), (end_row_left, end_column_left), self.board))
            #     elif end_piece_right == "--":
            #         moves.append(Move((row, column), (end_row_right, end_column_right), self.board))
            #     # If end_piece is an enemy piece
            #     elif end_piece_up[0] == enemy_color:
            #         moves.append(Move((row, column), (end_row_up, end_column_up), self.board))
            #     elif end_piece_down[0] == enemy_color:
            #         moves.append(Move((row, column), (end_row_down, end_column_down), self.board))
            #     elif end_piece_left[0] == enemy_color:
            #         moves.append(Move((row, column), (end_row_left, end_column_left), self.board))
            #     elif end_piece_right[0] == enemy_color:
            #         moves.append(Move((row, column), (end_row_right, end_column_right), self.board))
            #     # If end_piece is a friendly piece
            #     else:
            #         break
            # # Reach the end of the board
            # else:
            #     break

    def get_knight_moves(self, row, column, moves):
        pass

    def get_bishop_moves(self, row, column, moves):
        pass

    def get_queen_moves(self, row, column, moves):
        pass

    def get_king_moves(self, row, column, moves):
        pass


class Move:
    # Maps keys to values key : value
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in
                     ranks_to_rows.items()}  # Reverse it (for each key and value make a value: key pair)
    files_to_columns = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    columns_to_files = {v: k for k, v in
                        files_to_columns.items()}  # Reverse it (for each key and value make a value: key pair)

    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]
        self.start_column = start_square[1]
        self.end_row = end_square[0]
        self.end_column = end_square[1]
        self.piece_moved = board[self.start_row][self.start_column]
        self.piece_captured = board[self.end_row][self.end_column]
        self.move_ID = self.start_row * 1000 + self.start_column * 100 + self.end_row * 10 + self.end_column  # Unique ID: 0-7777

    # Overriding the equals method (this is because we are using a move class)
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_ID == other.move_ID
        return False

    def get_chess_notation(self):
        # Not using actual chess notation instead, using rank/file notation
        return self.get_rank_file(self.start_row, self.start_column) + self.get_rank_file(self.end_row, self.end_column)

    # Gets the rank and file for 1 square
    def get_rank_file(self, row, column):
        return self.columns_to_files[column] + self.rows_to_ranks[row]
