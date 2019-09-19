from battleships import *


def search_target_guessing(size, ships, print_output):
    board = generate_board(size, ships, False)

    target_stack = []

    while not board.game_over:
        if not target_stack:
            # No targets, we need to go randomly searching
            guess = board.get_random_pos()
        else:
            # Targets in list, choose the first target
            guess = target_stack[0]
            target_stack.pop(0)

        valid_guess, hit, _ = board.take_guess(guess, print_output)

        if valid_guess:

            if print_output:
                board.draw_board(False)
                print("Guess: %s" % (pos_to_code(guess)))

            if hit:
                # Get the four adjacent cells
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


if __name__ == '__main__':
    search_target_guessing(10, STD_SHIPS, True)