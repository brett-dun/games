#!/usr/bin/env python

__author__ = "Brett Duncan"
__copyright__ = "Copyright 2019"
__credits__ = []
__license__ = ""
__version__ = "0.0.0"
__maintainer__ = "Brett Duncan"
__email__ = "dunca384@umn.edu"
__status__ = "Development"


from typing import Tuple, List
import math

from tictactoe import check_for_winner, table_is_full, Table


# More or less based off of: https://en.wikipedia.org/wiki/Minimax
def calculate_move(table: Table, player_num: int, max_depth: int) -> Tuple:
    """

    :param table:
    :param player_num:
    :param max_depth:
    :return:
    """

    # store the results of each potential move
    results = [[], [], []]

    for i, row in enumerate(table):

        for j, box in enumerate(row):

            # check if the box is empty
            if box != 0:
                results[i].append((-math.inf, math.inf, -math.inf, math.inf))
                continue

            # make the play at the current location
            table[i][j] = player_num

            if check_for_winner(table) == player_num:  # make the play to win when possible
                return i, j
            elif table_is_full(table):  # if the table is full, there is nothing more that can be done
                return i, j
            else:  # in all other cases, find the number of wins, losses, ties, and incomplete solves that this path leads to
                results[i].append(func(table, player_num, max_depth))

            # reset the current location
            table[i][j] = 0

    # priority is: minimize min_losses, minimize min_losses, maximize max_wins
    max_wins = -math.inf  # maximum number of potential wins at a given number of losses and incompletes
    min_losses = math.inf  # minimum number of potential losses
    min_incomplete = math.inf  # minimum number of incompletes for the given value of min_losses

    loc = (0, 0)  # location of safest play

    for i, row in enumerate(results):

        for j, result in enumerate(row):

            if result[1] < min_losses or (result[1] == min_losses and (result[3] < min_incomplete or (result[3] == min_incomplete and max_wins > result[0]) ) ):

                max_wins, min_losses, _, min_incomplete = result
                loc = (i, j)

    return loc


def func(table: Table, player_num: int, max_depth: int, current_depth: int = 1) -> Tuple:
    """

    :param table:
    :param player_num:
    :param max_depth:
    :param current_depth:
    :return:
    """

    other_num = 2 if player_num == 1 else 1

    wins, losses, draws, incomplete = (0, 0, 0, 0)

    for row in table:

        for j, box in enumerate(row):

            # check if the box is empty
            if box != 0:
                continue

            # set the box to the player's number
            row[j] = player_num if current_depth % 2 == 0 else other_num

            winner = check_for_winner(table)

            if winner == player_num:

                wins += 1

            elif winner == other_num:

                losses += 1

            elif table_is_full(table):

                draws += 1

            elif current_depth < max_depth:

                tup = func(table, player_num, max_depth, current_depth+1)

                wins += tup[0]
                losses += tup[1]
                draws += tup[2]
                incomplete += tup[3]

            else: # no winner, table is not full, current_depth == max_depth

                incomplete += 1

            # reset the box to how we found it
            row[j] = 0

    return wins, losses, draws, incomplete


def main():

    # read initial input telling the player number
    player_num = int(input())

    while True:

        # get table as string
        inpt = input()

        # parse table into list
        li = [int(c) for c in inpt if c.isnumeric()]

        table = []

        for i in range(3):

            table.append([])

            table[i].append(li[i * 3])
            table[i].append(li[i * 3 + 1])
            table[i].append(li[i * 3 + 2])

        move = calculate_move(table, player_num, 5)

        # move = (random.randint(0, 2), random.randint(0, 2))

        print(move)  # return the move


if __name__ == '__main__':
    main()



# func(table, player_num, max_depth, current_depth = 0)
# recursively calls itself with all possible moves of player_num
# recursively calls itself with all possible moves of the other player
# this continues until the maximum depth is reached
# returns tuple in the form of (wins, losses, draws, incomplete) except for when current_depth == 0
# returns optimal move as determined by minimum number of losses then maximum number of wins when current_depth == 0
# use deep copy to modify array before passing it into the function recursively

# example:

# current_depth = 0 -> 1 state
# [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

# current_depth = 1 -> less than 9^1 states
# [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
# [[0, 1, 0], [0, 0, 0], [0, 0, 0]]
# [[0, 0, 1], [0, 0, 0], [0, 0, 0]]
# ...

# current_depth = 2 -> less than 9^2 states
# [[1, 2, 0], [0, 0, 0], [0, 0, 0]]
# [[1, 0, 2], [0, 0, 0], [0, 0, 0]]
# ...
# [[2, 1, 0], [0, 0, 0], [0, 0, 0]]
# [[0, 1, 2], [0, 0, 0], [0, 0, 0]]
# ...
# ...

# pseudo code
# func(table, player_num, max_depth, current_depth = 0):
#   for i in range(3): # rows
#       for j in range(3): # cols
#           cpy = deepcopy(table)
#           if is_valid(table, (i,j)):
#