from models import Cell, Board, Player


class Controller:
    def __init__(self):
        self.board = Board()
        self.players: list[Player] = []

    def restart_game(self):
        del self.board
        for player in self.players:
            del player
        self.board = Board()
        self.players: list[Player] = []

    def add_player(self, name: str):
        self.players.append(Player(name))

    def make_move(self, cell_num: int):
        if not self.board.cells[cell_num].is_occupied and \
                not self.is_game_over():
            self.board.occupy_cell(cell_num)

    def get_lined_cells(self) -> list[int]:
        # rows
        for cell_num in range(0, len(self.board.cells), Board.dimension):
            i_row = self.board.cells[cell_num: cell_num + Board.dimension]
            if check_cells_sequence(i_row):
                return [cell.number for cell in i_row]

        # columns
        for col_num in range(Board.dimension):
            i_col = []
            for cell_num in range(col_num, Board.dimension ** 2,
                                  Board.dimension):
                i_col.append(self.board.cells[cell_num])
            if check_cells_sequence(i_col):
                return [cell.number for cell in i_col]

        # diagonals
        diagonal_1 = [
            self.board.cells[Board.dimension * row_num + col_num]
            for row_num in range(Board.dimension)
            for col_num in range(Board.dimension)
            if row_num == col_num
        ]
        diagonal_2 = [
            self.board.cells[Board.dimension * row_num + col_num]
            for row_num in range(Board.dimension)
            for col_num in range(Board.dimension)
            if row_num + col_num == Board.dimension - 1
        ]

        for i_diagonal in (diagonal_1, diagonal_2):
            if check_cells_sequence(i_diagonal):
                return [cell.number for cell in i_diagonal]

    def get_game_state(self):
        lined_cells = self.get_lined_cells()
        if lined_cells:
            return "win"
        elif not lined_cells and self.board.is_all_cells_occupied():
            return "draw"
        else:
            return "continue"

    def is_game_over(self) -> bool:
        if self.get_game_state() == "continue":
            return False
        return True

    def get_winner(self) -> Player:
        return self.players[not self.board.moves_num % 2]


def check_cells_sequence(obj: list[Cell]) -> bool:
    if all(cell.is_occupied for cell in obj) and \
            len(set([cell.marking for cell in obj])) == 1:
        return True
    return False
