#!/usr/bin/env python

__author__ = "Brett Duncan"
__copyright__ = "Copyright 2019"
__credits__ = []
__license__ = ""
__version__ = "0.0.0"
__maintainer__ = "Brett Duncan"
__email__ = "dunca384@umn.edu"
__status__ = "Development"


import random


def main():

    # read initial input telling the player number
    input()

    while True:

        input()

        move = random.randint(0, 6)

        print(move)  # return the random move


if __name__ == '__main__':
    main()
