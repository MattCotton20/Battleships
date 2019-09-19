from battleships import *


def manual_game(size, ships):
    while True:
        setup = input("Randomise board or user-generated? (r/u): ")

        if setup == "r":
            board = generate_board(size, ships, False)
            break
        elif setup == "u":
            board = generate_board(size, ships, True)
            break
        else:
            print("Invalid input, try again.")

    while not board.game_over:
        board.draw_board(False)
        board.manual_guess()


if __name__ == '__main__':
    manual_game(10, STD_SHIPS)