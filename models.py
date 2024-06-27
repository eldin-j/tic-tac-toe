class Cell:
    def __init__(self, number):
        self.number = number
        self.is_occupied = False
        self.marking = ''

    def __repr__(self):
        return self.marking


class Board:
    dimension = 3

    def __init__(self):
        self.cells = [Cell(num) for num in range(Board.dimension ** 2)]
        self.moves_num = 0

    def occupy_cell(self, cell_num) -> None:
        self.cells[cell_num].marking = ['X', 'O'][self.moves_num % 2]
        self.cells[cell_num].is_occupied = True
        self.moves_num += 1

    def is_all_cells_occupied(self) -> bool:
        return all(cell.is_occupied for cell in self.cells)


class Player:
    player_count = 0

    def __init__(self, name):
        self.name = name
        Player.player_count += 1

    def __del__(self):
        Player.player_count -= 1

    def __str__(self):
        return self.name
