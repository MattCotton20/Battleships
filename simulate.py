from battleships import *
from random_guessing import *
from search_guessing import *
from probabilistic_guessing import *

from statistics import mean, stdev


def simulate_battleships():

    while True:
        method = input("Select guessing method: random (r), search (s), probabilistic (p): ").lower()
        if method == "r":
            guess_function = random_guessing
            break
        elif method == "s":
            guess_function = search_target_guessing
            break
        elif method == "p":
            guess_function = probabilistic_guessing
            break
        else:
            print("Invalid input, try again.")

    while True:
        num_of_sims = input("Enter number of simulations: ")
        if num_of_sims.isdigit() and int(num_of_sims) > 0:
            num_of_sims = int(num_of_sims)
            break
        else:
            print("Invalid input, try again.")

    while True:
        csv_out = input("Output to csv? (y/n): ").lower()
        if csv_out in ("y", "n"):
            break
        else:
            print("Invalid input, try again.")

    print("Starting simulation...")

    guesses = []
    for sim in range(num_of_sims):
        guesses.append(guess_function(10, STD_SHIPS, False))

    print("Complete!")
    print("Mean: %d, StDev: %f, Min: %d, Max %d" % (mean(guesses), stdev(guesses), min(guesses), max(guesses)))

    # Generate CSV file
    if csv_out == "y":
        csv_file = open("battleships_CSV.csv", "w")
        for guess in guesses:
            csv_file.write("%d\n" % guess)
        csv_file.close()
        print("Data saved as 'battleships_CSV.csv'")


if __name__ == '__main__':
    simulate_battleships()