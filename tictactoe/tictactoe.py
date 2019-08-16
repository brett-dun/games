
from typing import Tuple, List
from subprocess import Popen, PIPE
import re

Table = List[List]

pattern = re.compile("\([0-9]+,\ ?[0-9]+\)")


def play(player1: str, player2: str) -> None:

    # 3x3 table of zeros
    table = [[0]*3 for _ in range(3)]

    human_player1 = (player1 == 'human')
    human_player2 = (player2 == 'human')

    if not human_player1:
        player1_process = Popen(['python', player1], shell=False, stdin=PIPE, stdout=PIPE)

    if not human_player2:
        player2_process = Popen(['python', player2], shell=False, stdin=PIPE, stdout=PIPE)

    # have the players play against each other until there is a winner or a tie
    while not board_is_full(table):

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
                player1_process.stdin.write((str(table)+'\r\n').encode())
                player1_process.stdin.flush()

                s = player1_process.stdout.readline().decode(encoding='utf-8').rstrip()

            move = parse_move(s)
            print('player 1 tried:', move)

            if validate_move(table, move):
                r, c = move
                table[r][c] = 1
                break

        if board_is_full(table):
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
                player2_process.stdin.write((str(table) + '\r\n').encode())
                player2_process.stdin.flush()

                s = player2_process.stdout.readline().decode(encoding='utf-8').rstrip()

            move = parse_move(s)
            print('player 2 tried:', move)

            if validate_move(table, move):
                r, c = move
                table[r][c] = 2
                break

    if board_is_full(table) and check_for_winner(table) == 0:
        print()
        print("It's a draw!")

    # stop the player processes
    if not human_player1:
        player1_process.kill()

    if not human_player2:
        player2_process.kill()

    return


def parse_move(s: str) -> Tuple:

    if s is None or pattern.match(s) is None:
        return None

    try:
        r, c = [int(x) for x in s[1:-1].split(',')]
        return r, c
    except ValueError:
        return None


# returns True if the move is valid, False otherwise
def validate_move(table: Table, move: Tuple) -> bool:

    if move is None:
        return False

    return (0 <= move[0] < 3) and (0 <= move[1] < 3) and (table[move[0]][move[1]] == 0)


# check to see if either player has won the game; returns the winner if there is one, 0 otherwise
def check_for_winner(table: Table) -> int:

    # check rows and columns
    for i in range(3):
        if table[i][0] != 0 and table[i][0] == table[i][1] == table[i][2]:
            return table[i][0]
        if table[0][i] != 0 and table[0][i] == table[1][i] == table[2][i]:
            return table[0][i]

    # check diagonals
    if table[0][0] != 0 and table[0][0] == table[1][1] == table[2][2]:
        return table[0][0]
    if table[2][0] != 0 and table[2][0] == table[1][1] == table[0][2]:
        return table[2][0]

    return 0


def print_table(table: Table) -> None:

    for row in table:
        print(row)


def board_is_full(table: Table) -> bool:

    for row in table:
        for box in row:
            if box == 0:
                return False

    return True
