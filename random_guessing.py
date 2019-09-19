from battleships import *


def random_guessing(size, ships, print_output):
    board = generate_board(size, ships, False)
    if print_output:
        board.draw_board(False)

    while not board.game_over:

        # Take a random guess
        guess = board.get_random_pos()
        valid_guess, _, _ = board.take_guess(guess, print_output)

        # Display output if required
        if valid_guess and print_output:
            board.draw_board(False)
            print("Guess: %s" % (pos_to_code(guess)))

    return board.guesses


if __name__ == '__main__':
    random_guessing(10, STD_SHIPS, True)
