from battleships import *


def probabilistic_guessing(size, ships, print_output):
    board = generate_board(size, ships, False)

    while not board.game_over:
        if print_output:
            board.draw_board(False)

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

                                        # Potential ship location. Increase probability score.
                                        if hit_intersects > 0:
                                            cell.prob += (10 ** hit_intersects)
                                        else:
                                            cell.prob += 1

        # Find the cell with the highest probability score
        best_pos = Pos(0, 0)
        best_cell = board.get_cell(best_pos)
        for col in range(size):
            for row in range(size):
                pos = Pos(row, col)
                cell = board.get_cell(pos)
                if cell.prob > best_cell.prob:
                    best_pos = pos
                    best_cell = cell

        if print_output:
            print("Best cell: %s, score: %d" % (pos_to_code(best_pos), best_cell.prob))

        # Guess that cell
        board.take_guess(best_pos, print_output)

    return board.guesses


if __name__ == '__main__':
    probabilistic_guessing(10, STD_SHIPS, True)