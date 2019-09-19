from battleships import *
from random_guessing import *
from search_guessing import *
from probabilistic_guessing import *


def simulate_random(games):
    guesses = []
    f = open('csvfile_random.csv', 'w')
    for game in range(games):
        guesses.append(random_guessing(10, STD_SHIPS))
        f.write("%d\n" % guesses[game])

    f.close()


def simulate_search(games):
    guesses = []
    f = open('csvfile_search.csv', 'w')
    for game in range(games):
        guesses.append(search_target_guessing(10, STD_SHIPS))
        f.write("%d\n" % guesses[game])

    f.close()


def simulate_probabilistic(games):
    guesses = []
    f = open('csvfile_prob.csv', 'w')
    for game in range(games):
        guesses.append(probabilistic_guessing(10, STD_SHIPS))
        f.write("%d\n" % guesses[game])

    f.close()


if __name__ == '__main__':
    simulate_probabilistic(1000)