"""
Battleships game

Matt Cotton
September 2019
"""

import random
import statistics
import csv

STD_SHIPS = [5, 4, 3, 3, 2]


class Cell:
    def __init__(self):
        self.ship = None
        self.guessed = False
        self.damaged = False
        self.sunk = False
        self.obstruction = False
        self.prob = 0

    def place_ship(self, ship):
        if self.ship:
            # print("There is already a ship here!")
            pass
        else:
            self.ship = ship

    def take_guess(self):
        if self.guessed:
            return False, None
        else:
            self.guessed = True
            if self.ship:
                self.damaged = True
                return True, self.ship
            else:
                self.obstruction = True
                return True, None


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Ship:
    def __init__(self, cells):
        self.sunk = False
        self.length = len(cells)
        self.cells = cells

    def test_if_sunk(self):
        sunk_flag = True
        for cell in self.cells:
            if not cell.damaged:
                sunk_flag = False

        if sunk_flag:
            # All ports of ship are damaged, lets sink it
            self.sunk = True
            for cell in self.cells:
                cell.damaged = False
                cell.sunk = True
                cell.obstruction = True

        return sunk_flag


def code_to_pos(code):
    if not (code[0].isalpha() and code[1:].isdigit()):
        print("Invalid code")
        return None
    else:
        if code[0].isupper():
            x = ord(code[0]) - ord("A")
        else:
            x = ord(code[0]) - ord("a")

        y = int(code[1:]) - 1

        return Pos(x, y)


def pos_to_code(pos):
    code = ""
    code += chr(pos.x + ord("A"))
    code += str(pos.y + 1)
    return code


class Board:
    def __init__(self, size):
        if size < 1:
            print("Invalid board size!")

        self.size = size
        self.cells = [[Cell() for i in range(size)] for j in range(size)]
        self.ships_alive = []
        self.ships_sunk = []
        self.guesses = 0
        self.game_over = False

    def get_cell(self, pos):
        try:
            return self.cells[pos.x][pos.y]
        except IndexError:
            return None

    def get_ship_cells(self, length, start_pos, orientation):
        # Calculate cell positions the ship will occupy
        positions = []
        if orientation == "h" or orientation == "v":
            for i in range(length):
                row_pos = start_pos.x + (i * (orientation == "v"))
                col_pos = start_pos.y + (i * (orientation == "h"))
                positions.append(Pos(row_pos, col_pos))
        else:
            raise Exception("Invalid orientation!")

        # Convert numerical positions to cell references
        cell_list = []
        for pos in positions:
            cell = self.get_cell(pos)
            if cell is not None:
                cell_list.append(cell)
            else:
                return None

        return cell_list

    def place_ship(self, length, start_pos, orientation):
        # Check if a ship can be placed in this position
        cell_list = self.get_ship_cells(length, start_pos, orientation)

        if cell_list is not None:
            # Check if a ship already occupies any of these cells
            valid_location = True
            for cell in cell_list:
                if cell.ship:
                    valid_location = False

            if valid_location:
                # Instantiate ship
                self.ships_alive.append(Ship(cell_list))

                # Tell each cell that this ship is occupying it
                for cell in cell_list:
                    cell.place_ship(self.ships_alive[-1])

                return True
        else:
            return False

    def random_board_setup(self, ships):
        ships = sorted(ships, reverse=True)
        for ship_size in ships:
            while True:
                orientation = random.choice(["h", "v"])
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)
                pos = Pos(x, y)
                if self.place_ship(ship_size, pos, orientation):
                    break
                else:
                    pass

    def manual_board_setup(self, ships):
        ships = sorted(ships, reverse=True)
        for ship_size in ships:
            while True:
                self.draw_board(True)
                while True:
                    orientation = input("Placing a ship of length %d. Horizontal or vertical? (h/v): " % ship_size)
                    if orientation == "h" or orientation == "v":
                        break
                    else:
                        print("Invalid input, try again.")

                while True:
                    pos = code_to_pos(input("Position of top-left corner: "))
                    if pos is not None:
                        break

                if self.place_ship(ship_size, pos, orientation):
                    print("Placed!")
                    break
                else:
                    print("Invalid position, try again.")

        print("All ships placed!")
        self.draw_board(True)

    def take_guess(self, pos):
        valid_guess, hit_ship, sunk = False, None, False
        # Get the cell reference and take a guess
        cell = self.get_cell(pos)
        if cell is not None:
            valid_guess, hit_ship = cell.take_guess()

            if valid_guess:
                self.guesses += 1
                if hit_ship:
                    sunk = hit_ship.test_if_sunk()
                    if sunk:
                        self.ships_alive.remove(hit_ship)
                        self.ships_sunk.append(hit_ship)
                        if len(self.ships_alive) <= 0:
                            # Game over
                            self.game_over = True

        return valid_guess, hit_ship is not None, sunk

    def manual_guess(self):
        while True:
            pos = code_to_pos(input("Guess a tile: "))
            if pos is not None:
                break
            else:
                print("Invalid input, try again.")

        valid_guess, hit, sunk = self.take_guess(pos)

        if not valid_guess:
            print("Invalid guess, try again.")
        else:
            if self.game_over:
                print("Final ship sunk, you win! Guesses: %d" % self.guesses)
            else:
                if sunk:
                    print("Hit and sunk! Ships remaining: %d" % len(self.ships_alive))
                elif hit:
                    print("Hit!")
                else:
                    print("Miss.")

    def get_random_pos(self):
        x = random.randint(0, self.size - 1)
        y = random.randint(0, self.size - 1)
        return Pos(x, y)

    def draw_board(self, show_boats):

        # Print column numbers (1, 2, 3, ...)
        print("   ", end="")
        for col in range(self.size):
            if col >= 9:
                spacing = " "
            else:
                spacing = "  "
            print("%d%s" % (col + 1, spacing), end="")
        print("")

        for row in range(self.size):
            print(chr(ord("A") + row), end="  ")  # Print row character (A, B, C, ...)
            for col in range(self.size):
                cell = self.get_cell(Pos(row, col))
                if cell.ship and cell.guessed:
                    icon = "@"
                elif cell.ship and show_boats:
                    icon = "O"
                elif cell.guessed:
                    icon = "x"
                else:
                    icon = "-"

                print(icon, end="  ")
            print("")


def generate_board(size, ships):
    board = Board(size)
    board.random_board_setup(ships)
    return board


def manual_game(size, ships):
    board = generate_board(size, ships)

    while not board.game_over:
        board.draw_board(False)
        board.manual_guess()


def random_guessing(size, ships):
    board = generate_board(size, ships)

    while not board.game_over:
        board.take_guess(board.get_random_pos())

    return board.guesses


def search_target_guessing(size, ships):
    board = generate_board(size, ships)

    target_stack = []

    while not board.game_over:
        if not target_stack:
            # No targets, we need to go randomly searching
            guess = board.get_random_pos()
        else:
            # Targets in list, choose the first target
            guess = target_stack[0]
            target_stack.pop(0)

        valid_guess, hit, sunk = board.take_guess(guess)

        if valid_guess:
            if hit:
                # Check the four adjacent cells to see if they have been guessed yet. If not, add to stack
                adjacent_positions = [Pos(guess.x - 1, guess.y),
                                      Pos(guess.x + 1, guess.y),
                                      Pos(guess.x, guess.y - 1),
                                      Pos(guess.x, guess.y + 1)
                                      ]

                # Remove invalid and already-guessed cells
                for pos in adjacent_positions:
                    cell = board.get_cell(pos)
                    if cell is None:
                        adjacent_positions.remove(pos)
                    elif cell.guessed:
                        adjacent_positions.remove(pos)

                target_stack.extend(adjacent_positions)

    return board.guesses


def probabilistic_guessing(size, ships):
    board = generate_board(size, ships)

    while not board.game_over:
        # board.draw_board(True)
        # Reset all cell prob's to 0
        for col in range(size):
            for row in range(size):
                cell = board.get_cell(Pos(row, col))
                cell.prob = 0

        # Attempt to place every ship in every location and orientation. Count the number of times each cell is occupied
        for ship in board.ships_alive:
            for col in range(size):
                for row in range(size):
                    for orientation in ["h", "v"]:

                        cell_list = board.get_ship_cells(ship.length, Pos(row, col), orientation)
                        if cell_list is not None:

                            # Check for obstructions
                            valid_location = True
                            hit_intersects = 0
                            for cell in cell_list:
                                if cell.obstruction:
                                    valid_location = False
                                elif cell.damaged:
                                    hit_intersects += 1

                            if valid_location:
                                for cell in cell_list:
                                    if not cell.guessed:
                                        if hit_intersects > 0:
                                            cell.prob += (10 ** hit_intersects)
                                        else:
                                            cell.prob += 1

        best_pos = Pos(0, 0)
        best_cell = board.get_cell(best_pos)
        for col in range(size):
            for row in range(size):
                pos = Pos(row, col)
                cell = board.get_cell(pos)
                if cell.prob > best_cell.prob:
                    best_pos = pos
                    best_cell = cell

        # print("Best cell: %s, prob: %d" % (pos_to_code(best_pos), best_cell.prob))
        # Guess that cell
        board.take_guess(best_pos)

    return board.guesses


# class TesterCell:
#     def __init__(self):
#         self.obstruction = False
#         self.damaged = False
#         self.prob = 0
#
#
# class TesterBoard(Board):
#     def __init__(self, size):
#         super().__init__(size)
#         self.cells = [[TesterCell() for i in range(size)] for j in range(size)]
#
#
# def probabilistic_guessing(size, ships):
#     board = generate_board(size, ships)
#     tester_board = TesterBoard(size)
#
#     while not board.game_over:
#         # Reset all cell prob's to 0
#         for col in range(size):
#             for row in range(size):
#                 cell = tester_board.get_cell(Pos(row, col))
#                 cell.prob = 0
#
#         # Attempt to place every ship in every location and orientation. Count the number of times each cell is occupied
#         for ship in board.ships_alive:
#             for col in range(size):
#                 for row in range(size):
#                     for orientation in ["h", "v"]:
#
#                         cell_list = tester_board.get_ship_cells(ship.length, Pos(row, col), orientation)
#                         if cell_list is not None:
#
#                             # Check for obstructions
#                             valid_location = True
#                             for cell in cell_list:
#                                 if cell.obstruction:
#                                     valid_location = False
#
#                             if valid_location:
#                                 for cell in cell_list:
#                                     cell.prob += 1
#
#         best_pos = Pos(0, 0)
#         best_cell = tester_board.get_cell(best_pos)
#         for col in range(size):
#             for row in range(size):
#                 pos = Pos(row, col)
#                 cell = tester_board.get_cell(pos)
#                 if cell.prob > best_cell.prob:
#                     best_pos = pos
#                     best_cell = cell
#
#         print("Best cell: %s" % pos_to_code(best_pos))
#         # Guess that cell
#         valid_guess, hit, sunk = board.take_guess(best_pos)
#         if sunk:
#             best_cell.obstruction = True
#             best_cell.damaged = False
#
#             # TODO Mark other damaged tester_cells as obstructions
#             ship = board.get_cell(best_pos).ship
#
#             for cell in ship.cells
#
#
#         elif hit:
#             best_cell.obstruction = False
#             best_cell.damaged = True
#         else:
#             best_cell.obstruction = True
#             best_cell.damaged = False
#
#     return board.guesses


def simulate_random(games):
    guesses = []
    f = open('csvfile_random.csv', 'w')
    for game in range(games):
        guesses.append(random_guessing(10, STD_SHIPS))
        f.write("%d\n" % guesses[game])

    f.close()


def simulate_search_target(games):
    guesses = []
    f = open('csvfile_search.csv', 'w')
    for game in range(games):
        guesses.append(search_target_guessing(10, STD_SHIPS))
        f.write("%d\n" % guesses[game])

    f.close()


def simulate_probabilistic_search(games):
    guesses = []
    f = open('csvfile_prob.csv', 'w')
    for game in range(games):
        guesses.append(probabilistic_guessing(10, STD_SHIPS))
        f.write("%d\n" % guesses[game])

    f.close()





# manual_game(10, STD_SHIPS)
# simulate_random(1000)
# simulate_search_target(1000)
simulate_probabilistic_search(1000)
