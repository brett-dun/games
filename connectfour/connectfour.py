
__author__ = "Brett Duncan"
__copyright__ = "Copyright 2019"
__credits__ = []
__license__ = ""
__version__ = "0.0.0"
__maintainer__ = "Brett Duncan"
__email__ = "dunca384@umn.edu"
__status__ = "Development"


from typing import Tuple, List
from subprocess import Popen, PIPE

Table = List[List]


def play(player1: str, player2: str):
    """

    :param player1:
    :param player2:
    :return:
    """

    # 6x7 table of zeros
    table = [[0] * 7 for _ in range(6)]

    human_player1 = (player1 == 'human')
    human_player2 = (player2 == 'human')

    if not human_player1:
        player1_process = Popen(player1, shell=True, stdin=PIPE, stdout=PIPE)

    if not human_player2:
        player2_process = Popen(player2, shell=True, stdin=PIPE, stdout=PIPE)

    # have the players play against each other until there is a winner or a tie
    while not table_is_full(table):

        print()

        # check if either player has won
        winner = check_for_winner(table)
        if winner != 0:
            print_table(table)
            print('winner: ', winner)
            break

        # player 1
        while True:

            print_table(table)

            if human_player1:
                s = input('player 1, enter your move: ')
            else:
                player1_process.stdin.write((str(table) + '\n').encode())
                player1_process.stdin.flush()

                s = player1_process.stdout.readline().decode(encoding='utf-8').rstrip()

            move = parse_move(s)
            print('player 1 tried:', move)

            if validate_move(table, move):
                take_move(table, 1, move)
                break

        if table_is_full(table):
            break

        print()

        # check if either player has won
        winner = check_for_winner(table)
        if winner != 0:
            print_table(table)
            print('winner: ', winner)
            break

        # player 2
        while True:

            print_table(table)

            if human_player2:
                s = input('player 2, enter your move: ')
            else:
                player2_process.stdin.write((str(table) + '\n').encode())
                player2_process.stdin.flush()

                s = player2_process.stdout.readline().decode(encoding='utf-8').rstrip()

            move = parse_move(s)
            print('player 2 tried:', move)

            if validate_move(table, move):
                print('valid move')
                take_move(table, 2, move)
                break

    if table_is_full(table) and check_for_winner(table) == 0:
        print()
        print("It's a draw!")

    # stop the player processes
    if not human_player1:
        player1_process.kill()

    if not human_player2:
        player2_process.kill()

    return


def parse_move(s: str) -> int:
    """

    :param s:
    :return:
    """

    try:
        v = int(s)
    except ValueError:
        v = -1

    return v


# returns True if the move is valid, False otherwise
def validate_move(table: Table, move: int) -> bool:
    """

    :param table:
    :param move:
    :return:
    """

    if move == -1:
        return False

    return (0 <= move < 7) and (table[0][move] == 0)


# check to see if either player has won the game; returns the winner if there is one, 0 otherwise
def check_for_winner(table: Table) -> int:
    """

    :param table:
    :return:
    """

    # check rows
    for i in range(6):
        for j in range(4):
            if table[i][j] != 0 and table[i][j] == table[i][j+1] == table[i][j+2] == table[i][j+3]:
                return table[i][j]

    # check columns
    for j in range(7):
        for i in range(3):
            if table[i][j] != 0 and table[i][j] == table[i+1][j] == table[i+2][j] == table[i+3][j]:
                return table[i][j]

    # check \ diagonals
    for i in range(3):
        for j in range(4):
            if table[i][j] != 0 and table[i][j] == table[i+1][j+1] == table[i+2][j+2] == table[i+3][j+3]:
                return table[i][j]

    # check / diagonals
    for i in range(3, 6):
        for j in range(4):
            if table[i][j] != 0 and table[i][j] == table[i-1][j+1] == table[i-2][j+2] == table[i-3][j+3]:
                return table[i][j]

    return 0


def print_table(table: Table) -> None:
    """

    :param table:
    :return:
    """

    for row in table:
        print(row)


def table_is_full(table: Table) -> bool:
    """

    :param table:
    :return:
    """

    for row in table:
        for box in row:
            if box == 0:
                return False

    return True


def table_is_full(table: Table) -> bool:
    """

    :param table:
    :return:
    """

    for row in table:
        for box in row:
            if box == 0:
                return False

    return True


def take_move(table: Table, player: int, move: int):
    """

    :param table:
    :param player:
    :param move:
    :return:
    """

    for i in range(5, -1, -1):

        if table[i][move] == 0:
            table[i][move] = player
            break
